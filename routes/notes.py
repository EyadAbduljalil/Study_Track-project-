from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import db, Note, Course, Sharing, User
from forms.note import NoteForm, ShareNoteForm

notes = Blueprint('notes', __name__)

@notes.route('/courses/<int:course_id>/notes')
@login_required
def index(course_id):
    """Display all notes for a specific course."""
    course = Course.query.filter_by(id=course_id, user_id=current_user.id).first_or_404()
    notes = course.notes.order_by(Note.updated_at.desc()).all()
    
    return render_template('notes/index.html', 
                          title=f'ملاحظات {course.title}',
                          course=course,
                          notes=notes)

@notes.route('/courses/<int:course_id>/notes/new', methods=['GET', 'POST'])
@login_required
def new(course_id):
    """Create a new note for a specific course."""
    course = Course.query.filter_by(id=course_id, user_id=current_user.id).first_or_404()
    form = NoteForm()
    
    if form.validate_on_submit():
        note = Note(
            course_id=course.id,
            title=form.title.data,
            content=form.content.data
        )
        db.session.add(note)
        db.session.commit()
        flash('تم إضافة الملاحظة بنجاح!', 'success')
        return redirect(url_for('notes.index', course_id=course.id))
    
    return render_template('notes/new.html', 
                          title='إضافة ملاحظة جديدة',
                          form=form,
                          course=course)

@notes.route('/notes/<int:id>')
@login_required
def show(id):
    """Display a specific note."""
    # Check if the note belongs to the user or is shared with them
    note = Note.query.join(Course).filter(
        Note.id == id,
        (Course.user_id == current_user.id) | 
        (Sharing.note_id == id, Sharing.shared_with == current_user.id)
    ).first_or_404()
    
    # Get the owner of the note
    owner = User.query.join(Course).filter(Course.id == note.course_id).first()
    
    # Check if the note is shared and with whom
    shared_with = []
    if owner.id == current_user.id:  # Only the owner can see who it's shared with
        shares = Sharing.query.filter_by(note_id=note.id).all()
        for share in shares:
            user = User.query.get(share.shared_with)
            if user:
                shared_with.append(user)
    
    return render_template('notes/show.html', 
                          title=note.title,
                          note=note,
                          owner=owner,
                          shared_with=shared_with)

@notes.route('/notes/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    """Edit a note."""
    note = Note.query.join(Course).filter(
        Note.id == id,
        Course.user_id == current_user.id  # Only the owner can edit
    ).first_or_404()
    
    form = NoteForm(obj=note)
    
    if form.validate_on_submit():
        note.title = form.title.data
        note.content = form.content.data
        
        db.session.commit()
        flash('تم تحديث الملاحظة بنجاح!', 'success')
        return redirect(url_for('notes.show', id=note.id))
    
    return render_template('notes/edit.html', 
                          title='تعديل الملاحظة',
                          form=form,
                          note=note)

@notes.route('/notes/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    """Delete a note."""
    note = Note.query.join(Course).filter(
        Note.id == id,
        Course.user_id == current_user.id  # Only the owner can delete
    ).first_or_404()
    
    course_id = note.course_id
    
    db.session.delete(note)
    db.session.commit()
    
    flash('تم حذف الملاحظة بنجاح!', 'success')
    return redirect(url_for('notes.index', course_id=course_id))

@notes.route('/notes/<int:id>/share', methods=['GET', 'POST'])
@login_required
def share(id):
    """Share a note with another user."""
    note = Note.query.join(Course).filter(
        Note.id == id,
        Course.user_id == current_user.id  # Only the owner can share
    ).first_or_404()
    
    form = ShareNoteForm()
    
    if form.validate_on_submit():
        # Find the user to share with
        user = User.query.filter_by(email=form.email.data).first()
        
        if not user:
            flash('لم يتم العثور على مستخدم بهذا البريد الإلكتروني.', 'danger')
            return redirect(url_for('notes.share', id=note.id))
        
        if user.id == current_user.id:
            flash('لا يمكنك مشاركة الملاحظة مع نفسك.', 'danger')
            return redirect(url_for('notes.share', id=note.id))
        
        # Check if already shared
        existing_share = Sharing.query.filter_by(
            note_id=note.id,
            shared_with=user.id
        ).first()
        
        if existing_share:
            flash('تم مشاركة الملاحظة مع هذا المستخدم بالفعل.', 'warning')
            return redirect(url_for('notes.share', id=note.id))
        
        # Create new sharing
        sharing = Sharing(
            note_id=note.id,
            shared_with=user.id
        )
        db.session.add(sharing)
        db.session.commit()
        
        flash(f'تم مشاركة الملاحظة مع {user.username} بنجاح!', 'success')
        return redirect(url_for('notes.show', id=note.id))
    
    # Get current shares
    shares = Sharing.query.filter_by(note_id=note.id).all()
    shared_users = []
    for share in shares:
        user = User.query.get(share.shared_with)
        if user:
            shared_users.append(user)
    
    return render_template('notes/share.html', 
                          title='مشاركة الملاحظة',
                          form=form,
                          note=note,
                          shared_users=shared_users)
