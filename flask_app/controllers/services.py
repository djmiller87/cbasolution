#Imports---------------------------------------------------------------------------------------------------------------
from flask_app import app
from flask import redirect, render_template, session, request, flash
from flask_app.models import service, user

#Services --Route that take user to page with all the business' services offered.--------------------------------------
@app.route('/services')
def all_services():
    #Access Control.
    if not 'user_id' in session:
        return redirect('/')
    data = {
        'id' : session['user_id']

    }
    #Grabbing all business services and user from account in database.
    all_services = service.Service.all_user_services(data)
    one_user = user.User.one_user_info(data)
    return render_template('services.html', one_user = one_user, all_services = all_services)

#New Service -->Route that takes user to a page with a form to create a new service their business offers.-------------
@app.route('/new_service')
def new_service():
    #Access Control.
    if not 'user_id' in session:
        return redirect('/')
    #Grabbing user object from database so as to attch form object to user.
    data = {
        'id' : session['user_id']
    }
    one_user = user.User.one_user_info(data)
    return render_template('/new_service.html', one_user = one_user)

#Create Service --> Route that takes the form inputs from New Service and save them to the database.-------------------
@app.route('/create_service', methods=['POST'])
def create_service():
    #Access Control
    if 'user_id' not in session:
        return redirect('/')
    #Validating form inputs.
    if not service.Service.validate_service(request.form):
        return redirect('/new_service')
    #Saving data from form as a Service object.
    data = {
        'service_name': request.form['service_name'],
        'hours': request.form['hours'],
        'price': request.form['price'],
        'business_cost': request.form['business_cost'],
        'description': request.form['description'],
        'user_id': request.form['user_id']
    }
    service.Service.save(data)
    return redirect(f"/dashboard/{session['user_id']}")

#Edit Service -->Route that takes user to a page with auto filled form to edit a current Service.----------------------
@app.route('/edit_service/<int:id>')
def edit_service(id):
    #Access Control.
    if 'user_id' not in session:
        return redirect('/')
    #Grabbing service object info to autofill form.
    data = {
        'id' : session['user_id']
    }
    a_service = {
        'id' : id
    }
    one_user = user.User.one_user_info(data)
    one_service = service.Service.get_one_service(a_service)
    return render_template('edit_service.html', one_service = one_service, one_user = one_user)

#Update Service -->Route that takes edited inputs from form and updates the database with them. -----------------------
@app.route('/update_service/<int:id>', methods=['POST'])
def update_service(id):
    #Access Control.
    if 'user_id' not in session:
        return redirect('/')
    #Validating updates.
    if not service.Service.validate_service(request.form):
        return redirect(f"/edit_service/{id}")
    #Saving updates to the object in the database.
    data = {
        'id': id,
        'service_name': request.form['service_name'],
        'hours': request.form['hours'],
        'price': request.form['price'],
        'business_cost': request.form['business_cost'],
        'description': request.form['description']
    }
    service.Service.update_service(data)
    return redirect(f"/dashboard/{session['user_id']}")

#Show Service -->Route that shows a page with all of one service's data.-----------------------------------------------
@app.route('/show_service/<int:id>')
def show_service(id):
    #Access Control
    if 'user_id' not in session:
        return redirect('/')
    #Grabbing Service object from database.
    data = {
        'id' : session['user_id']
    }
    a_service = {
        'id' : id
    }
    one_user = user.User.one_user_info(data)
    one_service = service.Service.get_one_service(a_service)
    return render_template('show_service.html', one_service = one_service, one_user = one_user )

#Delete -->Route that deletes the service from the database and redirects to dashboard page.---------------------------
@app.route('/delete/<int:id>')
def delete(id):
    #Access Control.
    if 'user_id' not in session:
        return redirect('/')
    #Grabbing Service object from database and deleting it.
    data = {
        'id' : id
    }
    service.Service.delete_service(data)
    return redirect(f"/dashboard/{session['user_id']}")
