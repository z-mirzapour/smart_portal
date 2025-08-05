from app.models.registration import Registration
from app.models.user import User
from app.models.course import Course

class RegistrationService:
    
    @staticmethod
    def get_all_student_enrollment_details():
        """
        Retrieves all registrations and groups them by student,
        including student details (username, id) and their registered courses.
        """
        all_registrations = Registration.get_all()
        students_data_map = {} # group registrations by student_id

        for reg_data in all_registrations:
            student_id = reg_data['student_id']
            course_id = reg_data['course_id']

            # If student not yet in th map, gets their details and initialize their entry
            if student_id not in students_data_map:
                student = User.get_by_id(student_id)
                if student:
                    students_data_map[student_id] = {
                        'student_id': student.id,
                        'username': student.username,
                        'email': student.email,
                        'courses': []
                    }
                else:
                    continue
            
            # Adds course details to the student's list of courses
            course = Course.get_by_id(course_id)
            if course: 
                students_data_map[student_id]['courses'].append({
                    'code': course.code,
                    'title': course.title,
                    'schedule': course.schedule 
                })
        
        return list(students_data_map.values())