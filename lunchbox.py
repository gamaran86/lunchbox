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

def compact_name(name):
    """Function to reformat names so that search is easier with name_spaces"""

    if " " in name: #separation des mots
        spl = name.split(" ")

        for i,_ in enumerate(spl): #construction du format "code"
            spl[i] = spl[i][0].upper() + spl[i][1:]
        new_name = "".join(spl)
        return new_name

    else:
        return name

def isgoodname(name):
    """Tests if name parameter is alphanumerical + space(true) or something else (false)"""
    r = re.compile("^[a-zA-Z ]*$")
    return r.match(name) is None

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
        self.code = str()
        self.ingredients = list()


    def set_rec(self):
        clear()
        self.name="_"

        #recipe name def
        while isgoodname(self.name):
            self.name = input("Recipe Name ? > ")

        self.code = compact_name(self.name)
        clear()

        #creation of ingredient list
        add_ingredients = input("Would you like to add ingredients? [y/n] > ").lower()
        while add_ingredients == 'y':
            n = input("ingredient name? > ")
            q = input("quantity? > ")
            u = input("unit? > ")

            #secure user input for integer conversion
            try:
                if "." in q:
                    q = float(q)
                else:
                    q = int(q)
                ing = dict()
                ing["name"] = n
                ing["quantity"] = q
                ing["unit"] = u
                self.ingredients.append(ing)
            except:
                print("there was an error with your quantity, \
please use only integers and floats")
            sleep(1.5)
            #continue adding ingredients or exit the edition loop
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
               + "6. Delete Recipe\n" \
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
        rec["code"] = new.code
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

        elif c == 6: # deletes a searched recipe
            self.delete_recipe()
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
        """Loads the  recipes from a json file"""

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

        #definitions for search and found variables
        searchable_str = str()
        found = []

        #list all potential candidates
        for recipe in self.recipe_book:
            searchable_str = searchable_str + recipe["code"] + " "
        research = input("Please enter search: > ")
        pattern =  r"[a-z]*[A-Z]*" + research + r"[a-z]*[A-Z]*\b"

        #input protection on pattern
        try:
            found = re.findall(pattern, searchable_str, flags=re.I)
        except:
            print(pattern, " has special symbols, use only alphanumerical")

        #choose the recipe if found
        if found != []:
            #creates a list of all matches
            for i,srecipe in enumerate(found):
                for recipe in self.recipe_book:
                    if recipe["code"] == srecipe:
                        name = recipe["name"]
                        print(f"{i}. {name}")

            #user choses the match he would like to print
            edit_index = input("choose recipe to use: >")

            #input protection on edit_index chosen by user
            try:
                edit_index = int(edit_index)
            except:
                print(edit_index, " is not the number of the recipe to edit")
                sleep(1.5)

        #returns the matching recipe name as a string
        for i,srecipe in enumerate(found):
            if edit_index == i:
                return srecipe


    def edit_recipe(self):
        """ Allows edition of one recipe """ # currently only opens the json file for modification in nvim

        editable = self.search_recipe()

        for recipe in self.recipe_book:
            if recipe["code"] == editable:
                system("nvim recipe.json")

        self.load_recipe_book()


    def print_recipe(self):
        """ prints the searche  recipe """ # currently only prints a dump of the exracted json file

        printable = self.search_recipe()
        output_print=""

        for recipe in self.recipe_book:
            if recipe["code"] == printable:
                output_print = dumps(recipe, indent = 4)

        if output_print != "":
            print(output_print)
            input("\ninput a key to continue> ...")
            return output_print

        else:
            input("\nno match: input a key to continue> ...")


    def confirmation(self):
        delete_sentence = input("type DELETE if you want to delete permanently > ")
        if delete_sentence == "DELETE":
            return True
        else:
            return False

    def delete_recipe(self):
        """deletes chosen recipes based on a search """

        deletable = self.search_recipe()

        for recipe in self.recipe_book:
            if recipe["code"] == deletable:
                if self.confirmation():
                    todel = recipe
        self.recipe_book.remove(todel)
        print(self.recipe_book)
        input("\ninput a key to continue> ...")

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
