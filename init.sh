#!/bin/bash

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

# Update of the packages
printf "$BALISE\n${PURPLE}Mise à jour des paquets ...${NC}\n$BALISE\n\n"
apt update && apt upgrade # check

# Install the dependencies
printf "\n\n$BALISE\n${PURPLE}Installation des dépendances ...${NC}\n$BALISE\n\n"
apt install -y git apache2 libapache2-mod-wsgi-py3 mariadb-server wget build-essential libreadline-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev zlib1g-dev #check

# Install python
printf "\n\n$BALISE\n${PURPLE}Installation de ${GREEN}python${PURPLE} (cette étape peut prendre du temps) ...${NC}\n$BALISE\n\n"

wget -c https://www.python.org/ftp/python/3.10.13/Python-3.10.13.tar.xz # check
tar -Jxvf Python-3.10.13.tar.xz # check
cd Python-3.10.13 #check
./configure --enable-optimizations --prefix=/usr/local --enable-shared LDFLAGS="-Wl,-rpath /usr/local/lib" #check
sudo make -j4 && sudo make altinstall # check 
cd .. # check
rm -r Python-3.10.13.tar.xz Python-3.10.13 # check

printf "\n\n$BALISE\n${GREEN}Installation des requirements python${NC}\n$BALISE\n\n" # check

pip3.10 install -r requirements.txt # check

pip3.10 install --upgrade pip # check

# Initialization
#### MARIADB ####
printf "\n\n$BALISE\n${YELLOW}Paramétrage de la base de donnees MariaDB${NC}\n$BALISE\n\n"

read -p "Entrez un nom d'administrateur : " 
echo    # (optional) move to a new line
repnom=$REPLY
read -p "Entrez un prenom d'administrateur : " 
echo    # (optional) move to a new line
repprenom=$REPLY
replog=$(python3.10 -c "from custom_paquets.converter import generate_login; print(generate_login('$repnom','$repprenom'))")
read -p "Entrez un mail d'administrateur : " 
echo    # (optional) move to a new line
repmail=$REPLY
read -p "Entrez un mot de passe administrateur : " 
echo    # (optional) move to a new line
repmdp=$REPLY

repmdp=$(python3.10 -c "from custom_paquets.security import encrypt_password; print(encrypt_password('$repmdp').decode('utf-8'))")

sed -i -e "s/--AREMPLACERNOM--/$repnom/" db_production.sql
sed -i -e "s/--AREMPLACERPRENOM--/$repprenom/" db_production.sql
sed -i -e "s/--AREMPLACERLOG--/$replog/" db_production.sql
sed -i -e "s/--AREMPLACERMDP--/$repmail/" db_production.sql
sed -i -e "s/--AREMPLACERMAIL--/$repmdp/" db_production.sql

printf "\n\n$BALISE\n${YELLOW}Démmarage de MariaDB${NC}\n$BALISE\n\n"

sudo systemctl enable mariadb.service # check
sudo systemctl start mariadb.service # check


printf "\n\n$BALISE\n${RED}Génération du mot de passe utilisateur${NC}\n$BALISE\n" # check
pwdadm=$(date | sha256sum) # check
pwdadm=$(echo "${pwdadm// -}") # check
pwdadm=$(echo "${pwdadm// }") # check

echo "root :" "'$pwdadm'" > db_adm_psswd.txt
printf "$BALISE\n${RED}>>> Stockage du mot de passe root dans le fichier db_adm_psswd.txt${NC}\n$BALISE\n\n"


printf "\n\n$BALISE\n${RED}Génération du mot de passe utilisateur${NC}\n$BALISE\n" # check
pwdusr=$(date | sha256sum) # check
pwdusr=$(echo "${pwdusr// -}") # check
pwdusr=$(echo "${pwdusr// }") # check

echo "user :" "'$pwdusr'" > db_usr_psswd.txt # check
printf "$BALISE\n${RED}>>> Stockage du mot de passe root dans le fichier db_usr_psswd.txt${NC}\n$BALISE\n\n"

sed -i -e "s/--AREMPLACER--/$pwdusr/" config.py

printf "\n\n$BALISE\n${YELLOW}Initialisation de la base de donnees MariaDB${NC}\n$BALISE\n\n"

## Create USER
mysql -e "CREATE OR REPLACE USER 'user'@'localhost' IDENTIFIED BY '$pwdusr';" # check
mysql -e "DROP DATABASE IF EXISTS db_fiches_prod;" # check
mysql -e "create database db_fiches_prod;" # check
mysql -e "grant all privileges on db_fiches_prod.* TO 'user'@'localhost' identified by '$pwdusr';"
mysql -e "flush privileges;" # check

mysql -h "localhost" -u "user" "-p$pwdusr" "db_fiches_prod" < "db_production.sql"

# Secure mariadb installation
# Kill off the demo database
mysql -e "DROP DATABASE IF EXISTS test" # check
# Make our changes take effect
mysql -e "FLUSH PRIVILEGES" # check
# Make sure that NOBODY can access the server without a password
mysql -e "ALTER USER 'root'@'localhost' IDENTIFIED BY '$pwdadm'; FLUSH PRIVILEGES;" # check

printf "\n\n$BALISE\n${YELLOW}Initialisation et paramétrage de la base de donnees terminée${NC}\n$BALISE\n\n"

# #### APACHE #### 
echo "Initialization of Apache..."
sudo systemctl enable apache2 # check
sudo systemctl start apache2 # check

# Create the virtual host
echo "Creating the virtual host..."
sudo cp app.conf /etc/apache2/sites-available/000-default.conf
sudo a2ensite app
sudo a2dissite 000-default
sudo systemctl reload apache2

# Restart the server
sudo systemctl restart apache2
echo "Initialization of Apache done."


#### CREATE ENVIRONMENTAL VARIABLE ####
echo "Creating the environmental variable..."
echo "SEND HELP"

# Install the python packages
echo "Testing the installation..."
sudo a2dissite app
sudo a2ensite 000-default
sudo systemctl reload apache2

echo "Testing done."
