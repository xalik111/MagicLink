@manager.user_loader
def load_user(user_id):
    try:
        return Users.get(user_id)
    except Exception as identifier:
        print(identifier)