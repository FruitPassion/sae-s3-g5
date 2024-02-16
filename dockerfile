# Utilisez l'image Debian comme base
FROM debian

# Créez un répertoire pour le projet
RUN mkdir -p /var/www/aepaj

# Copiez le contenu du répertoire local dans le conteneur au chemin /var/www/projet
COPY . /var/www/aepaj

# Accédez au répertoire copié
WORKDIR /var/www/aepaj

# Rendez le script exécutable
RUN chmod +x setup.sh

# Exécutez l'initialisation du répertoire
RUN ./setup.sh
