<br/>
<div style="text-align: center">
  <a href="https://github.com/FruitPassion/sae-s3-g5">
    <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/3c/Flask_logo.svg/1200px-Flask_logo.svg.png"
    alt="flask-logo" height="80">
  </a>
  <h1>SAE3 - Application d'aides aux élèves en difficulté</h1>

  <p>
    Documentation de développement et d'utilisation de l'application web.
    <br />
    <a href="https://github.com/FruitPassion/sae-s3-g5/blob/main/README.md"><strong>Lire la doc »</strong></a>
    <br />
  </p>
</div>

## Prérequis

### Utilisation d'une base de données

**A FAIRE** :
- [ ] Creation d'utilisateur
- [ ] Creation de la base de donnée

### - Installation de Python 3.10

Le projet tournant grâce à Python, il est necessaire de l'avoir installé sur sa machine.
La verison que nous utiliserons ici est la 3.10, elle est installable via
[ce lien](https://www.python.org/downloads/release/python-31013/)

Pour connaitre la version que l'on possède du langage, il suffit de taper `python --version` dans son terminal.
Si jamais vous posseder plusieurs versions, il suffit de tapper la version désirée pour la lancer.
Ainsi, si par exemple, je possède python 3.8 et 3.10, et que je veux lancer la 3.10 je taperai simplement `python3.10`
dans le terminal pour lancer un programme `.py` avec cette version.

Sinon, si on ne possède qu'une seule version, on peut
juste utiliser `python` ou `python3`.

### - Création de l'envrionnement virtuel

Un environnement virtuel en Python est comme une boîte de rangement virtuelle qui isole et organise les bibliothèques et
les dépendances spécifiques à un projet Python. Cela permet de travailler sur différents projets sans qu'ils
interfèrent les uns avec les autres, garantissant ainsi un développement propre et sans conflits. Chaque boîte de
rangement virtuelle contient les ressources nécessaires à un projet, assurant une gestion facile et une portabilité
pour collaborer avec d'autres développeurs.

Pour le projet, on créera un environnement virtuel en se plaçant dans le projet git.
Depuis ce projet, on ouvre le terminal et on tape :
`python -m venv .env`. Au bout de quelques secondes un dossier nommé `.env` est créé à la racine du projet.
C'est le dossier de notre environnement virtuel.

Maintenant, pour activer cet environnement, il suffit de taper la commande :

```shell
$ .env\Scripts\activate
``` 

Dans le terminal, devrait alors apparaitre `(.env)` au début de la ligne.

![img.png](https://imgur.com/he2zP1V.png)

Cela, signifie que l'envrionnement est maintenant activé et que toutes les installations que vous ferez seront stocké
dans l'envrionnement et pas directement sur votre machine.

> [!NOTE]  
> Quand vous lancerez de nouveau votre terminal, selon votre IDE, l'envrionnement s'activera automatiquement. Pensez à
> toujours vérifier

### - Installation des dépendances/librairies.

Maintenant que notre environnement virtuel est pret, il suffit de lui installer les dépendances et librairies.
Celles-ci sont stockées à la racine du projet dans le fichier `requirements.txt`, ainsi quand vous ajouterez une
librairie au projet, vous devrez aussi l'ajouter dans le `requirements.txt`.

L'installation des librairires se fait avec la commande pip en se placant à la racine du projet et avec l'envrionnement
virtuel activé.
```shell
(.env) $ pip install -r requirements.txt
``` 

Si tout se passe bien, à la fin de l'execution de la commande, le projet sera enfin prêt à être lancé.

### Lancement du projet

Le lancement s'effectue grâce au fichier `app.py` que l'on lance à la racine du projet avec l'environnement virtuel activé.

```shell
(.env) $ python app.py
``` 

On peut ensuite se rendre sur son navigateur web et acceder à l'index via `http://localhost:5000/` ou `http://127.0.0.1:5000/`

***

## Présentation du projet


### Structure du projet

Le projet suit le modèle de conception MVC. Ce concept de MVC (Model-View-Controller) dans une application web, comme Flask, est une manière de structurer et
d'organiser le code pour améliorer la clarté et la maintenabilité de l'application. Ainsi :

- **Modèle (Model) :**
  <br>Le modèle représente les données de l'application. Il s'agit de la logique métier qui stocke, gère et manipule les
  informations. Par exemple, dans un site web de vente en ligne, le modèle pourrait gérer les produits, les utilisateurs
  et les commandes.

- **Vue (View) :**
  <br>La vue est responsable de l'interface utilisateur et de l'affichage des données aux utilisateurs. Elle s'occupe de
  la présentation des informations et de la manière dont elles sont affichées à l'écran. Dans un site web, la vue serait
  la page web que les utilisateurs voient, avec des éléments tels que les formulaires, les boutons, etc.

- **Contrôleur (Controller) :**
  <br>Le contrôleur agit comme un intermédiaire entre le modèle et la vue. Il reçoit les requêtes des utilisateurs via
  l'interface utilisateur (vue), traite ces requêtes en utilisant les données du modèle et détermine ensuite comment
  afficher les résultats à l'utilisateur. Par exemple, il gère les actions comme l'ajout d'un produit au panier dans
  un site de commerce électronique.

> [!IMPORTANT]  
> Sur le schéma, il y a la mention de routes, celles-ci sont incluses dans chaque controlleur en tant que méthode
> d'appel.

<br/><br/>
<div style="text-align: center">
<img src="https://files.realpython.com/media/mvc_diagram_with_routes.e12c5b982ac8.png" alt="flask-logo" width="60%">
</div>


***

## Tips

- **Les balises TODOs** : 