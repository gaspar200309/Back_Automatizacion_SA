from app.models.user import User, Role, UserRole, db
import cloudinary
import cloudinary.uploader
import os
import secrets

cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET')
)

def create_user(username, name, last_name, email, password, role_id, phone=None, photo=None):
    existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
    if existing_user:
        return None, "El nombre de usuario o correo ya está en uso."

    photo_url = None
    if photo:
        upload_result = cloudinary.uploader.upload(photo, folder="user_photos")
        photo_url = upload_result.get('url')

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
    db.session.commit()

    role = Role.query.get(role_id)
    if not role:
        return None, "Role not found."

    user_role = UserRole(user_id=user.id, role_id=role.id)
    db.session.add(user_role)
    db.session.commit()

    return user, "User created successfully."




def authenticate_user(identifier, password):
    user = User.query.filter((User.username == identifier) | (User.email == identifier)).first()
    if user and user.check_password(password):
        return user, "Login successful"
    return None, "Invalid credentials"


"""   
    if user:
        is_password_correct = user.check_password(password)
        if is_password_correct:
            roles = [role.role.name for role in user.roles]
            access_token = create_access_token(identity={'username': user.username, 'roles': roles})
            return {"access_token": access_token, "username": user.username, "roles": roles}, "Authentication successful."
    return None, "Invalid username or password."
 """