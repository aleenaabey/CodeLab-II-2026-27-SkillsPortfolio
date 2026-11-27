import os
import json
import random
from datetime import *
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk


# -------------------- Light Warm Golden Theme & Fonts --------------------

BG_COLOR = "#2b1b0e"         # Fallback outer colour
CARD_COLOR = "#fff9ed"       # Bright warm ivory main card
STAGE_BOX_BG = "#ffffff"     # Clean white inner joke box
ENTRY_BG = "#fff3d6"         # Soft champagne input box
BORDER_OUTER = "#b45309"     # Rich amber outer border
BORDER_INNER = "#f59e0b"     # Bright golden inner border

GOLD_COLOR = "#fbbf24"       # Warm gold button
EMERALD_COLOR = "#34d399"    # Fresh mint-green button
SKY_COLOR = "#38bdf8"        # Bright sky-blue button
CORAL_COLOR = "#fb7185"      # Coral red (Quit / Reset)
AMBER_COLOR = "#f59e0b"      # Warm amber

TITLE_COLOR = "#92400e"      # Deep bronze-gold title
DARK_TEXT = "#1e293b"        # Crisp dark text on light background
PUNCH_COLOR = "#7c3aed"      # Rich purple for punchline
SUBTEXT_COLOR = "#475569"    # Clean slate grey text
WHITE_TEXT = "#ffffff"       # White text for dark/coral buttons

TITLE_FONT = "Georgia"       # Stylish serif font for headings & jokes
UI_FONT = "Verdana"          # Clean crisp font for buttons & labels


# -------------------- File Paths --------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JOKES_FILE = os.path.join(BASE_DIR, "randomJokes.txt")
STATS_FILE = os.path.join(BASE_DIR, "joke_stats.json")


# -------------------- Application Variables --------------------

jokes = []
current_joke = []
viewed_jokes = []
seq_index = -1
active_page = "joke"

bg_labels = []
icon_refs = []
last_size = (0, 0)


# -------------------- Read Jokes Text File --------------------

def load_jokes():
    if not os.path.exists(JOKES_FILE):
        messagebox.showerror("File Error", "randomJokes.txt could not be found.")
        return []

    loaded = []
    with open(JOKES_FILE, "r", encoding="utf-8") as file_handler:
        lines = file_handler.readlines()
        for line in lines:
            clean = line.rstrip()
            if "?" in clean:
                parts = clean.split("?", 1)
                setup = parts[0].strip() + "?"
                punchline = parts[1].strip()
                loaded.append([setup, punchline])
    return loaded


jokes = load_jokes()                # It read the jokes form the text fiel and will split at ?


# -------------------- JSON File Handling for Joke Stats --------------------

def create_default_stats():    # create_default_stats() It creates the starting dictionary for the joke stats
    today_now = datetime.now()
    return {
        "total_jokes_told": 0,
        "last_played": f"{today_now:%d %B %Y}",
        "category_counts": {
            "Why Jokes": 0,
            "What Jokes": 0,
            "Other Jokes": 0
        }
    }


def load_stats():       # load_stats() IT make the joke_stats,json file to read or make a new file if it is missing
    if not os.path.exists(STATS_FILE):
        data = create_default_stats()
        with open(STATS_FILE, "w", encoding="utf-8") as file_handler:
            json.dump(data, file_handler, indent=4)
        return data

    with open(STATS_FILE, "r", encoding="utf-8") as file_handler:
        return json.load(file_handler)


def save_stats():       # save_stats()  It will give us a updated joke that counts into joke_stats.json
    with open(STATS_FILE, "w", encoding="utf-8") as file_handler:
        json.dump(stats, file_handler, indent=4)


stats = load_stats()


# -------------------- Main Window --------------------

root = Tk()
root.title("Alexa - Tell Me a Joke")
root.geometry("920x600")
root.minsize(860, 540)
root.resizable(True, True)
root.configure(bg=BG_COLOR)


# -------------------- Load & Resize Button Icons --------------------

def load_icon(prefix_list, size=20):               #  it load and resize the png icons from the folder
    for filename in os.listdir(BASE_DIR):
        lower = filename.lower()
        if lower.endswith(".png"):
            for prefix in prefix_list:
                if lower.startswith(prefix):
                    img = Image.open(os.path.join(BASE_DIR, filename)).resize((size, size))
                    photo = ImageTk.PhotoImage(img)
                    icon_refs.append(photo)
                    return photo
    return None


header_icon = load_icon(["app_icon", "joke_icon"], 22)
joke_icon = load_icon(["joke_icon"], 20)
punchline_icon = load_icon(["punchline_ico", "punchline_icon"], 20)
next_icon = load_icon(["next_icon"], 20)
help_icon = load_icon(["questionmark", "help_icon"], 18)
quit_icon = load_icon(["quit_icon"], 20)


# -------------------- Load & Resize Outer Background Image --------------------

original_bg = None
for filename in os.listdir(BASE_DIR):
    lower = filename.lower()
    if lower.endswith((".png", ".jpg", ".jpeg", ".webp")):
        if lower.startswith(("alexa_bg", "comedy_stage", "joke_bg")):
            original_bg = Image.open(os.path.join(BASE_DIR, filename)).convert("RGB")
            break

if original_bg is not None:
    bg_photo = ImageTk.PhotoImage(original_bg.resize((920, 600)))
else:
    bg_photo = None


def add_background(frame):                 # add_background(frame) It wil pu the alexa_bg.png image behind the frame
    if original_bg is not None:
        lbl = Label(frame, image=bg_photo, bd=0)
        lbl.image = bg_photo
    else:
        lbl = Label(frame, bg=BG_COLOR, bd=0)
    lbl.place(x=0, y=0, relwidth=1, relheight=1)
    bg_labels.append(lbl)


def resize_all(event):          # resize_all() It resize the background and text when the window gets changed
    global bg_photo, last_size

    if event.widget != root or event.width < 820 or event.height < 500:
        return

    w = event.width
    h = event.height
    if (w, h) == last_size:
        return
    last_size = (w, h)

    if original_bg is not None:
        resized_bg = original_bg.resize((w, h))
        bg_photo = ImageTk.PhotoImage(resized_bg)
        for lbl in bg_labels:
            lbl.config(image=bg_photo)
            lbl.image = bg_photo

    # Scale fonts cleanly when window is maximized or minimized
    scale = min(w / 920, h / 600)
    if scale < 1.0:
        scale = 1.0
    if scale > 1.55:
        scale = 1.55

    wrap_px = int(w * 0.68)

    joke_heading.config(font=(TITLE_FONT, int(18 * scale), "bold"))
    add_nav_btn.config(font=(UI_FONT, int(9 * scale), "bold"))
    search_nav_btn.config(font=(UI_FONT, int(9 * scale), "bold"))
    stats_nav_btn.config(font=(UI_FONT, int(9 * scale), "bold"))
    inst_btn.config(font=(UI_FONT, int(9 * scale), "bold"))

    date_lbl.config(font=(UI_FONT, int(9 * scale), "bold"))
    viewed_lbl.config(font=(UI_FONT, int(9 * scale), "bold"))
    joke_counter.config(font=(UI_FONT, int(9 * scale), "bold"))

    setup_label.config(font=(TITLE_FONT,  int(19 * scale), "bold"), wraplength=wrap_px)
                             
    punchline_label.config(font=(TITLE_FONT, int(16 * scale), "italic"), wraplength=wrap_px)

    counter_check.config(font=(UI_FONT, int(9 * scale)))
    mode_lbl.config(font=(UI_FONT, int(9 * scale), "bold"))
    rand_rb.config(font=(UI_FONT, int(9 * scale)))
    seq_rb.config(font=(UI_FONT, int(9 * scale)))
    filter_lbl.config(font=(UI_FONT, int(9 * scale), "bold"))
    filter_menu.config(font=(UI_FONT, int(9 * scale), "bold"))

    tell_button.config(font=(UI_FONT, int(9 * scale), "bold"))
    reveal_button.config(font=(UI_FONT, int(9 * scale), "bold"))
    next_button.config(font=(UI_FONT, int(9 * scale), "bold"))
    quit_button.config(font=(UI_FONT, int(9 * scale), "bold"))

    browse_title_lbl.config(font=(TITLE_FONT, int(17 * scale), "bold"))
    search_lbl.config(font=(UI_FONT, int(9 * scale), "bold"))
    search_entry.config(font=(UI_FONT, int(9 * scale)))
    search_btn.config(font=(UI_FONT, int(9 * scale), "bold"))
    show_all_btn.config(font=(UI_FONT, int(9 * scale), "bold"))
    browse_text.config(font=(UI_FONT, int(9 * scale)))
    browse_back_btn.config(font=(UI_FONT, int(9 * scale), "bold"))

    add_title_lbl.config(font=(TITLE_FONT, int(17 * scale), "bold"))
    add_setup_lbl.config(font=(UI_FONT, int(10 * scale), "bold"))
    add_setup_entry.config(font=(UI_FONT, int(10 * scale)))
    add_punch_lbl.config(font=(UI_FONT, int(10 * scale), "bold"))
    add_punch_entry.config(font=(UI_FONT, int(10 * scale)))
    add_save_btn.config(font=(UI_FONT, int(10 * scale), "bold"))
    add_back_btn.config(font=(UI_FONT, int(10 * scale), "bold"))

    stats_title_lbl.config(font=(TITLE_FONT, int(17 * scale), "bold"))
    stats_text.config(font=(UI_FONT, int(10 * scale)))
    stats_reset_btn.config(font=(UI_FONT, int(9 * scale), "bold"))
    stats_back_btn.config(font=(UI_FONT, int(9 * scale), "bold"))


# -------------------- Frame Switching --------------------

def switch_to_frame(frame, page_name):       # switch_to_frame() it raises the selected frame to the front 
    global active_page
    active_page = page_name
    frame.tkraise()


# -------------------- Clean Light Box Helper (Nested Frames) --------------------

def create_styled_box(parent_frame, rw, rh):              # create_styled_box(parent_frame, rw, rh) This creat a double border car by using the frames     
    outer = Frame(parent_frame, 
                  bg=BORDER_OUTER, 
                  padx=3, pady=3)
    outer.place(relx=0.5,
                 rely=0.5, 
                 anchor=CENTER, 
                 relwidth=rw, 
                 relheight=rh)

    inner_border = Frame(outer, 
                         bg=BORDER_INNER, 
                         padx=2, pady=2)
    inner_border.pack(fill=BOTH, expand=YES)

    card = Frame(inner_border, 
                 bg=CARD_COLOR)
    card.pack(fill=BOTH, expand=YES)
    return card


# -------------------- Instructions Popup --------------------

def open_instructions():    # open_instructions() It open the help popup window with its instructions
    inst_win = Toplevel(root)
    inst_win.title("Instructions")
    inst_win.geometry("450x280")
    inst_win.resizable(0, 0)
    inst_win.configure(bg=BORDER_INNER, padx=2, pady=2)

    inner = Frame(inst_win, 
                  bg=CARD_COLOR)
    inner.pack(fill=BOTH, expand=YES)

    Label(
        inner,
        text="How to Use Alexa Joke Studio",
        font=(TITLE_FONT, 14, "bold"),
        bg=CARD_COLOR,
        fg=TITLE_COLOR
    ).pack(pady=(16, 10))

    Label(
        inner,
        text=(
            "1. Click 'Alexa tell me a Joke' to get a setup.\n"
            "2. Click 'Show Punchline' to reveal the answer.\n"
            "3. Choose Random or In Order + Category filter.\n"
            "4. Use 'Add Joke', 'Search', or 'Stats' in the top bar.\n"
            "5. Shortcuts: Space = Next Joke | Enter = Punchline."
        ),
        font=(UI_FONT, 9),
        bg=CARD_COLOR,
        fg=DARK_TEXT,
        justify=LEFT
    ).pack(padx=20, pady=5)

    Button(
        inner,
        text="Close",
        font=(UI_FONT, 9, "bold"),
        bg=GOLD_COLOR,
        fg=DARK_TEXT,
        width=12,
        pady=4,
        command=inst_win.destroy
    ).pack(pady=15)


# -------------------- Joke Filtering & Display Functions --------------------

def get_filtered_jokes():   # get_filtered_jokes() It filters the jokes by Why,What and Other
    category = filter_var.get()
    if category == "All Jokes":
        return jokes

    filtered = []
    for item in jokes:
        lower_setup = item[0].lower()
        if category == "Why Jokes" and lower_setup.startswith("why"):
            filtered.append(item)
        elif category == "What Jokes" and lower_setup.startswith("what"):
            filtered.append(item)
        elif category == "Other Jokes":
            if not lower_setup.startswith("why") and not lower_setup.startswith("what"):
                filtered.append(item)
    return filtered


def get_joke_category(setup_text):      # get_joke_category() it will check what category the joke belongs to
    lower_setup = setup_text.lower()
    if lower_setup.startswith("why"):
        return "Why Jokes"
    elif lower_setup.startswith("what"):
        return "What Jokes"
    else:
        return "Other Jokes"


def on_category_change(selected_value):    #on_category_change() It resets the order of index when the category gets change
    global seq_index
    seq_index = -1
    update_counter_display()


def tell_joke():              # the tell_joke is used to pick a random or ordered joke 
    global current_joke, seq_index

    pool = get_filtered_jokes()
    if len(pool) == 0:
        messagebox.showwarning("No Jokes", "No jokes found in this category.")
        return

    if mode_var.get() == "Order":
        seq_index = (seq_index + 1) % len(pool)
        new_joke = pool[seq_index]
    else:
        new_joke = random.choice(pool)
        if len(pool) > 1:
            while new_joke == current_joke:
                new_joke = random.choice(pool)

    current_joke = new_joke
    if current_joke[0] not in viewed_jokes:
        viewed_jokes.append(current_joke[0])

    # Update JSON stats
    stats["total_jokes_told"] += 1
    cat = get_joke_category(current_joke[0])
    stats["category_counts"][cat] += 1
    today_now = datetime.now()
    stats["last_played"] = f"{today_now:%d %B %Y}"
    save_stats()

    setup_label.config(text=current_joke[0])
    punchline_label.config(text="")
    update_counter_display()


def show_punchline():      # show_punchline() This displays the punchline of the question that will show in the screen(Answer of the question)
    if len(current_joke) == 0:
        messagebox.showinfo("Alexa Joke Studio", "Please click 'Alexa tell me a Joke' first!")
    else:
        punchline_label.config(text=current_joke[1])


def next_joke():   # next_joke() It will call th tell_joke to show up the another joke
    tell_joke()


def update_counter_display():      # update_counter_display()  It will update the viewed counts and the joke number
    pool = get_filtered_jokes()
    viewed_lbl.config(text="Viewed: " + str(len(viewed_jokes)) + "/" + str(len(jokes)))

    if show_counter_var.get() == 1:
        if len(current_joke) == 0 or current_joke not in pool:
            joke_counter.config(text="Joke 0 of " + str(len(pool)))
        else:
            num = pool.index(current_joke) + 1
            joke_counter.config(text="Joke " + str(num) + " of " + str(len(pool)))
    else:
        joke_counter.config(text="")


def quit_app():              # quit_app()  it will ask you yes or no before you try to close the app
    answer = messagebox.askyesno("Quit", "Are you sure you want to exit?")
    if answer:
        root.destroy()


# -------------------- Browse & Search Jokes Functions --------------------

def open_browse_screen():                      # open_brwose_screen() It opens the search page and will show up all the jokes over there 
    search_entry.delete(0, END)
    show_all_jokes_in_box()
    switch_to_frame(browse_frame, "browse")


def show_all_jokes_in_box():    #  show_all_jokes_in_box() It will print every joke into the text box
    browse_text.config(state=NORMAL)
    browse_text.delete("1.0", "end")

    count = 1
    for item in jokes:
        browse_text.insert(END, str(count) + ". " + item[0] + "\n")
        browse_text.insert(END, "   -> " + item[1] + "\n")
        browse_text.insert(END, "--------------------------------------------------\n")
        count += 1

    browse_text.config(state=DISABLED)


def search_jokes(event=None):       # search_jokes() This will filter out the jokes that will match from the typed keyword
    keyword = search_entry.get().strip().lower()
    if keyword == "":
        show_all_jokes_in_box()
        return

    browse_text.config(state=NORMAL)
    browse_text.delete("1.0", "end")

    count = 1
    found = 0
    for item in jokes:
        if keyword in item[0].lower() or keyword in item[1].lower():
            browse_text.insert(END, str(count) + ". " + item[0] + "\n")
            browse_text.insert(END, "   -> " + item[1] + "\n")
            browse_text.insert(END, "--------------------------------------------------\n")
            found += 1
        count += 1

    if found == 0:
        browse_text.insert(END, "No jokes matched '" + keyword + "'.\n")

    browse_text.config(state=DISABLED)


# -------------------- Add New Joke to Text File (Slide 143) --------------------

def open_add_screen():                # open_add_screen()  It will clesr out the text boxes and switch up to add a joke frame 
    add_setup_entry.delete(0, END)
    add_punch_entry.delete(0, END)
    switch_to_frame(add_frame, "add")
    add_setup_entry.focus()


def save_new_joke():       # save_new_joke() It is can add up a new joke to randomJoke.txt
    global jokes

    setup = add_setup_entry.get().strip()
    punch = add_punch_entry.get().strip()

    if setup == "" or punch == "":
        messagebox.showwarning("Missing Info", "Please enter both a setup and a punchline.")
        return

    if not setup.endswith("?"):
        setup = setup + "?"

    needs_newline = False
    if os.path.exists(JOKES_FILE):
        with open(JOKES_FILE, "r", encoding="utf-8") as f_check:
            content = f_check.read()
            if len(content) > 0 and not content.endswith("\n"):
                needs_newline = True

    with open(JOKES_FILE, "a", encoding="utf-8") as file_handler:
        if needs_newline:
            file_handler.write("\n" + setup + punch + "\n")
        else:
            file_handler.write(setup + punch + "\n")

    jokes = load_jokes()
    update_counter_display()
    messagebox.showinfo("Joke Added", "Your new joke was saved to randomJokes.txt!")
    switch_to_frame(joke_frame, "joke")


# -------------------- JSON Stats Screen Functions --------------------

def open_stats_screen():            # open_status_screen() It will show us the total and category counts from json
    global stats
    stats = load_stats()

    stats_text.config(state=NORMAL)
    stats_text.delete("1.0", "end")

    stats_text.insert(END, "ALEXA JOKE STUDIO - SAVED JSON ANALYTICS\n")
    stats_text.insert(END, "==================================================\n\n")
    stats_text.insert(END, "Total Jokes in Dataset  : " + str(len(jokes)) + "\n")
    stats_text.insert(END, "Total Jokes Told (All)  : " + str(stats["total_jokes_told"]) + "\n")
    stats_text.insert(END, "Viewed This Session     : " + str(len(viewed_jokes)) + "\n")
    stats_text.insert(END, "Last Played Date        : " + str(stats["last_played"]) + "\n\n")
    stats_text.insert(END, "Jokes Told by Category:\n")
    stats_text.insert(END, "--------------------------------------------------\n")

    for cat_name, cat_total in stats["category_counts"].items():
        stats_text.insert(END, "  " + cat_name + " : " + str(cat_total) + "\n")

    stats_text.config(state=DISABLED)
    switch_to_frame(stats_frame, "stats")


def reset_stats():             # reset_stats() It will rest all counts in joke_stats.json file back to zero(clear out th previous message)
    global stats
    if messagebox.askyesno("Reset Stats", "Reset all saved joke statistics in joke_stats.json?"):
        stats = create_default_stats()
        save_stats()
        open_stats_screen()


# -------------------- Keyboard Event Handler --------------------
 
def handle_keypress(event):       # handle_keypress() It will give a space for a next joke,and enter for punchline
    if active_page == "joke":
        if event.keysym == "space":
            tell_joke()
        elif event.keysym == "Return":
            show_punchline()


# =========================================================
# FRAME 1: MAIN JOKE STUDIO SCREEN
# =========================================================
joke_frame = Frame(root, bg=BG_COLOR)
joke_frame.place(x=0, y=0, 
                 relwidth=1, 
                 relheight=1)
add_background(joke_frame)

joke_card = create_styled_box(joke_frame, 0.88, 0.84)

# Top Header Bar
joke_top = Frame(joke_card, 
                 bg=CARD_COLOR)
joke_top.pack(fill=X, padx=26, 
              pady=(18, 4))

title_group = Frame(joke_top, 
                    bg=CARD_COLOR)
title_group.pack(side=LEFT)

if header_icon is not None:
    badge = Label(title_group, 
                  image=header_icon, 
                  bg=GOLD_COLOR, 
                  padx=6, pady=4)
    badge.image = header_icon
    badge.pack(side=LEFT, 
               padx=(0, 10))

joke_heading = Label(
    title_group,
    text="ALEXA JOKE STUDIO",
    font=(TITLE_FONT, 18, "bold"),
    bg=CARD_COLOR,
    fg=TITLE_COLOR
)
joke_heading.pack(side=LEFT)

top_btns = Frame(joke_top, bg=CARD_COLOR)
top_btns.pack(side=RIGHT)

add_nav_btn = Button(
    top_btns,
    text="+ Add Joke",
    font=(UI_FONT, 9, "bold"),
    bg=EMERALD_COLOR,
    fg=DARK_TEXT,
    padx=9,
    pady=4,
    cursor="hand2",
    command=open_add_screen
)
add_nav_btn.pack(side=LEFT, padx=3)

search_nav_btn = Button(
    top_btns,
    text="Search",
    font=(UI_FONT, 9, "bold"),
    bg=SKY_COLOR,
    fg=DARK_TEXT,
    padx=9,
    pady=4,
    cursor="hand2",
    command=open_browse_screen
)
search_nav_btn.pack(side=LEFT, padx=3)

stats_nav_btn = Button(
    top_btns,
    text="Stats",
    font=(UI_FONT, 9, "bold"),
    bg=AMBER_COLOR,
    fg=DARK_TEXT,
    padx=9,
    pady=4,
    cursor="hand2",
    command=open_stats_screen
)
stats_nav_btn.pack(side=LEFT, padx=3)

inst_btn = Button(
    top_btns,
    text=" Help" if help_icon else "Help",
    image=help_icon if help_icon else "",
    compound=LEFT if help_icon else NONE,
    font=(UI_FONT, 9, "bold"),
    bg=GOLD_COLOR,
    fg=DARK_TEXT,
    padx=9,
    pady=4,
    cursor="hand2",
    command=open_instructions
)
inst_btn.pack(side=LEFT, padx=3)

# Date & Counters Sub-bar
sub_bar = Frame(joke_card, bg=CARD_COLOR)
sub_bar.pack(fill=X, padx=26, pady=(0, 8))

today = datetime.now()
date_lbl = Label(
    sub_bar,
    text=f"{today:%A, %d %B %Y}",
    font=(UI_FONT, 9, "bold"),
    bg=CARD_COLOR,
    fg=SUBTEXT_COLOR
)
date_lbl.pack(side=LEFT)

counter_right = Frame(sub_bar, bg=CARD_COLOR)
counter_right.pack(side=RIGHT)

viewed_lbl = Label(
    counter_right,
    text="Viewed: 0/" + str(len(jokes)),
    font=(UI_FONT, 9, "bold"),
    bg=CARD_COLOR,
    fg=TITLE_COLOR
)
viewed_lbl.pack(side=LEFT, padx=(0, 14))

joke_counter = Label(
    counter_right,
    text="Joke 0 of " + str(len(jokes)),
    font=(UI_FONT, 9, "bold"),
    bg=CARD_COLOR,
    fg="#059669"
)
joke_counter.pack(side=LEFT)

display_border = Frame(joke_card, 
                       bg=BORDER_INNER, 
                       padx=2, pady=2)
display_border.pack(fill=BOTH, 
                    expand=YES, 
                    padx=26, pady=6)

display_box = Frame(display_border, 
                    bg=STAGE_BOX_BG, 
                    padx=24, pady=20)
display_box.pack(fill=BOTH, 
                 expand=YES)

setup_label = Label(
    display_box,
    text="Click 'Alexa tell me a Joke' to get started!",
    font=(TITLE_FONT, 19, "bold"),
    bg=STAGE_BOX_BG,
    fg=DARK_TEXT,
    wraplength=600,
    justify=CENTER
)
setup_label.pack(expand=YES, pady=(14, 6))

punchline_label = Label(
    display_box,
    text="",
    font=(TITLE_FONT, 16, "italic"),
    bg=STAGE_BOX_BG,
    fg=PUNCH_COLOR,
    wraplength=600,
    justify=CENTER
)
punchline_label.pack(expand=YES, pady=(4, 14))

# Controls Bar: Checkbutton + Radiobuttons + OptionMenu
options_bar = Frame(joke_card, bg=CARD_COLOR)
options_bar.pack(pady=4)

show_counter_var = IntVar(value=1)
counter_check = Checkbutton(
    options_bar,
    text="Show counter",
    variable=show_counter_var,
    command=update_counter_display,
    font=(UI_FONT, 9),
    bg=CARD_COLOR,
    fg=DARK_TEXT,
    selectcolor=ENTRY_BG,
    activebackground=CARD_COLOR
)
counter_check.pack(side=LEFT, 
                   padx=(4, 12))

mode_lbl = Label(
    options_bar,
    text="Mode:",
    font=(UI_FONT, 9, "bold"),
    bg=CARD_COLOR,
    fg=TITLE_COLOR
)
mode_lbl.pack(side=LEFT, padx=(4, 2))

mode_var = StringVar(value="Random")
rand_rb = Radiobutton(
    options_bar,
    text="Random",
    variable=mode_var,
    value="Random",
    font=(UI_FONT, 9),
    bg=CARD_COLOR,
    fg=DARK_TEXT,
    selectcolor=ENTRY_BG,
    activebackground=CARD_COLOR
)
rand_rb.pack(side=LEFT, padx=2)

seq_rb = Radiobutton(
    options_bar,
    text="In Order",
    variable=mode_var,
    value="Order",
    font=(UI_FONT, 9),
    bg=CARD_COLOR,
    fg=DARK_TEXT,
    selectcolor=ENTRY_BG,
    activebackground=CARD_COLOR
)
seq_rb.pack(side=LEFT, padx=(2, 12))

filter_lbl = Label(
    options_bar,
    text="Category:",
    font=(UI_FONT, 9, "bold"),
    bg=CARD_COLOR,
    fg=TITLE_COLOR
)
filter_lbl.pack(side=LEFT, padx=(4, 4))

filter_var = StringVar(value="All Jokes")
filter_menu = OptionMenu(
    options_bar,
    filter_var,
    "All Jokes",
    "Why Jokes",
    "What Jokes",
    "Other Jokes",
    command=on_category_change
)
filter_menu.config(
    font=(UI_FONT, 9, "bold"),
    bg=ENTRY_BG,
    fg=DARK_TEXT,
    highlightthickness=1,
    highlightbackground=BORDER_INNER,
    bd=0
)
filter_menu["menu"].config(bg=STAGE_BOX_BG, 
                           
                           fg=DARK_TEXT, font=(UI_FONT, 9))
filter_menu.pack(side=LEFT)

# Buttons using grid()
button_frame = Frame(joke_card, 
                     bg=CARD_COLOR)
button_frame.pack(pady=(6, 18))

tell_button = Button(
    button_frame,
    text=" Alexa tell me a Joke" if joke_icon else "Alexa tell me a Joke",
    image=joke_icon if joke_icon else "",
    compound=LEFT if joke_icon else NONE,
    font=(UI_FONT, 9, "bold"),
    bg=GOLD_COLOR,
    fg=DARK_TEXT,
    padx=10,
    pady=7,
    cursor="hand2",
    command=tell_joke
)
tell_button.grid(row=0, column=0, padx=5, pady=4)

reveal_button = Button(
    button_frame,
    text=" Show Punchline" if punchline_icon else "Show Punchline",
    image=punchline_icon if punchline_icon else "",
    compound=LEFT if punchline_icon else NONE,
    font=(UI_FONT, 9, "bold"),
    bg=EMERALD_COLOR,
    fg=DARK_TEXT,
    padx=10,
    pady=7,
    cursor="hand2",
    command=show_punchline
)
reveal_button.grid(row=0, column=1, padx=5, pady=4)

next_button = Button(
    button_frame,
    text=" Next Joke" if next_icon else "Next Joke",
    image=next_icon if next_icon else "",
    compound=LEFT if next_icon else NONE,
    font=(UI_FONT, 9, "bold"),
    bg=SKY_COLOR,
    fg=DARK_TEXT,
    padx=10,
    pady=7,
    cursor="hand2",
    command=next_joke
)
next_button.grid(row=0, column=2, padx=5, pady=4)

quit_button = Button(
    button_frame,
    text=" Quit" if quit_icon else "Quit",
    image=quit_icon if quit_icon else "",
    compound=LEFT if quit_icon else NONE,
    font=(UI_FONT, 9, "bold"),
    bg=CORAL_COLOR,
    fg=WHITE_TEXT,
    padx=12,
    pady=7,
    cursor="hand2",
    command=quit_app
)
quit_button.grid(row=0, column=3, padx=5, pady=4)


# =========================================================
# FRAME 2: SEARCH / BROWSE JOKES SCREEN (Text + Scrollbar)
# =========================================================
browse_frame = Frame(root, bg=BG_COLOR)
browse_frame.place(x=0, y=0, relwidth=1, relheight=1)
add_background(browse_frame)

browse_card = create_styled_box(browse_frame, 0.88, 0.84)

browse_title_lbl = Label(
    browse_card,
    text="BROWSE & SEARCH JOKES",
    font=(TITLE_FONT, 17, "bold"),
    bg=CARD_COLOR,
    fg=TITLE_COLOR
)
browse_title_lbl.pack(side=TOP, pady=(16, 8))

search_bar = Frame(browse_card, bg=CARD_COLOR)
search_bar.pack(side=TOP, pady=(0, 8))

search_lbl = Label(
    search_bar,
    text="Keyword:",
    font=(UI_FONT, 9, "bold"),
    bg=CARD_COLOR,
    fg=DARK_TEXT
)
search_lbl.pack(side=LEFT, padx=(0, 6))

search_entry = Entry(
    search_bar,
    font=(UI_FONT, 9),
    bg=STAGE_BOX_BG,
    fg=DARK_TEXT,
    width=26
)
search_entry.pack(side=LEFT, padx=4, ipady=3)
search_entry.bind("<Return>", search_jokes)

search_btn = Button(
    search_bar,
    text="Search",
    font=(UI_FONT, 9, "bold"),
    bg=GOLD_COLOR,
    fg=DARK_TEXT,
    padx=12,
    pady=3,
    cursor="hand2",
    command=search_jokes
)
search_btn.pack(side=LEFT, padx=6)

show_all_btn = Button(
    search_bar,
    text="Show All",
    font=(UI_FONT, 9, "bold"),
    bg=SKY_COLOR,
    fg=DARK_TEXT,
    padx=12,
    pady=3,
    cursor="hand2",
    command=show_all_jokes_in_box
)
show_all_btn.pack(side=LEFT, padx=4)

browse_back_btn = Button(
    browse_card,
    text="Back to Joke Studio",
    font=(UI_FONT, 9, "bold"),
    bg=GOLD_COLOR,
    fg=DARK_TEXT,
    padx=16,
    pady=6,
    cursor="hand2",
    command=lambda: switch_to_frame(joke_frame, "joke")
)
browse_back_btn.pack(side=BOTTOM, pady=(10, 16))

browse_box = Frame(browse_card, bg=BORDER_INNER, padx=2, pady=2)
browse_box.pack(fill=BOTH, expand=YES, padx=24)

browse_scroll = Scrollbar(browse_box)
browse_scroll.pack(side=RIGHT, fill=Y)

browse_text = Text(
    browse_box,
    height=6,
    font=(UI_FONT, 9),
    bg=STAGE_BOX_BG,
    fg=DARK_TEXT,
    bd=0,
    padx=14,
    pady=10,
    yscrollcommand=browse_scroll.set,
    wrap=WORD
)
browse_text.pack(side=LEFT, fill=BOTH, expand=YES)
browse_scroll.config(command=browse_text.yview)


# =========================================================
# FRAME 3: ADD NEW JOKE SCREEN (grid() + Text File Append)
# =========================================================
add_frame = Frame(root, bg=BG_COLOR)
add_frame.place(x=0, y=0, relwidth=1, relheight=1)
add_background(add_frame)

add_card = create_styled_box(add_frame, 0.78, 0.72)

add_inner = Frame(add_card, bg=CARD_COLOR, padx=24, pady=20)
add_inner.place(relx=0.5, rely=0.5, anchor=CENTER)

add_title_lbl = Label(
    add_inner,
    text="ADD A NEW JOKE",
    font=(TITLE_FONT, 17, "bold"),
    bg=CARD_COLOR,
    fg=TITLE_COLOR
)
add_title_lbl.grid(row=0, column=0, columnspan=2, pady=(0, 18))

add_setup_lbl = Label(
    add_inner,
    text="Joke Setup (?):",
    font=(UI_FONT, 10, "bold"),
    bg=CARD_COLOR,
    fg=DARK_TEXT
)
add_setup_lbl.grid(row=1, column=0, sticky=W, pady=10, padx=(0, 12))

add_setup_entry = Entry(
    add_inner,
    font=(UI_FONT, 10),
    bg=STAGE_BOX_BG,
    fg=DARK_TEXT,
    width=36
)
add_setup_entry.grid(row=1, column=1, pady=10, ipady=4)

add_punch_lbl = Label(
    add_inner,
    text="Punchline:",
    font=(UI_FONT, 10, "bold"),
    bg=CARD_COLOR,
    fg=DARK_TEXT
)
add_punch_lbl.grid(row=2, column=0, sticky=W, pady=10, padx=(0, 12))

add_punch_entry = Entry(
    add_inner,
    font=(UI_FONT, 10),
    bg=STAGE_BOX_BG,
    fg=DARK_TEXT,
    width=36
)
add_punch_entry.grid(row=2, column=1, pady=10, ipady=4)

add_btn_row = Frame(add_inner, bg=CARD_COLOR)
add_btn_row.grid(row=3, column=0, columnspan=2, pady=(20, 4))

add_save_btn = Button(
    add_btn_row,
    text="Save Joke",
    font=(UI_FONT, 10, "bold"),
    bg=EMERALD_COLOR,
    fg=DARK_TEXT,
    padx=16,
    pady=6,
    cursor="hand2",
    command=save_new_joke
)
add_save_btn.pack(side=LEFT, padx=8)

add_back_btn = Button(
    add_btn_row,
    text="Back to Jokes",
    font=(UI_FONT, 10, "bold"),
    bg=GOLD_COLOR,
    fg=DARK_TEXT,
    padx=16,
    pady=6,
    cursor="hand2",
    command=lambda: switch_to_frame(joke_frame, "joke")
)
add_back_btn.pack(side=LEFT, padx=8)


# =========================================================
# FRAME 4: JSON STATS SCREEN (joke_stats.json)
# =========================================================
stats_frame = Frame(root, bg=BG_COLOR)
stats_frame.place(x=0, y=0, relwidth=1, relheight=1)
add_background(stats_frame)

stats_card = create_styled_box(stats_frame, 0.80, 0.78)

stats_title_lbl = Label(
    stats_card,
    text="JOKE STUDIO STATISTICS (JSON)",
    font=(TITLE_FONT, 17, "bold"),
    bg=CARD_COLOR,
    fg=TITLE_COLOR
)
stats_title_lbl.pack(side=TOP, pady=(16, 10))

stats_btn_bar = Frame(stats_card, bg=CARD_COLOR)
stats_btn_bar.pack(side=BOTTOM, pady=(10, 16))

stats_reset_btn = Button(
    stats_btn_bar,
    text="Reset Stats",
    font=(UI_FONT, 9, "bold"),
    bg=CORAL_COLOR,
    fg=WHITE_TEXT,
    padx=14,
    pady=6,
    cursor="hand2",
    command=reset_stats
)
stats_reset_btn.pack(side=LEFT, padx=6)

stats_back_btn = Button(
    stats_btn_bar,
    text="Back to Joke Studio",
    font=(UI_FONT, 9, "bold"),
    bg=GOLD_COLOR,
    fg=DARK_TEXT,
    padx=14,
    pady=6,
    cursor="hand2",
    command=lambda: switch_to_frame(joke_frame, "joke")
)
stats_back_btn.pack(side=LEFT, padx=6)

stats_box = Frame(stats_card, bg=BORDER_INNER, padx=2, pady=2)
stats_box.pack(fill=BOTH, expand=YES, padx=26)

stats_text = Text(
    stats_box,
    height=6,
    font=(UI_FONT, 10),
    bg=STAGE_BOX_BG,
    fg=DARK_TEXT,
    bd=0,
    padx=16,
    pady=14,
    wrap=WORD
)
stats_text.pack(fill=BOTH, expand=YES)


# -------------------- Bind Events & Start App --------------------
root.bind("<Configure>", resize_all)
root.bind("<Key>", handle_keypress)
switch_to_frame(joke_frame, "joke")
root.mainloop()