from flask import Flask, render_template, redirect, url_for, session, request
from auth import auth0
import os

app = Flask(__name__)
app.secret_key = os.getenv('AUTH0_SECRET')

@app.route('/')
async def index():
    user = session.get('user')
    return render_template('index.html', user=user)

@app.route('/login')
async def login():
    return await auth0.login()

@app.route('/callback')
async def callback():
    await auth0.callback(request=request)
    return redirect(url_for('index'))

@app.route('/profile')
async def profile():
    user = session.get('user')
    if not user:
        return redirect(url_for('login'))
    return render_template('profile.html', user=user)

@app.route('/logout')
async def logout():
    return await auth0.logout(return_to=url_for('index', _external=True))

if __name__ == '__main__':
    app.run(debug=True)