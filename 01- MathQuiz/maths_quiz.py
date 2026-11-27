import os
import random
from datetime import *
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk


# -------------------- Colours and Fonts --------------------

BG_COLOR = "#020b24"
CARD_COLOR = "#030d24"
NEON_GLOW = "#0077b6"
NEON_CYAN = "#00f5ff"
NEON_BLUE = "#0088ff"
NEON_GREEN = "#39ff14"
NEON_PINK = "#ff4d6d"
TEXT_COLOR = "#e6f9ff"
SUBTEXT_COLOR = "#9be7ff"
FONT_NAME = "Segoe UI"
TOTAL_QUESTIONS = 10


# -------------------- Quiz Variables --------------------

difficulty = "Easy"
question_num = 1
score = 0
attempt = 1
question_history = []

num1 = 0
num2 = 0
operation = "+"

bg_labels = []
card_bg_labels = []
last_size = (0, 0)
history_return_frame = None


# -------------------- Main Window --------------------

root = Tk()
root.title("Maths Quiz")
root.geometry("500x400")
root.minsize(500, 400)
root.resizable(True, True)
root.configure(bg=BG_COLOR)


# -------------------- Load Images --------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCORES_FILE = os.path.join(BASE_DIR, "quiz_scores.txt")

bg_image = Image.open(os.path.join(BASE_DIR, "math_bg.png"))
background_photo = ImageTk.PhotoImage(bg_image.resize((500, 400)))

card_image = Image.open(os.path.join(BASE_DIR, "maths_equation_bg.png"))
card_photo_init = ImageTk.PhotoImage(card_image.resize((360, 260)))


def add_background(frame):    # add_background(frame) It will put the math_bg.png image behind the frame
    lbl = Label(frame, image=background_photo, bd=0)
    lbl.image = background_photo
    lbl.place(x=0, y=0, relwidth=1, relheight=1)
    bg_labels.append(lbl)


def resize_background(event):          #resize_background(event) It will resize both background images and scales the text when window changes
    global background_photo, last_size

    if event.widget != root or event.width < 480 or event.height < 380:
        return

    w = event.width
    h = event.height
    if (w, h) == last_size:
        return
    last_size = (w, h)

    # Resize outer background
    resized_bg = bg_image.resize((w, h))
    background_photo = ImageTk.PhotoImage(resized_bg)
    for lbl in bg_labels:
        lbl.config(image=background_photo)
        lbl.image = background_photo

    # Resize card background inside neon boxes
    for card_lbl, rw, rh in card_bg_labels:
        cw = int(w * rw)
        ch = int(h * rh)
        if cw < 100:
            cw = 100
        if ch < 100:
            ch = 100
        resized_card = card_image.resize((cw, ch))
        new_card_photo = ImageTk.PhotoImage(resized_card)
        card_lbl.config(image=new_card_photo)
        card_lbl.image = new_card_photo

    # Scale font sizes when window is maximized or minimized
    scale = min(w / 500, h / 400)
    if scale < 1.0:
        scale = 1.0
    if scale > 1.75:
        scale = 1.75

    date_lbl.config(font=(FONT_NAME, int(9 * scale), "bold"))
    home_title_lbl.config(font=(FONT_NAME, int(20 * scale), "bold"))
    home_dev_lbl.config(font=(FONT_NAME, int(10 * scale), "italic"))
    home_sub_lbl.config(font=(FONT_NAME, int(9 * scale)))
    inst_btn.config(font=(FONT_NAME, int(10 * scale), "bold"))
    cont_btn.config(font=(FONT_NAME, int(10 * scale), "bold"))

    menu_title_lbl.config(font=(FONT_NAME, int(15 * scale), "bold"))
    for rb in diff_radios:
        rb.config(font=(FONT_NAME, int(10 * scale), "bold"))
    score_check.config(font=(FONT_NAME, int(9 * scale)))
    start_btn.config(font=(FONT_NAME, int(10 * scale), "bold"))
    history_menu_btn.config(font=(FONT_NAME, int(10 * scale), "bold"))
    home_back_btn.config(font=(FONT_NAME, int(10 * scale), "bold"))

    progress_label.config(font=(FONT_NAME, int(9 * scale), "bold"))
    score_label.config(font=(FONT_NAME, int(9 * scale), "bold"))
    problem_label.config(font=(FONT_NAME, int(22 * scale), "bold"))
    answer_entry.config(font=(FONT_NAME, int(14 * scale)))
    submit_btn.config(font=(FONT_NAME, int(10 * scale), "bold"))
    feedback_label.config(font=(FONT_NAME, int(9 * scale), "bold"))

    res_title_lbl.config(font=(FONT_NAME, int(18 * scale), "bold"))
    final_score_label.config(font=(FONT_NAME, int(14 * scale), "bold"))
    rank_label.config(font=(FONT_NAME, int(16 * scale), "bold"))
    res_prompt_lbl.config(font=(FONT_NAME, int(10 * scale)))
    for btn in res_buttons:
        btn.config(font=(FONT_NAME, int(9 * scale), "bold"))

    rev_title_lbl.config(font=(FONT_NAME, int(15 * scale), "bold"))
    review_text.config(font=(FONT_NAME, int(9 * scale)))
    rev_back_btn.config(font=(FONT_NAME, int(10 * scale), "bold"))

    hist_title_lbl.config(font=(FONT_NAME, int(15 * scale), "bold"))
    history_text.config(font=(FONT_NAME, int(9 * scale)))
    hist_clear_btn.config(font=(FONT_NAME, int(9 * scale), "bold"))
    hist_back_btn.config(font=(FONT_NAME, int(10 * scale), "bold"))


# -------------------- Frame Switching--------------------

def switch_to_frame(frame):             #switch_to_frame(frame) It brings the chosen frame to the front
    frame.tkraise()


# -------------------- Instructions Popup --------------------

def open_instructions():  #open_instructions() It opens the popup window showing how to play the quiz
    inst_win = Toplevel(root)
    inst_win.title("Instructions")
    inst_win.geometry("380x250")
    inst_win.resizable(0, 0)
    inst_win.configure(bg=NEON_CYAN, padx=2, pady=2)

    inner = Frame(inst_win, bg=CARD_COLOR)
    inner.pack(fill=BOTH, expand=YES)

    Label(
        inner,
        text="How to Play Maths Quiz",
        font=(FONT_NAME, 13, "bold"),
        bg=CARD_COLOR,
        fg=NEON_CYAN
    ).pack(pady=(16, 10))

    Label(
        inner,
        text=(
            "1. Click Continue and select a difficulty level.\n"
            "2. Solve 10 addition or subtraction questions.\n"
            "3. 1st attempt correct = 10 points.\n"
            "4. 2nd attempt correct = 5 points.\n"
            "5. Press Enter or Submit to check your answer."
        ),
        font=(FONT_NAME, 9),
        bg=CARD_COLOR,
        fg=TEXT_COLOR,
        justify=LEFT
    ).pack(padx=20, pady=5)

    Button(
        inner,
        text="Close",
        font=(FONT_NAME, 9, "bold"),
        bg=NEON_CYAN,
        fg=BG_COLOR,
        width=12,
        pady=4,
        command=inst_win.destroy
    ).pack(pady=15)


# -------------------- Neon Box Using Nested Frames --------------------

def create_neon_box(parent_frame, rw, rh, rely_pos=0.5): # create_neon_box(...) It will make a double neon border box by using nested frames
    outer_glow = Frame(parent_frame, bg=NEON_GLOW, padx=3, pady=3)
    outer_glow.place(relx=0.5, rely=rely_pos, anchor=CENTER, relwidth=rw, relheight=rh)

    neon_border = Frame(outer_glow, bg=NEON_CYAN, padx=2, pady=2)
    neon_border.pack(fill=BOTH, expand=YES)

    card = Frame(neon_border, bg=CARD_COLOR)
    card.pack(fill=BOTH, expand=YES)

    card_bg_lbl = Label(card, image=card_photo_init, bd=0)
    card_bg_lbl.place(x=0, y=0, relwidth=1, relheight=1)
    card_bg_lbl.image = card_photo_init
    card_bg_labels.append((card_bg_lbl, rw, rh))

    return card


# -------------------- Required Quiz Functions --------------------

def randomInt(level): # randomInt(level) It generates the random numbers for Easy, Moderate, or Advanced
    if level == "Easy":
        return random.randint(1, 9)
    elif level == "Moderate":
        return random.randint(10, 99)
    else:
        return random.randint(1000, 9999)


def decideOperation(): # decideOperation() It randomly picks + or - for the question
    return random.choice(["+", "-"])


def isCorrect(n1, n2, op, user_answer):  # isCorrect(...)  It checks if the user answer matches the right answer
    if op == "+":
        correct_answer = n1 + n2
    else:
        correct_answer = n1 - n2

    if user_answer == correct_answer:
        return True
    else:
        return False


def get_rank(final_score): # get_rank(final_score) It gives A+ to F grade based on the final score
    if final_score >= 90:
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


# -------------------- File Handling for Score History --------------------

def save_score_log(level, final_score, rank):     # save_score_log(...)  It saves the date, level, score and rank into quiz_scores.txt
    date_now = datetime.now()
    entry = f"{date_now:%d %B %Y} | Level: {level} | Score: {final_score}/100 | Rank: {rank}\n"
    with open(SCORES_FILE, "a") as file_handler:
        file_handler.write(entry)


def read_score_history():       # read_score_history() It will read all the saved scores from quiz_scores.txt
    if not os.path.exists(SCORES_FILE):
        return []

    saved_lines = []
    with open(SCORES_FILE, "r") as file_handler:
        lines = file_handler.readlines()
        for line in lines:
            clean = line.rstrip()
            if clean != "":
                saved_lines.append(clean)
    return saved_lines


def clear_score_history():  # clear_score_history()  It asks yes or no and clears quiz_scores.txt
    confirm = messagebox.askyesno(
        "Clear History",
        "Are you sure you want to clear all saved score history?"
    )
    if confirm:
        with open(SCORES_FILE, "w") as file_handler:
            file_handler.write("")
        displayHistory()


def displayHistory(return_frame=None):  # displayHistory(...) It will showup the saved scores in the history text box
    global history_return_frame
    if return_frame is not None:
        history_return_frame = return_frame
        if return_frame == menu_frame:
            hist_back_btn.config(text="Back to Menu")
        else:
            hist_back_btn.config(text="Back to Results")

    history_text.config(state=NORMAL)
    history_text.delete("1.0", "end")

    entries = read_score_history()
    if len(entries) == 0:
        history_text.insert(END, "No saved quiz scores yet.\n")
    else:
        count = 1
        for line in entries:
            history_text.insert(END, str(count) + ". " + line + "\n")
            history_text.insert(END, "----------------------------------------\n")
            count += 1

    history_text.config(state=DISABLED)
    switch_to_frame(history_frame)


# -------------------- Quiz Flow Functions --------------------

def displayMenu():   # displayMenu() It resets to Easy and opens the difficulty menu
    diff_var.set("Easy")
    switch_to_frame(menu_frame)


def start_quiz(chosen_level):   # start_quiz(chosen_level) It resets the score and starts from question 1
    global difficulty, question_num, score, attempt, question_history

    difficulty = chosen_level
    question_num = 1
    score = 0
    attempt = 1
    question_history = []
    score_label.config(text="Score: 0")

    displayProblem()
    switch_to_frame(quiz_frame)


def displayProblem():    # displayProblem() It will create and shows the next maths question
    global num1, num2, operation, attempt

    attempt = 1
    num1 = randomInt(difficulty)
    num2 = randomInt(difficulty)
    operation = decideOperation()

    progress_label.config(
        text="Question " + str(question_num) + "/" + str(TOTAL_QUESTIONS) + " - " + difficulty
    )

    if show_score_var.get() == 1:
        score_label.config(text="Score: " + str(score))
    else:
        score_label.config(text="Score: Hidden")

    problem_label.config(text=str(num1) + " " + operation + " " + str(num2) + " =")

    answer_entry.config(state=NORMAL)
    answer_entry.delete(0, END)
    answer_entry.focus()

    feedback_label.config(text="Attempt 1 of 2", fg=NEON_CYAN)

    submit_btn.config(
        text="Submit Answer",
        command=check_answer,
        state=NORMAL
    )


def check_answer(event=None):  # check_answer() It checks input, gives 10 pts first try or 5 pts second try
    global score, attempt

    if answer_entry["state"] == DISABLED:
        return

    user_input = answer_entry.get().strip()

    try:
        user_answer = int(user_input)
    except ValueError:
        messagebox.showwarning("Invalid Input", "Please enter a whole number.")
        answer_entry.focus()
        return

    if operation == "+":
        correct_answer = num1 + num2
    else:
        correct_answer = num1 - num2

    if isCorrect(num1, num2, operation, user_answer):
        if attempt == 1:
            points_earned = 10
        else:
            points_earned = 5

        score += points_earned

        question_history.append({
            "question": str(num1) + " " + operation + " " + str(num2),
            "your_answer": user_answer,
            "correct_answer": correct_answer,
            "result": "Correct (+" + str(points_earned) + " pts)"
        })

        finish_question("Correct! (+" + str(points_earned) + " points)", NEON_GREEN)
    else:
        if attempt == 1:
            attempt = 2
            feedback_label.config(
                text="Incorrect! Try one more time (Attempt 2 of 2).",
                fg=NEON_PINK
            )
            answer_entry.delete(0, END)
            answer_entry.focus()
        else:
            question_history.append({
                "question": str(num1) + " " + operation + " " + str(num2),
                "your_answer": user_answer,
                "correct_answer": correct_answer,
                "result": "Incorrect (0 pts)"
            })
            finish_question("Incorrect! Correct answer: " + str(correct_answer), NEON_PINK)


def finish_question(message, color):   # finish_question(...) This disables the entry and changes the button to Next Question
    answer_entry.config(state=DISABLED)
    feedback_label.config(text=message, fg=color)

    if show_score_var.get() == 1:
        score_label.config(text="Score: " + str(score))

    submit_btn.config(text="Next Question", command=next_question)


def next_question():   # next_question() It moves to next question or opens results after 10
    global question_num

    if question_num < TOTAL_QUESTIONS:
        question_num += 1
        displayProblem()
    else:
        displayResults(score)


def ask_replay():   # ask_replay() It will ask the user if they want to play again or quit
    replay = messagebox.askyesno(
        "Play Again?",
        "Would you like to play another Maths Quiz?"
    )
    if replay:
        displayMenu()
    else:
        root.destroy()


def displayResults(final_score): # displayResults(final_score)  It will save the score and show the final score and rank
    rank = get_rank(final_score)
    save_score_log(difficulty, final_score, rank)

    final_score_label.config(text="Final Score: " + str(final_score) + " / 100")

    if final_score >= 50:
        rank_color = NEON_GREEN
    else:
        rank_color = NEON_PINK

    rank_label.config(text="Rank: " + rank, fg=rank_color)
    switch_to_frame(results_frame)


def displayReview():   # displayReview()  It will display all 10 questions and answers in review box
    review_text.config(state=NORMAL)
    review_text.delete("1.0", "end")

    if len(question_history) == 0:
        review_text.insert(END, "No questions answered yet.\n")
    else:
        index = 1
        for item in question_history:
            review_text.insert(END, str(index) + ". " + item["question"] + "\n")
            review_text.insert(END, "   Your answer    : " + str(item["your_answer"]) + "\n")
            review_text.insert(END, "   Correct answer : " + str(item["correct_answer"]) + "\n")
            review_text.insert(END, "   Result         : " + item["result"] + "\n")
            review_text.insert(END, "----------------------------------------\n")
            index += 1

    review_text.config(state=DISABLED)
    switch_to_frame(review_frame)


# =========================================================
# FRAME 1: HOME PAGE (Slide 146)
# =========================================================
home_frame = Frame(root, bg=BG_COLOR)
home_frame.place(x=0, y=0, relwidth=1, relheight=1)
add_background(home_frame)

today = datetime.now()
date_frame = Frame(home_frame, bg=NEON_CYAN, padx=2, pady=2)
date_frame.place(relx=0.5, rely=0.09, anchor=CENTER)

date_lbl = Label(
    date_frame,
    text=f"{today:%A, %d %B %Y}",
    font=(FONT_NAME, 9, "bold"),
    bg=CARD_COLOR,
    fg=NEON_CYAN,
    padx=12,
    pady=3
)
date_lbl.pack()

home_center = create_neon_box(home_frame, 0.66, 0.44, rely_pos=0.47)

home_inner = Frame(home_center, bg=CARD_COLOR, padx=14, pady=10)
home_inner.place(relx=0.5, rely=0.5, anchor=CENTER)

home_title_lbl = Label(
    home_inner,
    text="Maths Quiz App",
    font=(FONT_NAME, 20, "bold"),
    bg=CARD_COLOR,
    fg=NEON_CYAN
)
home_title_lbl.pack(pady=(0, 6))

home_dev_lbl = Label(
    home_inner,
    text="Developed by Aleena",
    font=(FONT_NAME, 10, "italic"),
    bg=CARD_COLOR,
    fg=TEXT_COLOR
)
home_dev_lbl.pack(pady=(0, 8))

home_sub_lbl = Label(
    home_inner,
    text="Test your addition & subtraction skills!",
    font=(FONT_NAME, 9),
    bg=CARD_COLOR,
    fg=SUBTEXT_COLOR
)
home_sub_lbl.pack()

inst_btn = Button(
    home_frame,
    text="Instructions",
    font=(FONT_NAME, 10, "bold"),
    bg=NEON_BLUE,
    fg="#ffffff",
    padx=16,
    pady=6,
    command=open_instructions
)
inst_btn.place(relx=0.05, rely=0.93, anchor=SW)

cont_btn = Button(
    home_frame,
    text="Continue",
    font=(FONT_NAME, 10, "bold"),
    bg=NEON_CYAN,
    fg=BG_COLOR,
    padx=20,
    pady=6,
    command=lambda: switch_to_frame(menu_frame)
)
cont_btn.place(relx=0.95, rely=0.93, anchor=SE)


# =========================================================
# FRAME 2: DIFFICULTY MENU FRAME
# =========================================================
menu_frame = Frame(root, bg=BG_COLOR)
menu_frame.place(x=0, y=0, relwidth=1, relheight=1)
add_background(menu_frame)

menu_card = create_neon_box(menu_frame, 0.76, 0.72)

menu_inner = Frame(menu_card, bg=CARD_COLOR, padx=18, pady=12)
menu_inner.place(relx=0.5, rely=0.5, anchor=CENTER)

menu_title_lbl = Label(
    menu_inner,
    text="DIFFICULTY LEVEL",
    font=(FONT_NAME, 15, "bold"),
    bg=CARD_COLOR,
    fg=NEON_CYAN
)
menu_title_lbl.pack(pady=(0, 10))

diff_var = StringVar(value="Easy")
diff_radios = []

for txt, val, col in [
    ("1. Easy (Single Digit)", "Easy", NEON_GREEN),
    ("2. Moderate (Double Digit)", "Moderate", NEON_CYAN),
    ("3. Advanced (Four Digit)", "Advanced", NEON_PINK),
]:
    rb = Radiobutton(
        menu_inner,
        text=txt,
        variable=diff_var,
        value=val,
        font=(FONT_NAME, 10, "bold"),
        bg=CARD_COLOR,
        fg=col,
        selectcolor=BG_COLOR,
        activebackground=CARD_COLOR,
        activeforeground=col
    )
    rb.pack(anchor=W, pady=4)
    diff_radios.append(rb)

show_score_var = IntVar(value=1)
score_check = Checkbutton(
    menu_inner,
    text="Show live score during quiz",
    variable=show_score_var,
    font=(FONT_NAME, 9),
    bg=CARD_COLOR,
    fg=TEXT_COLOR,
    selectcolor=BG_COLOR,
    activebackground=CARD_COLOR
)
score_check.pack(pady=8)

menu_btns = Frame(menu_inner, bg=CARD_COLOR)
menu_btns.pack(pady=6)

start_btn = Button(
    menu_btns,
    text="Start Quiz",
    font=(FONT_NAME, 10, "bold"),
    bg=NEON_CYAN,
    fg=BG_COLOR,
    padx=12,
    pady=5,
    command=lambda: start_quiz(diff_var.get())
)
start_btn.pack(side=LEFT, padx=4)

history_menu_btn = Button(
    menu_btns,
    text="History",
    font=(FONT_NAME, 10, "bold"),
    bg=NEON_BLUE,
    fg="#ffffff",
    padx=12,
    pady=5,
    command=lambda: displayHistory(menu_frame)
)
history_menu_btn.pack(side=LEFT, padx=4)

home_back_btn = Button(
    menu_btns,
    text="Home",
    font=(FONT_NAME, 10, "bold"),
    bg=NEON_PINK,
    fg="#ffffff",
    padx=12,
    pady=5,
    command=lambda: switch_to_frame(home_frame)
)
home_back_btn.pack(side=LEFT, padx=4)


# =========================================================
# FRAME 3: QUIZ FRAME
# =========================================================
quiz_frame = Frame(root, bg=BG_COLOR)
quiz_frame.place(x=0, y=0, relwidth=1, relheight=1)
add_background(quiz_frame)

quiz_card = create_neon_box(quiz_frame, 0.76, 0.72)

quiz_inner = Frame(quiz_card, bg=CARD_COLOR, padx=16, pady=12)
quiz_inner.place(relx=0.5, rely=0.5, anchor=CENTER, relwidth=0.84)

top_bar = Frame(quiz_inner, bg=CARD_COLOR)
top_bar.pack(fill=X, pady=(0, 8))

progress_label = Label(
    top_bar,
    text="",
    font=(FONT_NAME, 9, "bold"),
    bg=CARD_COLOR,
    fg=TEXT_COLOR
)
progress_label.pack(side=LEFT)

score_label = Label(
    top_bar,
    text="Score: 0",
    font=(FONT_NAME, 9, "bold"),
    bg=CARD_COLOR,
    fg=NEON_CYAN
)
score_label.pack(side=RIGHT)

problem_label = Label(
    quiz_inner,
    text="",
    font=(FONT_NAME, 22, "bold"),
    bg=CARD_COLOR,
    fg="#ffffff"
)
problem_label.pack(pady=14)

entry_border = Frame(quiz_inner, bg=NEON_CYAN, padx=2, pady=2)
entry_border.pack(pady=6)

answer_entry = Entry(
    entry_border,
    font=(FONT_NAME, 14),
    width=12,
    justify=CENTER,
    bg="#040e26",
    fg=NEON_CYAN,
    insertbackground=NEON_CYAN,
    bd=0
)
answer_entry.pack(ipady=4)
answer_entry.bind("<Return>", check_answer)

submit_btn = Button(
    quiz_inner,
    text="Submit Answer",
    font=(FONT_NAME, 10, "bold"),
    bg=NEON_CYAN,
    fg=BG_COLOR,
    padx=16,
    pady=6,
    command=check_answer
)
submit_btn.pack(pady=12)

feedback_label = Label(
    quiz_inner,
    text="",
    font=(FONT_NAME, 9, "bold"),
    bg=CARD_COLOR,
    fg=NEON_CYAN
)
feedback_label.pack(pady=4)


# =========================================================
# FRAME 4: RESULTS FRAME
# =========================================================
results_frame = Frame(root, bg=BG_COLOR)
results_frame.place(x=0, y=0, relwidth=1, relheight=1)
add_background(results_frame)

res_card = create_neon_box(results_frame, 0.80, 0.70)

res_inner = Frame(res_card, bg=CARD_COLOR, padx=18, pady=12)
res_inner.place(relx=0.5, rely=0.5, anchor=CENTER)

res_title_lbl = Label(
    res_inner,
    text="QUIZ COMPLETE!",
    font=(FONT_NAME, 18, "bold"),
    bg=CARD_COLOR,
    fg=NEON_CYAN
)
res_title_lbl.pack(pady=8)

final_score_label = Label(
    res_inner,
    text="",
    font=(FONT_NAME, 14, "bold"),
    bg=CARD_COLOR,
    fg=TEXT_COLOR
)
final_score_label.pack(pady=6)

rank_label = Label(
    res_inner,
    text="",
    font=(FONT_NAME, 16, "bold"),
    bg=CARD_COLOR,
    fg=NEON_GREEN
)
rank_label.pack(pady=6)

res_prompt_lbl = Label(
    res_inner,
    text="Would you like to play again?",
    font=(FONT_NAME, 10),
    bg=CARD_COLOR,
    fg=TEXT_COLOR
)
res_prompt_lbl.pack(pady=8)

button_frame = Frame(res_inner, bg=CARD_COLOR)
button_frame.pack(pady=6)

b1 = Button(
    button_frame,
    text="Review",
    font=(FONT_NAME, 9, "bold"),
    bg=NEON_CYAN,
    fg=BG_COLOR,
    padx=9,
    pady=6,
    command=displayReview
)
b1.pack(side=LEFT, padx=3)

b2 = Button(
    button_frame,
    text="Play Again",
    font=(FONT_NAME, 9, "bold"),
    bg=NEON_BLUE,
    fg="#ffffff",
    padx=9,
    pady=6,
    command=ask_replay
)
b2.pack(side=LEFT, padx=3)

b3 = Button(
    button_frame,
    text="Quit",
    font=(FONT_NAME, 9, "bold"),
    bg=NEON_PINK,
    fg="#ffffff",
    padx=9,
    pady=6,
    command=root.destroy
)
b3.pack(side=LEFT, padx=3)

b4 = Button(
    button_frame,
    text="History",
    font=(FONT_NAME, 9, "bold"),
    bg=NEON_GREEN,
    fg=BG_COLOR,
    padx=9,
    pady=6,
    command=lambda: displayHistory(results_frame)
)
b4.pack(side=LEFT, padx=3)

res_buttons = [b1, b2, b3, b4]


# =========================================================
# FRAME 5: REVIEW ANSWERS FRAME
# =========================================================
review_frame = Frame(root, bg=BG_COLOR)
review_frame.place(x=0, y=0, relwidth=1, relheight=1)
add_background(review_frame)

rev_card = create_neon_box(review_frame, 0.84, 0.82)

rev_inner = Frame(rev_card, bg=CARD_COLOR, padx=10, pady=8)
rev_inner.place(relx=0.5, rely=0.5, anchor=CENTER, relwidth=0.90, relheight=0.88)

rev_title_lbl = Label(
    rev_inner,
    text="ANSWER REVIEW",
    font=(FONT_NAME, 15, "bold"),
    bg=CARD_COLOR,
    fg=NEON_CYAN
)
rev_title_lbl.pack(side=TOP, pady=(0, 8))

rev_back_btn = Button(
    rev_inner,
    text="Back to Results",
    font=(FONT_NAME, 10, "bold"),
    bg=NEON_CYAN,
    fg=BG_COLOR,
    padx=16,
    pady=6,
    command=lambda: switch_to_frame(results_frame)
)
rev_back_btn.pack(side=BOTTOM, pady=(10, 0))

review_box = Frame(rev_inner, bg=NEON_CYAN, padx=2, pady=2)
review_box.pack(fill=BOTH, expand=YES)

scrollbar = Scrollbar(review_box)
scrollbar.pack(side=RIGHT, fill=Y)

review_text = Text(
    review_box,
    height=6,
    font=(FONT_NAME, 9),
    bg=CARD_COLOR,
    fg=NEON_CYAN,
    bd=0,
    padx=12,
    pady=10,
    yscrollcommand=scrollbar.set,
    wrap=WORD
)
review_text.pack(side=LEFT, fill=BOTH, expand=YES)
scrollbar.config(command=review_text.yview)


# =========================================================
# FRAME 6: SCORE HISTORY FRAME
# =========================================================
history_frame = Frame(root, bg=BG_COLOR)
history_frame.place(x=0, y=0, relwidth=1, relheight=1)
add_background(history_frame)

hist_card = create_neon_box(history_frame, 0.86, 0.84)

hist_inner = Frame(hist_card, bg=CARD_COLOR, padx=10, pady=8)
hist_inner.place(relx=0.5, rely=0.5, anchor=CENTER, relwidth=0.92, relheight=0.90)

hist_title_lbl = Label(
    hist_inner,
    text="SCORE HISTORY",
    font=(FONT_NAME, 15, "bold"),
    bg=CARD_COLOR,
    fg=NEON_CYAN
)
hist_title_lbl.pack(side=TOP, pady=(0, 8))

hist_btn_bar = Frame(hist_inner, bg=CARD_COLOR)
hist_btn_bar.pack(side=BOTTOM, pady=(10, 0))

hist_clear_btn = Button(
    hist_btn_bar,
    text="Clear History",
    font=(FONT_NAME, 9, "bold"),
    bg=NEON_PINK,
    fg="#ffffff",
    padx=12,
    pady=6,
    command=clear_score_history
)
hist_clear_btn.pack(side=LEFT, padx=6)

hist_back_btn = Button(
    hist_btn_bar,
    text="Back to Results",
    font=(FONT_NAME, 10, "bold"),
    bg=NEON_CYAN,
    fg=BG_COLOR,
    padx=14,
    pady=6,
    command=lambda: switch_to_frame(history_return_frame)
)
hist_back_btn.pack(side=LEFT, padx=6)

history_box = Frame(hist_inner, bg=NEON_CYAN, padx=2, pady=2)
history_box.pack(fill=BOTH, expand=YES)

hist_scrollbar = Scrollbar(history_box)
hist_scrollbar.pack(side=RIGHT, fill=Y)

history_text = Text(
    history_box,
    height=6,
    font=(FONT_NAME, 9),
    bg=CARD_COLOR,
    fg=TEXT_COLOR,
    bd=0,
    padx=12,
    pady=10,
    yscrollcommand=hist_scrollbar.set,
    wrap=WORD
)
history_text.pack(side=LEFT, fill=BOTH, expand=YES)
hist_scrollbar.config(command=history_text.yview)


# -------------------- Start App --------------------

root.bind("<Configure>", resize_background)
switch_to_frame(home_frame)
root.mainloop()