from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FileField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from models import User

class LoginForm(FlaskForm):
    email = StringField('البريد الإلكتروني', validators=[DataRequired(), Email()])
    password = PasswordField('كلمة المرور', validators=[DataRequired()])
    remember_me = BooleanField('تذكرني')
    submit = SubmitField('تسجيل الدخول')

class RegistrationForm(FlaskForm):
    username = StringField('اسم المستخدم', validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField('البريد الإلكتروني', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('كلمة المرور', validators=[DataRequired(), Length(min=8)])
    password2 = PasswordField('تأكيد كلمة المرور', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('تسجيل')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('اسم المستخدم مستخدم بالفعل. الرجاء اختيار اسم آخر.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('البريد الإلكتروني مستخدم بالفعل. الرجاء استخدام بريد آخر.')

class ProfileForm(FlaskForm):
    username = StringField('اسم المستخدم', validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField('البريد الإلكتروني', validators=[DataRequired(), Email(), Length(max=120)])
    bio = TextAreaField('نبذة عنك', validators=[Length(max=500)])  # ✅ أضفناه لحل المشكلة
    password = PasswordField('كلمة المرور الجديدة', validators=[Length(min=0, max=128)])
    password2 = PasswordField('تأكيد كلمة المرور الجديدة', validators=[EqualTo('password')])
    profile_picture = FileField('صورة الملف الشخصي')
    submit = SubmitField('تحديث الملف الشخصي')

    def __init__(self, original_username, original_email, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('اسم المستخدم مستخدم بالفعل. الرجاء اختيار اسم آخر.')

    def validate_email(self, email):
        if email.data != self.original_email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('البريد الإلكتروني مستخدم بالفعل. الرجاء استخدام بريد آخر.')
