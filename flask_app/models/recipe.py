from flask_app.config.mysqlconnection import MySQLConnection
from flask import flash


class Recipe:

    dB = "recipes_data"

    def __init__(self, recipe_data):
        self.id = recipe_data["id"]
        self.name = recipe_data["name"]
        self.description = recipe_data["description"]
        self.instruction = recipe_data["instruction"]
        self.created_at = recipe_data["created_at"]
        self.updated_at = recipe_data["updated_at"]
        self.user_id = recipe_data["user_id"]
        self.duration = None
        self.liked_by = []

    @classmethod
    def save(cls, data):
        query = """
            INSERT INTO recipes (name, description, instruction, duration, user_id) VALUES (%(name)s, %(description)s, %(instruction)s, %(duration)s,%(user_id)s);
        """
        result = MySQLConnection(cls.dB).query_db(query, data)
        return result

    @classmethod
    def create(cls, data):
        cls.save(data)
        return data

    @classmethod
    def get_by_id(cls, id):
        query = """
            SELECT * FROM recipes WHERE id = %(id)s;
        """
        result = MySQLConnection(cls.dB).query_db(query, {"id": id})
        print(cls(result[0]) if result else None)
        return cls(result[0]) if result else None
    
    @classmethod
    def update_recipe(cls, data):
        query = """
            UPDATE recipes SET name = %(name)s, description = %(description)s, instruction = %(instruction)s, duration = %(duration)s WHERE id = %(id)s;
        """
        result = MySQLConnection(cls.dB).query_db(query, data)
        print(cls(result[0]) if result else None)
        return result
    
    @classmethod
    def delete(cls, id):
        query = """
            DELETE FROM recipes WHERE id = %(id)s;
        """
        result = MySQLConnection(cls.dB).query_db(query, {"id": id})
        return result

    @classmethod
    def get_all(cls):
        query = """
            SELECT * FROM recipes LEFT JOIN users ON recipes.user_id = users.id;
        """
        result = MySQLConnection(cls.dB).query_db(query)
        return result    
    
    @classmethod
    def get_many_id(cls, id):
        from flask_app.models.user import User
        query = """
            SELECT * 
            FROM recipes 
            LEFT JOIN likes ON likes.recipe_id = recipes.id 
            LEFT JOIN users ON users.id = likes.user_id
            WHERE recipes.id = %(id)s;
        """
        results = MySQLConnection(cls.dB).query_db(query, {"id": id})

        print(results)

        if results:
            likes = cls(results[0])

            for result in results:
                if result["user_id"]:
                    likes_data = {
                        "id": result["users.id"],
                        "first_name": result["first_name"],
                        "last_name": result["last_name"],
                        "email": result["email"],
                        "password": result["password"],
                        "created_at": result["created_at"],
                        "updated_at": result["updated_at"]
                    }
                    likes.liked_by.append(User(likes_data))
            print(likes)
            return likes
        return None
    
    @staticmethod
    def validate_recipe(data):
        is_valid = True

        if len(data["name"]) < 3:
            is_valid = False
            flash("Name is too short", "create_recipe")
        if len(data["description"]) < 3:
            is_valid = False
            flash("Description is too short", "create_recipe")
        if len(data["instruction"]) < 3:
            is_valid = False
            flash("Instruction is too short", "create_recipe")   
        if data["duration"] == "yes":
            data["duration"] == 1
        if data["duration"] == "no":
            data["duration"] == 0
        return is_valid, data