from flask import Blueprint, render_template, redirect, url_for, flash, request 
from flask_login import login_required, current_user
from app.models.course import Course
from app.models.registration import Registration
import uuid

student_bp = Blueprint('student', __name__)

@student_bp.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('student.dashboard'))
    return redirect(url_for('auth.login'))

@student_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('student/dashboard.html') 

@student_bp.route('/courses')
@login_required
def view_courses():
    all_courses = Course.get_all()
    registrations = Registration.get_by_student(current_user.id)
    registered_course_ids = [r['course_id'] for r in registrations]
    return render_template('student/courses.html', 
                         courses=all_courses,
                         registered_course_ids=registered_course_ids)
    
@student_bp.route('/register-course/<course_id>')
@login_required
def register_course(course_id):
    success, message = Registration.register(current_user.id, course_id)
    flash(message)
    return redirect(url_for('student.view_courses'))


@student_bp.route('/unregister-course/<course_id>', methods=['POST']) 
@login_required
def unregister_course(course_id):
    success, message = Registration.unregister(current_user.id, course_id)
    flash(message, 'success' if success else 'danger') 
    return redirect(url_for('student.view_schedule')) 

@student_bp.route('/schedule')
@login_required
def view_schedule():
    registrations = Registration.get_by_student(current_user.id)
    courses = []
    for reg in registrations:
        course = Course.get_by_id(reg['course_id'])
        if course:
            courses.append(course)
    return render_template('student/schedule.html', courses=courses)


from flask_login import current_user, login_required

@student_bp.route('/checkout', methods=['POST'])
@login_required  # makes sure only logged-in users can access
def checkout():
    selected_course_ids = request.form.getlist('selected_courses')
    if not selected_course_ids:
        flash('Please select at least one course', 'error')
        return redirect(url_for('student.view_courses'))
    
    # Gets course details
    selected_courses = []
    total_amount = 0
    for course_id in selected_course_ids:
        course = Course.get_by_id(course_id)
        if course:
            selected_courses.append(course)
            total_amount += course.price
    
    return render_template('student/checkout.html',
                         selected_courses=selected_courses,
                         total_amount=total_amount,
                         course_ids=','.join(selected_course_ids))

@student_bp.route('/process_payment', methods=['POST'])
@login_required
def process_payment():
    course_ids = request.form.get('course_ids', '').split(',')
    if not course_ids or not course_ids[0]:
        flash('No courses selected for payment', 'error')
        return redirect(url_for('student.view_courses'))
    
    # Register for new courses
    registered_courses = []
    total_amount = 0
    
    for course_id in course_ids:
        course = Course.get_by_id(course_id)
        if course:
            success, message = Registration.register(current_user.id, course_id)
            if success:
                registered_courses.append(course)
                total_amount += course.price
            else:
                flash(f'Could not register for {course.code}: {message}', 'warning')
    
    if not registered_courses:
        flash('No courses were successfully registered', 'error')
        return redirect(url_for('student.view_courses'))
    
    # Generate mock transaction details
    transaction_id = f"mock_{uuid.uuid4().hex[:8]}"
    
    return render_template('student/payment_success.html',
                         registered_courses=registered_courses,
                         transaction_id=transaction_id,
                         amount_paid=total_amount)

@student_bp.route('/course-details/<course_id>')
@login_required
def course_details(course_id):
    course = Course.get_by_id(course_id)
    if not course:
        flash('Course not found', 'error')
        return redirect(url_for('student.view_courses'))
    
    # is student registered for this course
    is_registered = Registration.is_student_registered(current_user.id, course_id)
    
    return render_template('student/course_details.html', 
                         course=course,
                         is_registered=is_registered)