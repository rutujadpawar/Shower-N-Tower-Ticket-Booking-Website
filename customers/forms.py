from wtforms import Form, StringField, TextAreaField, PasswordField,SubmitField,validators, ValidationError
from flask_wtf.file import FileRequired,FileAllowed, FileField
from flask_wtf import FlaskForm
from .model import Register
import re



class CustomerRegisterForm(FlaskForm):
    name = StringField('Name: ',[validators.DataRequired()])
    username = StringField('Username: ', [validators.DataRequired()])
    email = StringField('Email: ', [validators.Email(), validators.DataRequired()])
    password = PasswordField('Password: ', [validators.DataRequired(), validators.EqualTo('confirm', message=' Both password must match! ')])
    confirm = PasswordField('Repeat Password: ', [validators.DataRequired()])
    country = StringField('Country: ', [validators.DataRequired()])
    city = StringField('City: ', [validators.DataRequired()])
    contact = StringField('Contact: ', [validators.DataRequired(), validators.Length(max=12)])
    address = StringField('Address: ', [validators.DataRequired()])
    zipcode = StringField('PinCode: ', [validators.DataRequired()])

    profile = FileField('Profile', validators=[FileAllowed(['jpg','png','jpeg','gif'], 'Image only please')])
    submit = SubmitField('Register')


    def validate_name(self, name):
        if re.search('[0-9]',name.data) is not None:
           raise ValidationError("Make sure your name doesn't has a number in it")
        elif re.search("[+\-*\/!()£^@#$%&]",name.data) is not None: 
            raise ValidationError("Make sure your name doesn't has a special character(+,\,-,*,\,/,!,(,),£,^,@,#,$,%,&) in it")
        

    def validate_username(self, username):
        if Register.query.filter_by(username=username.data).first():
            raise ValidationError("This username is already in use!")
        
    def validate_email(self, email):
        if Register.query.filter_by(email=email.data).first():
            raise ValidationError("This email address is already in use!")


    def validate_password(self,password):
        if len(password.data) < 8:
           raise ValidationError("Make sure your password is at least 8 letters")
        elif re.search('[0-9]',password.data) is None:
           raise ValidationError("Make sure your password has a number in it")
        elif re.search('[A-Z]',password.data) is None: 
            raise ValidationError("Make sure your password has a capital letter in it")
        elif re.search('[a-z]',password.data) is None: 
            raise ValidationError("Make sure your password has a small letter in it")
        elif re.search("[[+\-*\/!()£^@#$%&]",password.data) is None: 
            raise ValidationError("Make sure your password has a special character(+,\,-,*,\,/,!,(,),£,^,@,#,$,%,&) in it")
        
    def validate_contact(self,contact):
      
        # 1) Begins with 0 or 91
        # 2) Then contains 7 or 8 or 9.
        # 3) Then contains 9 digits
        Pattern = re.compile("(0|91)?[7-9][0-9]{9}")
        if(not Pattern.match(contact.data)):
            raise ValidationError("Invalid phone number")

    def validate_zipcode(self,zipcode):
        if len(zipcode.data) < 6:
           raise ValidationError("Make sure your zipcode is at least 6 digits")
        



class CustomerLoginFrom(FlaskForm):
    email = StringField('Email: ', [validators.Email(), validators.DataRequired()])
    password = PasswordField('Password: ', [validators.DataRequired()])

   




   

 

    

     

   


    

