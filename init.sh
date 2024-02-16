#!/bin/bash

read -p "Entrez un nom d'administrateur : " 
echo    # (optional) move to a new line
repnom=$REPLY
read -p "Entrez un prenom d'administrateur : " 
echo    # (optional) move to a new line
repprenom=$REPLY

read -p "Entrez un mail d'administrateur : " 
echo    # (optional) move to a new line
repmail=$REPLY

read -p "Entrez un mot de passe administrateur : " 
echo    # (optional) move to a new line
repavmdp=$REPLY

read -p "Entrez un nom de domaine pour acceder localement à l'application (ex: site.local ) : " 
echo    
nomdom=$REPLY

# export all variable in a txt file
echo "repnom=$repnom" > temp.txt
echo "repprenom=$repprenom" >> temp.txt
echo "repmail=$repmail" >> temp.txt
echo "repavmdp=$repavmdp" >> temp.txt
echo "nomdom=$nomdom" >> temp.txt

# Initialization docker
docker build -t appaj .

docker run --name appaj -d -p 80:80 -p 443:443 appaj