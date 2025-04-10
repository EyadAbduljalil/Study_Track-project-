from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import db, Course, Task, Note

main = Blueprint('main', __name__)

@main.route('/')
def index():
    """Landing page for visitors."""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('index.html', title='StudyTrack - منصة إدارة المهام التعليمية')

@main.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard for authenticated users."""
    # Get user's courses
    courses = Course.query.filter_by(user_id=current_user.id).all()
    
    # Get upcoming tasks (due within 7 days)
    from datetime import datetime, timedelta
    upcoming_tasks = Task.query.join(Course).filter(
        Course.user_id == current_user.id,
        Task.status != 'completed',
        Task.due_date <= datetime.utcnow() + timedelta(days=7)
    ).order_by(Task.due_date).limit(5).all()
    
    # Get recent notes
    recent_notes = Note.query.join(Course).filter(
        Course.user_id == current_user.id
    ).order_by(Note.updated_at.desc()).limit(3).all()
    
    # Get task statistics
    total_tasks = Task.query.join(Course).filter(Course.user_id == current_user.id).count()
    completed_tasks = Task.query.join(Course).filter(
        Course.user_id == current_user.id,
        Task.status == 'completed'
    ).count()
    pending_tasks = Task.query.join(Course).filter(
        Course.user_id == current_user.id,
        Task.status == 'pending'
    ).count()
    in_progress_tasks = Task.query.join(Course).filter(
        Course.user_id == current_user.id,
        Task.status == 'in_progress'
    ).count()
    
    # Calculate completion rate
    completion_rate = 0
    if total_tasks > 0:
        completion_rate = (completed_tasks / total_tasks) * 100
    
    return render_template('dashboard.html', 
                          title='لوحة المعلومات',
                          courses=courses,
                          upcoming_tasks=upcoming_tasks,
                          recent_notes=recent_notes,
                          total_tasks=total_tasks,
                          completed_tasks=completed_tasks,
                          pending_tasks=pending_tasks,
                          in_progress_tasks=in_progress_tasks,
                          completion_rate=completion_rate)

@main.route('/statistics')
@login_required
def statistics():
    """Statistics and analytics page."""
    # Get task statistics by course
    courses = Course.query.filter_by(user_id=current_user.id).all()
    course_stats = []
    
    for course in courses:
        total = Task.query.filter_by(course_id=course.id).count()
        completed = Task.query.filter_by(course_id=course.id, status='completed').count()
        rate = 0
        if total > 0:
            rate = (completed / total) * 100
        
        course_stats.append({
            'course': course,
            'total': total,
            'completed': completed,
            'rate': rate
        })
    
    # Get task statistics by priority
    priority_stats = {
        'low': Task.query.join(Course).filter(
            Course.user_id == current_user.id,
            Task.priority == 'low'
        ).count(),
        'medium': Task.query.join(Course).filter(
            Course.user_id == current_user.id,
            Task.priority == 'medium'
        ).count(),
        'high': Task.query.join(Course).filter(
            Course.user_id == current_user.id,
            Task.priority == 'high'
        ).count()
    }
    
    # Get task statistics by status
    status_stats = {
        'pending': Task.query.join(Course).filter(
            Course.user_id == current_user.id,
            Task.status == 'pending'
        ).count(),
        'in_progress': Task.query.join(Course).filter(
            Course.user_id == current_user.id,
            Task.status == 'in_progress'
        ).count(),
        'completed': Task.query.join(Course).filter(
            Course.user_id == current_user.id,
            Task.status == 'completed'
        ).count()
    }
    
    return render_template('statistics.html',
                          title='الإحصائيات',
                          course_stats=course_stats,
                          priority_stats=priority_stats,
                          status_stats=status_stats)
