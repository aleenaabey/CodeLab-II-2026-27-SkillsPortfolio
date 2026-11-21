import os
import random
from tkinter import *
from tkinter import messagebox

BG_COLOUR = "#fff4e0"

# Look for the text file next to this script so it works from any folder
JOKES_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "randomJokes.txt")

jokes = []             # list of (setup, punchline) tuples
currentJoke = None     # the joke currently on screen


def loadJokes():
    """Read the file and return a list of (setup, punchline) tuples."""
    jokeList = []
    try:
        with open(JOKES_FILE, "r", encoding="utf-8") as fileHandler:
            for line in fileHandler:
                line = line.strip()
                if "?" not in line:          # skip blank / malformed lines
                    continue
                # split only on the FIRST '?' so punchlines can contain '?'
                setup, punchline = line.split("?", 1)
                jokeList.append((setup + "?", punchline.strip()))
    except FileNotFoundError:
        messagebox.showerror("File not found",
                             f"Could not find:\n{JOKES_FILE}")
    return jokeList


def tellJoke():
    """Pick a random joke (different from the last one) and show the setup."""
    global currentJoke
    if not jokes:
        return

    newJoke = random.choice(jokes)
    while newJoke == currentJoke and len(jokes) > 1:
        newJoke = random.choice(jokes)
    currentJoke = newJoke

    setupLabel.config(text=currentJoke[0])
    punchlineLabel.config(text="")           # hide the old punchline
    punchlineButton.config(state=NORMAL)     # now a punchline can be shown
    nextButton.config(state=NORMAL)
    alexaButton.config(state=DISABLED)       # first button only needed once


def showPunchline():
    """Display the punchline underneath the setup."""
    if currentJoke is not None:
        punchlineLabel.config(text=currentJoke[1])
        punchlineButton.config(state=DISABLED)


# ---------------------------------------------------------------------------
# Window
# ---------------------------------------------------------------------------
root = Tk()
root.title("Alexa, tell me a Joke")
root.geometry("560x380")
root.config(bg=BG_COLOUR)

jokes = loadJokes()

Label(root, text="Joke Assistant", font=("Arial", 20, "bold"),
      bg=BG_COLOUR).pack(pady=(20, 10))

alexaButton = Button(root, text="Alexa tell me a Joke", font=("Arial", 13),
                     width=22, command=tellJoke)
alexaButton.pack(pady=5)

# wraplength makes long jokes wrap onto several lines instead of being cut off
setupLabel = Label(root, text="", font=("Arial", 15, "bold"), bg=BG_COLOUR,
                   wraplength=500, justify="center", height=3)
setupLabel.pack(pady=(15, 5))

punchlineLabel = Label(root, text="", font=("Arial", 15, "italic"),
                       bg=BG_COLOUR, fg="#c62828", wraplength=500,
                       justify="center", height=3)
punchlineLabel.pack(pady=5)

# Buttons side by side in their own frame
buttonFrame = Frame(root, bg=BG_COLOUR)
buttonFrame.pack(pady=10)

punchlineButton = Button(buttonFrame, text="Show Punchline", width=14,
                         state=DISABLED, command=showPunchline)
punchlineButton.grid(row=0, column=0, padx=6)

nextButton = Button(buttonFrame, text="Next Joke", width=14,
                    state=DISABLED, command=tellJoke)
nextButton.grid(row=0, column=1, padx=6)

Button(buttonFrame, text="Quit", width=14,
       command=root.destroy).grid(row=0, column=2, padx=6)

root.mainloop()