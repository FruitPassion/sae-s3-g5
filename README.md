<br><br>
<div align="center">
   <img src="https://imgur.com/mAozU4s.png" height="140px">
  <h1>SAE3 - Application d'aide aux élèves en difficulté</h1>
  <p>
    Documentation de déploiement de l'application web.
    <br />
  </p>
</div>

***
<div align="center">
<img src="https://camo.githubusercontent.com/4bc4b80fb435c49242edde00eecfd62b2bfebc2931e83fd5f0b651192a290386/68747470733a2f2f696d6775722e636f6d2f784b6249336e662e706e67">
</div>

***

## Prérequis

- Type de serveur: dédié/vierge
- OS: Debian 11/12
- Processeur: amd64 (x86_64) our arm64 (aarch64)
- RAM (minimum recommandé): 2 Go
- Stockage (minimum recommandé): 15 Go 
- Paquets: git
- Privilèges: Accès root

## Installation/Déploiement

Cloner ce projet dans le répertoire souhaité

```bash
$ git clone https://github.com/FruitPassion/sae-s3-g5.git nom-projet
```

Mettez vous en root.

```bash
$ sudo su -
```

ou


```bash
$ su -
```

Rendez le fichier `init.sh` à la racine du projet executable.

```bash
$ chmod +x init.sh
```

Il ne vous reste plus qu'à executer le fichier `init.sh` et à vous servir un café en attendant la fin de l'installation.

```bash
$ ./init.sh
```

