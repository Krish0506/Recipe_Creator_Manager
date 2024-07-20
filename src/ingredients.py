import csv

import db_base as db

class Ingredients:
    def __init__(self, row):
        self.id = row[0]
        self.recipe_id = row[1]
        self.ingredient = row[2]
        self.qty = row[3]

class IngredientsDb(db.DBbase):
    def reset_or_create_db(self):
        try:
            sql = """
                DROP TABLE IF EXISTS Ingredients;

                Create TABLE Ingredients (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                    recipe_id INTEGER NOT NULL,
                    ingredient VARCHAR(100) NOT NULL,
                    qty INTEGER
                );
            """
            super().execute_script(sql)
        except Exception as e:
            print(e)

    def read_ingredients_data(self, file_name):
        self.ingredients_list = []

        try:
            with open(file_name, 'r') as record:
                csv_contents = csv.reader(record)
                next(record)
                for row in csv_contents:
                    # print(row)
                    ingredient = Ingredients(row)
                    self.ingredients_list.append(ingredient)

        except Exception as e:
            print(e)

    def save_to_database(self):
        print("Number of records to save:", len(self.ingredients_list))

        for item in self.ingredients_list:
            try:
                super().get_cursor.execute(
                    """
                    INSERT INTO Ingredients
                    (recipe_id, ingredient, qty)
                        VALUES(?,?,?)
                    """,
                    (item.recipe_id, item.ingredient, item.qty)
                )
                super().get_connection.commit()
                print("Saved item: ", item.id, item.recipe_id, item.ingredient)

            except Exception as e:
                print(e)

    def get_all_ingredients(self):
        try:
            # Execute the SQL query to select distinct ingredients
            super().get_cursor.execute(
                """
                SELECT DISTINCT ingredient FROM Ingredients ORDER BY ingredient
                """
            )
            # Fetch all the rows from the result of the query
            ingredients = super().get_cursor.fetchall()
            return [ingredient[0] for ingredient in ingredients]  # Return a list of distinct ingredients
        except Exception as e:
            print("Error retrieving ingredients:", e)
            return []  # Return an empty list in case of error

    def get_recipe_by_ingredient(self, ingredient):
        try:
            # Execute the SQL query to select recipe IDs by ingredient
            super().get_cursor.execute(
                """
                SELECT recipe_id FROM Ingredients WHERE ingredient LIKE ?
                """,
                (f"%{ingredient}%",)  # Note the comma to create a single-element tuple
            )
            # Fetch all the rows from the result of the query
            recipe_ids = super().get_cursor.fetchall()
            # Process the recipe IDs
            recipe_ids_list = [row[0] for row in recipe_ids]
            return recipe_ids_list  # Return a list of recipe IDs

        except Exception as e:
            print("Error retrieving recipes by ingredient:", e)
            return []  # Return an empty list in case of error

    def reset_and_reload(self):
        self.reset_or_create_db()
        self.read_ingredients_data("Ingredients.csv")
        self.save_to_database()
