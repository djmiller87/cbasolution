from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.controllers import orders, users, services
from flask import flash

class Order:
    db_name = 'cba_solution'
    def __init__(self, data):
        self.id = data['id'],
        self.customer_name = data['customer_name'],
        self.service_id = data['service_id'],
        self.date = data['date'],
        self.notes = data['notes'],
        self.created_at = data['created_at'],
        self.updated_at = data['updated_at'],
        self.business_id = data['business_id']
    
    @classmethod
    def save(cls, data):
        print("data model")
        print(data)
        query = "INSERT INTO orders (customer_name, service_id, date, notes, business_id) VALUES (%(customer_name)s, %(service_id)s, %(date)s, %(notes)s, %(business_id)s);"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results
    
    @classmethod
    def get_one_order(cls,data):
        query = "SELECT * FROM orders LEFT JOIN services ON service_id = services.id WHERE orders.id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if len(results) < 1:
            return False
        one_order = results[0]
        return one_order

    @classmethod
    def get_all_orders(cls, data):
        print(data)
        query = "SELECT * FROM orders LEFT JOIN services ON service_id = services.id LEFT JOIN users ON users.id = business_id WHERE business_id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        all_orders = []
        if results:
            for order in results:
                all_orders.append(order)
        return all_orders

    @classmethod
    def update_order(cls, data):
        query = "UPDATE orders SET customer_name = %(customer_name)s, service_id = %(service_id)s, date = %(date)s, notes = %(notes)s, updated_at = NOW() WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results

    @classmethod
    def delete_order(cls, data):
        query = "DELETE FROM orders WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results

    @classmethod
    def gross_income(cls, data):
        query = "SELECT price FROM orders LEFT JOIN services ON service_id = services.id LEFT JOIN users ON users.id = business_id WHERE business_id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        gross = 0
        if results:
            for price in results:
                gross = gross + price['price']
                print(gross)
        return gross

    @classmethod
    def business_costs(cls, data):
        query = "SELECT business_cost FROM orders LEFT JOIN services ON service_id = services.id LEFT JOIN users ON users.id = business_id WHERE business_id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        costs = 0
        if results:
            for cost in results:
                costs = costs + cost['business_cost']
                print(costs)
        return costs

    @classmethod
    def business_hours(cls, data):
        query = "SELECT hours FROM orders LEFT JOIN services ON service_id = services.id LEFT JOIN users ON users.id = business_id WHERE business_id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        hours = 0
        if results:
            for time in results:
                hours = hours + time['hours']
                print(hours)
        return hours

    @staticmethod
    def validate_order(order):
        is_valid = True
        if len(order['customer_name']) < 2:
            flash("*Customer name must be more than 2 characters!")
            is_valid = False
        if order['service_id'] is None:
            flash("*You must choose a service!")
            is_valid = False
        if order['date'] == "":
            flash("*Invalid date!")
            is_valid = False
        return is_valid