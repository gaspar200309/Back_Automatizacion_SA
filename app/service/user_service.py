from app.models.user import User, Role, Teacher, UserRole, db
import os
import cloudinary.uploader

class UserService:
   
    @staticmethod
    def get_all_users():
        return User.query.all()
    

    @staticmethod
    def get_user_by_id(user_id):
        user = User.query.get(user_id)
        if user:
            # Solo obtener el primer rol
            role = user.roles[0].role.name if user.roles else None
            return {
                'id': user.id,
                'name': user.name,
                'last_name': user.last_name,
                'username': user.username,
                'email': user.email,
                'photo': user.photo,
                'phone': user.phone,
                'role': role  
            }
        return None


    @staticmethod
    def update_user(user_id, username, name, last_name, email, role_ids, phone, photo):
        user = User.query.get(user_id)
        if user:
            user.username = username
            user.name = name
            user.last_name = last_name
            user.phone = phone
            user.email = email

            if photo:
                # Si hay una foto existente, eliminarla de Cloudinary
                if user.photo:
                    public_id = user.photo.split('/')[-1].split('.')[0]  # Obtén el public_id de Cloudinary
                    cloudinary.uploader.destroy(public_id)
                
                # Subir la nueva foto a Cloudinary
                upload_result = cloudinary.uploader.upload(photo, folder="user_photos")
                user.photo = upload_result.get('url')

            # Actualizar roles
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

            if user.photo:
                public_id = user.photo.split('/')[-1].split('.')[0] 
                cloudinary.uploader.destroy(public_id)

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
