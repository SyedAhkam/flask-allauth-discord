def save_token(token, session):
    session['token'] = token

def get_token(session):
    return session.get('token', None)

def delete_token(session):
    session.pop('token')
