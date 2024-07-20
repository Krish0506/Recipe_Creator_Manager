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

csv_lab = IngredientsDb("RecipeManager.sqlite")
csv_lab.reset_or_create_db()
csv_lab.read_ingredients_data("Ingredients.csv")
csv_lab.save_to_database()
