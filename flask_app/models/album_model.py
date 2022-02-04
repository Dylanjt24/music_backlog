from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app import bcrypt
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
DATABASE = 'music_backlog'
class Album:
    def __init__( self , data ):
        self.id = data['id']
        self.artist = data['artist']
        self.album = data['album']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def get_all(cls) -> list:
        query = "SELECT * FROM albums;"
        results = connectToMySQL(DATABASE).query_db(query)
        if results:
            albums = []
            for album in results:
                albums.append( cls(album) )
            return albums
        return []

    @classmethod
    def get_one(cls, data:dict) -> list:
        query = "SELECT * FROM albums WHERE id = %(id)s;"
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
    def get_one_by_artist_album(cls, data:dict) -> list:
        query = "SELECT * FROM albums WHERE artist = %(artist)s AND album = %(album)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        if result:
            return cls(result[0])
        return False

    @classmethod
    def create(cls, data:dict) -> int:
        query = "INSERT INTO albums (artist, album, img_url) VALUES (%(artist)s, %(album)s, %(img_url)s);"
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def add_to_backlog(cls, data) -> int:
        query = "INSERT INTO saved_albums (album_id, user_id) VALUES (%(album_id)s, %(user_id)s);"
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def ignore_album(cls, data) -> int:
        query = "INSERT INTO ignored_albums (album_id, user_id) VALUES (%(album_id)s, %(user_id)s);"
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def remove_from_backlog(cls, data:dict) -> None:
        query = "DELETE FROM saved_albums WHERE id = %(id)s"
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def remove_from_ignored(cls, data:dict) -> None:
        query = "DELETE FROM ignored_albums WHERE id = %(id)s"
        return connectToMySQL(DATABASE).query_db(query, data)


    # @classmethod
    # def update_one(cls, data:dict) -> None:
    #     query = "UPDATE users SET name=%(name)s WHERE id = %(id)s"
    #     return connectToMySQL(DATABASE).query_db(query, data)

    # @classmethod
    # def delete_one(cls, data:dict) -> None:
    #     query = "DELETE FROM users WHERE id = %(id)s"
    #     return connectToMySQL(DATABASE).query_db(query, data)