import csv

from typing import List

import db_base as db
class Recipe:
    def __init__(self, row):
        self.id = row[0]
        self.recipe_name = row[1]
        self.servings = row[2]
        self.cuisine = row[3]
        self.course = row[4]

class RecipeDb(db.DBbase):
    recipe_list = []
    def reset_or_create_db(self):
        try:
            sql = """
                DROP TABLE IF EXISTS Recipe;

                Create TABLE Recipe (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                    recipe_name VARCHAR(100) NOT NULL,
                    servings INTEGER,
                    cuisine VARCHAR(30),
                    course VARCHAR(30)
                );
            """
            super().execute_script(sql)
        except Exception as e:
            print(e)

    def read_recipe_data(self, file_name):
        self.recipe_list = []

        try:
            with open(file_name, 'r') as record:
                csv_contents = csv.reader(record)
                next(record)
                for row in csv_contents:
                    # print(row)
                    recipe = Recipe(row)
                    self.recipe_list.append(recipe)

        except Exception as e:
            print(e)

    def save_to_database(self):
        print("Number of records to save:", len(self.recipe_list))
        last_id = None
        for item in self.recipe_list:
            try:
                super().get_cursor.execute(
                    """
                    INSERT INTO Recipe
                    (recipe_name, servings, cuisine, course)
                        VALUES(?,?,?,?)
                    """,
                    (item.recipe_name, item.servings, item.cuisine, item.course)
                )
                super().get_connection.commit()
                last_id = super().get_cursor.lastrowid
                print("Saved item: ", last_id, item.recipe_name)
            except Exception as e:
                print(e)
        self.recipe_list = []
        return last_id


    def reset_and_reload(self):
        self.reset_or_create_db()
        self.read_recipe_data("Recipe.csv")
        self.save_to_database()

    def get_recipe_by_ids(self, recipe_ids: List[int]):
        try:
            # Prepare the SQL query with placeholders for the recipe IDs
            query = """
                SELECT * FROM Recipe
                WHERE id IN ({seq})
            """.format(seq=','.join('?' for _ in recipe_ids))

            # Execute the SQL query with the list of recipe IDs
            super().get_cursor.execute(query, recipe_ids)
            # Fetch all the rows from the result of the query
            recipes = super().get_cursor.fetchall()
            return recipes  # Return the list of recipes

        except Exception as e:
            print("Error retrieving recipes by IDs:", e)
            return []  # Return an empty list in case of error
