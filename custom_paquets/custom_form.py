from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, HiddenField, DateField
from wtforms.validators import InputRequired, Length
from wtforms.widgets import TextArea


class LoginPersonnelForm(FlaskForm):
    login = StringField(validators=[InputRequired(), Length(min=5, max=5)], render_kw={"placeholder": "ABC12"})

    password = PasswordField(validators=[InputRequired(), Length(min=2)], render_kw={"placeholder": "*********"})

    submit = SubmitField("Se connecter")


class AjouterFiche(FlaskForm):
    nominput = StringField(validators=[InputRequired()], render_kw={"onchange": "validateForm()"})
    dateinput = DateField(validators=[InputRequired()], render_kw={"onchange": "validateForm()"})
    lieuinput = StringField(validators=[InputRequired()], render_kw={"onchange": "validateForm()"})
    decriptioninput = StringField(u'Text', widget=TextArea(), render_kw={"onchange": "validateForm()"})
    submit = SubmitField("Ajouter", render_kw={"disabled": "true"})


class AjouterApprenti(FlaskForm):
    nom = StringField(validators=[InputRequired()], render_kw={"placeholder": "Dupont"})
    prenom = StringField(validators=[InputRequired()], render_kw={"placeholder": "Jean"})
    submit = SubmitField("Enregistrer")

