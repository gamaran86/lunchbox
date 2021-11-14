# -*- coding: utf-8 -*

"""Lunchbox.py: Recipe book program
-----------------------------------
Features in developpement:
    - create, save, load and display recipes, ingredients
    - generate cooking plannings
    - generate shopping lists
"""
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
       self.cost = float()
       self.meals_num = int()
       self.prep_time = int()

class Menu():
    """App Console UI"""

    def __init__(self):
        self.text = "1. Create Recipe\n2. Exit"
        self.recipe_book = list()
        self.running = True

    def display(self):
        clear()
        print(self.text)

    def create_recipe(self):
        clear()
        new = Recipe()
        rec = dict()

        new.name = input("Recipe Name ? > ")
        rec["name"] = new.name
        self.recipe_book.append(rec)

    def ls_recipe(self):
        pass

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
            print("Exiting...")
            menu.running = False
            return 0
        else:
            return c


if __name__ == "__main__":
    menu = Menu()
    while menu.running:
        tr = Recipe()
        menu.display()

        user_choice = menu.choice()
        if user_choice != 0:
            print(f"{user_choice} is not a valid choice, please try again.")

    print(menu.recipe_book)
    s = dumps(menu.recipe_book, indent = 4)
    print(s)

