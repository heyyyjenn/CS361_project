from tkinter import *
from urllib.request import urlopen
from PIL import Image, ImageTk
import requests
from io import BytesIO

# create program shell/dimensions
window = Tk()
window.geometry("1200x800+300+100")
window.title("Cocktail Recipes")

# background image
bg = PhotoImage(file="background.PNG")
background = Canvas(window, width=400, height=400)
background.pack(fill="both", expand=True)
background.create_image(0, 0, image=bg, anchor="nw")

# program title
background.create_text(600, 50, fill="white", font=("Bradley Hand ITC", 50, "bold"),
                       text="Cocktail Recipes")

# creating empty placeholders to update later dynamically
drinkName = background.create_text(600, 250, fill="white", font=("Bradley Hand ITC", 40, "bold"), text="", width=1000)

# information
infoVar = StringVar()
info_label = Label(window, font=("Candara", 15), textvariable=infoVar, wraplength=600, width=60, height=5, bg='#9AACAA')
info_label.place(x=100, y=300)
info_label.place_forget()

# ingredients
ingredientVar = StringVar()
ingredient_label = Label(window, textvariable=ingredientVar, font=("Candara", 15), wraplength=500, width=30, height=12,
                         bg='#9AACAA')
ingredient_label.place(x=550, y=600)
ingredient_label.place_forget()

# recipe
recipeVar = StringVar()
recipe_label = Label(window, textvariable=recipeVar, font=("Candara", 15), wraplength=300, width=30, height=12,
                     bg='#9AACAA')
recipe_label.place(x=550, y=600)
recipe_label.place_forget()

# image
image_label = Label(bg='#9AACAA', width=332, height=140)
image_label.place(x=730, y=300)
image_label.place_forget()

# refresh button
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

# there isn't a reload function so we have to manually hide all the labels & reset text for search bar
def refresh():
    search_input.delete(0, END)
    info_label.place_forget()
    ingredient_label.place_forget()
    recipe_label.place_forget()
    image_label.place_forget()
    background.itemconfig(drinkName, text="")
    search_input.insert(0, "Search cocktail by name")
    refresh_button.focus()
    search_button.bind("<FocusIn>", lambda args: search_input.delete('0', 'end'))


# --- SEARCH ---

# search text
background.create_text(300, 150, fill="#eaac72", font=("Candara", 18),
                       text="Learn about a cocktail and learn how to make it! \n               Enter the cocktail "
                            "name below:",
                       width=500)
search_text = StringVar()

# search field
search_input = Entry(window,
                     font=("Candara", 15),
                     bg='#9AACAA',
                     fg='black',
                     bd=5,
                     textvariable=search_text,
                     borderwidth=2)

# search entry placeholder text
search_input.insert(0, "Search cocktail by name")

# delete placeholder/searched text upon clicking inside entry field
search_input.bind("<FocusIn>", lambda args: search_input.delete('0', END))
search_input.bind("<Return>", lambda args: random_or_specified("specified"))
search_input.place(x=100, y=180, height=41, width=330)

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

# --- RANDOM ---

# random text
background.create_text(900, 150, fill="#eaac72", font=("Candara", 18),
                       text="Can't decide or looking for a random cocktail? \n                    Click the button "
                            "below:",
                       width=500)

# random button
random_button = Button(window,
                       bg='#9AACAA',
                       height=1,
                       width=30,
                       font=("Candara", 15),
                       borderwidth=2,
                       command=lambda: random_or_specified("random"),
                       text="Surprise Me!")
random_button.place(x=730, y=180)


# this method determines whether or not the search is a specified or random drink and passes the appropriate url
def random_or_specified(search_type):
    if search_type == "specified":
        drink = search_text.get()
        url = "http://www.thecocktaildb.com/api/json/v1/1/search.php?s=" + drink + ""
    else:
        url = "http://www.thecocktaildb.com/api/json/v1/1/random.php"

    get_cocktail(url)

def display_drink_name_title(drink_name):
    background.itemconfig(drinkName, text=drink_name)

def get_ingredients(drink):
    ingredient_lst = []
    for i in range(1, 9):
        if drink["drinks"][0][f"strIngredient{i}"] is None or drink["drinks"][0][f"strIngredient{i}"] == "":
            break
        ingredient_lst.append(drink["drinks"][0][f"strIngredient{i}"])
    return ingredient_lst

def get_measurements(drink):
    measurement_lst = []
    for i in range(1, 9):
        if drink["drinks"][0][f"strMeasure{i}"] is None or drink["drinks"][0][f"strMeasure{i}"] == "":
            break
        measurement_lst.append(drink["drinks"][0][f"strMeasure{i}"])
    return measurement_lst

def display_ingredients_and_measurements(ingredient_lst, measurement_lst):
    ingredients_and_measurements = ""
    for i in range(len(ingredient_lst)):
        try:
            measurement = measurement_lst[i]
        except IndexError:
            measurement = ""
        ingredients_and_measurements += (measurement + "  " + ingredient_lst[i] + "\n")
    ingredientVar.set("Ingredients \n\n" + ingredients_and_measurements)
    ingredient_label.place(x=200, y=430)

def display_recipe(instructions):
    recipeVar.set("Recipe \n \n" + instructions)
    recipe_label.place(x=730, y=430)

def get_wiki(drink_name):
    wiki_url = "https://wiki-scrape-361.herokuapp.com/firstxpara/" + drink_name + "_(cocktail)/1"

    # GET request
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
    infoVar.set(info)
    info_label.place(x=50, y=300)

def display_image(drink_img):
    # cocktail image - place image
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
    # delete text inside search entry field
    search_input.delete(0, END)
    search_input.insert(0, "Search cocktail by name")
    refresh_button.focus()
    search_button.bind("<FocusIn>", lambda args: search_input.delete('0', 'end'))

def get_cocktail(url):
    # GET request
    response = requests.get(url)
    json = response.json()
    drink_name = json['drinks'][0]['strDrink']
    drink_instr = json['drinks'][0]['strInstructions']
    drink_img = json['drinks'][0]['strDrinkThumb']

    display_drink_name_title(drink_name)
    display_ingredients_and_measurements(get_ingredients(json), get_measurements(json))
    display_recipe(drink_instr)
    display_wiki(get_wiki(drink_name))
    display_image(drink_img)
    clear_search_entry_field()


window.mainloop()
