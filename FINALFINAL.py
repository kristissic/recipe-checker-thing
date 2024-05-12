import sys
import os
import tkinter as tk  # Tkinter GUI
from tkinter import messagebox
import json

# Constant variables
INGREDIENTS_LIST_FILE_PATH = 'ingredients.txt'
RECIPES_LIST_FILE_PATH = 'recipes.json'

#  paslaugų funkcijos, kurios atlieka konkrečias užduotis, susijusias su programos logika.

def add_ingredients_to_file(ingredients_list):
    with open(INGREDIENTS_LIST_FILE_PATH, 'a') as file:
        for ingredient in ingredients_list:
            file.write(f"{ingredient}\n")

def load_ingredients_from_file():
    if os.path.exists(INGREDIENTS_LIST_FILE_PATH):
        with open(INGREDIENTS_LIST_FILE_PATH, 'r') as file:
            ingredients_list = file.read().splitlines()
            return ingredients_list
    else:
        return []

def load_recipes_from_file(file_path):
    with open(file_path, 'r') as file:
        recipes = json.load(file)
    return recipes

def find_recipes(ingredients_list, recipes):
    found_food = []
    for recipe in recipes:
        if all(ingredient.lower() in map(str.lower, ingredients_list) for ingredient in recipe['ingredients']):
            found_food.append(recipe['name'])
    return found_food

def clear_ingredients_file():
    try:
        os.remove(INGREDIENTS_LIST_FILE_PATH)
    except FileNotFoundError:
        pass

# This is the main class of the application. It inherits from the tk.Frame class./Tai yra pagrindinė programos klasė. Jis paveldimas iš tk.Frame klasės.
class Application(tk.Frame):
    # The __init__ method - constructor. Jis iškviečiamas, kai iš klasės sukuriamas objektas.
    def __init__(self, master=None):
        super().__init__(master)  # Call the constructor of the parent class (tk.Frame).
        self.master = master
        self.pack()
        self.create_widgets()  # Call the method to create the widgets.

    # This method creates the widgets (GUI elementus).
    def create_widgets(self):
        # Create an Entry widget for the user to enter ingredients.
        self.ingredients_entry = tk.Entry(self)
        self.ingredients_entry.pack(side="top")

        #Button widget to add ingredients. Komandos parametras nurodo būdą, kaip iškviesti paspaudus mygtuką.
        self.add = tk.Button(self)
        self.add["text"] = "Add Ingredients"
        self.add["command"] = self.add_ingredients
        self.add.pack(side="top")

        # Button widget to find recipes.
        self.find = tk.Button(self)
        self.find["text"] = "Find Recipes"
        self.find["command"] = self.find_recipes
        self.find.pack(side="top")

        # valdiklis kuris rodo visus ingredientus
        self.ingredients_listbox = tk.Listbox(self)
        self.ingredients_listbox.pack(side="top")

        # uždaro programa
        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")

    # This method is called when the "Add Ingredients" button is clicked.
    def add_ingredients(self):
        ingredients = self.ingredients_entry.get().split(',')
        add_ingredients_to_file(ingredients)
        self.ingredients_listbox.delete(0, tk.END)  # Clear the listbox
        for ingredient in load_ingredients_from_file():  # Load the updated ingredients list
            self.ingredients_listbox.insert(tk.END, ingredient)  # Add each ingredient to the listbox
        messagebox.showinfo("Info", "Ingredients added!")

    # method is called when the "find recipe" button is pressed.
    def find_recipes(self):
        ingredients_list = load_ingredients_from_file()
        recipes = load_recipes_from_file(RECIPES_LIST_FILE_PATH)
        found_recipes = find_recipes(ingredients_list, recipes)
        if found_recipes:
            messagebox.showinfo("Info", f"Found recipes: {', '.join(found_recipes)}")
        else:
            messagebox.showinfo("Info", "No recipes found.")

# Tai yra pagrindinė programos funkcija. Jis sukuria programos klasės egzempliorių ir paleidžia „Tkinter“ įvykio loop'ą.
def main():
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()

if __name__ == '__main__':
    main()
