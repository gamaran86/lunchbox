# -*- coding: utf-8 -*

"""Lunchbox.py: Recipe book program
-----------------------------------
Features in developpement:
    - create, save, load and display recipes, ingredients
    - generate cooking plannings
    - generate shopping lists
"""

# recipe creation is done : next step recipe search + print / dition

from os import system, name as osname
from json import loads, dumps
from time import sleep
import re

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
        """Allows user to input a choice when in the main menu"""

        c = input("Please choose an option: > ")
        try:
            c = int(c)
        except:
            return c

        if c == 1: # create recipe
            self.create_recipe()
            return 0

        elif c == 2: # print recipe (not done)
            self.print_recipe()
            return 0

        elif c == 3: # search and edit a recipe (on-going, currently editing the json file directly)
            self.edit_recipe()
            return 0

        elif c == 4: # lists all recipes in recipe file
            self.list_recipes()
            return 0

        elif c == 5: # save the changes in the recipes in the recipe book
            self.save_recipe_book()
            return 0

        elif c == 0: # exit
            clear()
            print("Exiting...")
            menu.running = False
            return 0

        else:
            return c


    def list_recipes(self):
        clear()
        print("Recipe list:\n---------------\n")
        for recipe in self.recipe_book:
            name = recipe["name"]
            print(f"- {name}")
        input("\nPress on any key to continue... >")


    def load_recipe_book(self):
        clear()
        with open('recipe.json',"r") as f:
            recipe_str = f.read()
            if recipe_str == None or recipe_str == "":
                print("Empty recipe file/ No recipe.json file found")
            else:
                self.recipe_book = loads(recipe_str)


    def save_recipe_book(self):
        """saves the recipes in a json file"""

        with open('recipe.json',"w") as f:
            f.write(dumps(self.recipe_book, indent = 4))
        clear()
        print("Successfully saved.")
        sleep(1)


    def search_recipe(self):
        """search the recipes name attribute for a match"""

        searchable_str = str()

        #list all potential candidates
        for recipe in self.recipe_book:
            searchable_str = searchable_str + recipe["name"] + " "
        research = input("Please enter search: > ")
        pattern =  r"[a-z]*[A-Z]*" + research + r"[a-z]*[A-Z]*\b"

        found = re.findall(pattern, searchable_str, flags=re.I)

        if found != []:
            #choose the searched recipe
            for i,srecipe in enumerate(found):
                for recipe in self.recipe_book:
                    if recipe["name"] == srecipe:
                        print(f"{i}. {srecipe}")
            edit_index = input("choose recipe to use: >")
            try:
                edit_index = int(edit_index)
            except:
                print(edit_index, " is not the number of the recipe to edit")

        for i,srecipe in enumerate(found):
            if edit_index == i:
                return srecipe

    def edit_recipe(self):
        """ Allows edition of one recipe """ # currently only opens the json file for modification in nvim

        editable = self.search_recipe()
        for recipe in self.recipe_book:
            if recipe["name"] == editable:
                system("nvim recipe.json")


    def print_recipe(self):
        """ prints the searche  recipe """ # currently only prints a dump of the exracted json file

        printable = self.search_recipe()
        output_print=""

        for recipe in self.recipe_book:
            if recipe["name"] == printable:
                output_print = dumps(recipe, indent = 4)

        if output_print != "":
            print(output_print)
            input("\ninput a key to continue> ...")
            return output_print
        else:
            input("\nno match: input a key to continue> ...")


if __name__ == "__main__":
    menu = Menu()
    menu.load_recipe_book()

    while menu.running:
        menu.display()
        user_choice = menu.choice()
        if user_choice != 0:
            print(f"{user_choice} is not a valid choice, please try again.")
            sleep(2)
    menu.save_recipe_book()
