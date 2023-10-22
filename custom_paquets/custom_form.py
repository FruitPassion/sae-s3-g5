from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length


class RegisterPersonnelForm(FlaskForm):
    login = StringField(validators=[InputRequired(), Length(min=5, max=5)], render_kw={"placeholder": "ABC12"})

    password = PasswordField(validators=[InputRequired(), Length(min=2)], render_kw={"placeholder": "*********"})

    submit = SubmitField("Se connecter")
