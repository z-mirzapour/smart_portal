from werkzeug.security import generate_password_hash
from app.models.user import User
import uuid

class AuthService:
    @staticmethod
    def register_user(username, email, password, role='student'):
        if User.get_by_username(username):
            return None  # if user already exists
        
        new_user = User(
            id=str(uuid.uuid4()),  
            username=username,
            email=email,
            password_hash=generate_password_hash(password),
            role=role
        )
        new_user.save()
        return new_user

    @staticmethod
    def login_user(username, password):
        user = User.get_by_username(username)
        if user and user.verify_password(password):
            return user
        return None