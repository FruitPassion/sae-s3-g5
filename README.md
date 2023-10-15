<br><br>
<div align="center">
   <img src="https://www.apeaj.com/wp-content/uploads/2022/05/APEAJ_color2.png" height="130px">
  <h1>SAE3 - Application d'aide aux élèves en difficulté</h1>
  <p>
    Documentation de développement et d'utilisation de l'application web.
    <br />
  </p>
</div>

***
<div align="center">
<img src="https://blog.appseed.us/content/images/2022/01/blog-flask-cover.jpg">
</div>

***

## Prérequis

### - Utilisation de XAMPP/WAMP  <img src="https://pic.clubic.com/v1/images/1501317/raw" height="20">

L'utilisation de XAMPP est nécessaire, mais uniquement pour faire tourner la base de donnée. Ainsi, il suffit seulement
de lancer MySql.

Une fois mysql démaré, on cherchera à executer en tant que root le script `db_creation.sql` en se basant sur
[ces méthodes](https://dev.mysql.com/doc/refman/8.0/en/mysql-batch-commands.html). Ledit script permet ainsi de créer 
l'utilisateur nécessaire à la connexion, mais aussi de créer le schéma de la base de donnée.

### - Installation de Python 3.10 <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/1/1f/Python_logo_01.svg/1200px-Python_logo_01.svg.png" height="20">

Le projet tournant grâce à Python, il est necessaire de l'avoir installé sur sa machine.
La verison que nous utiliserons ici est la 3.10, elle est installable via
[ce lien](https://www.python.org/downloads/release/python-31013/)

Pour connaitre la version que l'on possède du langage, il suffit de taper `python --version` dans son terminal.
Si jamais vous posseder plusieurs versions, il suffit de tapper la version désirée pour la lancer.
Ainsi, si par exemple, je possède python 3.8 et 3.10, et que je veux lancer la 3.10 je taperai simplement `python3.10`
dans le terminal pour lancer un programme `.py` avec cette version.

Sinon, si on ne possède qu'une seule version, on peut
juste utiliser `python` ou `python3`.

### - Création de l'envrionnement virtuel <img src="https://imgur.com/xBG59oA.png" height="20">

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

### - Installation des dépendances/librairies <img src="https://seeklogo.com/images/P/python-package-index-logo-F2EC9F1F8C-seeklogo.com.png" height="20">

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

Le lancement s'effectue grâce au fichier `app.py` que l'on lance à la racine du projet avec l'environnement virtuel
activé.

```shell
(.env) $ python app.py
``` 

On peut ensuite se rendre sur son navigateur web et acceder à l'index via `http://localhost:5000/`
ou `http://127.0.0.1:5000/`

***

<div align="center">
<img src="https://www.payette.com/wp-content/uploads/2018/10/blog-banner_2018_01jan_sketches_3840x1200-e1539271126270-1920x600.jpg" style="height: 120px;width: 100%;object-fit: cover;">
</div>

***

## Architecutre

Le projet suit le modèle de conception MVC. Ce concept de MVC (Model-View-Controller) dans une application web, comme
Flask, est une manière de structurer et d'organiser le code pour améliorer la clarté et la maintenabilité de
l'application. Ainsi :

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
> Sur le schéma, il y a la mention de routes, celles-ci sont incluses dans chaque controller en tant que méthode d'appel.

<br/>
<div align="center">
<img src="https://files.realpython.com/media/mvc_diagram_with_routes.e12c5b982ac8.png" alt="flask-logo" width="60%">
</div>

***

<div align="center">
<img src="https://images.unsplash.com/photo-1555680510-34daedadbdb1?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NHx8Y29tcHV0ZXIlMjBjb2RlfGVufDB8fDB8fHww&w=1000&q=80" style="height: 120px;width: 100%;object-fit: cover;">
</div>

***

## Structure du projet

> [!NOTE]  
> Tous les dossiers contiennent le fichier .gitkeep, ce dernier permet de garder le dossier vide quand on l'envoie sur 
> github. Sans cela, un dossier vide n'est pas pris en compte par le git.

Ainsi, à la racine du projet, on retrouve plusieurs fichiers et dossiers :

### Controller :
Les controller comme dit précedement, permettent à partir d'une route donnée par l'utilisateur, d'effectuer des actions
avec le model et d'afficher une vue.

Dans le fichier `auth.py` par exemple, on retrouve la route **hello-world** dans le navigateur. Cette route est associé
à la fonction `hello_world()`.
Ainsi quand on tape `http://localhost:5000/hello-world` dans notre navigateur, Flask effectue la fonction qui suit nommée
`hello_world()`.

```python
@auth.route('/hello-world')
def hello_world():
    return "Hello World"
```

Cette fonction retourne pour l'instant uniquement du texte. Quand on se rend sur la route en question dans le navigateur,
on voit alors ceci :

![return-hello](https://imgur.com/viWTeIA.png)

On a aussi dans le fichier `auth.py` une autre route nommée `/`. Celle-ci se réferre à un chemin tel que 
`http://localhost:5000/`. Elle est rattaché à la fonction `index()`.

```python
@auth.route('/')
def index():
    personnel = getAllPersonnel()
    return render_template('auth/index.html', personnel=personnel)
```

La fonction `index()` appelle ici la fonction `getAllPersonnel()` et stocke son contenu dans la variable `personnel`.
`getAllPersonnel()` est issue d'un fichier [model](#model-) et permet de récupérer les noms, prénoms et role de tout les
membres de la table Personel.
<br>
On retourne par la suite la fonction `render_template()` à laquelle on passe deux paramètres. Le premier est obligatoire
et correspond au chemin du fichier HTML (la [vue](#view-)) que l'on veut afficher à l'utilisateur. Après le chemin de la
vue, on peut passer autant de paramètre que l'on souhaite et qui correpspondront aux variables que l'on stockera dans la
session utilisateur. <br>
Le résultat de ce chemin est le suivant :

![index](https://imgur.com/fomZxjy.png)

### Custom-Paquets :

Ce dossier contient tous les fichiers python qui ne rentre pas dans les autres dossiers.

### Model :

Les fichiers models sont nommés d'après la table sur laquelle ils se basent.
Quand on se rend sur le fichier `model/personnel.py` par exemple, on peut y voir la fonction `getAllPersonnel()` que
l'on a utilisé précedemment dans notre controller.

```python
def getAllPersonnel():
    personnel = Personnel.query.with_entities(Personnel.Id_Personnel, Personnel.Nom, Personnel.Prenom, Personnel.Role).all()
    return convertToDict(personnel)
```

La premiere ligne est la définition du nom de la fonction ainsi que les paramètres entre les parenthèses (il n'y en a
pas). La seconde ligne est la query qui pourrait se traduire comme suit en SQL:

```sql
SELECT Id_Personnel, Nom, Prenom, Role
FROM Personnel;
```

On indique d'abord la classe python depuis laquelle on veut baser la selection (voir [Model-DB](#model-db-)), ensuite 
on appel la méthode `.query` pour dire que c'est un SELECT. Ensuite, on précise les colonnes que l'on souhaite avec
la méthode `.with_entities` (ne pas en mettre revient à faire un `SELECT *`).<br>
A la toute fin, on utilise la méthode `.all()` pour dire que l'on souhaite récupérer l'ensemble des résultats. Si on 
veut le premier résultat, on aurait par exemple utilisé `.first()`, ou encore pour avoir le nombre de résultats, on aurait
utilisé `.count()`

> [!NOTE]  
> Pour plus d'infos, n'hésitez à consulter la [documentation officielle](https://flask-sqlalchemy.palletsprojects.com/en/2.x/queries/)
ou cet article de [Digital Ocean](https://www.digitalocean.com/community/tutorials/how-to-use-flask-sqlalchemy-to-interact-with-databases-in-a-flask-application)

On stocke le résultat de la query dans une variable `personnel`. Cette variable contient maintenant une liste de classe.
On la retourne donc en utilisant la fonction `convertToDict()` qui permet de convertir une liste de classe en une liste 
de dictionnaire (c'est plus simple à utiliser par la suite).


### Model-DB :

Ce dossier contient toutes les structures des tables de la base de donnée translatée en python.
Cela permet l'utilisation de la librairie SQLAlchemy et ainsi la création des fonctions de 
[model](#model-).

Ici par exemple, on a la table Apprenti.

![table-avoir](https://imgur.com/PvH0dZk.png)

Le fichier `apprenti.py` reprend les différents noms de colonnes, mais précise aussi les types,
les indexs, si la valeur peux être nulle, la clée primaire, etc.

```python
class Apprenti(db.Model):
    __tablename__ = 'Commentaire'
    __table_args__ = {'schema': 'db_fiches_dev'}

    Id_Apprenti = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Nom = db.Column(db.String(50), nullable=False)
    Prenom = db.Column(db.String(50), nullable=False)
    Login = db.Column(db.String(50), nullable=False)
    MDP = db.Column(db.Integer(9), nullable=False)
    Id_Formation = db.Column(db.ForeignKey(f'db_fiches_dev.Formation.Id_Formation'), nullable=False, index=True)

    Formation = db.relationship('Formation', primaryjoin='Apprenti.Id_Formation == Formation.Id_Formation', backref='apprentis')
```

> [!IMPORTANT]   
> La derniere ligne permet de faire la jointure interne de manière automatique si aucune autre jointure n'est précisée.

### Static :

Ce dossier en contient trois autres :
- **CSS** : pour stocker tout les fichiers CSS
- **images** : pour stocker toutes les images
- **JS** : pour stocker tout les fichiers JS

On pourrait par exemple rajouter le dossier 'audio' pour stocker tous les fichiers audio.

### app.py :

Fichier à executer pour lancer l'application. Permet d'importer les différents controller ainsi que de préciser
la configuration à utiliser.

### config.py :

Fichier utilisé pour créer différentes parametrer différentes configurtions pour l'application.