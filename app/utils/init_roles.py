
def init_roles(app):
    with app.app_context():
        from app.models.user import Role
        from .. import db
        roles = ['Administrador', 'Usuario', 'Cordinador'] 
        for role_name in roles:
            role = Role.query.filter_by(name=role_name).first()
            if not role:
                new_role = Role(name=role_name)
                db.session.add(new_role)
        db.session.commit()