# -*- coding: utf-8 -*

"""Lunchbox.py: Recipe book program
-----------------------------------
Features in developpement:
    - create, save, load and display recipes, ingredients
    - generate cooking plannings
    - generate shopping lists
"""

# recipe creation is done : next step recipe search + print / edition

from os import system, name as osname
from json import loads, dumps

def clear():
    """function to clear the console according to os after function execution"""
    if osname == 'nt':
        system("cls")
    else:
        system("clear")

class Recipe():
    """ Stores recipe related data and methods """
    def __init__(self):
        self.name = str()
        self.ingredients = list()

    def set_rec(self):
        clear()
        self.name = input("Recipe Name ? > ")

        clear()
        add_ingredients = input("Would you like to add ingredients? [y/n] > ").lower()
        while add_ingredients == 'y':
            n = input("ingredient name? > ")
            q = input("quantity? > ")
            u = input("unit? > ")
            q = int(q)
            ing = dict()
            ing["name"] = n
            ing["quantity"] = q
            ing["unit"] = u
            self.ingredients.append(ing)

            clear()
            add_ingredients = input("Continue adding ingredients? [y/n] > ").lower()

class Menu():
    """App Console UI"""

    def __init__(self):
        self.text = "1. New Recipe\n" \
               + "2. Print Recipe\n" \
               + "3. Edit Recipe\n" \
               + "4. List Recipes\n" \
               + "5. Save Recipes\n" \
               + "0. Exit\n"

        self.recipe_book = list()
        self.running = True

    def display(self):
        clear()
        print(self.text)

    def create_recipe(self):
        clear()
        new = Recipe()
        rec = dict()

        new.set_rec()
        rec["name"] = new.name
        rec["ingredients"] = new.ingredients
        self.recipe_book.append(rec)

    def choice(self):
        c = input("Please choose an option: > ")
        try:
            c = int(c)
        except:
            return c

        if c == 1:
            self.create_recipe()
            return 0

        elif c == 2:
            self.print_recipe()
            return 0

        elif c == 0:
            clear()
            print("Exiting...")
            menu.running = False
            return 0

        else:
            return c

    def load_recipe_book(self):
        clear()
        with open('recipe.json',"r") as f:
            recipe_str = f.read()
            self.recipe_book = loads(recipe_str)

    def save_recipe_book(self):
        with open('recipe.json',"w") as f:
            f.write(dumps(self.recipe_book, indent = 4))

if __name__ == "__main__":
    menu = Menu()
    menu.load_recipe_book()

    while menu.running:
        menu.display()
        user_choice = menu.choice()
        if user_choice != 0:
            print(f"{user_choice} is not a valid choice, please try again.")

    menu.save_recipe_book()

