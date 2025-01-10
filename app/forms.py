# app/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, URLField, IntegerField, SubmitField
from wtforms.validators import DataRequired, URL, Optional, Length, NumberRange, ValidationError

class AddPasswordForm(FlaskForm):
    site_name = StringField('Site Name', validators=[
        DataRequired(message="Site name is required"),
        Length(min=1, max=150, message="Site name must be between 1 and 150 characters")
    ])
    site_url = URLField('Site URL', validators=[
        Optional(),
        URL(message="Please enter a valid URL")
    ])
    site_password = PasswordField('Password', validators=[
        DataRequired(message="Password is required")
    ])

class SharePasswordForm(FlaskForm):
    expiry_hours = IntegerField('Expiry Time (hours)', validators=[
        DataRequired(message="Expiry time is required"),
        NumberRange(
            min=1, 
            max=72, 
            message="Expiry time must be between 1 and 72 hours"
        )
    ])
    submit = SubmitField('Generate Shareable Link')

    def validate_expiry_hours(self, field):
        """Custom validator to ensure expiry hours is a positive integer"""
        try:
            value = int(field.data)
            if value <= 0:
                raise ValidationError('Expiry time must be a positive number')
        except (ValueError, TypeError):
            raise ValidationError('Expiry time must be a valid number')