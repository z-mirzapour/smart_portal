from werkzeug.security import check_password_hash
from flask_login import UserMixin
from app.services.json_handler import JSONHandler

class User(UserMixin):
    def __init__(self, id, username, email, password_hash, role='student'):
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.role = role

    @staticmethod
    def get_by_id(user_id):
        users = JSONHandler.load_data('users.json')
        user_data = next((u for u in users if u['id'] == user_id), None)
        if user_data:
            return User(**user_data)
        return None


    @staticmethod
    def get_by_username(username):
        users = JSONHandler.load_data('users.json')
        user_data = next((u for u in users if u['username'] == username), None)
        if user_data:
            return User(**user_data)
        return None

    def verify_password(self, password):
        if not self.password_hash or not password:
            return False
        return check_password_hash(self.password_hash, password)
    
    @staticmethod
    def get_all():
        users_data = JSONHandler.load_data(User.FILE)
        return [User(**data) for data in users_data]

    def save(self):
        users = JSONHandler.load_data('users.json')
        users.append({
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'password_hash': self.password_hash,
            'role': self.role
        })
        JSONHandler.save_data('users.json', users)

    @staticmethod
    def get_all_students():
        users = JSONHandler.load_data('users.json')
        return [User(**u) for u in users if u.get('role') == 'student']