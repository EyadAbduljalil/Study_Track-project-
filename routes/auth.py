from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.urls import url_parse
from models import db, User
from forms.auth import LoginForm, RegistrationForm, ProfileForm
from werkzeug.utils import secure_filename
import os

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    """User registration page."""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        db.session.add(user)
        db.session.commit()
        flash('تم تسجيل حسابك بنجاح! يمكنك الآن تسجيل الدخول.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', title='تسجيل حساب جديد', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """User login page."""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('البريد الإلكتروني أو كلمة المرور غير صحيحة.', 'danger')
            return redirect(url_for('auth.login'))
        
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.dashboard')
        
        flash(f'مرحباً بك، {user.username}!', 'success')
        return redirect(next_page)
    
    return render_template('auth/login.html', title='تسجيل الدخول', form=form)

@auth.route('/logout')
@login_required
def logout():
    """User logout."""
    logout_user()
    flash('تم تسجيل خروجك بنجاح.', 'info')
    return redirect(url_for('main.index'))

@auth.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """User profile page."""
    form = ProfileForm(original_username=current_user.username, original_email=current_user.email)

    
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        
        if form.password.data:
            current_user.set_password(form.password.data)
        
        if form.profile_picture.data:
            filename = secure_filename(form.profile_picture.data.filename)
            file_ext = os.path.splitext(filename)[1]
            new_filename = f"user_{current_user.id}{file_ext}"
            form.profile_picture.data.save(os.path.join(
                current_app.config['UPLOAD_FOLDER'], new_filename
            ))
            current_user.profile_picture = new_filename
        
        db.session.commit()
        flash('تم تحديث ملفك الشخصي بنجاح.', 'success')
        return redirect(url_for('auth.profile'))
    
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    
    return render_template('auth/profile.html', title='الملف الشخصي', form=form)

@auth.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(obj=current_user)

    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('تم تحديث الملف الشخصي بنجاح!', 'success')
        return redirect(url_for('auth.profile'))

    return render_template('auth/profile_edit.html', title='تعديل الملف الشخصي', form=form)
