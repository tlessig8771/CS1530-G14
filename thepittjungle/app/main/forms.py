from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField, DateField
from flask_wtf.file import FileField
from wtforms.validators import DataRequired, Length, Email, Regexp
from wtforms import ValidationError
from flask_pagedown.fields import PageDownField
from ..models import Role, User
from datetime import date


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


class EditProfileForm(FlaskForm):
    name = StringField('Real name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')


class EditProfileAdminForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    username = StringField('Username', validators=[
        DataRequired(), Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               'Usernames must have only letters, numbers, dots or '
               'underscores')])
    confirmed = BooleanField('Confirmed')
    role = SelectField('Role', coerce=int)
    name = StringField('Real name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')


class PostForm(FlaskForm):
    body = PageDownField("What's on your mind?", validators=[DataRequired()])
    submit = SubmitField('Submit')


class CommentForm(FlaskForm):
    body = StringField('Enter your comment', validators=[DataRequired()])
    submit = SubmitField('Submit')
    
class RestaurantForm(FlaskForm):
    name = StringField('Restaurant Name', validators=[
        DataRequired(), Length(1, 64)])
    phone = StringField('Telephone', validators=[DataRequired(), Length(1, 12)])
    address = StringField('Address', validators=[
        DataRequired(), Length(1, 100)])
    tags = StringField('Tags', validators=[Length(0,64)])
    about_me = TextAreaField('About this restaurant')
    file=FileField('Image')
    submit = SubmitField('Submit')
    
    
class EventForm(FlaskForm):
    title = StringField('Title', validators=[
        DataRequired(), Length(1, 64)])
    start_date = DateField('Start date ', validators=[DataRequired()],default=date.today)
    end_date = DateField('End date: ', validators=[DataRequired()],default=date.today)
    tags = StringField('Tags', validators=[Length(0,64)])
    about_me = TextAreaField('Description')
    file=FileField('Image')
    submit = SubmitField('Submit')
    
class AttractionForm(FlaskForm):
    attraction_name = StringField('Attraction Name', validators=[
        DataRequired(), Length(1, 64)])
    phone = StringField('Telephone', validators=[DataRequired(), Length(1, 12)])
    address = StringField('Address', validators=[
        DataRequired(), Length(1, 100)])
    tags = StringField('Tags', validators=[Length(0,64)])
    about_me = TextAreaField('About this attraction')
    file=FileField('Image')
    submit = SubmitField('Submit')
    
class HikeForm(FlaskForm):
    hike_name = StringField('Hike Name', validators=[
        DataRequired(), Length(1, 64)])
    address = StringField('Trail Head', validators=[
        DataRequired(), Length(1, 100)])
    tags = StringField('Tags', validators=[Length(0,64)])
    about_me = TextAreaField('About this hike')
    file=FileField('Image')
    submit = SubmitField('Submit')