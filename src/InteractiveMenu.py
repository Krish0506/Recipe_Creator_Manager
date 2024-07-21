from recipe import RecipeDb, Recipe
from ingredients import IngredientsDb
from user import User, UserDb

class InteractiveMenu:
    def __init__(self):
        self.recipe_db = RecipeDb("RecipeManager.sqlite")
        self.ingredients_db = IngredientsDb("RecipeManager.sqlite")
        self.user_db = UserDb("RecipeManager.sqlite")
        # self.recipe_db.reset_or_create_db()
        # self.ingredients_db.reset_or_create_db()
    
    def display_menu(self):
        print("\nRecipe Creator Menu:")
        print("1. Add New Recipe")
        print("2. View All Recipes")
        print("3. Add Ingredients to Recipe")
        print("4. View Ingredients for a Recipe")
        print("5. View Recipe by Ingredients")
        # 7 update
        # 8 delete
        print("6. Exit")
        choice = input("Enter your choice: ")
        return choice

    def display_admin_menu(self):
        print("\nAdmin Menu:")
        print("1. Reset User DB")
        print("2. Reset Ingredient DB")
        print("3. Reset Recipe DB")
        print("4. Exit")
        choice = input("Enter your choice: ")
        return choice
    
    def add_new_recipe(self):
        recipe_name = input("Enter the recipe name: ")
        servings = int(input("Enter the number of servings: "))
        cuisine = input("Enter the cuisine: ")
        course = input("Enter the course (e.g., Appetizer, Main Course, Dessert): ")
        last_id = None
        try:
            self.recipe_db.recipe_list.append(Recipe([9999, recipe_name, servings, cuisine, course]))
            last_id = self.recipe_db.save_to_database()
            self.add_ingredients_to_recipe(last_id)
            print("Recipe added successfully!")
        except Exception as e:
            print(f"Error adding recipe: {e}")

    def view_all_recipes(self):
        try:
            self.recipe_db.get_cursor.execute("SELECT * FROM Recipe")
            recipes = self.recipe_db.get_cursor.fetchall()
            for recipe in recipes:
                print(f"ID: {recipe[0]}, Name: {recipe[1]}, Servings: {recipe[2]}, Cuisine: {recipe[3]}, Course: {recipe[4]}")
        except Exception as e:
            print(f"Error fetching recipes: {e}")

    def recipes_by_ingredients(self):
        try:
            ingredient_list = self.ingredients_db.get_all_ingredients()
            for item in ingredient_list:
                print(item)
            ingredient = input("Select an ingredient from the list: ")
            recipe_ids = self.ingredients_db.get_recipe_by_ingredient(ingredient)
            recipes = self.recipe_db.get_recipe_by_ids(recipe_ids)
            print(f"Recipes using {ingredient} are: ")
            for recipe in recipes:
                print(f"ID: {recipe[0]}, Name: {recipe[1]}, Servings: {recipe[2]}, Cuisine: {recipe[3]}, Course: {recipe[4]}")
        except Exception as e:
            print(f"Error fetching recipes: {e}")

    def add_ingredients_to_recipe(self, last_id = None):

        recipe_id = int(input("Enter the recipe ID to add ingredients to: ")) if not last_id else last_id
        while True:
            ingredient = input("Enter the ingredient or exit: ")
            if ingredient.lower() == "exit":
                break
            qty = input("Enter the quantity: ")

            try:
                self.ingredients_db.get_cursor.execute(
                    """
                    INSERT INTO Ingredients (recipe_id, ingredient, qty)
                    VALUES (?, ?, ?)
                    """, (recipe_id, ingredient, qty)
                )
                self.ingredients_db.get_connection.commit()
                print("Ingredient added successfully!")
            except Exception as e:
                print(f"Error adding ingredient: {e}")

    def view_ingredients_for_recipe(self):
        recipe_id = int(input("Enter the recipe ID to view ingredients: "))
        
        try:
            self.ingredients_db.get_cursor.execute("SELECT * FROM Ingredients WHERE recipe_id = ?", (recipe_id,))
            ingredients = self.ingredients_db.get_cursor.fetchall()
            for ingredient in ingredients:
                print(f"ID: {ingredient[0]}, Ingredient: {ingredient[2]}, Quantity: {ingredient[3]}")
        except Exception as e:
            print(f"Error fetching ingredients: {e}")


    def run(self):
        print("************************ Login Page ************************")
        user_id = input("Enter username: ")
        password = input("Enter password: ")
        privilege = self.user_db.check_privilege(User(user_id, password))

        if privilege == None:
            create_acct = input("User not found, Create new account. Yes/no: ")
            if create_acct.lower() == "yes":
                self.user_db.save_to_database(user_id, password, 'user')
                self.run_user(user_id)
            else:
                print("Login Denied!")
                return
        elif privilege == 'user':
            self.run_user(user_id)
        else:
            self.run_admin()

    def run_user(self, username):
        print(f"************************ Logged in as {username} ************************")
        while True:
            choice = self.display_menu()
            if choice == '1':
                self.add_new_recipe()
            elif choice == '2':
                self.view_all_recipes()
            elif choice == '3':
                self.add_ingredients_to_recipe()
            elif choice == '4':
                self.view_ingredients_for_recipe()
            elif choice == "5":
                self.recipes_by_ingredients()
            elif choice == '6':
                self.recipe_db.close_db()
                self.ingredients_db.close_db()
                print("Exiting the program. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

    def run_admin(self):
        while True:
            choice = self.display_admin_menu()
            if choice == '1':
                self.user_db.reset_and_reload()
            elif choice == '2':
                self.ingredients_db.reset_and_reload()
            elif choice == '3':
                self.recipe_db.reset_and_reload()
            elif choice == '4':
                print("Logging out of admin profile")
                self.run()
            else:
                print("Invalid choice. Please try again.")




if __name__ == "__main__":
    print("************************ Welcome to Recipe Manager! ************************")
    menu = InteractiveMenu()
    menu.run()