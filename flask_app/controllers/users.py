#Imports ---------------------------------------------------------------------------------------------------------------
from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import user, service, order
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

#Index --> Route that takes you to Intro page with Register/Login button.------------------------------------------------
@app.route('/')
def index():
    return render_template('index.html')

#Login and Rgister --> Route that takes you to Login/Register page.------------------------------------------------------
@app.route('/login_register')
def login_register():
    return render_template('login.html')


#Register --> Route that validates form info and registers user in database. Redirected to dashboard.---------------------
@app.route('/register', methods=['POST'])
def register():
    #Validating form inputs.
    if not user.User.validate_user(request.form): 
        return redirect('/login_register')
    #Hashing password for security.
    pw_hash = bcrypt.generate_password_hash(request.form['password']) 
    print(pw_hash)
    #Taking form data and saving user to database.
    data ={ 
        'business_name': request.form['business_name'],
        'email': request.form['email'],
        'password': pw_hash
    }
    user_id = user.User.save(data)
    #Placing user in session for access control.
    session['user_id'] = user_id 
    return redirect(f"/dashboard/{user_id}")

#Login --> Route that validates user has an account and redirects them to their dashboard.--------------------------------
@app.route('/login', methods=['POST'])
def login():
    #Pulling form email input and searching for it in database to grab user.
    data = {'email': request.form['email']}
    user_in_db = user.User.get_by_email(data)
    print(data)
    #Validating user account.
    if not user_in_db:
        flash("*Invalid Email/Password", 'login')
        return redirect('/login_register')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("*Invalid Email/Password", 'login')
        return redirect('/login_register')
    #Placing user in session for access control.
    session['user_id'] = user_in_db.id
    print(user_in_db.id)
    return redirect(f"/dashboard/{user_in_db.id}")

#Dashboard -->Route that takes user to personal dashboard with their account information.---------------------------------
@app.route('/dashboard/<int:id>')
def dashboard(id):
    #Access Control.
    if session['user_id'] != id:
        return redirect('/')
    data = {
        'id' : id
    }
    #Pulling information from database used on dashboard.
    one_user = user.User.one_user_info(data)
    gross = order.Order.gross_income(data)
    costs = order.Order.business_costs(data)
    worked_hours = order.Order.business_hours(data)
    all_orders = order.Order.get_all_orders(data)
    total_orders = len(all_orders)
    #Rendering dashboard template and sending dabase information with it.
    return render_template('dashboard.html', all_orders = all_orders, gross = gross, costs = costs,
    worked_hours = worked_hours, one_user = one_user ,total_orders = total_orders)

#Logout --> Route that exits application and removes access to account.--------------------------------------------------
@app.route('/logout')
def logout():
    #Clearing Session so protected pages cannot be accessed.
    session.clear()
    return redirect('/')