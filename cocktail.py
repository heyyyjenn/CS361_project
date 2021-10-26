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
drinkName = background.create_text(600, 250, fill="white", font=("Bradley Hand ITC", 40, "bold"), text="", width=500)

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
search_input.bind("<Return>", lambda args: search())
search_input.place(x=100, y=180, height=41, width=330)

# magnifying glass search button
search_image = Image.open("search.PNG")
resize_image = search_image.resize((40, 40))
new_image = ImageTk.PhotoImage(resize_image)
search_button = Button(window,
                       image=new_image,
                       height=35,
                       width=40,
                       command=lambda: [search()],
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
                       text="Surprise Me!")
random_button.place(x=730, y=180)

# search function calls get_cocktail() with entry field text inside search bar
def search():
    get_cocktail(search_text.get())
    
def get_cocktail(drink):
    print(drink)
    url = "http://www.thecocktaildb.com/api/json/v1/1/search.php?s=" + drink + ""
    params = [{"positions": [0, 6, 7, 29]}]
    headers = {"Content-Type": "application/json"}
    
    # GET request
    response = requests.get(url, json=params, headers=headers)
    json = response.json()
    drink_name = json['drinks'][0]['strDrink']
    drink_instr = json['drinks'][0]['strInstructions']
    ingredient1 = json['drinks'][0]['strIngredient1']
    drink_img = json['drinks'][0]['strDrinkThumb']

    # place drink name title
    background.itemconfig(drinkName, text=drink_name)
    
    # some drinks have less ingredients - if the json data doesn't have an ingredient listed then leave it empty
    if json['drinks'][0]['strIngredient2']:
        ingredient2 = json['drinks'][0]['strIngredient2']
    else:
        ingredient2 = ""
    if json['drinks'][0]['strIngredient3']:
        ingredient3 = json['drinks'][0]['strIngredient3']
    else:
        ingredient3 = ""
    if json['drinks'][0]['strIngredient4']:
        ingredient4 = json['drinks'][0]['strIngredient4']
    else:
        ingredient4 = ""
    if json['drinks'][0]['strIngredient5']:
        ingredient5 = json['drinks'][0]['strIngredient5']
    else:
        ingredient5 = ""
    if json['drinks'][0]['strIngredient6']:
        ingredient6 = json['drinks'][0]['strIngredient6']
    else:
        ingredient6 = ""
    if json['drinks'][0]['strIngredient7']:
        ingredient7 = json['drinks'][0]['strIngredient7']
    else:
        ingredient7 = ""
    if json['drinks'][0]['strIngredient8']:
        ingredient8 = json['drinks'][0]['strIngredient8']
    else:
        ingredient8 = ""
    if json['drinks'][0]['strIngredient9']:
        ingredient9 = json['drinks'][0]['strIngredient9']
    else:
        ingredient9 = ""

    # some drinks have less measurements - if the json data doesn't have a measurement listed then leave it empty
    strMeasure1 = json['drinks'][0]['strMeasure1']
    if json['drinks'][0]['strMeasure2']:
        strMeasure2 = json['drinks'][0]['strMeasure2']
    else:
        strMeasure2 = ""
    if json['drinks'][0]['strMeasure3']:
        strMeasure3 = json['drinks'][0]['strMeasure3']
    else:
        strMeasure3 = ""
    if json['drinks'][0]['strMeasure4']:
        strMeasure4 = json['drinks'][0]['strMeasure4']
    else:
        strMeasure4 = ""
    if json['drinks'][0]['strMeasure5']:
        strMeasure5 = json['drinks'][0]['strMeasure5']
    else:
        strMeasure5 = ""
    if json['drinks'][0]['strMeasure6']:
        strMeasure6 = json['drinks'][0]['strMeasure6']
    else:
        strMeasure6 = ""
    if json['drinks'][0]['strMeasure7']:
        strMeasure7 = json['drinks'][0]['strMeasure7']
    else:
        strMeasure7 = ""
    if json['drinks'][0]['strMeasure8']:
        strMeasure8 = json['drinks'][0]['strMeasure8']
    else:
        strMeasure8 = ""
    if json['drinks'][0]['strMeasure9']:
        strMeasure9 = json['drinks'][0]['strMeasure9']
    else:
        strMeasure9 = ""

    # place ingredients
    ingredientVar.set("Ingredients \n\n" + strMeasure1 + "  " + ingredient1 + "\n" + strMeasure2 + "  " + ingredient2
                      + "\n" + strMeasure3 + "  " + ingredient3 + "\n" + strMeasure4 + "  " + ingredient4 + "\n"
                      + strMeasure5 + "  " + ingredient5 + "\n" + strMeasure6 + "  " + ingredient6 + "\n"
                      + strMeasure7 + "  " + ingredient7 + "\n" + strMeasure8 + "  " + ingredient8 + "\n"
                      + strMeasure9 + "  " + ingredient9)
    ingredient_label.place(x=200, y=430)

    # place recipe
    recipeVar.set("Recipe \n \n" + drink_instr)
    recipe_label.place(x=730, y=430)
    
    # use teammate's wiki scraper API
    wiki_url = "https://wiki-scrape-361.herokuapp.com/firstxpara/" + drink + "_(cocktail)/1"
    params = [{"positions": [0, 6, 7, 29]}]
    headers = {"Content-Type": "application/json"}
    
    # GET request
    response = requests.get(wiki_url, json=params, headers=headers)
    json = response.json()
    wiki_info = json['output'][0]
    
    # we only want the first two sentences - place info
    two_sentences = ""
    num_of_periods = 0
    for i in wiki_info:
        if num_of_periods == 2:
            break
        two_sentences += i
        if i == ".":
            num_of_periods += 1
    infoVar.set(two_sentences)
    info_label.place(x=50, y=300)

    # cocktail image - place image
    image_url = urlopen(drink_img)
    raw_data = image_url.read()
    image_url.close()
    im = Image.open(BytesIO(raw_data))
    resized_image = im.resize((140, 140))
    photo = ImageTk.PhotoImage(resized_image)
    label = Label(image=photo, bg='#9AACAA', width=332, height=140)
    label.image = photo
    label.place(x=730, y=300)

    # delete text inside search entry field
    search_input.delete(0, END)


window.mainloop()
