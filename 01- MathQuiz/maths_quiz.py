"""
Exercise 1 - Maths Quiz
A Tkinter quiz of 10 addition / subtraction questions.
Scoring: 10 points for a correct first attempt, 5 for the second attempt.
"""

import os
import random
from tkinter import *
from tkinter import messagebox

# Pillow is only needed for background images (pip install pillow)
try:
    from PIL import ImageTk, Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

BG_COLOR = "#0b132b"
CARD_COLOR = "#1c2541"
TEXT_COLOR = "#f8f9fa"
ACCENT_COLOR = "#5bc0be"
BTN_EASY = "#3a86ff"
BTN_MOD = "#5bc0be"
BTN_ADV = "#ff6b6b"

FONT_NAME = "Trebuchet MS"
TITLE_SIZE = 22
PROBLEM_SIZE = 26
BODY_SIZE = 12
# ============================================================#

TOTAL_QUESTIONS = 10

# Folder this script is saved in (used to find the background image)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Quiz state (these change while the quiz is running)
difficulty = ""
question_num = 1
score = 0
attempt = 1
num1 = 0
num2 = 0
operation = "+"

# ---- Create the main window (must come before any function uses root) ----
root = Tk()
root.title("Maths Quiz")
root.geometry("480x380")
root.resizable(False, False)
root.config(bg=BG_COLOR)


def set_background(window, img_name, width, height):
    """Show a background image if one is set; otherwise return None."""
    if img_name and HAS_PIL:
        img_path = os.path.join(BASE_DIR, img_name)
        if os.path.exists(img_path):
            raw_img = Image.open(img_path).resize((width, height))
            bg_photo = ImageTk.PhotoImage(raw_img)
            lbl = Label(window, image=bg_photo)
            lbl.image = bg_photo      # keep a reference so the image stays visible
            lbl.place(x=0, y=0, relwidth=1, relheight=1)
            return lbl
    return None

BG_IMAGE = "math_bg.jpg"
BG_COLOR = "#0b132b"
CARD_COLOR = "#1c2541"
bg_label = set_background(root, BG_IMAGE, 480, 380)              # background image label (used to clear the window later)


# ---------------------------------------------------------------------------
# Required functions
# ---------------------------------------------------------------------------
def randomInt(level):
    """Return a random integer based on the chosen difficulty level."""
    if level == "Easy":
        return random.randint(1, 9)          # single digit
    elif level == "Moderate":
        return random.randint(10, 99)        # double digit
    else:
        return random.randint(1000, 9999)    # four digit


def decideOperation():
    """Randomly choose and return '+' or '-'."""
    return random.choice(["+", "-"])


def isCorrect(n1, n2, op, user_answer):
    """Check whether user_answer matches the correct result."""
    correct_answer = n1 + n2 if op == "+" else n1 - n2
    return user_answer == correct_answer


def clear_window():
    """Remove every widget except the background image label."""
    for widget in root.winfo_children():
        if widget is not bg_label:
            widget.destroy()


def displayMenu():
    """Display the difficulty selection menu."""
    clear_window()

    card = Frame(root, 
                 bg=CARD_COLOR, 
                 padx=30, 
                 pady=25, 
                 bd=2, 
                 relief=RIDGE)
    card.place(relx=0.5, 
               rely=0.5, 
               anchor=CENTER)

    Label(card, 
          text="MATHS QUIZ", 
          font=(FONT_NAME, TITLE_SIZE, "bold"),
          bg=CARD_COLOR, 
          fg=TEXT_COLOR).pack(pady=(0, 4))

    Label(card, 
          text="DIFFICULTY LEVEL", 
          font=(FONT_NAME, BODY_SIZE, "bold"),
          bg=CARD_COLOR, 
          fg=ACCENT_COLOR).pack(pady=(0, 18))

    Button(card, 
           text="1. Easy (Single Digit)", 
           width=24,
           font=(FONT_NAME, BODY_SIZE, "bold"), 
           bg=BTN_EASY, 
           fg="#081c15",
           relief=FLAT, 
           pady=6,
           command=lambda: start_quiz("Easy")).pack(pady=5)

    Button(card, 
           text="2. Moderate (Double Digit)", 
           
           width=24,
           font=(FONT_NAME, BODY_SIZE, "bold"), 
           bg=BTN_MOD, 
           fg="#081c15",
           relief=FLAT, 
           pady=6,
           command=lambda: start_quiz("Moderate")).pack(pady=5)

    Button(card, 
           text="3. Advanced (4-Digit)", 
           width=24,
           font=(FONT_NAME, BODY_SIZE, "bold"), 
           bg=BTN_ADV, 
           fg="white",
           relief=FLAT, 
           pady=6,
           command=lambda: start_quiz("Advanced")).pack(pady=5)


def start_quiz(chosen_level):
    """Reset everything for a new play, then show the first question."""
    global difficulty, question_num, score, attempt
    difficulty = chosen_level
    question_num = 1
    score = 0
    attempt = 1
    build_quiz_screen()
    displayProblem()


def build_quiz_screen():
    """Create the widgets used by the quiz screen (filled in by displayProblem)."""
    global progress_label, score_label, problem_label
    global answer_entry, feedback_label, submit_btn
    clear_window()

    card = Frame(root, bg=CARD_COLOR, 
                 padx=25, 
                 pady=20, 
                 bd=2, 
                 relief=RIDGE,
                 width=380, 
                 height=300)
    card.place(relx=0.5, 
               rely=0.5, 
               anchor=CENTER)
    card.pack_propagate(False)

    # Top bar: question number on the left, score on the right
    top_bar = Frame(card, 
                    bg=CARD_COLOR)
    top_bar.pack(fill=X, 
                 pady=(0, 15))

    progress_label = Label(top_bar, 
                           text="", 
                           font=(FONT_NAME, 11, "bold"),
                           bg=CARD_COLOR, 
                           fg=TEXT_COLOR)
    progress_label.pack(side=LEFT)

    score_label = Label(top_bar, 
                        text="Score: 0", 
                        font=(FONT_NAME, 11, "bold"),
                        bg=CARD_COLOR, 
                        fg=ACCENT_COLOR)
    score_label.pack(side=RIGHT)

    # The question
    problem_label = Label(card, 
                          text="", 
                          font=(FONT_NAME, PROBLEM_SIZE, "bold"),
                          bg=CARD_COLOR, 
                          fg="#ffffff")
    problem_label.pack(pady=(18, 12))

    # Answer box (pressing Enter also submits)
    answer_entry = Entry(card, 
                         font=(FONT_NAME, 16), 
                         width=12, 
                         justify="center")
    answer_entry.pack(pady=6)
    answer_entry.bind("<Return>", 
                      lambda event: check_answer())

    submit_btn = Button(card, 
                        text="Submit Answer",
                        font=(FONT_NAME, BODY_SIZE, "bold"), 
                        bg=ACCENT_COLOR,
                        fg="#1b4332",
                          width=16, 
                          pady=5, 
                          relief=FLAT,
                        command=check_answer)
    submit_btn.pack(pady=14)

    feedback_label = Label(card, 
                           text="", 
                           font=(FONT_NAME, 11, "bold"),
                           bg=CARD_COLOR, 
                           fg=ACCENT_COLOR)
    feedback_label.pack(pady=4)


def displayProblem():
    """Create a new random question and show it."""
    global num1, num2, operation, attempt
    attempt = 1
    num1 = randomInt(difficulty)
    num2 = randomInt(difficulty)
    operation = decideOperation()

    progress_label.config(text=f"Q {question_num}/{TOTAL_QUESTIONS} ({difficulty})")
    score_label.config(text=f"Score: {score}")
    problem_label.config(text=f"{num1} {operation} {num2} =")

    answer_entry.config(state=NORMAL)
    answer_entry.delete(0, END)
    answer_entry.focus()
    submit_btn.config(state=NORMAL)


def check_answer():
    """Called when the user submits an answer: validate, mark and score it."""
    global score, attempt
    raw = answer_entry.get().strip()                   # get the user's input and remove whitespace

    # Input validation
    try:
        user_ans = int(raw)             # convert the input to an integer (will raise ValueError if not a valid whole number)
    except ValueError:
        messagebox.showwarning("Invalid Input", "Please enter a valid whole number.")
        answer_entry.focus()
        return

    if isCorrect(num1, num2, operation, user_ans):
        points = 10 if attempt == 1 else 5
        score += points
        score_label.config(text=f"Score: {score}")
        feedback_label.config(text=f"Correct! +{points} points", fg="#95d5b2")
        advance_quiz()
    else:
        if attempt == 1:
            # First wrong answer: allow one more try
            attempt = 2
            feedback_label.config(text="Incorrect! Try one more time.", fg=ACCENT_COLOR)
            answer_entry.delete(0, END)
            answer_entry.focus()
        else:
            # Second wrong answer: show the right answer and move on
            correct_val = num1 + num2 if operation == "+" else num1 - num2
            feedback_label.config(text=f"Incorrect! Answer was {correct_val}.", fg="#ffadad")
            advance_quiz()


def advance_quiz():
    """Pause briefly so the feedback can be read, then go to the next screen."""
    global question_num
    submit_btn.config(state=DISABLED)
    answer_entry.config(state=DISABLED)
    if question_num < TOTAL_QUESTIONS:
        question_num += 1
        root.after(900, next_question_step)
    else:
        root.after(900, lambda: displayResults(score))


def next_question_step():
    """Clear the feedback message and show the next question."""
    feedback_label.config(text="")
    displayProblem()


def get_rank(final_score):
    """Convert the final score into a rank."""
    if final_score > 90:
        return "A+"
    elif final_score >= 80:
        return "A"
    elif final_score >= 70:
        return "B"
    elif final_score >= 60:
        return "C"
    elif final_score >= 50:
        return "D"
    else:
        return "F"


def displayResults(final_score):
    """Show the final score out of 100, the rank and play again / quit buttons."""
    clear_window()
    rank = get_rank(final_score)

    card = Frame(root, 
                 bg=CARD_COLOR, 
                 padx=30, 
                 pady=25, 
                 bd=2, 
                 relief=RIDGE)
    card.place(relx=0.5, 
               rely=0.5, 
               anchor=CENTER)

    Label(card, 
          text="QUIZ COMPLETE!", 
          font=(FONT_NAME, TITLE_SIZE - 2, "bold"),
          bg=CARD_COLOR, 
          fg=ACCENT_COLOR).pack(pady=(0, 10))

    Label(card, 
          text=f"Final Score: {final_score} / 100",
          font=(FONT_NAME, 16, "bold"), 
          bg=CARD_COLOR, 
          fg=TEXT_COLOR).pack(pady=6)

    Label(card, 
          text=f"Rank: {rank}", 
          font=(FONT_NAME, 18, "bold"),
          bg=CARD_COLOR, 
          fg="#95d5b2").pack(pady=6)

    Label(card, text="Would you like to play again?", 
          font=(FONT_NAME, BODY_SIZE),
          bg=CARD_COLOR, 
          fg=TEXT_COLOR).pack(pady=(12, 10))

    btn_frame = Frame(card, bg=CARD_COLOR)
    btn_frame.pack()

    Button(btn_frame, 
           text="Play Again",
             width=12,
           font=(FONT_NAME, BODY_SIZE, "bold"), 
           bg=BTN_EASY, 
           fg="#081c15",
           relief=FLAT, 
           pady=5, 
           command=displayMenu).pack(side=LEFT, padx=6)

    Button(btn_frame, 
           text="Quit", 
           width=12,
           font=(FONT_NAME,BODY_SIZE, "bold"), 
                 bg=BTN_ADV, fg="white",
           relief=FLAT, pady=5, command=root.destroy).pack(side=LEFT, padx=6)


# ---------------------------------------------------------------------------
# Start the program
# ---------------------------------------------------------------------------
displayMenu()
root.mainloop()