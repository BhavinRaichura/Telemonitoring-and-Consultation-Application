from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,EmailField, BooleanField,SubmitField
from wtforms.validators import DataRequired,Email,Length,EqualTo,ValidationError
#from application.models import User

class LoginForm(FlaskForm):
    style_email={'class':'input-field','placeholder':"Email"}
    style_pass={'class':'input-field','placeholder':"Password"}
    style_submit={'class':"submit-btn"}

    email = EmailField("Email",validators=[DataRequired(),Email()], render_kw=style_email)
    password = PasswordField("Password",validators=[DataRequired(),Length(min=8,max=15)], render_kw=style_pass)
    submit = SubmitField("Login",render_kw=style_submit)

class RegisterForm(FlaskForm):
    style_name={'class':'input-field','placeholder':"Name"}
    style_email={'class':'input-field','placeholder':"Email"}
    style_pass={'class':'input-field','placeholder':"Password"}
    #style_con_pass={'class':'input-field','placeholder':"Confirm Password"}
    style_submit={'class':"submit-btn"}

    username = StringField("Name",validators=[DataRequired(),Length(min=2,max=50)],render_kw=style_name)
    email = EmailField("Email",validators=[DataRequired(),Email()],render_kw=style_email)
    password= PasswordField("Password",validators=[DataRequired(),Length(min=8,max=15)],render_kw=style_pass)
    #password_confirm = PasswordField("Confirm Password", validators=[DataRequired(),Length(min=6,max=15), EqualTo('password')],render_kw=style_con_pass)
    submit = SubmitField("Signup",render_kw=style_submit)
