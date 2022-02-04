from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app import bcrypt
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
DATABASE = 'music_backlog'
class User:
    def __init__( self , data ):
        self.id = data['id']
        self.username = data['username']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.backlog = []


    @classmethod
    def get_all(cls) -> list:
        query = "SELECT * FROM users;"
        results = connectToMySQL(DATABASE).query_db(query)
        if results:
            users = []
            for user in results:
                users.append( cls(user) )
            return users
        return []

    @classmethod
    def get_one(cls, data:dict) -> list:
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            return cls(results[0])
        return []

    # @classmethod
    # def get_dojo_with_ninjas(cls, data:dict):
    #     query = "SELECT * FROM dojos LEFT JOIN ninjas ON ninjas.dojo_id = dojos.id WHERE dojos.id = %(id)s"
    #     results = connectToMySQL(DATABASE).query_db(query, data)
    #     dojo = cls(results[0])
    #     for item in results:
    #         ninja_data = {
    #             'id': item['ninjas.id'],
    #             'first_name': item['first_name'],
    #             'last_name': item['last_name'],
    #             'age': item['age'],
    #             'created_at': item['ninjas.created_at'],
    #             'updated_at': item['ninjas.updated_at']
    #         }
    #         dojo.ninjas.append(ninja_model.Ninja(ninja_data))
    #     return dojo

    @classmethod
    def get_one_by_email(cls, data:dict) -> list:
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        if result:
            return cls(result[0])
        return False

    @classmethod
    def get_one_by_username(cls, data:dict) -> list:
        query = "SELECT * FROM users WHERE username = %(username)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        if result:
            return cls(result[0])
        return False

    @classmethod
    def create(cls, data:dict) -> int:
        query = "INSERT INTO users (username, email, password) VALUES (%(username)s, %(email)s, %(password)s);"
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def get_backlog(cls, data:dict) -> list:
        query = "SELECT * FROM saved_albums JOIN albums ON albums.id = saved_albums.album_id WHERE saved_albums.user_id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def get_one_backlog(cls, data:dict) -> list:
        query = "SELECT * FROM saved_albums WHERE user_id = %(user_id)s AND album_id = %(album_id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def get_ignored(cls, data:dict) -> list:
        query = "SELECT * FROM ignored_albums JOIN albums ON albums.id = ignored_albums.album_id WHERE ignored_albums.user_id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def get_one_ignored(cls, data:dict) -> list:
        query = "SELECT * FROM ignored_albums WHERE user_id = %(user_id)s AND album_id = %(album_id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)


    # @classmethod
    # def update_one(cls, data:dict) -> None:
    #     query = "UPDATE users SET name=%(name)s WHERE id = %(id)s"
    #     return connectToMySQL(DATABASE).query_db(query, data)

    # @classmethod
    # def delete_one(cls, data:dict) -> None:
    #     query = "DELETE FROM users WHERE id = %(id)s"
    #     return connectToMySQL(DATABASE).query_db(query, data)
    
    @staticmethod
    def validate_reg(data:dict) -> bool:
        is_valid = True
        if len(data['username']) < 3:
            flash('Username must be at least 3 characters', 'reg_name_err')
            is_valid = False
        elif User.get_one_by_username(data):
            flash('Username already exists', 'reg_name_err')
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash('Invalid email address', 'reg_email_err')
            is_valid = False
        elif User.get_one_by_email(data):
            flash('Email already exists', 'reg_email_err')
            is_valid = False
        if len(data['password']) < 8:
            flash('Password must be at least 8 characters', 'reg_pw_err')
            is_valid = False
        if data['password'] != data['conf_password']:
            flash('Passwords do not match', 'reg_pw_err')
            is_valid = False
        return is_valid

    @staticmethod
    def validate_login(data:dict) -> bool:
        is_valid = True
        user = User.get_one_by_email(data)
        if user:
            if not bcrypt.check_password_hash(user.password, data['password']):
                flash('Invalid email/password', 'login_err')
                is_valid = False
            else:
                session['uuid'] = user.id
                return is_valid
        flash('Invalid email/password', 'login_err')
        is_valid = False
        return is_valid