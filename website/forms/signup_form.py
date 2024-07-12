from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,BooleanField,SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from website.models.Admin_models import Admin

class AdminSignUpForm(FlaskForm):
    email = StringField('Email_Id', 
                        validators=[DataRequired(), Email()], 
                        render_kw={"placeholder": "Enter your Email_Id"})
    
    emp_id = StringField('Employee ID', 
                         validators=[DataRequired()], 
                         render_kw={"placeholder": "Enter your Employee_ID"})
    
    first_name = StringField('Name', 
                             validators=[DataRequired(), Length(min=2, max=150)], 
                             render_kw={"placeholder": "Enter your Full_Name"})
    
    password = PasswordField('Password', 
                             validators=[DataRequired(), Length(min=6)], 
                             render_kw={"placeholder": "Enter your Password"})
    
    confirm_password = PasswordField('Confirm Password', 
                                     validators=[DataRequired(), EqualTo('password')], 
                                     render_kw={"placeholder": "Confirm your Password"})
    
    mobile = StringField('Mobile Number', 
                         validators=[DataRequired(), Length(min=10, max=10)], 
                         render_kw={"placeholder": "Enter your Mobile number"})
    
    user_type = SelectField('Employee Type', 
                            choices=[('admin', 'Admin'), ('employee', 'Employee')],
                              validators=[DataRequired()])
    


    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = Admin.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email is already in use.')

    def validate_mobile(self, mobile):
        user = Admin.query.filter_by(mobile=mobile.data).first()
        if user:
            raise ValidationError('Mobile number is already in use.')

    def validate_emp_id(self, emp_id):
        user = Admin.query.filter_by(emp_id=emp_id.data).first()
        if user:
            raise ValidationError('Employee ID is already in use.')
        

class AdminLoginForm(FlaskForm):
    email = StringField('Email', 
                        validators=[DataRequired(), Email()], 
                        render_kw={"placeholder": "Enter your Email"})
    
    password = PasswordField('Password', 
                             validators=[DataRequired()], 
                             render_kw={"placeholder": "Enter your Password"})
    remember = BooleanField('Remember Me')
    
    def validate_on_submit(self, extra_validators=None):
        return super().validate_on_submit(extra_validators)
    

class AdminVerifyForm(FlaskForm):
    employee_Id = StringField('Employee ID', 
                         validators=[DataRequired()], 
                         render_kw={"placeholder": "Enter your Employee_ID"})
    
    submit = SubmitField('Submit')