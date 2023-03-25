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
        self.creator = None

    def is_liked_by(self, id):
        for user in self.liked_by:
            print(user.id)
            if user.id == id:
                print("true", "is_liked_by")
                return True
            else:
                print("false", "is_liked_by")
                return False
        print("false", "is_liked_by")
        return False
        # found_users = list(filter(lambda user: user.id == id, self.liked_by))
        # return len(found_users) > 0
    
    @classmethod
    def like(cls, data):
        query = """
            INSERT INTO likes (user_id, recipe_id) VALUES (%(user_id)s, %(recipe_id)s);
        """
        result = MySQLConnection(cls.dB).query_db(query, data)
        print("liked", result)
        return result

    @classmethod
    def unlike(cls, data):
        query = """
            DELETE FROM likes WHERE 
            user_id = %(user_id)s AND recipe_id = %(recipe_id)s;
        """
        result = MySQLConnection(cls.dB).query_db(query, data)
        print("unliked", result)
        return result
    
    @classmethod
    def get_one_with_likes(cls, id):
        from flask_app.models.user import User
        query = """
            SELECT * FROM recipes LEFT JOIN likes ON likes.recipe_id = recipes.id LEFT JOIN users ON users.id = likes.user_id WHERE recipes.id = %(id)s; 
        """
        results = MySQLConnection(cls.dB).query_db(query, {"id": id})
        print(results)
        
        if results:
            one_with_likes = cls(results[0])

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
                    one_with_likes.liked_by.append(User(likes_data))
            # print(one_with_likes, "*"*20)
            return one_with_likes 
        else:
            return None

    @classmethod
    def get_many_id(cls, id):
        from flask_app.models.user import User
        query = """
            SELECT * FROM recipes LEFT JOIN likes ON likes.recipe_id = recipes.id LEFT JOIN users ON users.id = likes.user_id WHERE likes.user_id = %(id)s;
        """
        results = MySQLConnection(cls.dB).query_db(query, {"id": id})

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
            return likes
        return None
    
    @classmethod
    def get_many(cls):
        from flask_app.models.user import User
        query = """
            SELECT * 
            FROM recipes 
            LEFT JOIN likes ON likes.recipe_id = recipes.id 
            LEFT JOIN users ON users.id = likes.user_id;
        """
        results = MySQLConnection(cls.dB).query_db(query)
        
        if results:

            for result in results:
                likes = cls(results[0])
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
            return likes
        return None

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
        return cls(result[0]) if result else None
    
    @classmethod
    def update_recipe(cls, data):
        query = """
            UPDATE recipes SET name = %(name)s, description = %(description)s, instruction = %(instruction)s, duration = %(duration)s WHERE id = %(id)s;
        """
        result = MySQLConnection(cls.dB).query_db(query, data)
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
        # print(result)
        # list = []
        # for i in result
            # varaible = get_many_by_id(i.id) | return a list
            # data_dict_user = {"id" : i["user.id"]}
            # variable.creator = User(data_dict_user)
            # list.append(variable)
            # return list
        return result
    
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