from recipe import RecipeDb
from ingredients import IngredientsDb

class InteractiveMenu:
    def __init__(self):
        self.recipe_db = RecipeDb("RecipeManager.sqlite")
        self.ingredients_db = IngredientsDb("RecipeManager.sqlite")
        self.recipe_db.reset_or_create_db()
        self.ingredients_db.reset_or_create_db()
    
    def display_menu(self):
        print("\nRecipe Creator Menu:")
        print("1. Add New Recipe")
        print("2. View All Recipes")
        print("3. Add Ingredients to Recipe")
        print("4. View Ingredients for a Recipe")
        print("5. Exit")
        choice = input("Enter your choice: ")
        return choice
    
    def add_new_recipe(self):
        recipe_name = input("Enter the recipe name: ")
        servings = int(input("Enter the number of servings: "))
        cuisine = input("Enter the cuisine: ")
        course = input("Enter the course (e.g., Appetizer, Main Course, Dessert): ")
        
        try:
            self.recipe_db.get_cursor.execute(
                """
                INSERT INTO Recipe (recipe_name, servings, cuisine, course)
                VALUES (?, ?, ?, ?)
                """, (recipe_name, servings, cuisine, course)
            )
            self.recipe_db.get_connection.commit()
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

    def add_ingredients_to_recipe(self):
        recipe_id = int(input("Enter the recipe ID to add ingredients to: "))
        ingredient = input("Enter the ingredient: ")
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
            elif choice == '5':
                self.recipe_db.close_db()
                self.ingredients_db.close_db()
                print("Exiting the program. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    menu = InteractiveMenu()
    menu.run()