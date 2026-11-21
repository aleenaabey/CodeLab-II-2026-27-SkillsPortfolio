# Exercise 2 - Alexa tell me a Joke
import os
import random
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image     

# ---------- THEME CONFIGURATION ----------
CARD_COLOR = "#3b0a0a"       # dark card behind the joke text
TEXT_COLOR = "#ffffff"
ACCENT_COLOR = "#ffd166"     # gold
FONT_NAME = "Trebuchet MS"
BG_IMAGE = "joke_bg.png"    


BASE_DIR = os.path.dirname(os.path.abspath(__file__))     # get the directory of this script
file_path = os.path.join(BASE_DIR, "randomJokes.txt")
image_path = os.path.join(BASE_DIR, BG_IMAGE)           # path to the background image


#--------- Read jokes from file ----------
jokes = []    # each joke will be stored as [setup, punchline]

with open(file_path, "r", encoding="utf-8") as file_handler:
    lines = file_handler.readlines()                  # read all lines from the file

for line in lines:
    line = line.strip()
    if line != "":
        parts = line.split("?")
        setup = parts[0] + "?"                             
        punchline = parts[1]
        jokes.append([setup, punchline])                   # store the joke as a list of [setup, punchline]

current_joke = []    # the joke on screen at the moment


# ---------- Functions ----------
def tell_joke():
    """Pick a random joke and show only the setup."""
    global current_joke
    current_joke = random.choice(jokes)
    setup_label.config(text=current_joke[0])
    punchline_label.config(text="")


def show_punchline():
    """Show the punchline under the setup."""
    if current_joke == []:
        messagebox.showinfo("No joke yet", "Click 'Alexa tell me a Joke' first!")
    else:
        punchline_label.config(text=current_joke[1])


# ---------- Window ----------
root = Tk()
root.title("Alexa tell me a Joke")
root.geometry("440x520")                       # set the window size to match the background image
root.resizable(False, False)                        # prevent the window from being resized

raw_image = Image.open(image_path).resize((440, 520))
bg_photo = ImageTk.PhotoImage(raw_image)
bg_label = Label(root, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)            # place the background image to fill the window

# Title and main button at the top
title_label = Label(root, text="Joke Assistant", font=(FONT_NAME, 22, "bold"),
                    bg=CARD_COLOR, fg=ACCENT_COLOR, padx=15, pady=3)
title_label.place(relx=0.5, y=25, anchor=N)

alexa_button = Button(root, text="Alexa tell me a Joke", font=(FONT_NAME, 13, "bold"),             # Also used for the "Next Joke" button
                      bg=ACCENT_COLOR, fg="#3b0a0a", width=22, command=tell_joke)
alexa_button.place(relx=0.5, y=85, anchor=N)

# Dark card at the bottom holds the joke, so the microphone stays visible
card = Frame(root, bg=CARD_COLOR, padx=15, pady=15, bd=2, relief=RIDGE)
card.place(relx=0.5, rely=1.0, y=-20, anchor=S, width=400)

setup_label = Label(card, text="", font=(FONT_NAME, 14, "bold"), bg=CARD_COLOR,
                    fg=TEXT_COLOR, wraplength=360, height=2)
setup_label.pack(pady=5)

punchline_label = Label(card, text="", font=(FONT_NAME, 14, "italic"), bg=CARD_COLOR,
                        fg=ACCENT_COLOR, wraplength=360, height=2)
punchline_label.pack(pady=5)

button_frame = Frame(card, bg=CARD_COLOR)
button_frame.pack(pady=10)

punchline_button = Button(button_frame, text="Show Punchline", width=12,
                          command=show_punchline)
punchline_button.pack(side=LEFT, padx=4)

next_button = Button(button_frame, text="Next Joke", width=12, command=tell_joke)                 
next_button.pack(side=LEFT, padx=4)

quit_button = Button(button_frame, text="Quit", width=12, command=root.destroy)
quit_button.pack(side=LEFT, padx=4)

root.mainloop()             # start the GUI event loop