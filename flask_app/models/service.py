from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.controllers import services, users
from flask import flash

class Service:
    db_name = 'cba_solution'
    def __init__(self, data):
        self.id = data['id'],
        self.service_name = data['service_name']
        self.hours = data['hours']
        self.price = data['price']
        self.business_cost = data['business_cost']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO services (service_name, hours, price, business_cost, description, user_id) VALUES (%(service_name)s, %(hours)s, %(price)s, %(business_cost)s, %(description)s, %(user_id)s);"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results

    @classmethod
    def get_one_service(cls, data):
        query = "SELECT * FROM services WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        print(results)
        if len(results) < 1:
            return False
        service_info = results[0]
        return service_info

    @classmethod
    def all_user_services(cls, data):
        query = "SELECT * FROM services WHERE user_id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        print(results)
        services = []
        if results:
            for service in results:
                services.append(service)
        print(services)
        return services

    @classmethod
    def update_service(cls, data):
        query = "UPDATE services SET service_name = %(service_name)s, hours = %(hours)s, price = %(price)s, business_cost = %(business_cost)s, description = %(description)s, updated_at = NOW() WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results

    @classmethod
    def delete_service(cls, data):
        query = "DELETE FROM services WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results

    @staticmethod
    def validate_service(service):
        is_valid = True
        if len(service['service_name']) < 2:
            flash("*Service name must be more than 2 characters!")
            is_valid = False
        if not int(service['hours']) > 0:
            flash("*Must include time to complete serivice in hours!")
            is_valid = False
        if not int(service['price']) > 0:
            flash("Price must be greater than zero!")
            is_valid = False
        if len(service['description']) < 5:
            flash("*Description must be at least 5 characters!")
        return is_valid