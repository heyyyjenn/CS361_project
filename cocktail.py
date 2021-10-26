from tkinter import *

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

window.mainloop()
