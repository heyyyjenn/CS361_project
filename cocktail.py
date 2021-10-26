from tkinter import *
from PIL import Image, ImageTk

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


window.mainloop()
