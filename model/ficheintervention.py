from datetime import date
import logging
from sqlalchemy import func, asc
from time import strftime, localtime

from custom_paquets.converter import convert_to_dict
from custom_paquets.gestions_erreur import suplement_erreur

from model.apprenti import Apprenti
from model.personnel import Personnel
from model.shared_model import db, DB_SCHEMA
from model.composer import Compo


class FicheIntervention(db.Model):
    __tablename__ = 'FicheIntervention'
    __table_args__ = {'schema': DB_SCHEMA}

    id_fiche = db.Column(db.Integer, primary_key=True, autoincrement=True)
    numero = db.Column(db.Integer, nullable=False)
    nom_du_demandeur = db.Column(db.String(50))
    date_demande = db.Column(db.Date)
    localisation = db.Column(db.String(50))
    description_demande = db.Column(db.Text)
    degre_urgence = db.Column(db.Integer)
    couleur_intervention = db.Column(db.String(50))
    etat_fiche = db.Column(db.Integer)
    date_creation = db.Column(db.DateTime)
    photo_avant = db.Column(db.String(150))
    photo_apres = db.Column(db.String(150))
    nom_intervenant = db.Column(db.String(50), nullable=False)
    prenom_intervenant = db.Column(db.String(50), nullable=False)
    id_apprenti = db.Column(db.ForeignKey(f'{DB_SCHEMA}.Apprenti.id_apprenti'), nullable=False, index=True)
    id_personnel = db.Column(db.ForeignKey(f'{DB_SCHEMA}.Personnel.id_personnel'), nullable=False, index=True)
    id_cours = db.Column(db.ForeignKey(f'{DB_SCHEMA}.Cours.id_cours'), nullable=False, index=True)

    Apprenti = db.relationship('Apprenti', primaryjoin='FicheIntervention.id_apprenti == Apprenti.id_apprenti',
                               backref='fiches')
    Personnel = db.relationship('Personnel', primaryjoin='FicheIntervention.id_personnel == Personnel.id_personnel',
                                backref='fiches')
    Cours = db.relationship('Cours', primaryjoin='FicheIntervention.id_cours == Cours.id_cours',
                            backref='fiches')

    @staticmethod
    def get_fiches_techniques_par_login(login):
        """
        Récupère les identifiants des fiches techniques associées à un apprenti à partir de son Login

        :return: Les fiches techniques de l'apprenti
        """
        try:
            from model.apprenti import Apprenti
            id_apprenti = Apprenti.get_id_apprenti_by_login(login)
            return FicheIntervention.query.filter_by(id_apprenti=id_apprenti).order_by(asc(
                FicheIntervention.etat_fiche)).all()
        except Exception as e:
            logging.error(f"Erreur lors de la récupération des fiches techniques de l'apprenti {login}")
            logging.error(e)

    @staticmethod
    def get_proprietaire_fiche_par_id_fiche(id_fiche):
        """
        Récupère le propriétaire d'une fiche à partir de son id

        :return: Le propriétaire de la fiche
        """
        try:
            return FicheIntervention.query.filter_by(id_fiche=id_fiche).join(Apprenti).with_entities(
                Apprenti.login).first().login
        except Exception as e:
            logging.error(f"Erreur lors de la récupération du propriétaire de la fiche {id_fiche}")
            logging.error(e)

    @staticmethod
    def get_fiche_par_id_apprenti(id_apprenti):
        """
        Récupère les identifiants des fiches techniques associées à un apprenti à partir de son id

        :return: Les fiches techniques de l'apprenti
        """
        try:
            return FicheIntervention.query.filter_by(id_apprenti=id_apprenti).with_entities(
                FicheIntervention.id_fiche, FicheIntervention.numero).first()
        except Exception as e:
            logging.error(f"Erreur lors de la récupération des fiches techniques de l'apprenti {id_apprenti}")
            logging.error(e)

    @staticmethod
    def get_fiche_par_id_fiche(id_fiche):
        """
        Récupère les identifiants des fiches techniques associées à un apprenti à partir de son id

        :return: Les fiches techniques de l'apprenti
        """
        try:
            return FicheIntervention.query.filter_by(id_fiche=id_fiche).first()
        except Exception as e:
            logging.error(f"Erreur lors de la récupération des fiches techniques de l'apprenti {id_fiche}")
            logging.error(e)

    @staticmethod
    def get_niveau_etat_fiches_par_login(login):
        """
        Récupère le total des niveaux de chaque fiche technique associé à un apprenti à partir de son Login

        :return: Les niveaux des fiches techniques de l'apprenti
        """
        try:
            id_apprenti = Apprenti.get_id_apprenti_by_login(login)
            fiche_niveau = (
                db.session.query(FicheIntervention.numero, func.sum(Compo.niveau).label('total_niveau'),
                                 FicheIntervention.etat_fiche).join(Compo).join(Apprenti)
                .filter(FicheIntervention.id_apprenti == id_apprenti)
                .filter(~Compo.position_elem.like('%0%')).group_by(FicheIntervention.id_fiche).all()
            )
            return convert_to_dict(fiche_niveau)
        except Exception as e:
            logging.error(f"Erreur lors de la récupération des niveaux des fiches techniques de l'apprenti {login}")
            logging.error(e)

    @staticmethod
    def get_niveau_moyen_champs_par_login(login):
        """
        Récupère le niveau moyen des champs de chaque fiche technique associée à un apprenti à partir de son Login

        :return: Le niveau moyen des champs de chaque fiche technique de l'apprenti
        """
        try:
            id_apprenti = Apprenti.get_id_apprenti_by_login(login)
            niveau_champ = (
                db.session.query(FicheIntervention.numero, func.avg(Compo.niveau).label('moyenne_niveau'))
                .join(Compo)
                .join(Apprenti)
                .filter(FicheIntervention.id_apprenti == id_apprenti)
                .filter(~Compo.position_elem.like('%0%'))
                .group_by(FicheIntervention.id_fiche)
                .all()
            )
            liste_niveau_champ = niveau_champ
            total_niveau_champ = 0
            if len(liste_niveau_champ) == 0:
                return 0
            else:
                for niveau in liste_niveau_champ:
                    total_niveau_champ += niveau.moyenne_niveau
                return round(total_niveau_champ / len(liste_niveau_champ), 2)
        except Exception as e:
            logging.error(
                f"Erreur lors de la récupération des niveaux moyens des champs des fiches techniques de l'apprenti {login}")
            logging.error(e)

    @staticmethod
    def valider_fiche(id_fiche):
        """
        Valide une fiche

        :param id_fiche: id de la fiche à valider
        :return: Code de validation en fonction du résultat
        """
        try:
            fiche = FicheIntervention.query.filter_by(id_fiche=id_fiche).first()
            fiche.etat_fiche = 1
            db.session.commit()
        except Exception as e:
            logging.error(f"Erreur lors de la validation de la fiche {id_fiche}")
            logging.error(e)

    @staticmethod
    def get_nombre_fiches_finies_par_login(login):
        """
        Récupère le nombre de fiches finies par un apprenti à partir de son Login

        :return: Les fiches techniques de l'apprenti
        """
        try:
            id_apprenti = Apprenti.get_id_apprenti_by_login(login)
            return FicheIntervention.query.filter_by(id_apprenti=id_apprenti).filter_by(etat_fiche=True).count()
        except Exception as e:
            logging.error(f"Erreur lors de la récupération du nombre de fiches finies de l'apprenti {login}")
            logging.error(e)

    @staticmethod
    def get_etat_fiche_par_id_fiche(id_fiche):
        """
        Récupère l'état d'une fiche à partir de son id

        :return: L'état de la fiche
        """
        try:
            return FicheIntervention.query.filter_by(id_fiche=id_fiche).with_entities(
                FicheIntervention.etat_fiche).first().etat_fiche
        except Exception as e:
            logging.error(f"Erreur lors de la récupération de l'état de la fiche {id_fiche}")
            logging.error(e)

    @staticmethod
    def get_fiches_techniques_finies_par_login(login):
        """
        Récupère les identifiants des fiches techniques associées à un apprenti à partir de son Login

        :return: Les fiches techniques de l'apprenti
        """
        try:
            id_apprenti = Apprenti.get_id_apprenti_by_login(login)
            return FicheIntervention.query.filter_by(id_apprenti=id_apprenti).filter_by(etat_fiche=True).all()
        except Exception as e:
            logging.error(f"Erreur lors de la récupération des fiches techniques finies de l'apprenti {login}")
            logging.error(e)

    @staticmethod
    def get_fiche_apprentis_existe(login: str):
        """
        Vérifie si l'apprenti a déjà une fiche

        :return: True s'il en a au moins une, False sinon
        """
        try:
            return FicheIntervention.query.filter_by(id_apprenti=Apprenti.get_id_apprenti_by_login(login)).count() != 0
        except Exception as e:
            logging.error(f"Erreur lors de la vérification de l'existence d'une fiche pour l'apprenti {login}")
            logging.error(e)

    @staticmethod
    def get_id_fiche_apprenti(login: str, numero: int):
        """
        Récupère l'id de la fiche d'un apprenti

        :param login: login de l'apprenti
        :param numero: numéro de la fiche
        :return: id de la fiche
        """
        try:
            if FicheIntervention.get_fiche_apprentis_existe(login):
                return FicheIntervention.query.filter_by(id_apprenti=Apprenti.get_id_apprenti_by_login(login),
                                                         numero=numero).with_entities(
                    FicheIntervention.id_fiche).first().id_fiche
            else:
                return None
        except Exception as e:
            logging.error(f"Erreur lors de la récupération de l'id de la fiche de l'apprenti {login}")
            logging.error(e)

    @staticmethod
    def get_dernier_numero_fiche_apprenti(login: str):
        try:
            if FicheIntervention.get_fiche_apprentis_existe(login):
                return FicheIntervention.query.filter_by(id_apprenti=Apprenti.get_id_apprenti_by_login(login)).with_entities(
                    FicheIntervention.numero).order_by(FicheIntervention.numero.desc()).first().numero
            else:
                return 0
        except Exception as e:
            logging.error(f"Erreur lors de la récupération du dernier numéro de la fiche de l'apprenti {login}")
            logging.error(e)

    @staticmethod
    def get_dernier_id_fiche_apprenti(login: str):
        """
        Récupère le dernier id de la fiche d'un apprenti

        :param login: login de l'apprenti
        :return: id de la fiche
        """
        try:
            if FicheIntervention.get_fiche_apprentis_existe(login):
                return FicheIntervention.query.filter_by(id_apprenti=Apprenti.get_id_apprenti_by_login(login)).with_entities(
                    FicheIntervention.id_fiche).order_by(FicheIntervention.id_fiche.desc()).first().id_fiche
            else:
                return None
        except Exception as e:
            logging.error(f"Erreur lors de la récupération du dernier id de la fiche de l'apprenti {login}")
            logging.error(e)

    @staticmethod
    def copier_fiche(id_fiche: int, login_personnel: str):
        """
        A partir d'une fiche existante, la duplique et l'assigne a un apprenti

        :param id_fiche: id de la fiche à copier
        :param login_personnel: login du personnel
        :return: Code de validation en fonction du résultat
        """
        try:
            fiche_a_copier = FicheIntervention.query.filter_by(id_fiche=id_fiche).first()
            fiche_a_copier.etat_fiche = 2
            login_apprenti = Apprenti.get_login_apprenti_by_id(fiche_a_copier.id_apprenti)
            numero = FicheIntervention.get_dernier_numero_fiche_apprenti(login_apprenti) + 1
            nouvelle_fiche = FicheIntervention(numero=numero, nom_du_demandeur=fiche_a_copier.nom_du_demandeur,
                                               date_demande=fiche_a_copier.date_demande,
                                               localisation=fiche_a_copier.localisation,
                                               description_demande=fiche_a_copier.description_demande,
                                               degre_urgence=fiche_a_copier.degre_urgence,
                                               couleur_intervention=fiche_a_copier.couleur_intervention,
                                               etat_fiche=0, date_creation=strftime("%Y-%m-%d %H:%M:%S", localtime()),
                                               photo_avant=None, photo_apres=None,
                                               nom_intervenant=fiche_a_copier.nom_intervenant,
                                               prenom_intervenant=fiche_a_copier.prenom_intervenant,
                                               id_personnel=Personnel.get_id_personnel_by_login(login_personnel),
                                               id_apprenti=Apprenti.get_id_apprenti_by_login(login_apprenti),
                                               id_cours=fiche_a_copier.id_cours)
            db.session.add(nouvelle_fiche)
            db.session.commit()
            composer_fiche = Compo.get_composer_presentation(id_fiche)
            FicheIntervention.remplir_fiche(composer_fiche, nouvelle_fiche)

            return nouvelle_fiche.id_fiche
        except Exception as e:
            logging.error(f"Erreur lors de la copie de la fiche {id_fiche}")
            logging.error(e)

    @staticmethod
    def assigner_fiche_dummy_eleve(login_apprenti: str, id_personnel: str, date_demande: date, nom_demandeur: str,
                                   localisation: str, description_demande: str, degre_urgence: int,
                                   couleur_intervention: str, nom_intervenant: str, prenom_intervenant: str, id_cours: str):
        """
        A partir de la fiche par defaut, la duplique et l'assigne a un apprenti

        :param login_apprenti: login de l'apprenti
        :param id_personnel: login du personnel
        :param date_demande: date de la demande
        :param nom_demandeur: nom du demandeur
        :param localisation: localisation de la demande
        :param description_demande: description de la demande
        :param degre_urgence: degré d'urgence de la demande
        :param couleur_intervention: couleur de l'intervention
        :param nom_intervenant: nom de l'intervenant
        :param prenom_intervenant: prénom de l'intervenant
        :param id_cours: id du cours
        :return: Code de validation en fonction du résultat
        """
        try:
            # Si l'apprenti a déjà une fiche, on copie les éléments de la dernière fiche
            if FicheIntervention.get_fiche_apprentis_existe(login_apprenti):
                composer_fiche = Compo.get_composer_presentation(FicheIntervention.get_dernier_id_fiche_apprenti(login_apprenti))
            # Sinon on copie les éléments de la fiche par défaut
            else:
                composer_fiche = Compo.get_composer_presentation()

            numero = FicheIntervention.get_dernier_numero_fiche_apprenti(login_apprenti) + 1

            print(id_personnel)
            nouvelle_fiche = FicheIntervention(numero=numero, nom_du_demandeur=nom_demandeur, date_demande=date_demande,
                                               localisation=localisation, description_demande=description_demande,
                                               degre_urgence=degre_urgence, couleur_intervention=couleur_intervention,
                                               etat_fiche=0, date_creation=strftime("%Y-%m-%d %H:%M:%S", localtime()),
                                               photo_avant=None, photo_apres=None, nom_intervenant=nom_intervenant,
                                               prenom_intervenant=prenom_intervenant,
                                               id_personnel=id_personnel,
                                               id_apprenti=Apprenti.get_id_apprenti_by_login(login_apprenti), id_cours=id_cours)
            db.session.add(nouvelle_fiche)
            db.session.commit()
            # On ajoute les éléments de la fiche
            FicheIntervention.remplir_fiche(composer_fiche, nouvelle_fiche)

            return FicheIntervention.get_dernier_id_fiche_apprenti(login_apprenti)

        except Exception as e:
            logging.error(f"Erreur lors de l'assignation de la fiche à l'apprenti {login_apprenti}")
            logging.error(e)

    @staticmethod
    def remplir_fiche(composer_fiche, fiche):
        """
        Remplit la fiche avec les éléments de la fiche par défaut

        :param composer_fiche: éléments de la fiche par défaut
        :param fiche: fiche à remplir
        :return:
        """
        try:
            for element in composer_fiche:
                composer = Compo(id_element=element.id_element, id_fiche=fiche.id_fiche,
                                                id_pictogramme=element.id_pictogramme,
                                                taille_pictogramme=element.taille_pictogramme,
                                                couleur_pictogramme=element.couleur_pictogramme,
                                                text=None, taille_texte=element.taille_texte, audio=None,
                                                police=element.police, couleur=element.couleur,
                                                couleur_fond=element.couleur_fond, niveau=element.niveau,
                                                position_elem=element.position_elem,
                                                ordre_saisie_focus=element.ordre_saisie_focus)
                db.session.add(composer)
            db.session.commit()
        except Exception as e:
            suplement_erreur(e, f"Erreur lors du remplissage de la fiche {fiche.id_fiche}")

    @staticmethod
    def definir_photo(id_fiche, avant_apres):
        """
        Définit la photo avant et la photo après de la fiche
        """
        try:
            fiche = FicheIntervention.query.filter_by(id_fiche=id_fiche).first()
            if avant_apres:
                fiche.photo_apres = f'{id_fiche}_photo-apres.jpg'
            else:
                fiche.photo_avant = f'{id_fiche}_photo-avant.jpg'
            db.session.commit()
        except Exception as e:
            suplement_erreur(e, f"Erreur lors de la définition des photos de la fiche {id_fiche}")
