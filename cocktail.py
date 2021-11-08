from tkinter import *
from urllib.request import urlopen
from PIL import Image, ImageTk
import requests
from io import BytesIO

# create frame + set background image/title
window = Tk()
window.geometry("1200x800+300+100")
window.title("Cocktail Recipes")
background_image = PhotoImage(file="background.PNG")
background = Canvas(window,
                    width=400,
                    height=400)
background.pack(fill="both",
                expand=True)
background.create_image(0, 0,
                        image=background_image,
                        anchor="nw")
background.create_text(600, 50,
                       fill="white",
                       font=("Bradley Hand ITC", 50, "bold"),
                       text="Cocktail Recipes")

# create empty placeholders for drink name, info, ingredients, recipe, image, and invalid drink to update dynamically
drinkName = background.create_text(600, 250,
                                   fill="white",
                                   font=("Bradley Hand ITC", 40, "bold"),
                                   text="",
                                   width=1000)

infoVar = StringVar()
info_label = Label(window,
                   font=("Candara", 15),
                   textvariable=infoVar,
                   wraplength=600,
                   width=60,
                   height=5,
                   bg='#9AACAA')

ingredientVar = StringVar()
ingredient_label = Label(window,
                         textvariable=ingredientVar,
                         font=("Candara", 15),
                         wraplength=500,
                         width=30,
                         height=16,
                         bg='#9AACAA')

recipeVar = StringVar()
recipe_label = Label(window,
                     textvariable=recipeVar,
                     font=("Candara", 15),
                     wraplength=300,
                     width=30,
                     height=16,
                     bg='#9AACAA')

image_label = Label(bg='#9AACAA',
                    width=332,
                    height=140)

invalid_drink_label = Label(window,
                            text="Sorry, we couldn't find that drink. Please enter a different drink and try again.",
                            font=("Candara", 15),
                            wraplength=600,
                            width=60,
                            height=5,
                            bg='#9AACAA')

# refresh button & function
refresh_button = Button(window,
                        text="Start Over",
                        font=("Candara", 15),
                        bg='#9AACAA',
                        fg='black',
                        height=1,
                        width=10,
                        command=lambda: refresh(),
                        borderwidth=2)
refresh_button.place(x=540, y=182)


def refresh():
    """
    A method that "refreshes" the frame so the user can start over searches by hiding any existing drink name title,
    info, ingredients/measurements, image, and recipe. It deletes any existing text inside the search bar and resets
    the placeholder text
    """
    search_input.delete(0, END)
    info_label.place_forget()
    ingredient_label.place_forget()
    recipe_label.place_forget()
    image_label.place_forget()
    background.itemconfig(drinkName, text="")
    invalid_drink_label.place_forget()
    refresh_button.focus()
    clear_search_entry_field()


# search bar description text, entry field, placeholder text, and button
background.create_text(300, 150,
                       fill="#eaac72",
                       font=("Candara", 18),
                       text="Learn about a cocktail and learn how to make it! \n               Enter the cocktail "
                            "name below:",
                       width=500)
search_text = StringVar()
search_input = Entry(window,
                     font=("Candara", 15),
                     bg='#9AACAA',
                     fg='black',
                     bd=5,
                     textvariable=search_text,
                     borderwidth=2)
search_input.insert(0, "Search cocktail by name")

# delete placeholder/searched text upon clicking inside entry field
search_input.bind("<FocusIn>", lambda args: search_input.delete('0', END))

# allows users to press enter to start search after entering a drink name
search_input.bind("<Return>", lambda args: random_or_specified("specified"))

search_input.place(x=100,
                   y=180,
                   height=41,
                   width=330)

# magnifying glass search button
search_image = Image.open("search.PNG")
resize_image = search_image.resize((40, 40))
new_image = ImageTk.PhotoImage(resize_image)
search_button = Button(window,
                       image=new_image,
                       height=35,
                       width=40,
                       command=lambda: [random_or_specified("specified")],
                       borderwidth=2)

# delete searched text inside entry field upon clicking search button
search_button.bind("<FocusIn>", lambda args: search_input.delete('0', 'end'))
search_button.place(x=430, y=182)

# random text
background.create_text(900, 150,
                       fill="#eaac72",
                       font=("Candara", 18),
                       text="Can't decide or looking for a random cocktail? \n                    Click the button "
                            "below:",
                       width=500)

# random drink description text, entry field, placeholder text, and button
random_button = Button(window,
                       bg='#9AACAA',
                       height=1,
                       width=30,
                       font=("Candara", 15),
                       borderwidth=2,
                       command=lambda: random_or_specified("random"),
                       text="Surprise Me!")
random_button.place(x=730, y=180)


def random_or_specified(search_type):
    """
    A method that is bound to the <enter> key, search, and random button that determines whether or not the search is
    from the search bar if a user enters a drink name or from the random button if a user clicks to find a random drink
    and passes the appropriate url to the method get_cocktail() to retrieve drink info
    """
    if search_type == "specified":
        drink = search_text.get()
        url = "http://www.thecocktaildb.com/api/json/v1/1/search.php?s=" + drink + ""
    else:
        url = "http://www.thecocktaildb.com/api/json/v1/1/random.php"
    get_cocktail(url)


def display_drink_name_title(drink_name):
    """
    A method that is called by get_cocktail() to display the drink name title
    """
    background.itemconfig(drinkName, text=drink_name)


def get_ingredients(drink):
    """
    A method that is called by get_cocktail() to get the drink ingredients and returns it in a list
    """
    ingredient_lst = []
    for i in range(1, 9):
        if drink["drinks"][0][f"strIngredient{i}"] is None or drink["drinks"][0][f"strIngredient{i}"] == "":
            break
        ingredient_lst.append(drink["drinks"][0][f"strIngredient{i}"])
    return ingredient_lst


def get_measurements(drink):
    """
    A method that is called by get_cocktail() to get the drink ingredient measurements and returns it in a list
    """
    measurement_lst = []
    for i in range(1, 9):
        if drink["drinks"][0][f"strMeasure{i}"] is None or drink["drinks"][0][f"strMeasure{i}"] == "":
            break
        measurement_lst.append(drink["drinks"][0][f"strMeasure{i}"])
    return measurement_lst


def display_ingredients_and_measurements(ingredient_lst, measurement_lst):
    """
    A method that is called by get_cocktail() to display the ingredients and their measurements
    """
    ingredients_and_measurements = ""
    for i in range(len(ingredient_lst)):
        # sometimes an exact measurement isn't needed so we only display the ingredient in these cases
        try:
            measurement = measurement_lst[i]
        except IndexError:
            measurement = ""
        ingredients_and_measurements += (measurement + "  " + ingredient_lst[i] + "\n")
    ingredientVar.set("Ingredients \n\n" + ingredients_and_measurements)
    ingredient_label.place(x=200, y=430)


def display_recipe(instructions):
    """
    A method that is called by get_cocktail() to display the recipe instructions
    """
    recipeVar.set("Recipe \n \n" + instructions)
    recipe_label.place(x=730, y=415)


def get_wiki(drink_name):
    """
    A method that is called by get_cocktail() to send a GET request to my teammate Dani's wiki scraper microservice to
    retrieve and return the first two sentences from Wikipedia. If the drink doesn't exist on wikipedia then it displays
    a message telling the user
    """
    wiki_url = "https://wiki-scrape-361.herokuapp.com/firstxpara/" + drink_name + "_(cocktail)/1"
    response = requests.get(wiki_url)
    json = response.json()
    wiki_info = json['output'][0]

    if "Other reasons this message may be displayed:" in wiki_info:
        info = "Sorry, Wikipedia doesn't have info on this drink, but we hope you still enjoy making it!"
    else:
        # we only want the first two sentences
        info = ""
        num_of_periods = 0
        for i in wiki_info:
            if num_of_periods == 2:
                break
            info += i
            if i == ".":
                num_of_periods += 1

    return info


def display_wiki(info):
    """
    A method that is called by get_cocktail() to display the drink info from wikipedia
    """
    infoVar.set(info)
    info_label.place(x=50, y=300)


def display_image(drink_img):
    """
    A method that is called by get_cocktail() to resize and display the drink image
    """
    image_url = urlopen(drink_img)
    raw_data = image_url.read()
    image_url.close()
    im = Image.open(BytesIO(raw_data))
    resized_image = im.resize((140, 140))
    photo = ImageTk.PhotoImage(resized_image)
    image_label.configure(image=photo)
    image_label.image = photo
    image_label.place(x=730, y=300)


def clear_search_entry_field():
    """
    A method that is called by get_cocktail() to clear any existing drink names in the search bar and reset the
    placeholder text after a search is made
    """
    search_input.delete(0, END)
    search_input.insert(0, "Search cocktail by name")
    refresh_button.focus()
    search_button.bind("<FocusIn>", lambda args: search_input.delete('0', 'end'))


def display_invalid_drink():
    """
    A method that is called by get_cocktail() if the drink searched doesn't exist in the database and displays a message
    to the user telling them the drink is invalid and to try searching a different drink name then resets the search
    bar
    """
    refresh()
    invalid_drink_label.place(x=50, y=300)
    clear_search_entry_field()


def get_cocktail(url):
    """
    A method that sends a GET request to the appropriate URL and retrieves information from theCocktailDB API and my
    teammate Dani's wiki scraper microservice then dynamically displays the drink name title, info, ingredients &
    measurements, drink image, and recipe. If the drink doesn't exist in the database then it displays a message for
    the user
    """
    response = requests.get(url)
    json = response.json()

    if json["drinks"] is None:
        display_invalid_drink()
    else:
        refresh()
        drink_name = json['drinks'][0]['strDrink']
        drink_instr = json['drinks'][0]['strInstructions']
        drink_img = json['drinks'][0]['strDrinkThumb']

        display_drink_name_title(drink_name)
        display_ingredients_and_measurements(get_ingredients(json), get_measurements(json))
        display_recipe(drink_instr)
        display_wiki(get_wiki(drink_name))
        display_image(drink_img)


window.mainloop()
