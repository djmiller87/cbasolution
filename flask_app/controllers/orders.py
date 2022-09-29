#Imports---------------------------------------------------------------------------------------------------------------
from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_app.models import order, service, user

#New Order -->Route takes user to a page with form to add new order.---------------------------------------------------
@app.route('/new_order')
def new_order():
    #Access Control.
    if 'user_id' not in session:
        return redirect('/')
    #Grabbing all the business' services for dropdown input on form.
    data = {
        'id' : session['user_id']
    }
    one_user = user.User.one_user_info(data)
    all_services = service.Service.all_user_services(data)
    return render_template('new_order.html', all_services = all_services, one_user = one_user)

#Create Order -->Route takes form inputs and creates order object in database.-----------------------------------------
@app.route('/create_order', methods=['POST'])
def create_order():
    #Access Control
    if 'user_id' not in session:
        return redirect('/')
    #Validating inputs from new order form.
    if not order.Order.validate_order(request.form):
        return redirect('/new_order')
    #Saving inputs from new order form to create new Order object in database.
    data = {
        'customer_name' : request.form['customer_name'],
        'date' : request.form['date'],
        'notes' : request.form['notes'],
        'service_id' : request.form['service_id'],
        'business_id' : request.form['business_id']
    }
    order.Order.save(data)
    return redirect(f"/dashboard/{session['user_id']}")

#Show Order -->Route takes user to a page with all of the Order objects info.------------------------------------------
@app.route('/show_order/<int:id>')
def show_order(id):
    #Access Control.
    if 'user_id' not in session:
        return ('/')
    #Grabbing order from database.
    data = {
        'id' : id
    }
    one_order = order.Order.get_one_order(data)
    return render_template('show_order.html', one_order = one_order)

#Edit Order -->Route takes user to page with autofilled form to edit order object.-------------------------------------
@app.route('/edit_order/<int:id>')
def edit_order(id):
    #Access Control.
    if 'user_id' not in session:
        return redirect('/')
    #Grabbing Order object from database to autofill form along with all services for drop down input.
    data = {
        'id' : id
    }
    serve = {
        'id': session['user_id']
    }
    all_services = service.Service.all_user_services(serve)
    one_order = order.Order.get_one_order(data)
    print(one_order)
    return render_template('edit_order.html', one_order = one_order, all_services = all_services)

#Update Order -->Route takes edited form inputs and updates Order object in database.----------------------------------
@app.route('/update_order/<int:id>', methods=['POST'])
def update_order(id):
    #Access Control.
    if 'user_id' not in session:
        return ('/')
    #Saving input edits from form to Order object in database.
    data = {
        'id' : request.form['id'],
        'customer_name' : request.form['customer_name'],
        'service_id' : request.form['service_id'],
        'date' : request.form['date'],
        'notes' : request.form['notes']
    }
    order.Order.update_order(data)
    return redirect(f"/dashboard/{session['user_id']}")

#Delete -->Deletes Order object from database.-------------------------------------------------------------------------
@app.route('/delete_order/<int:id>')
def delete_order(id):
    #Access control.
    if 'user_id' not in session:
        return redirect('/')
    #Deleting Order object from database.
    data = {
        'id' : id
    }
    order.Order.delete_order(data)
    return redirect(f"/dashboard/{session['user_id']}")