import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, send_from_directory, redirect, url_for, make_response
from database.user import User

load_dotenv()
DATABASE_URI = os.getenv('DATABASE_URI')
SECRET_KEY = os.getenv('SECRET_KEY')
UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER')
IMAGES_ROOT = os.getenv('IMAGES_ROOT')

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
IMAGES_ROOT = IMAGES_ROOT

def is_authenticated(request):
    username = request.cookies.get('username', '')
    ssid = request.cookies.get('ssid', '')

    list_user = User.filter(username=username)

    if list_user != []: 
        user = list_user[0]
        if ssid == str(user.id):
            return True
        
    return False


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        repassword = request.form.get('repassword', '')

        if  not username or not password:
            return "deo nhap username, password a`"
        
        if password != repassword:
            return "nhap sai repassword roi`"

        list_user = User.filter(username=username)
        if list_user != []:
            return "existed"
        
        user = User.create_user(username, password)
        return f"created successfully, id = {user.id}"
        
    else:
        return render_template('register.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    response = make_response(redirect(url_for('login')))
    response.set_cookie(key='ssid',value="")
    return response


@app.route('/login', methods=['GET', 'POST'])
def login():
    if is_authenticated(request):
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')

        if  not username or not password:
            return "deo nhap username, password a`"
        
        list_user = User.filter(username=username)
        if list_user == []:
            return "khong ton tai"
        
        user = list_user[0]
        if not user.authenticate(password):
            return "sai mat khau"
        
        response = make_response(redirect(url_for('index')))
        response.set_cookie(key='username',value=str(user.username))
        response.set_cookie(key='ssid',value=str(user.id))
        return response
    return render_template('login.html')


@app.route('/', methods=['GET'])
def index():
    return redirect(url_for('books'))


@app.route('/book', methods=['GET', 'POST'])
def books():
    return render_template('books.html')


@app.route('/book/<string:book_id>', methods=['GET', 'POST'])
def book_detail(book_id):
    pass


@app.route('/profile/user/<string:user_id>', methods=['GET', 'POST'])
def profile(user_id):
    pass


@app.route('/profile/admin', methods=['GET', 'POST'])
def profile_control():
    pass

if __name__ == '__main__':
    print('Server started!')
    app.run("localhost", 5000, debug=True)