from flask_wtf import FlaskForm
from wtforms import (
    DateField,
    EmailField,
    HiddenField,
    IntegerField,
    PasswordField,
    StringField,
    SubmitField,
)
from wtforms.validators import InputRequired, Length
from wtforms.widgets import NumberInput, TextArea

VALIDATE = "validateForm()"
COLMATER_FUITE = "colmater fuite"


class LoginApprentiForm(FlaskForm):
    """
    Formulaire de connexion pour les apprentis
    """

    login = HiddenField(validators=[InputRequired(), Length(min=5, max=5)])

    password = HiddenField(validators=[InputRequired(), Length(min=1, max=9)])


class LoginPersonnelForm(FlaskForm):
    """
    Formulaire de connexion pour le personnel
    """

    login = StringField(validators=[InputRequired(message="Le champ login est obligatoire"), Length(min=5, max=5, message="Le login doit etre de 5 caractères")], render_kw={"placeholder": "ABC12"})

    password = PasswordField(
        validators=[InputRequired(message="Le champ mot de passe est obligatoire"), Length(min=5, message="La longueur du mot de passe est trop courte")], render_kw={"placeholder": "*********"}
    )

    submit = SubmitField("Se connecter")


class LoginPersonnelPin(FlaskForm):
    """
    Formulaire de connexion pour le personnel
    """

    """
    translate this :
    <input type="hidden" name="hiddencode" id="hiddencode" maxlength="6" minlength="6" required value="">
    """
    hiddencode = HiddenField(validators=[InputRequired(), Length(min=6, max=6)], widget=NumberInput(), render_kw={"hidden": "true"})

    fantomclick = SubmitField(render_kw={"hidden": "true"})


class RaisonArretForm(FlaskForm):
    """
    Formulaire de raison d'arrêt
    """

    # text area pour la raison d'arrêt
    raison_arret = StringField("Text", widget=TextArea(), render_kw={"maxlength": "500", "class": "modifiable form-control mb-3"})
    enregistrer = SubmitField("Enregistrer", render_kw={"class": "btn btn-primary form-control"})


class CompleterFiche(FlaskForm):
    """
    Validation CSRF pour la fiche
    """

    submit = SubmitField("Sauvegarder")


class ModifierFiche(FlaskForm):
    """
    Validation CSRF pour la fiche
    """

    # <button class="btn btn-primary form-control" type="submit" value="Submit" form="personnalisation">Envoyer</button>
    submit = SubmitField("Envoyer", render_kw={"class": "btn btn-primary form-control", "form": "personnalisation"})


class AjouterFiche(FlaskForm):
    """
    Formulaire d'ajout de fiche
    """

    nominput = StringField(validators=[InputRequired()], render_kw={"onchange": VALIDATE})
    dateinput = DateField(validators=[InputRequired()], render_kw={"onchange": VALIDATE})
    lieuinput = StringField(validators=[InputRequired()], render_kw={"onchange": VALIDATE})
    decriptioninput = StringField("Text", widget=TextArea(), render_kw={"onchange": VALIDATE})
    nomintervenant = StringField(validators=[InputRequired()], render_kw={"onchange": VALIDATE})
    prenomintervenant = StringField(validators=[InputRequired()], render_kw={"onchange": VALIDATE})
    submit = SubmitField("Ajouter", render_kw={"disabled": "true"})


class AjouterApprenti(FlaskForm):
    """
    Formulaire d'ajout d'apprenti
    """

    nom = StringField(validators=[InputRequired()], render_kw={"placeholder": "Dupont"})
    prenom = StringField(validators=[InputRequired()], render_kw={"placeholder": "Jean"})
    submit = SubmitField("Enregistrer")


class ModifierApprenti(FlaskForm):
    """
    Formulaire de modification d'apprenti
    """

    form_identifiant = HiddenField()
    form_nom = StringField(validators=[InputRequired()], render_kw={"placeholder": "Dupont"})
    form_prenom = StringField(validators=[InputRequired()], render_kw={"placeholder": "Jean"})
    form_submit = SubmitField("Modifier")


class AjouterPersonnel(FlaskForm):
    """
    Formulaire d'ajout de personnel
    """

    password = PasswordField(validators=[InputRequired(), Length(min=6, max=6)], widget=NumberInput())
    nom = StringField(validators=[InputRequired()], render_kw={"placeholder": "Durand"})
    prenom = StringField(validators=[InputRequired()], render_kw={"placeholder": "Paul"})
    email = EmailField(validators=[InputRequired()], render_kw={"placeholder": "paul.durand@gmail.com"})
    submit = SubmitField("Enregistrer")


class ModifierPersonnel(FlaskForm):
    """
    Formulaire de modification de personnel
    """

    form_nom = StringField(validators=[InputRequired()], render_kw={"placeholder": "Durand"})
    form_prenom = StringField(validators=[InputRequired()], render_kw={"placeholder": "Paul"})
    form_email = EmailField(validators=[InputRequired()], render_kw={"placeholder": "paul.durand@gmail.com"})
    form_password = PasswordField(widget=NumberInput())
    submit = SubmitField("Modifier")


class ModifierAdmin(FlaskForm):
    """
    Formulaire de modification de l'admin
    """

    form_identifiant = HiddenField()
    form_nom = StringField(validators=[InputRequired()], render_kw={"placeholder": "Durand"})
    form_prenom = StringField(validators=[InputRequired()], render_kw={"placeholder": "Paul"})
    form_email = EmailField(validators=[InputRequired()], render_kw={"placeholder": "jean@neuil@gmail.com"})
    form_password = PasswordField()
    submit = SubmitField("Modifier Admin")


class AjouterFormation(FlaskForm):
    """
    Formulaire d'ajout de formation
    """

    intitule = StringField(validators=[InputRequired()], render_kw={"placeholder": "Parcours plomberie"})
    niveau_qualif = StringField(validators=[InputRequired()], render_kw={"placeholder": "3"})
    groupe = StringField(validators=[InputRequired()], render_kw={"placeholder": "1"})
    submit = SubmitField("Ajouter")


class ModifierFormation(FlaskForm):
    """
    Formulaire de modification de formation
    """

    form_identifiant = HiddenField()
    form_intitule = StringField(validators=[InputRequired()], render_kw={"placeholder": "Parcours electricité"})
    form_niveau_qualif = StringField(validators=[InputRequired()], render_kw={"placeholder": "3"})
    form_groupe = StringField(validators=[InputRequired()], render_kw={"placeholder": "3"})
    form_submit = SubmitField("Modifier")


class AjouterCours(FlaskForm):
    """
    Formulaire d'ajout d'un cours
    """

    theme = StringField(validators=[InputRequired()], render_kw={"placeholder": "Problème tuyauterie"})
    cours = StringField(validators=[InputRequired()], render_kw={"placeholder": COLMATER_FUITE})
    duree = StringField(validators=[InputRequired()], render_kw={"placeholder": "3"})
    submit = SubmitField("Ajouter")


class ModifierCours(FlaskForm):
    """
    Formulaire de modification d'un cours
    """

    form_theme = StringField(validators=[InputRequired()], render_kw={"placeholder": "Problème tuyauterie"})
    form_cours = StringField(validators=[InputRequired()], render_kw={"placeholder": COLMATER_FUITE})
    form_duree = IntegerField(widget=NumberInput(min=1))
    form_submit = SubmitField("Modifier")


class AjouterMateriel(FlaskForm):
    """
    Formulaire d'ajout d'un matériel
    """

    nom = StringField(validators=[InputRequired()], render_kw={"placeholder": "Chalumeau"})
    submit = SubmitField("Ajouter")


class ModifierMateriel(FlaskForm):
    """
    Formulaire de modification d'un matériel
    """

    form_identifiant = HiddenField()
    form_modifier_nom = StringField(validators=[InputRequired()], render_kw={"placeholder": "Chalumeau"})
    form_modifier_submit = SubmitField("Valider")


class AjouterPicto(FlaskForm):
    """
    Formulaire d'ajout d'un matériel
    """

    label = StringField(render_kw={"placeholder": "Calendrier"})
    souscategorie = StringField(render_kw={"placeholder": "ajouter"})
    submit = SubmitField("Ajouter")


class ModifierPicto(FlaskForm):
    """
    Formulaire de modification d'un matériel
    """

    form_identifiant = HiddenField()
    form_modifier_label = StringField(render_kw={"placeholder": "Calendrier"})
    form_modifier_souscategorie = StringField(render_kw={"placeholder": "ajouter"})
    form_modifier_submit = SubmitField("Valider")
