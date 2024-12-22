#!/bin/bash
: <<'END_COMMENT'
Ce script d'initiation permet de gérer les tâches suivantes :
- installation des dépendances
- Generation du .env
- Gestion de l'interface
- Configuration de l'hote
- Generation certificat
- Mise en point wifi (si hardware compatible)
(Non utilisé) - Generation conf dns mask
- Lancement du docker compose
- Mise en place de CRON pour:
    - Mise a jour du certificats
    - Cron pour sauvegarde base de donnée
END_COMMENT

set -e

# Couleurs
BLACK='\033[0;30m'
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'
BALISE='\n##############################\n'

generate_login() {
  local nom="$1"
  local prenom="$2"

  # Get the first two characters of 'prenom', uppercase, and strip whitespace
  local prenom_part=$(echo "$prenom" | head -c 2 | tr '[:lower:]' '[:upper:]' | xargs)

  # Get the first character of 'nom', uppercase, and strip whitespace
  local nom_part=$(echo "$nom" | head -c 1 | tr '[:lower:]' '[:upper:]' | xargs)

  # Combine trimmed 'nom' and 'prenom' and calculate the length without newline
  local combined=$(echo -n "$nom$prenom" | xargs)
  local total_length=$(echo -n "$combined" | wc -c)

  # Generate the login
  local login="${prenom_part}${nom_part}$(printf "%02d" "$total_length")"

  echo "$login"
}

# Vérifie que le script est executé en root
if [ "$EUID" -ne 0 ]; then
    printf "\n\n${RED}Ce script doit être exécuté en tant que root${NC}\n\n"
    exit 1
fi


printf "${BALISE}${GREEN}Installation des dépendances${NC}${BALISE}\n"

apt update -y && apt upgrade -y  && apt install -y git dialog wget build-essential libreadline-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev zlib1g-dev iptables ca-certificates curl libcurl4-openssl-dev libpcre3 libghc-regex-pcre-dev network-manager cron openssl docker.io docker-compose

if ! [ -x "$(command -v docker)" ]; then
    printf "${BALISE}${GREEN}Installation de Docker${NC}${BALISE}\n"
    install -m 0755 -d /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc
    chmod a+r /etc/apt/keyrings/docker.asc
    echo \
    "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian \
    $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
    tee /etc/apt/sources.list.d/docker.list > /dev/null
    apt-get update
    apt-get -y  install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose docker-compose-plugin
fi

systemctl enable docker
systemctl start docker

printf "${BALISE}${GREEN}Configuration de l'environnement${NC}${BALISE}\n"
CONFIG=prod
CACHE_HOST=cache
REDIS_USER=default
REDIS_PASSWORD=$(openssl rand -base64 32)

read -p "Nom de l'administrateur : "
echo
ADMIN_NOM=$REPLY
read -p "Prenom de l'administrateur : "
echo
ADMIN_PRENOM=$REPLY
read -p "Email de l'administrateur : "
echo
ADMIN_MAIL=$REPLY
while true; do
    read -s -p "Entrez un mot de passe administrateur pour l'application (sans @ dedans) : " ADMIN_PASSWORD
    echo

    if [ ${#ADMIN_PASSWORD} -lt 12 ]; then
        echo "Le mot de passe doit contenir au moins 12 caractères."
        continue
    fi

    if ! [[ "$ADMIN_PASSWORD" =~ [[:upper:]] ]]; then
        echo "Le mot de passe doit contenir au moins une lettre majuscule."
        continue
    fi

    if ! [[ "$ADMIN_PASSWORD" =~ [[:lower:]] ]]; then
        echo "Le mot de passe doit contenir au moins une lettre minuscule."
        continue
    fi

    if ! [[ "$ADMIN_PASSWORD" =~ [[:digit:]] ]]; then
        echo "Le mot de passe doit contenir au moins un chiffre."
        continue
    fi

    if ! [[ "$ADMIN_PASSWORD" =~ [[:punct:]] ]]; then
        echo "Le mot de passe doit contenir au moins un caractère spécial (autre que @)."
        continue
    fi

    echo "Le mot de passe est valide."
    break
done

echo "CONFIG=$CONFIG" > .env
echo "CACHE_HOST=$CACHE_HOST" >> .env
echo "REDIS_USER=$REDIS_USER" >> .env
echo "REDIS_PASSWORD=$REDIS_PASSWORD" >> .env
echo "ADMIN_NOM=$ADMIN_NOM" >> .env
echo "ADMIN_PRENOM=$ADMIN_PRENOM" >> .env
echo "ADMIN_MAIL=$ADMIN_MAIL" >> .env
echo "ADMIN_PASSWORD=$ADMIN_PASSWORD" >> .env

printf "${BALISE}${GREEN}Gestion de l'interface${NC}${BALISE}\n"

while true; do
    read -p "Entrez le type d'installation (server/pc) : " TYPEINSTALL
    case $TYPEINSTALL in
        [Ss][Ee][Rr][Vv][Ee][Rr]* ) TYPEINSTALL="ethernet"; break;;
        [Pp][Cc]* ) TYPEINSTALL="wifi"; break;;
        * ) echo "Veuillez répondre par 'server' ou 'pc'";;
    esac
done

output=$(nmcli --get-values GENERAL.DEVICE,GENERAL.TYPE device show)
INTERFACE=$(echo "$output" | grep -B 1 $TYPEINSTALL | head -n 1)
if [ -z "$INTERFACE" ]; then
    printf "${RED}Aucune interface n'a été trouvée${NC}\n"
    exit 1
fi

printf "${BALISE}${GREEN}Configuration de l'hote${NC}${BALISE}\n"

read -p "Entrez un nom de domaine pour acceder localement à l'application (ex: site.local ) : "
echo
DOMAIN_NAME=$REPLY

printf "${BALISE}${GREEN}Generation des certificats${NC}${BALISE}\n"

cd ./nginx/ssl
openssl req -new -newkey rsa:4096 -x509 -sha256 -nodes -subj "/C=FR/ST=France/L=Toulouse/O=APEAJ/OU=Aide/CN=$DOMAIN_NAME" -out certs/self_ssl_certs.pem -keyout private/self_ssl_certs.key
cd -

if [ "$TYPEINSTALL" = "wifi" ]; then
    printf "${BALISE}${GREEN}Configuration du point d'accès sans fil${NC}${BALISE}\n"

    while true; do
        read -p "Entrez le nom du ssid du point d'accès : " WIFI_SSID
        echo
        if [ -z "$WIFI_SSID" ]; then
            echo "Le nom du ssid ne peut pas être vide."
            continue
        fi
        break
    done
    while true; do
        read -p "Entrez le mot de passe du point d'accès : " WIFI_PASSWORD
        echo
        if [ -z "$WIFI_PASSWORD" ]; then
            echo "Le mot de passe ne peut pas être vide."
            continue
        fi

        if [ ${#WIFI_PASSWORD} -lt 8 ]; then
            echo "Le mot de passe doit contenir au moins 8 caractères."
            continue
        fi
        break
    done

    printf "${BLUE}Interface du relai : $INTERFACE${NC}\n\n"

    if [ -f /etc/NetworkManager/system-connections/$WIFI_SSID.nmconnection ]; then
        nmcli con down $WIFI_SSID
        nmcli con delete $WIFI_SSID
    fi

    nmcli con add type wifi ifname $INTERFACE mode ap con-name $WIFI_SSID ssid $WIFI_SSID
    nmcli con modify $WIFI_SSID 802-11-wireless.band bg
    nmcli con modify $WIFI_SSID 802-11-wireless.channel 1
    nmcli con modify $WIFI_SSID 802-11-wireless-security.key-mgmt wpa-psk
    nmcli con modify $WIFI_SSID 802-11-wireless-security.proto rsn
    nmcli con modify $WIFI_SSID 802-11-wireless-security.group ccmp
    nmcli con modify $WIFI_SSID 802-11-wireless-security.pairwise ccmp
    nmcli con modify $WIFI_SSID 802-11-wireless-security.psk "$WIFI_PASSWORD"
    nmcli con modify $WIFI_SSID ipv4.method shared
    nmcli con up $WIFI_SSID
fi

SELFIP=$(ip -4 addr show $INTERFACE | grep -oP '(?<=inet\s)\d+(\.\d+){3}')
echo "$SELFIP $DOMAIN_NAME" >> /etc/hosts

# DNSMask container redirection
# printf "${BALISE}${GREEN}Generation config DNSMask${NC}${BALISE}\n"

# echo "log-queries" > ./dnsmasq.conf
# echo "no-resolv" >> ./dnsmasq.conf
# echo "server=$SELFIP" >> ./dnsmasq.conf
# echo "strict-order" >> ./dnsmasq.conf
# echo "address=/$DOMAIN_NAME/$SELFIP" >> ./dnsmasq.conf

printf "${BALISE}${GREEN}Initialisation du docker compose${NC}${BALISE}\n"

docker-compose up -d --build

# DNSMask container redirection
# printf "${BALISE}${GREEN}Configuration des règles iptables${NC}${BALISE}\n"
# iptables -t nat -A OUTPUT -p udp --dport 53 -j DNAT --to $SELFIP:5653
# iptables -t nat -A OUTPUT -p tcp --dport 53 -j DNAT --to $SELFIP:5653

printf "${BALISE}${GREEN}Mise en place des CRON${NC}${BALISE}\n"

FOLDER_PATH=$(pwd)

printf "${BLUE}CRON pour renouvellement du certificat tous les 1er janvier à minuit${NC}\n"
cp ./scripts/renew_cert.sh /usr/local/bin/renew_cert.sh

chmod +x /usr/local/bin/renew_cert.sh

(crontab -l 2>/dev/null; echo "0 0 1 1 * /usr/local/bin/renew_cert.sh $DOMAIN_NAME $FOLDER_PATH") | crontab -

printf "${BLUE}CRON pour backup de la base de donnée tous les jours à minuit${NC}\n"
cp ./scripts/backup_db.sh /usr/local/bin/backup_db.sh

chmod +x /usr/local/bin/backup_db.sh

(crontab -l 2>/dev/null; echo "0 0 * * * /usr/local/bin/backup_db.sh") | crontab -

printf "${BALISE}${GREEN}Fin de l'initialisation${NC}${BALISE}\n"
printf "${BLUE}L'application est maintenant accessible à l'adresse https://$DOMAIN_NAME${NC}\n"
ADMIN_LOGIN=$(generate_login $ADMIN_NOM $ADMIN_PRENOM)
printf "Login admin: %s\n" "$ADMIN_LOGIN"
printf "Admin password: %s\n" "${ADMIN_PASSWORD}"
printf "Redis admin: %s\n" "$REDIS_USER"
printf "Redis password: %s\n" "${REDIS_PASSWORD}"

if [ "$TYPEINSTALL" = "wifi" ]; then
    printf "${BLUE}Le point d'accès sans fil est maintenant disponible avec le ssid $WIFI_SSID et le mot de passe $WIFI_PASSWORD${NC}\n"
fi
