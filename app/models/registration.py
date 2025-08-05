from app.services.json_handler import JSONHandler
import uuid

class Registration:
    @staticmethod
    def get_by_student(student_id):
        registrations = JSONHandler.load_data('registrations.json')
        return [r for r in registrations if r['student_id'] == student_id]

    @staticmethod
    def get_by_course(course_id):
        registrations = JSONHandler.load_data('registrations.json')
        return [r for r in registrations if r['course_id'] == course_id]

    @staticmethod
    def has_schedule_conflict(student_id, new_course_id):
        from app.models.course import Course
        registrations = Registration.get_by_student(student_id)
        registered_courses = []
        
        for reg in registrations:
            course = Course.get_by_id(reg['course_id'])
            if course:
                registered_courses.append(course)
        
        new_course = Course.get_by_id(new_course_id)
        if not new_course:
            return False
    
        for course in registered_courses:
            if course.schedule == new_course.schedule:
                return True
        
        return False

    @staticmethod
    def register(student_id, course_id):
        existing = Registration.get_by_student(student_id)
        if any(r['course_id'] == course_id for r in existing):
            return False, "Already registered for this course"
        
        if Registration.has_schedule_conflict(student_id, course_id):
            return False, "Schedule conflict with existing registration"
        
        registrations = JSONHandler.load_data('registrations.json')
        new_reg = {
            'id': str(uuid.uuid4()),
            'student_id': student_id,
            'course_id': course_id,
            'status': 'registered'
        }
        registrations.append(new_reg)
        JSONHandler.save_data('registrations.json', registrations)
        return True, "Successfully registered"
    
    @staticmethod
    def unregister(student_id, course_id):
        registrations = JSONHandler.load_data('registrations.json')
    
        updated_registrations = [
            r for r in registrations 
            if not (r['student_id'] == student_id and r['course_id'] == course_id)
        ]

        if len(updated_registrations) < len(registrations):  
            JSONHandler.save_data('registrations.json', updated_registrations)
            return True, "Successfully unregistered"
        return False, "Registration not found"

    @staticmethod
    def delete(user_id, course_id):
        registrations = JSONHandler.load_data('registrations.json')
        updated_registrations = [
            r for r in registrations 
            if not (r.get('user_id') == user_id and r.get('course_id') == course_id)
        ]
        if len(updated_registrations) < len(registrations):
            JSONHandler.save_data('registrations.json', updated_registrations)
            return True, "Unregistered successfully."
        return False, "Registration not found."
    
    @staticmethod
    def remove_course_registrations(course_id):
        """Remove all registrations for a deleted course"""
        registrations = JSONHandler.load_data('registrations.json')
        updated_registrations = [r for r in registrations if r['course_id'] != course_id]
        JSONHandler.save_data('registrations.json', updated_registrations)

    @staticmethod
    def get_all():
        """Get all registrations"""
        try:
            return JSONHandler.load_data('registrations.json') or []
        except FileNotFoundError:
            return []
        
    @classmethod
    def is_student_registered(cls, student_id, course_id):
        registrations = cls.get_by_student(student_id)
        return any(r['course_id'] == course_id for r in registrations)
