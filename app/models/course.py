from app.models.registration import Registration
from app.services.json_handler import JSONHandler
import uuid

class Course:
    def __init__ (self, id, code, title, schedule, capacity, description="", prerequisites=None, price=99.99, video_id=None):
        self.id = id
        self.code = code
        self.title = title
        self.description = description
        self.schedule = schedule
        self.capacity = capacity
        self.prerequisites = prerequisites or []
        self.price = float(price)  
        self.video_id = video_id

    @staticmethod
    def get_all():
        courses = JSONHandler.load_data('courses.json')
        return [Course(**course) for course in courses]

    @staticmethod
    def get_by_id(course_id):
        courses = JSONHandler.load_data('courses.json')
        course_data = next((c for c in courses if c['id'] == course_id), None)
        if course_data:
            return Course(**course_data)
        return None

    def save(self):
        courses = JSONHandler.load_data('courses.json')
    
        existing_index = next((i for i, c in enumerate(courses) if c['id'] == self.id), None)
    
        if existing_index is not None:
            courses[existing_index] = {
                'id': self.id,
                'code': self.code,
                'title': self.title,
                'description': self.description,
                'schedule': self.schedule,
                'capacity': self.capacity,
                'prerequisites': self.prerequisites,
                'price': self.price,
                'video_id': self.video_id
            }
        else:
            courses.append({
                'id': self.id,
                'code': self.code,
                'title': self.title,
                'description': self.description,
                'schedule': self.schedule,
                'capacity': self.capacity,
                'prerequisites': self.prerequisites,
                'price': self.price,
                'video_id': self.video_id
            })
    
        JSONHandler.save_data('courses.json', courses)

    @staticmethod
    def save_course(course_data):
        courses = JSONHandler.load_data('courses.json')
    
        existing = next((c for c in courses if c['id'] == course_data['id']), None)
        if existing:
            existing.update(course_data)
        else:
            courses.append(course_data)
    
        JSONHandler.save_data('courses.json', courses)

    @staticmethod
    def delete(course_id):
        try:
            courses = JSONHandler.load_data('courses.json')
            initial_count = len(courses)
        
            updated_courses = [c for c in courses if c['id'] != course_id]
        
            if len(updated_courses) < initial_count:
                JSONHandler.save_data('courses.json', updated_courses)
                Registration.remove_course_registrations(course_id)
                return True, "Course deleted successfully"
            return False, "Course not found"
        except Exception as e:
            return False, f"Error deleting course: {str(e)}"

    @classmethod
    def create(cls, **kwargs):
        """Handle both required and optional fields"""
        kwargs.setdefault('description', "")
        kwargs.setdefault('prerequisites', [])
        kwargs.setdefault('price', 99.99)  
        kwargs['id'] = str(uuid.uuid4())
        return cls(**kwargs).save()
    
    @staticmethod
    def update(course_id, **kwargs):
        courses = JSONHandler.load_data('courses.json')
        for course in courses:
            if course['id'] == course_id:
                kwargs['id'] = course_id  
                course.update(kwargs)
                JSONHandler.save_data('courses.json', courses)
                return True
        return False
    
    @staticmethod
    def create_course(code, title, description, schedule, capacity, prerequisites=None, price=99.99):
        new_course = Course(
            id=str(uuid.uuid4()),
            code=code,
            title=title,
            description=description,
            schedule=schedule,
            capacity=capacity,
            prerequisites=prerequisites or [],
            price = float(price)
        )
        new_course.save()
        return new_course
