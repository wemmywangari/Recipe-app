# libraries that hepl to process the link of the image that will we will get from the recipes
from io import BytesIO
from PIL import Image, ImageTk     

# library that plays the click sound when I click search    
from playsound import playsound

# Library that gives access to the numerous recipes in Edaman
from py_edamam import PyEdamam

import requests
import tkinter as tk


# library that helps us open the link
import webbrowser

# CONSTANTS
BUTTON_CLICK_SOUND = "clicksound.mp3"  
WINDOW_TITLE = "Recipe Art App"
RECIPE_IMAGE_WIDTH = 450
RECIPE_IMAGE_HEIGHT = 600



class RecipeApp():
    # Initializing the class
    def __init__(self, recipe_app_id, recipe_app_key):

        
        self.recipe_app_id = recipe_app_id
        self.recipe_app_key = recipe_app_key
        self.window = tk.Tk()          #Initializes the window so as to be able to create window
       
        # Auto resize geometry
        self.window.geometry("")
        self.window.configure(bg="#E99497")
        self.window.title(WINDOW_TITLE)

        # The search LABEL properties and placement  on window
        self.search_label = tk.Label(self.window, text = "Search For A Recipe", bg = "#444444",fg="black")
        self.search_label.grid(column = 0, row = 0, padx=5)


        # The search ENTRY properties and placement on window
        self.search_entry = tk.Entry(master = self.window, width = 40)
        self.search_entry.grid(column = 1, row = 0, padx=5, pady = 10)

        # The search BUTTON properties and placement  on window
        self.search_button = tk.Button(self.window, text = "search", highlightbackground = "#FFD8CC",fg="black")
        command = self.__run_search_query
        self.search_button.grid(column = 2, row = 0, padx = 5)


    #Function that runs the search   
    def __run_search_query(self):

        playsound(BUTTON_CLICK_SOUND)
        query = self.search_entry.get()    # to capture/get what was entered in search box
        recipe = self.__get_recipe(query)        # to capture/get the recipe that is being searched
    
        if recipe:
            # When recipe is found
            recipe_image = recipe.image                      # gets the image of the recipe being searched
            recipe_url = recipe.url                          # gets the link of the recipe being searched
        
        else:
            # When Recipe not found
            recipe_image = "https://i.pinimg.com/originals/57/11/ff/5711ff78c1e72030bcc46bf63f068f68.jpg"       #  shows a 404 image
            recipe_url = ""                         # cause there is no recipe found they'll be no url
       

        # Shows the image and ingredients
        self.__show_image(recipe_image)
        self.__get_ingredients(recipe)


        # Function that shoes the recipe link
        def __recipe_link():
            playsound(BUTTON_CLICK_SOUND)
            webbrowser.open(recipe_url)


        # Create the recipe link button
        self.recipe_button = tk.Button(self.window, text = "Recipe link", highlightbackground = " #FFD8CC",fg="black")
        command = __recipe_link
        self.recipe_button.grid(column = 1, row = 7, pady = 10)

    # Function that queries the API and gets recipe
    def __get_recipe(self, query):
        edamam_object = PyEdamam(recipes_appid=self.recipe_app_id, recipes_appkey=self.recipe_app_key)
        query_result = edamam_object.search_recipe(query)   # SEARCHES THE RECIPES
        
        # Get first recipe in list
        for recipe in query_result:
            return recipe
    # Function that shows image
    def __show_image(self, image_url):
        response = requests.get(image_url)
        
        img = Image.open(BytesIO(response.content))           # converts the response to a suitable format
        img = img.resize((RECIPE_IMAGE_WIDTH, RECIPE_IMAGE_HEIGHT))
        image = ImageTk.PhotoImage(img)


        #Show the image on window and get the ingredients
        holder = tk.Label(self.window, image = image)
        holder.photo = image
        holder.grid(column=1, row=6, pady=10)
    
    # Function that takes the recipe
    def __get_ingredients(self, recipe):
        ingredients = tk.Text(master = self.window, height = 15, width = 50, bg = "FAF1E6",fg="red")         # HOW THE TEXT OF THE INGREDIENTS WILL DISPLAY
        ingredients.grid(column=1,row=4, pady = 10)                                           # The placement of the ingredients on  on window
        ingredients.delete("1.0", tk.END)                                                   # to be able to  keep getting a new set of ingredients after searching for different recipes
   

        # TO tell the user when a certain ingredient is not found
        if recipe == None :
            ingredients.insert(tk.END, "No Recipe found for search criteria")
            return

        # When a recipe is found
        ingredients.insert(tk.END, "\n" + recipe.label + "\n")       # shows the recipe label
        for ingredient in recipe.ingredient_names:                   # displays the ingredients in form of a list
            ingredients.insert(tk.END, "\n- " + ingredient)

    def run_app(self):
        self.window.mainloop()
        return
      

# Create App and run the app
if __name__ == "__main__":
        #API Keys
        APP_ID = "c32045a0"                                #Put your app id for edamam api
        APP_KEY = "0c9f7226cfc05af813bbcd57c1ccf8e0	—"     #Put your app key for edamam api

        recipe_app = RecipeApp(APP_ID, APP_KEY)
        recipe_app.run_app()
  
