import logging
from datetime import datetime

from model.shared_model import DB_SCHEMA, db


class LaisserTrace(db.Model):
    __tablename__ = "LaisserTrace"
    __table_args__ = {"schema": DB_SCHEMA}

    id_personnel = db.Column(db.ForeignKey(f"{DB_SCHEMA}.Personnel.id_personnel"), primary_key=True)
    horodatage = db.Column(db.DateTime, primary_key=True)
    intitule = db.Column(db.String(50), nullable=False)
    eval_texte = db.Column(db.Text, nullable=False)
    commentaire_texte = db.Column(db.Text, nullable=False)
    eval_audio = db.Column(db.String(255))
    commentaire_audio = db.Column(db.String(50))
    apprenti = db.Column(db.Integer, nullable=True)
    id_fiche = db.Column(db.ForeignKey(f"{DB_SCHEMA}.FicheIntervention.id_fiche"), nullable=False, index=True)

    FicheIntervention = db.relationship("FicheIntervention", primaryjoin="LaisserTrace.id_fiche == FicheIntervention.id_fiche", backref="traces")
    Personnel = db.relationship("Personnel", primaryjoin="LaisserTrace.id_personnel == Personnel.id_personnel", backref="traces")

    @staticmethod
    def get_commentaires_par_fiche(id_fiche):
        """
        Récupère les commentaires de la fiche id_fiche d'un apprenti

        :return: Tous les commentaires
        """
        try:
            return LaisserTrace.query.filter_by(id_fiche=id_fiche).all()
        except Exception as e:
            logging.error(f"Erreur lors de la récupération des commentaires de la fiche {id_fiche}")
            logging.error(e)

    @staticmethod
    def get_commentaires_type_par_fiche(id_fiche, apprenti="0"):
        """
        Récupère les commentaires de la fiche id_fiche d'un apprenti

        :return: Tous les commentaires (évaluation texte et audio et commentaires audio et texte), leur horodatage
        et l'identifiant de l'éducateur ayant créé la trace
        """
        try:
            return LaisserTrace.query.filter_by(id_fiche=id_fiche, apprenti=apprenti).first()
        except Exception as e:
            logging.error(f"Erreur lors de la récupération des commentaires de la fiche {id_fiche}")
            logging.error(e)

    @staticmethod
    def modifier_commentaire_texte(id_fiche, horodatage, commentaire_texte, type_commentaire):
        """
        Récupère le commentaire texte la la fiche id_fiche
        Modifie le commentaire textuel avec commentaire_texte

        :return: None
        """
        try:
            trace = LaisserTrace.query.filter_by(id_fiche=id_fiche, horodatage=horodatage, apprenti=f"{int(type_commentaire != 'educateur')}").first()
            trace.commentaire_texte = commentaire_texte
            db.session.commit()
        except Exception as e:
            logging.error(f"Erreur lors de la modification du commentaire textuel de la fiche {id_fiche} du {horodatage}")
            logging.error(e)

    @staticmethod
    def modifier_commentaire_audio(id_fiche, horodatage, commentaire_audio, type_commentaire):
        """
        Récupère le commentaire audio du horodatage (date/heure) de la fiche id_fiche
        Modifie le (chemin ?) commentaire audio  avec commentaire_audio
        :return: None
        """
        try:
            trace = LaisserTrace.query.filter_by(id_fiche=id_fiche, horodatage=horodatage, apprenti=f"{int(type_commentaire != 'educateur')}").first()
            trace.commentaire_audio = commentaire_audio
            db.session.commit()
        except Exception as e:
            logging.error(f"Erreur lors de la modification du commentaire audio de la fiche {id_fiche} du {horodatage}")
            logging.error(e)

    @staticmethod
    def modifier_evaluation_texte(id_fiche, horodatage, evaluation_texte, type_commentaire):
        """
        Récupère l'évaluation textuelle du horodatage (date/heure) de la fiche id_fiche
        Modifie l'évaluation textuelle evaluation_texte avec evaluation_texte

        :return: None
        """
        try:
            trace = LaisserTrace.query.filter_by(id_fiche=id_fiche, horodatage=horodatage, apprenti=f"{int(type_commentaire != 'educateur')}").first()
            trace.eval_texte = evaluation_texte
            db.session.commit()
        except Exception as e:
            logging.error(f"Erreur lors de la modification de l'évaluation textuelle de la fiche {id_fiche} du {horodatage}")
            logging.error(e)

    @staticmethod
    def modifier_eval_audio(id_fiche, horodatage, eval_audio, type_commentaire):
        """
        Récupère l'évaluation audio du horodatage (date/heure) de la fiche id_fiche
        Modifie (le chemin ?) l'évaluation audio eval_audio avec eval_audio

        :return: None
        """
        try:
            trace = LaisserTrace.query.filter_by(id_fiche=id_fiche, horodatage=horodatage, apprenti=f"{int(type_commentaire != 'educateur')}").first()
            trace.eval_audio = eval_audio
            db.session.commit()
        except Exception as e:
            logging.error(f"Erreur lors de la modification de l'évaluation audio de la fiche {id_fiche} du {horodatage}")
            logging.error(e)

    @staticmethod
    def ajouter_commentaires_evaluation(id_fiche, commentaire_texte, eval_texte, commentaire_audio, eval_audio, login, intitule, type_c):
        """
        Ajoute les commentaires et évaluations d'une fiche technique d'un apprenti

        :return: None
        """
        try:
            from model.personnel import Personnel

            id_personnel = Personnel.get_id_personnel_by_login(login)
            horodatage = datetime.now()
            trace = LaisserTrace(
                id_fiche=id_fiche,
                id_personnel=id_personnel,
                horodatage=horodatage,
                commentaire_texte=commentaire_texte,
                eval_texte=eval_texte,
                commentaire_audio=commentaire_audio,
                eval_audio=eval_audio,
                apprenti=type_c,
                intitule=intitule,
            )
            db.session.add(trace)
            db.session.commit()
        except Exception as e:
            logging.error(f"Erreur lors de l'ajout des commentaires et évaluations de la fiche {id_fiche}")
            logging.error(e)
