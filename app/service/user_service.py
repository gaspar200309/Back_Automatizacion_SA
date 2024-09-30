from app.models.user import User, Role, Teacher, UserRole, db
import os
from werkzeug.utils import secure_filename

class UserService:
    UPLOAD_FOLDER = 'path/to/uploads'  # Especifica tu ruta aquí
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

    @staticmethod
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in UserService.ALLOWED_EXTENSIONS

    @staticmethod
    def save_photo(file):
        if file and UserService.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(UserService.UPLOAD_FOLDER, filename)
            file.save(file_path)
            return filename  
        return None
    
    
    @staticmethod
    def get_all_users():
        return User.query.all()
    

    @staticmethod
    def get_user_by_id(user_id):
        return User.query.get(user_id)

    @staticmethod
    def create_user(username, name, last_name, email, password, role_ids, photo_file=None):
        new_user = User(username=username, name=name, last_name=last_name, email=email)
        new_user.set_password(password)

        if photo_file:
            photo_filename = UserService.save_photo(photo_file)
            if photo_filename:
                new_user.photo = photo_filename

        db.session.add(new_user)
        db.session.commit()

        for role_id in role_ids:
            user_role = UserRole(user_id=new_user.id, role_id=role_id)
            db.session.add(user_role)
        db.session.commit()
        return new_user


    @staticmethod
    def update_user(user_id, username, name, last_name, email, role_ids):
        user = User.query.get(user_id)
        if user:
            user.username = username
            user.name = name
            user.last_name = last_name
            user.email = email
            UserRole.query.filter_by(user_id=user_id).delete()
            for role_id in role_ids:            
                if isinstance(role_id, str) and role_id.isdigit():
                    role_id = int(role_id)
                user_role = UserRole(user_id=user_id, role_id=role_id)
                db.session.add(user_role)
            db.session.commit()
            return user
        return None


    @staticmethod
    def delete_user(user_id):
        user = User.query.get(user_id)
        if user:
            UserRole.query.filter_by(user_id=user_id).delete()
            # Aquí eliminamos la foto del sistema de archivos si existe
            if user.photo:
                os.remove(os.path.join(UserService.UPLOAD_FOLDER, user.photo))
            db.session.delete(user)
            db.session.commit()
            return True
        return False

    @staticmethod
    def get_user_count():
        return User.query.count()

    @staticmethod
    def get_all_roles():
        return Role.query.all()
