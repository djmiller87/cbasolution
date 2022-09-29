from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.controllers import users, services
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
class User:
    db_name = 'cba_solution'
    def __init__(self, data):
        self.id = data['id']
        self.business_name = data['business_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (business_name, email, password, created_at, updated_at) VALUES (%(business_name)s, %(email)s, %(password)s, NOW(), NOW());"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def one_user_info(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if len(results) < 1:
            return False
        user_info = cls(results[0])
        return user_info

    @classmethod
    def get_all_users(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.db_name).query_db(query)
        users = []
        for user in results:
            users.append(cls(user))
        return users


    @staticmethod
    def validate_user(user):
        is_valid = True
        bname = str(user['business_name'])
        user_in_db = User.get_by_email({'email': user['email']})
        if len(user['business_name']) < 2:
            flash("*Business name must contain at least 2 characters!", 'register')
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("*Invalid email address!", 'register')
            is_valid = False
        if user_in_db:
            flash("*Email already taken!", 'register')
            is_valid = False
        if len(user['password']) < 8:
            flash("*Password must contain at least 8 characters!", 'register')
            is_valid = False
        if user['password'] != user['confirm_password']:
            flash("*Passwords do not match!", 'register')
            is_valid = False
        if re.search('[0-9]', user['password']) is None:
            flash("*Passwords must contain a number!", 'register')
            is_valid = False
        if re.search('[A-Z]', user['password']) is None:
            flash("*Passwords must contain a capital letter!", 'register')
            is_valid = False
        if re.search('[$#@]', user['password']) is None:
            flash("*Passwords must contain a symbol!", 'register')
            is_valid = False
        return is_valid
        