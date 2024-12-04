from app.models.user import User, Role, UserRole, db
import cloudinary
import cloudinary.uploader
import os

# Configuración de Cloudinary
cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET')
)

def create_user(username, name, last_name, email, password, role_id, phone=None, photo=None):
    try:
        print("Verificando existencia de usuario o correo")
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            return None, "El nombre de usuario o correo ya está en uso."

        # Verificar existencia del rol
        role = Role.query.get(role_id)
        if not role:
            return None, "El rol especificado no existe."

        # Subir la foto si está presente
        photo_url = None
        if photo:
            try:
                upload_result = cloudinary.uploader.upload(photo, folder="user_photos")
                photo_url = upload_result.get('url')
            except Exception as e:
                return None, f"Error al subir la foto: {str(e)}"

        # Crear el usuario
        print("Creando usuario")
        user = User(
            username=username,
            name=name,
            last_name=last_name,
            email=email,
            phone=phone,
            photo=photo_url
        )
        user.set_password(password)
        db.session.add(user)
        db.session.flush()

        user_role = UserRole(user_id=user.id, role_id=role.id)
        db.session.add(user_role)
        db.session.commit()

        return user, "Usuario creado exitosamente."

    except Exception as e:
        import traceback
        print("Error en create_user:", traceback.format_exc())
        db.session.rollback()
        return None, "Error al crear el usuario."



def authenticate_user(identifier, password):
    user = User.query.filter((User.username == identifier) | (User.email == identifier)).first()
    if user and user.check_password(password):
        return user, "Login successful"
    return None, "Invalid credentials"

