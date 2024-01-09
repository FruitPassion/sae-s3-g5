from flask import request
from flask_wtf import FlaskForm
from wtforms import EmailField, HiddenField, IntegerField, StringField, PasswordField, SubmitField, DateField
from wtforms.validators import InputRequired, Length
from wtforms.widgets import TextArea, NumberInput

VALIDATE = "validateForm()"


class LoginPersonnelForm(FlaskForm):
    """
    Formulaire de connexion pour le personnel
    """
    login = StringField(validators=[InputRequired(), Length(min=5, max=5)], render_kw={"placeholder": "ABC12"})

    password = PasswordField(validators=[InputRequired(), Length(min=2)], render_kw={"placeholder": "*********"})

    submit = SubmitField("Se connecter")


class AjouterFiche(FlaskForm):
    """
    Formulaire d'ajout de fiche
    """
    nominput = StringField(validators=[InputRequired()], render_kw={"onchange": VALIDATE})
    dateinput = DateField(validators=[InputRequired()], render_kw={"onchange": VALIDATE})
    lieuinput = StringField(validators=[InputRequired()], render_kw={"onchange": VALIDATE})
    decriptioninput = StringField(u'Text', widget=TextArea(), render_kw={"onchange": VALIDATE})
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
    form_identifiant = HiddenField()
    form_nom = StringField(validators=[InputRequired()], render_kw={"placeholder": "Durand"})
    form_prenom = StringField(validators=[InputRequired()], render_kw={"placeholder": "Paul"})
    form_email = EmailField(validators=[InputRequired()], render_kw={"placeholder": "paul.durand@gmail.com"})
    form_password = PasswordField()
    submit = SubmitField("Modifier")


class ModifierAdmin(FlaskForm):
    """
    Formulaire de modification de l'admin admin
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
    cours = StringField(validators=[InputRequired()], render_kw={"placeholder": "Colmater fuite"})
    duree = StringField(validators=[InputRequired()], render_kw={"placeholder": "3"})
    submit = SubmitField("Ajouter")


class ModifierCours(FlaskForm):
    """
    Formulaire de modification d'un cours
    """
    form_identifiant = HiddenField()
    form_theme = StringField(validators=[InputRequired()], render_kw={"placeholder": "Problème tuyauterie"})
    form_cours = StringField(validators=[InputRequired()], render_kw={"placeholder": "Colmater fuite"})
    form_duree = IntegerField(widget=NumberInput(min = 1))
    select_formation = StringField(validators=[InputRequired()], render_kw={"placeholder": "Colmater fuite"})
    form_submit = SubmitField("Modifier")