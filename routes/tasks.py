from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import db, Task, Course
from forms.task import TaskForm
from datetime import datetime

tasks = Blueprint('tasks', __name__)

@tasks.route('/tasks')
@login_required
def index():
    status = request.args.get('status', 'all')
    priority = request.args.get('priority', 'all')
    course_id = request.args.get('course_id', 'all')

    query = Task.query.join(Course).filter(Course.user_id == current_user.id)

    if status != 'all':
        query = query.filter(Task.status == status)

    if priority != 'all':
        query = query.filter(Task.priority == priority)

    if course_id != 'all' and course_id.isdigit():
        query = query.filter(Task.course_id == int(course_id))

    tasks = query.order_by(Task.due_date).all()
    courses = Course.query.filter_by(user_id=current_user.id).all()

    return render_template('tasks/index.html',
                           title='المهام',
                           tasks=tasks,
                           courses=courses,
                           current_filters={
                               'status': status,
                               'priority': priority,
                               'course_id': course_id
                           })


@tasks.route('/courses/<int:course_id>/tasks/new', methods=['GET', 'POST'])
@login_required
def new(course_id):
    course = Course.query.filter_by(id=course_id, user_id=current_user.id).first_or_404()
    form = TaskForm()

    form.course_id.choices = [(c.id, c.title) for c in Course.query.filter_by(user_id=current_user.id).all()]
    form.course_id.data = course.id

    if form.validate_on_submit():
        task = Task(
            title=form.title.data,
            description=form.description.data,
            due_date=form.due_date.data,
            priority=form.priority.data,
            status=form.status.data,
            course_id=form.course_id.data
        )
        db.session.add(task)
        db.session.commit()
        flash('تم إضافة المهمة بنجاح!', 'success')
        return redirect(url_for('tasks.index'))  # ✅ تغيير المسار لتفادي الخطأ

    return render_template('tasks/new.html',
                           title='إضافة مهمة جديدة',
                           form=form,
                           course=course)


@tasks.route('/tasks/<int:id>')
@login_required
def show(id):
    task = Task.query.join(Course).filter(
        Task.id == id,
        Course.user_id == current_user.id
    ).first_or_404()

    return render_template('tasks/show.html', title=task.title, task=task)


@tasks.route('/tasks/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    task = Task.query.join(Course).filter(
        Task.id == id,
        Course.user_id == current_user.id
    ).first_or_404()

    form = TaskForm(obj=task)
    form.course_id.choices = [(c.id, c.title) for c in Course.query.filter_by(user_id=current_user.id).all()]
    form.course_id.data = task.course_id

    if form.validate_on_submit():
        task.title = form.title.data
        task.description = form.description.data
        task.due_date = form.due_date.data
        task.priority = form.priority.data
        task.status = form.status.data
        task.course_id = form.course_id.data

        db.session.commit()
        flash('تم تحديث المهمة بنجاح!', 'success')
        return redirect(url_for('tasks.show', id=task.id))

    return render_template('tasks/edit.html',
                           title='تعديل المهمة',
                           form=form,
                           task=task)


@tasks.route('/tasks/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    task = Task.query.join(Course).filter(
        Task.id == id,
        Course.user_id == current_user.id
    ).first_or_404()

    db.session.delete(task)
    db.session.commit()

    flash('تم حذف المهمة بنجاح!', 'success')
    return redirect(url_for('tasks.index'))  # ✅ تغيير للمسار الآمن


@tasks.route('/tasks/<int:id>/status', methods=['POST'])
@login_required
def update_status(id):
    task = Task.query.join(Course).filter(
        Task.id == id,
        Course.user_id == current_user.id
    ).first_or_404()

    new_status = request.form.get('status')
    if new_status in ['pending', 'in_progress', 'completed']:
        task.status = new_status
        db.session.commit()
        flash('تم تحديث حالة المهمة بنجاح!', 'success')

    return redirect(request.referrer or url_for('tasks.index'))
