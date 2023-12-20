from flask import request
from flask_wtf import FlaskForm
from wtforms import EmailField, HiddenField, StringField, PasswordField, SubmitField, DateField
from wtforms.validators import InputRequired, Length
from wtforms.widgets import TextArea, NumberInput


class LoginPersonnelForm(FlaskForm):
    login = StringField(validators=[InputRequired(), Length(min=5, max=5)], render_kw={"placeholder": "ABC12"})

    password = PasswordField(validators=[InputRequired(), Length(min=2)], render_kw={"placeholder": "*********"})

    submit = SubmitField("Se connecter")


class AjouterFiche(FlaskForm):
    nominput = StringField(validators=[InputRequired()], render_kw={"onchange": "validateForm()"})
    dateinput = DateField(validators=[InputRequired()], render_kw={"onchange": "validateForm()"})
    lieuinput = StringField(validators=[InputRequired()], render_kw={"onchange": "validateForm()"})
    decriptioninput = StringField(u'Text', widget=TextArea(), render_kw={"onchange": "validateForm()"})
    nomintervenant = StringField(validators=[InputRequired()], render_kw={"onchange": "validateForm()"})
    prenomintervenant = StringField(validators=[InputRequired()], render_kw={"onchange": "validateForm()"})
    submit = SubmitField("Ajouter", render_kw={"disabled": "true"})


class AjouterApprenti(FlaskForm):
    nom = StringField(validators=[InputRequired()], render_kw={"placeholder": "Dupont"})
    prenom = StringField(validators=[InputRequired()], render_kw={"placeholder": "Jean"})
    submit = SubmitField("Enregistrer")


class ModifierApprenti(FlaskForm):
    form_identifiant = HiddenField()
    form_password = PasswordField()
    form_nom = StringField(validators=[InputRequired()], render_kw={"placeholder": "Dupont"})
    form_prenom = StringField(validators=[InputRequired()], render_kw={"placeholder": "Jean"})
    form_submit = SubmitField("Modifier")


class AjouterPersonnel(FlaskForm):
    password = PasswordField(validators=[InputRequired(), Length(min=6, max=6)], widget=NumberInput())
    nom = StringField(validators=[InputRequired()], render_kw={"placeholder": "Durand"})
    prenom = StringField(validators=[InputRequired()], render_kw={"placeholder": "Paul"})
    email = EmailField(validators=[InputRequired()], render_kw={"placeholder": "paul.durand@gmail.com"})
    submit = SubmitField("Enregistrer")


class ModifierPersonnel(FlaskForm):
    form_identifiant = HiddenField()
    form_nom = StringField(validators=[InputRequired()], render_kw={"placeholder": "Durand"})
    form_prenom = StringField(validators=[InputRequired()], render_kw={"placeholder": "Paul"})
    form_email = EmailField(validators=[InputRequired()], render_kw={"placeholder": "paul.durand@gmail.com"})
    form_password = PasswordField()
    submit = SubmitField("Modifier")


class ModifierAdmin(FlaskForm):
    form_identifiant = HiddenField()
    form_nom = StringField(validators=[InputRequired()], render_kw={"placeholder": "Durand"})
    form_prenom = StringField(validators=[InputRequired()], render_kw={"placeholder": "Paul"})
    form_email = EmailField(validators=[InputRequired()], render_kw={"placeholder": "paul.durand@gmail.com"})
    form_password = PasswordField()
    submit = SubmitField("Modifier Admin")


class AjouterFormation(FlaskForm):
    intitule = StringField(validators=[InputRequired()], render_kw={"placeholder": "Parcours plomberie"})
    niveau_qualif = StringField(validators=[InputRequired()], render_kw={"placeholder": "3"})
    groupe = StringField(validators=[InputRequired()], render_kw={"placeholder": "1"})
    submit = SubmitField("Ajouter")
    
class ModifierFormation(FlaskForm):
    form_identifiant = HiddenField()
    form_intitule = StringField(validators=[InputRequired()], render_kw={"placeholder": "Parcours electricité"})
    form_niveau_qualif = StringField(validators=[InputRequired()], render_kw={"placeholder": "3"})
    form_groupe = StringField(validators=[InputRequired()], render_kw={"placeholder": "3"})
    form_submit = SubmitField("Modifier")