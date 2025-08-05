from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.course import Course
from app.models.registration import Registration
from app.models.user import User
from app.services.registration_service import RegistrationService 
from app.models.registration import Registration 

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.before_request
@login_required
def restrict_to_admin():
    if not current_user.is_authenticated or current_user.role != 'admin':
        flash("Admin access required", "danger")
        return redirect(url_for('student.dashboard'))

# Admin Dashboard - Shows students and their courses
@admin_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'admin':
        flash("Access denied: Admin privileges required.", "danger")
        return redirect(url_for('student.dashboard'))

    total_students = len(User.get_all_students()) 
    total_courses = len(Course.get_all())
    registrations = Registration.get_all() 
    
    # Data for Student Enrollments table on dashboard
    students_for_dashboard_table = RegistrationService.get_all_student_enrollment_details()

    return render_template('admin/dashboard.html',
                           total_students=total_students,
                           total_courses=total_courses,
                           registrations=registrations,
                           students=students_for_dashboard_table)


@admin_bp.route('/courses', methods=['GET', 'POST'])
def courses():
    print("Request method:", request.method)  # Debugging
    
    if request.method == 'POST':
        print("Form data:", request.form)  
        try:
            Course.create_course(
                code=request.form['code'],
                title=request.form['title'],
                description=request.form['description'],
                schedule=request.form['schedule'],
                capacity=int(request.form['capacity']),
                price=float(request.form.get('price', 100.00)),
                prerequisites=[p.strip() for p in request.form.get('prerequisites', '').split(',') if p.strip()]
            )
            flash('Course added successfully!', 'success')
            return redirect(url_for('admin.courses'))
        except Exception as e:
            print("Error:", str(e))  
            flash(f'Error: {str(e)}', 'danger')
    
    return render_template('admin/courses.html', courses=Course.get_all())

@admin_bp.route('/courses/edit/<course_id>', methods=['GET', 'POST'])  
@login_required
def edit_course(course_id):
    if current_user.role != 'admin':
        flash("Access denied: Admin privileges required.", "danger")
        return redirect(url_for('student.dashboard'))

    course = Course.get_by_id(course_id)
    if not course:
        flash('Course not found.', 'error')
        return redirect(url_for('admin.courses'))

    if request.method == 'POST':
        # Handles form submission
        course.code = request.form.get('code')
        course.title = request.form.get('title')
        course.description = request.form.get('description')
        course.schedule = request.form.get('schedule')
        course.capacity = int(request.form.get('capacity'))
        course.price = float(request.form.get('price', 100.00))
        prerequisites = request.form.get('prerequisites', '')
        course.prerequisites = [p.strip() for p in prerequisites.split(',') if p.strip()]
        
        course.save()
        flash('Course updated successfully.', 'success')
        return redirect(url_for('admin.courses'))

    # GET request - shows the form
    return render_template('admin/course_form.html', course=course)

@admin_bp.route('/courses/delete/<course_id>', methods=['POST'])
@login_required
def delete_course(course_id):
    if current_user.role != 'admin':
        flash("Access denied: Admin privileges required.", "danger")
        return redirect(url_for('student.dashboard'))

    # verifying that the course exists
    if not Course.get_by_id(course_id):
        flash("Course not found", "error")
        return redirect(url_for('admin.courses'))

    success, message = Course.delete(course_id)
    if success:
        flash(message, "success")
    else:
        flash(message, "error")
    
    return redirect(url_for('admin.courses'))


@admin_bp.route('/add_course', methods=['GET', 'POST'])
@login_required
def add_course():
    if current_user.role != 'admin':
        flash("Access denied", "danger")
        return redirect(url_for('student.dashboard'))

    if request.method == 'POST':
        code = request.form.get('code')
        title = request.form.get('title')
        description = request.form.get('description')
        schedule = request.form.get('schedule')
        capacity = int(request.form.get('capacity'))
        price = float(request.form.get('price', 100.00))
        prerequisites = request.form.get('prerequisites', '').split(',')
        
        Course.create_course(
            code=code,
            title=title,
            description=description,
            schedule=schedule,
            capacity=capacity,
            prerequisites=[p.strip() for p in prerequisites if p.strip()],
            price=price
        )
        flash('Course created successfully', 'success')
        return redirect(url_for('admin.courses'))

    # GET request - shows empty form
    return render_template('admin/course_form.html', course=None)


#'All Student Schedules' page
@admin_bp.route('/manage_schedules') 
@login_required
def manage_schedules(): 
    if current_user.role != 'admin':
        flash("Access denied: Admin privileges required.", "danger")
        return redirect(url_for('student.dashboard'))
    
    students_data = RegistrationService.get_all_student_enrollment_details()
    
    return render_template('admin/schedules.html', students_data=students_data)
