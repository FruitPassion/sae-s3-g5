from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, HiddenField, DateField
from wtforms.validators import InputRequired, Length
from wtforms.widgets import TextArea


class LoginPersonnelForm(FlaskForm):
    login = StringField(validators=[InputRequired(), Length(min=5, max=5)], render_kw={"placeholder": "ABC12"})

    password = PasswordField(validators=[InputRequired(), Length(min=2)], render_kw={"placeholder": "*********"})

    submit = SubmitField("Se connecter")


class AjouterFiche(FlaskForm):
    nominput = StringField(validators=[InputRequired()])
    dateinput = DateField(validators=[InputRequired()])
    lieuinput = StringField(validators=[InputRequired()])
    decriptioninput = StringField(u'Text', widget=TextArea())
    submit = SubmitField("Ajouter")
