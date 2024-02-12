#!/bin/bash
# Update of the packages
echo "Update of the packages..."
apt update && apt upgrade # check

# Install the dependencies
echo "Installation of the dependencies..."
apt install -y git
apt install -y apache2 # check
apt install -y libapache2-mod-wsgi-py3 # check
apt install wget build-essential libreadline-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev zlib1g-dev #check
wget -c https://www.python.org/ftp/python/3.10.13/Python-3.10.13.tar.xz # check
tar -Jxvf Python-3.10.13.tar.xz # check
cd Python-3.10.13 #check
./configure --enable-optimizations --prefix=/usr/local --enable-shared LDFLAGS="-Wl,-rpath /usr/local/lib" #check
sudo make -j4 && sudo make altinstall # check 
cd ..
rm Python-3.10.13.tar.xz Python-3.10.13

sudo apt install -y mariadb-server # check

# Initialization
#### MARIADB ####
echo "Initialization of MariaDB users..." # check
sudo systemctl enable mariadb.service # check
sudo systemctl start mariadb.service # check



# Generer mot de passe random et le stocker pour la base de donnée
echo "Generation du mot de passe admin.." # check
pwdadm=$(date | sha256sum) # check
pwdadm=$(echo "${pwdadm// -}") # check
pwdadm=$(echo "${pwdadm// }") # check

echo "root :" "'$pwdadm'" > db_adm_psswd.txt
echo "Stockage du mot de passe root dans le fichier db_adm_psswd.txt" # check

# Generer mot de passe random et le stocker pour la base de donnée
echo "Generation du mot de passe utilisateur.." # check
pwdusr=$(date | sha256sum) # check
pwdusr=$(echo "${pwdusr// -}") # check
pwdusr=$(echo "${pwdusr// }") # check

echo "user :" "'$pwdusr'" > db_usr_psswd.txt # check
echo "Stockage du mot de passe user dans le fichier db_usr_psswd.txt" # check

sed -i -e "s/--AREMPLACER--/$pwdusr/" oui.txt

## Create USER
mysql -e "CREATE OR REPLACE USER 'user'@'localhost' IDENTIFIED BY '$pwdusr';" # check
mysql -e "DROP DATABASE IF EXISTS db_fiches_prod;" # check
mysql -e "create database db_fiches_prod;" # check
mysql -e "grant all privileges on db_fiches_prod.* TO 'user'@'localhost' identified by '$pwdusr';"
mysql -e "flush privileges;" # check

# Secure mariadb installation
# Kill the anonymous users
mysql -e "DROP USER ''@'localhost'" # check
# Because our hostname varies we'll use some Bash magic here.
mysql -e "DROP USER ''@'$(hostname)'" # check
# Kill off the demo database
mysql -e "DROP DATABASE IF EXISTS test" # check
# Make our changes take effect
mysql -e "FLUSH PRIVILEGES" # check
# Make sure that NOBODY can access the server without a password
mysql -e "ALTER USER 'root'@'localhost' IDENTIFIED BY '$pwdadm'; FLUSH PRIVILEGES;" # check

echo "Initialization of MariaDB done." # check

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

s
echo "Testing the installation..."
sudo a2dissite app
sudo a2ensite 000-default
sudo systemctl reload apache2

echo "Testing done."
