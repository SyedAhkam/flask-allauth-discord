from flask import Flask, url_for, redirect, session, render_template
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv

import utils
import os

load_dotenv()
CLIENT_ID = os.getenv('DISCORD_CLIENT_ID')
CLIENT_SECRET = os.getenv('DISCORD_CLIENT_SECRET')

app = Flask(__name__)
app.secret_key = 'secret!'
oauth = OAuth(app)

discord = oauth.register(
    name='discord',
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    access_token_url='https://discord.com/api/oauth2/token',
    authorize_url='https://discord.com/api/oauth2/authorize',
    api_base_url='https://discord.com/api',
    client_kwargs={'scope': 'identify email guilds connections'}
)

@app.route('/')
def index():
    token = utils.get_token(session)
    is_logged_in = session.get('is_logged_in')
    if is_logged_in:
        user = discord.get('/api/users/@me', token=token).json()
        guilds = discord.get('/api/users/@me/guilds', token=token).json()
        connections = discord.get('/api/users/@me/connections', token=token).json()
    else:
        user = None
        guilds = None
        connections = None

    ctx = {
        'user': user,
        'is_logged_in': is_logged_in,
        'guilds': guilds,
        'connections': connections
    }
    return render_template('index.html', **ctx)

@app.route('/login')
def login():
    redirect_uri = url_for('authorize', _external=True)
    return discord.authorize_redirect(redirect_uri=redirect_uri)

@app.route('/authorize')
def authorize():
    token = discord.authorize_access_token()
    session['is_logged_in'] = True
    utils.save_token(token, session)
    return redirect('/')

@app.route('/logout')
def logout():
    session['is_logged_in'] = False
    utils.delete_token(session)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
