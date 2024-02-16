#!/bin/bash

# Colors
BLACK='\033[0;30m'        
RED='\033[0;31m'         
GREEN='\033[0;32m'       
YELLOW='\033[0;33m'       
BLUE='\033[0;34m'         
PURPLE='\033[0;35m'      
CYAN='\033[0;36m'         
WHITE='\033[0;37m'
NC='\033[0m'
BALISE='##############################'

# Get the current directory
current_directory=$(basename $(pwd))
parent_directory=$(dirname "$(pwd)")

# Check if the script is run as root
if [ "$EUID" -ne 0 ]; then
    printf "\n\n${RED}Ce script doit être exécuté en tant que root${NC}\n\n"
    exit 1
fi

# Check if the script is run in the right directory
if [ "$parent_directory/" != "/var/www/" ]; then
    echo "Le dossier $current_directory n'est pas dans /var/www/"
    printf "\n\n${RED}Le dossier $current_directory doit être dans le répertoire /var/www/${NC}\n\n"
    exit 1
fi

# Check the architecture of the system and if it is supported
architecture=$(dpkg --print-architecture)
if [ "$architecture" = "amd64" ]; then
    proc="x86_64"
elif [ "$architecture" = "arm64" ]; then
    proc="aarch64"
else
    printf "\n\n${RED}L'architecture de votre système n'est pas supportée${NC}\n\n"
    exit 1
fi
printf "\n\n$BALISE\n${GREEN}Architecture detectée : $proc${NC}\n$BALISE\n\n"

# Update of the packages
printf "$BALISE\n${PURPLE}Mise à jour des paquets ...${NC}\n$BALISE\n\n"
apt update -y && apt upgrade -y

# Install the dependencies
printf "\n\n$BALISE\n${PURPLE}Installation des dépendances ...${NC}\n$BALISE\n\n"
apt install -y git unzip dialog mariadb-server wget build-essential libreadline-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev zlib1g-dev

# Install python
printf "\n\n$BALISE\n${PURPLE}Installation de ${GREEN}python${PURPLE} (cette étape peut prendre du temps) ...${NC}\n$BALISE\n\n"

wget -c https://www.python.org/ftp/python/3.10.13/Python-3.10.13.tar.xz 
tar -Jxvf Python-3.10.13.tar.xz 
cd Python-3.10.13 #check
./configure --enable-optimizations --prefix=/usr/local --enable-shared LDFLAGS="-Wl,-rpath /usr/local/lib" #check
sudo make -j4 && sudo make altinstall  
cd .. 
rm -r Python-3.10.13.tar.xz Python-3.10.13 

printf "\n\n$BALISE\n${GREEN}Installation des requirements Apache${NC}\n$BALISE\n\n" 

apt install -y libapache2-mod-wsgi-py3 apache2 apache2-utils apache2-dev libapache2-mod-security2 
apt install -y libcurl4-openssl-dev libpcre3 libghc-regex-pcre-dev 

printf "\n\n$BALISE\n${GREEN}Installation des requirements python${NC}\n$BALISE\n\n" 

cd ..
chown -R www-data:www-data "$current_directory/"

cd $current_directory

pip3.10 install virtualenv
virtualenv .env 

source .env/bin/activate 

pip3.10 install -r requirements.txt 

pip3.10 install --upgrade pip 

pip3.10 install mod-wsgi

deactivate


cp ".env/lib/python3.10/site-packages/mod_wsgi/server/mod_wsgi-py310.cpython-310-$proc-linux-gnu.so" /usr/lib/apache2/modules/
echo "LoadModule wsgi_module /usr/lib/apache2/modules/mod_wsgi-py310.cpython-310-$proc-linux-gnu.so" > /etc/apache2/mods-enabled/wsgi.load

# Initialization
#### MARIADB ####
printf "\n\n$BALISE\n${YELLOW}Paramétrage de la base de donnees MariaDB${NC}\n$BALISE\n\n"

read -p "Entrez un nom d'administrateur : " 
echo    # (optional) move to a new line
repnom=$REPLY
read -p "Entrez un prenom d'administrateur : " 
echo    # (optional) move to a new line
repprenom=$REPLY

source .env/bin/activate

replog=$(python3.10 -c "from custom_paquets.converter import generate_login; print(generate_login('$repnom','$repprenom'))")
read -p "Entrez un mail d'administrateur : " 
echo    # (optional) move to a new line
repmail=$REPLY
read -p "Entrez un mot de passe administrateur : " 
echo    # (optional) move to a new line
repavmdp=$REPLY

repmdp=$(python3.10 -c "from custom_paquets.security import encrypt_password; print(encrypt_password('$repavmdp').decode('utf-8'))")

deactivate

sed -i -e "s/--AREMPLACERNOM--/$repnom/" db_production.sql
sed -i -e "s/--AREMPLACERPRENOM--/$repprenom/" db_production.sql
sed -i -e "s/--AREMPLACERLOG--/$replog/" db_production.sql
sed -i -e "s@--AREMPLACERMDP--@$repmdp@" db_production.sql
sed -i -e "s/--AREMPLACERMAIL--/$repmail/" db_production.sql

printf "\n\n$BALISE\n${YELLOW}Démarrage de MariaDB${NC}\n$BALISE\n\n"

sudo systemctl enable mariadb.service 
sudo systemctl start mariadb.service 


printf "\n\n$BALISE\n${RED}Génération du mot de passe administrateur${NC}\n$BALISE\n" 
pwdadm=$(date | sha256sum) 
pwdadm=$(echo "${pwdadm// -}") 
pwdadm=$(echo "${pwdadm// }")

sleep 1

printf "\n\n$BALISE\n${RED}Génération du mot de passe utilisateur${NC}\n$BALISE\n" 
pwdusr=$(date | sha256sum) 
pwdusr=$(echo "${pwdusr// -}") 
pwdusr=$(echo "${pwdusr// }") 

source .env/bin/activate 

python3.10 -c "from custom_paquets.security import generate_key, encrypt_file; generate_key(); encrypt_file('$pwdusr');"

deactivate

printf "\n\n$BALISE\n${YELLOW}Initialisation de la base de donnees MariaDB${NC}\n$BALISE\n\n"

## Create USER
mysql -e "CREATE OR REPLACE USER 'user'@'localhost' IDENTIFIED BY '$pwdusr';" 
mysql -e "DROP DATABASE IF EXISTS db_fiches_prod;" 
mysql -e "create database db_fiches_prod;" 
mysql -e "grant all privileges on db_fiches_prod.* TO 'user'@'localhost' identified by '$pwdusr';"
mysql -e "flush privileges;" 

mysql -h "localhost" -u "user" "-p$pwdusr" "db_fiches_prod" < "db_production.sql"

# Secure mariadb installation
# Kill off the demo database
mysql -e "DROP DATABASE IF EXISTS test" 
# Make our changes take effect
mysql -e "FLUSH PRIVILEGES" 
# Make sure that NOBODY can access the server without a password
mysql -e "ALTER USER 'root'@'localhost' IDENTIFIED BY '$pwdadm'; FLUSH PRIVILEGES;" 

printf "\n\n$BALISE\n${YELLOW}Initialisation et paramétrage de la base de donnees terminée${NC}\n$BALISE\n\n"

# #### APACHE #### 
printf "\n\n$BALISE\n${BLUE}Activation des mods de Apache2${NC}\n$BALISE\n\n"

a2enmod ssl
a2enmod rewrite
a2enmod headers
a2enmod unique_id
a2enmod security2

echo "Activation des modules terminée"

# Create the virtual host
printf "\n\n$BALISE\n${BLUE}Creation de l'host virtuel${NC}\n$BALISE\n\n"

read -p "Entrez un nom de domaine pour acceder localement à l'application (ex: site.local ) : " 
echo    
nomdom=$REPLY

sed -i -e "s/__AREMPLACERSN__/$current_directory/g" app.conf
sed -i -e "s/__AREMPLACERSN__/$current_directory/g" app.wsgi
sed -i -e "s/__AREMPLACERDN__/$nomdom/g" app.conf

cp app.conf /etc/apache2/sites-available/000-default.conf
a2ensite 000-default

# Create the virtual host
printf "\n\n$BALISE\n${BLUE}Creation d'un certificat SSL${NC}\n$BALISE\n\n"

mkdir /etc/apache2/certificate
cd /etc/apache2/certificate
openssl req -new -newkey rsa:4096 -x509 -sha256 -nodes -subj "/C=FR/ST=France/L=Toulouse/O=APEAJ/OU=Aide/CN=$nomdom" -out apache-certificate.crt -keyout apache.key 
selfip=$(ip -4 addr show wlan0 | grep -oP '(?<=inet\s)\d+(\.\d+){3}')
echo "$selfip   $nomdom" >> /etc/hosts

cd -

# Create the virtual host
printf "\n\n$BALISE\n${BLUE}Configuration de ModSecurity${NC}\n$BALISE\n\n"

cd /etc/apache2/
git clone https://github.com/owasp-modsecurity/ModSecurity.git modsecurity
cd modsecurity
./build.sh
git submodule init
git submodule update
./configure
make
make install
cd ..
mkdir conf
cd conf
wget https://github.com/coreruleset/coreruleset/archive/v3.3.5.tar.gz
tar -xvzf v3.3.5.tar.gz
ln -s coreruleset-3.3.5 /etc/apache2/conf/crs
cp crs/crs-setup.conf.example crs/crs-setup.conf
rm v3.3.5.tar.gz
cd ..

# Start and enable apache
printf "\n\n$BALISE\n${BLUE}Demarrage d'Apache${NC}\n$BALISE\n\n"

systemctl enable apache2 
systemctl start apache2 

printf "\n\n$BALISE\n${BLUE}Suppression des fichiers sensibles${NC}\n$BALISE\n\n"

rm db_production.sql app.conf

printf "\n\n$BALISE\n${BLUE}Fin de l'initialisation\nApplication prête sur le port 443 à l'adresse : https://$nomdom ${NC}\n$BALISE\n\n"

printf "$BALISE\n${GREEN}Identfiants administrateur de l'application :\n - login : '$replog'\n - mot de passe : '$repavmdp'\n\n"

printf "Identfiants administrateur de la base de donnée :\n - login : 'root'\n - mot de passe : '$pwdadm'\n\n"

printf "Identfiants utilisateur de la base de donnée :\n - login : 'user'\n - mot de passe : '$pwdusr'  ${NC}\n$BALISE\n\n"

printf "$BALISE\n${RED}Notez les quelques part, ils ne seront plus affichés et ne seront enregistrés nulle part.${NC}\n$BALISE\n\n"
