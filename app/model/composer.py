from custom_paquets.converter import convert_to_dict
from custom_paquets.gestions_erreur import suplement_erreur
from model.shared_model import DB_SCHEMA
from model.shared_model import ElementBase as Elem
from model.shared_model import db

ERREUR_RECUPERATION = "Erreur lors de la récupération des éléments de la fiche."


class ComposerPresentation(db.Model):
    __tablename__ = "ComposerPresentation"
    __table_args__ = {"schema": DB_SCHEMA}

    id_element = db.Column(db.ForeignKey(f"{DB_SCHEMA}.ElementBase.id_element"), primary_key=True)
    id_fiche = db.Column(db.ForeignKey(f"{DB_SCHEMA}.FicheIntervention.id_fiche"), primary_key=True)
    text = db.Column(db.String(50))
    taille_texte = db.Column(db.String(50))
    audio = db.Column(db.String(50))
    police = db.Column(db.String(50))
    couleur = db.Column(db.String(7))
    couleur_fond = db.Column(db.String(7))
    niveau = db.Column(db.Integer)
    position_elem = db.Column(db.String(50))
    ordre_saisie_focus = db.Column(db.String(50))
    id_pictogramme = db.Column(db.ForeignKey(f"{DB_SCHEMA}.Pictogramme.id_pictogramme"), index=True)
    taille_pictogramme = db.Column(db.Integer)
    couleur_pictogramme = db.Column(db.String(7))
    id_materiel = db.Column(db.ForeignKey(f"{DB_SCHEMA}.Materiel.id_materiel"), index=True)

    ElementBase = db.relationship("ElementBase", primaryjoin="ComposerPresentation.id_element == ElementBase.id_element", backref="composerpresentations")
    FicheIntervention = db.relationship("FicheIntervention", primaryjoin="ComposerPresentation.id_fiche == FicheIntervention.id_fiche", backref="composerpresentations")
    Pictogramme = db.relationship("Pictogramme", primaryjoin="ComposerPresentation.id_pictogramme == Pictogramme.id_pictogramme", backref="composerpresentations")

    @staticmethod
    def get_composer_presentation(id_fiche=1):
        """
        Permet de récupérer tous les éléments d'une fiche

        :return: liste de dictionnaires
        """
        try:
            return ComposerPresentation.query.filter_by(id_fiche=id_fiche).all()
        except Exception as e:
            suplement_erreur(e, message=ERREUR_RECUPERATION)

    @staticmethod
    def get_composer_categorie(id_fiche=1):
        """
        Permet de récupérer toutes les catégories d'une fiche

        :return: liste de dictionnaires
        """
        try:
            return convert_to_dict(ComposerPresentation.query.filter_by(id_fiche=id_fiche).join(Elem).filter_by(type="categorie").all())
        except Exception as e:
            suplement_erreur(e, message=ERREUR_RECUPERATION)

    @staticmethod
    def get_composer_non_categorie(id_fiche=1):
        """
        Permet de récupérer tous les éléments d'une fiche associés à une catégorie

        :return: liste de dictionnaires
        """
        try:
            return convert_to_dict(
                ComposerPresentation.query.with_entities(
                    ComposerPresentation.id_element,
                    ComposerPresentation.text,
                    ComposerPresentation.taille_texte,
                    ComposerPresentation.police,
                    ComposerPresentation.audio,
                    ComposerPresentation.police,
                    ComposerPresentation.couleur,
                    ComposerPresentation.couleur_fond,
                    ComposerPresentation.niveau,
                    ComposerPresentation.position_elem,
                    ComposerPresentation.taille_pictogramme,
                    ComposerPresentation.ordre_saisie_focus,
                    ComposerPresentation.id_pictogramme.label("pictogramme"),
                    ComposerPresentation.taille_pictogramme,
                    ComposerPresentation.couleur_pictogramme,
                    ComposerPresentation.id_materiel,
                )
                .filter_by(id_fiche=id_fiche)
                .join(Elem)
                .filter(Elem.type != "categorie")
                .all()
            )
        except Exception as e:
            suplement_erreur(e, message=ERREUR_RECUPERATION)

    @staticmethod
    def get_elements_base():
        """
        Permet de récupérer les éléments de base de la table ComposerPresentation

        :return: liste de dictionnaires avec l'id, le libellé, le type et l'url audio des éléments
        """
        try:
            return convert_to_dict(
                ComposerPresentation.query.with_entities(
                    Elem.id_element, Elem.libelle.label("libelle_elem"), Elem.type.label("type_elem"), Elem.text.label("label_elem"), Elem.audio.label("audio_elem")
                ).all()
            )
        except Exception as e:
            suplement_erreur(e, message="Erreur lors de la récupération des éléments de base.")

    @staticmethod
    def modifier_composition(form_data, id_fiche):
        try:
            compositions = ComposerPresentation.query.filter_by(id_fiche=id_fiche).all()
            for composition in compositions:
                for key, value in form_data.items():
                    if composition.position_elem == key.split("-")[-1] and "selecteur-element" not in key:
                        ComposerPresentation.modifier_composition_par_element(composition, key, value)
            db.session.commit()
        except Exception as e:
            suplement_erreur(e, message="Erreur lors de la modification de la composition de la fiche.")

    @staticmethod
    def modifier_composition_par_element(composition, key, value):
        from model.pictogramme import Pictogramme

        try:
            if "selecteur-niveau" in key:
                composition.niveau = value
            elif "selecteur-police" in key:
                composition.police = value
            elif "taille-police" in key:
                composition.taille_texte = value
            elif "couleur-police" in key:
                composition.couleur = value
            elif "couleur-fond" in key:
                composition.couleur_fond = value
            elif "selecteur-picto" in key:
                composition.id_pictogramme = Pictogramme.get_pictogramme_by_url(value).id_pictogramme
            elif "taille-picto" in key:
                composition.taille_pictogramme = value
            elif "couleur-picto" in key:
                composition.couleur_pictogramme = value

        except Exception as e:
            suplement_erreur(e, message="Erreur lors de la modification de la composition de la fiche.")

    @staticmethod
    def maj_materiaux_fiche(majs: dict, id_fiche: str):
        """
        Permet de mettre à jour les matériaux d'une fiche

        :param majs: dictionnaire contenant les matériaux à mettre à jour
        :param id_fiche: id de la fiche à mettre à jour
        :return: None
        """
        try:
            compositions = ComposerPresentation.query.filter_by(id_fiche=id_fiche).all()
            for element in compositions:
                if element.position_elem in majs.keys():
                    element.id_materiel = majs[f"{element.position_elem}"]
            db.session.commit()
        except Exception as e:
            suplement_erreur(e, message="Erreur lors de l'enregistrement des modifications de la fiche.")

    @staticmethod
    def maj_contenu_fiche(majs: dict, id_fiche: str):
        """
        Permet de mettre à jour le contenu d'une fiche

        :param majs: dictionnaire contenant les éléments à mettre à jour
        :param id_fiche: id de la fiche à mettre à jour
        :return:
        """
        try:
            compositions = ComposerPresentation.query.filter_by(id_fiche=id_fiche).all()
            for element in compositions:
                if element.position_elem in majs.keys():
                    element.text = majs[f"{element.position_elem}"]
            db.session.commit()
        except Exception as e:
            suplement_erreur(e, message="Erreur lors de l'enregistrement des modifications de la fiche.")

    @staticmethod
    def get_composer_presentation_par_apprenti(id_fiche):
        """
        Permet de récupérer ce que l'apprenti a complété dans une fiche
        """
        try:
            return db.session.query(ComposerPresentation).filter_by(id_fiche=id_fiche).join(Elem).all()
        except Exception as e:
            suplement_erreur(e, message="Erreur lors de la récupération des éléments de la fiche.")

    @staticmethod
    def get_checkbox_on(id_fiche):
        """
        Permet de récupérer les checkbox cochées de la fiche

        :param id_fiche:
        :return:
        """
        try:
            return ComposerPresentation.query.filter_by(text="on", id_fiche=id_fiche).all()
        except Exception as e:
            suplement_erreur(e, message="Erreur lors de la récupération des checkbox de la fiche.")

    @staticmethod
    def get_radio_radioed(id_fiche):
        """
        Permet de récupérer les radios cochées de la fiche

        :param id_fiche:
        :return:
        """
        try:
            return ComposerPresentation.query.filter_by(text="radioed", id_fiche=id_fiche).all()
        except Exception as e:
            suplement_erreur(e, message="Erreur lors de la récupération des radios de la fiche.")
