from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import db, Course, Task , Note
from forms.course import CourseForm
from models import Task
from models import Note



courses = Blueprint('courses', __name__)

@courses.route('/courses')
@login_required
def index():
    """Display all courses for the current user."""
    user_courses = Course.query.filter_by(user_id=current_user.id).all()
    return render_template('courses/index.html', title='المقررات', courses=user_courses)

@courses.route('/courses/new', methods=['GET', 'POST'])
@login_required
def new():
    """Create a new course."""
    form = CourseForm()
    if form.validate_on_submit():
        course = Course(
            user_id=current_user.id,
            title=form.title.data,
            code=form.code.data,
            instructor=form.instructor.data,
            color=form.color.data
        )
        db.session.add(course)
        db.session.commit()
        flash('تم إضافة المقرر بنجاح!', 'success')
        return redirect(url_for('courses.index'))
    
    return render_template('courses/new.html', title='إضافة مقرر جديد', form=form)

@courses.route('/courses/<int:id>')
@login_required
def show(id):
    """Display a specific course and its tasks and notes."""
    course = Course.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    
    # Get tasks for this course
    tasks = course.tasks.order_by(Task.due_date).all()
    
    # Get notes for this course
    notes = course.notes.order_by(Note.updated_at.desc()).all()
    
    return render_template('courses/show.html', 
                          title=course.title,
                          course=course,
                          tasks=tasks,
                          notes=notes)

@courses.route('/courses/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    """Edit a course."""
    course = Course.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    form = CourseForm(obj=course)
    
    if form.validate_on_submit():
        course.title = form.title.data
        course.code = form.code.data
        course.instructor = form.instructor.data
        course.color = form.color.data
        
        db.session.commit()
        flash('تم تحديث المقرر بنجاح!', 'success')
        return redirect(url_for('courses.show', id=course.id))
    
    return render_template('courses/edit.html', title='تعديل المقرر', form=form, course=course)

@courses.route('/courses/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    """Delete a course."""
    course = Course.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    
    db.session.delete(course)
    db.session.commit()
    
    flash('تم حذف المقرر بنجاح!', 'success')
    return redirect(url_for('courses.index'))
