import csv
import db_base as db
class Recipe:
    def __init__(self, row):
        self.id = row[0]
        self.recipe_name = row[1]
        self.servings = row[2]
        self.cuisine = row[3]
        self.course = row[4]

class RecipeDb(db.DBbase):
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
                print("Saved item: ", item.recipe_name)

            except Exception as e:
                print(e)
csv_lab = RecipeDb("RecipeManager.sqlite")
csv_lab.reset_or_create_db()
csv_lab.read_recipe_data("Recipe.csv")
csv_lab.save_to_database()
