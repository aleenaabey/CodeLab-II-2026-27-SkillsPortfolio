"""
Exercise 3 - Student Manager (Light Purple Theme)
Manages student marks from studentMarks.txt with Core Options (1-4)
and Extension Options (5-8: Sort, Add, Delete, Update).
Note: Structure/extension logic developed with assistance from AI
(Prompt: "<insert your prompt here>").
"""

import os
from tkinter import *
from tkinter import messagebox

# Pillow for background image (same safe fallback as Exercise 1)
try:
    from PIL import ImageTk, Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

# ---------- LIGHT PURPLE THEME & CONSTANTS ----------
BG_IMAGE = "student_bg.jpg"     # Put this image in the 03- StudentManager folder
BG_COLOR = "#f3e8ff"            # Fallback soft lavender if no image is found
PANEL_COLOR = "#faf5ff"         # Light lilac card background
OUTPUT_BG = "#ffffff"           # Clean white output area
TEXT_COLOR = "#2e1065"          # Deep purple text for high readability
ACCENT_COLOR = "#7c3aed"        # Vibrant violet for headings & primary buttons
LILAC_BTN = "#ddd6fe"           # Soft lilac button for Highest / Lowest
EXT_COLOR = "#6d28d9"           # Rich royal purple for Extension buttons
DANGER_COLOR = "#e11d48"        # Rose red for Quit
FONT_NAME = "Times New Roman"

COURSEWORK_MAX = 60             # 3 coursework marks x 20
EXAM_MAX = 100
TOTAL_MAX = COURSEWORK_MAX + EXAM_MAX   # 160 total marks

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(BASE_DIR, "studentMarks.txt")
students = []

# ---------- MAIN WINDOW (AT THE TOP) ----------
root = Tk()
root.title("Student Manager")
root.geometry("920x580")
root.minsize(850, 560)
root.resizable(True, True)     # Enables both Minimize and Maximize buttons
root.config(bg=BG_COLOR)

# Load background image sized to screen so Maximize never leaves empty space
if os.path.exists(IMAGE_PATH):
    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()
    raw_img = Image.open(IMAGE_PATH).resize((screen_w, screen_h))
    bg_photo = ImageTk.PhotoImage(raw_img)
    bg_label = Label(root, image=bg_photo)
    bg_label.place(x=0, y=0)

# ---------- FILE HANDLING ----------
def load_students():
    """Read student records from studentMarks.txt into the students list."""
    students.clear()
    try:
        with open(FILE_PATH, "r", encoding="utf-8") as file:
            lines = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        messagebox.showerror("File Not Found", f"Could not find:\n{FILE_PATH}")
        return

    # First line is the student count; student records start from index 1
    for line in lines[1:]:
        parts = line.split(",")
        students.append({
            "code": int(parts[0]),
            "name": parts[1].strip(),
            "marks": [int(parts[2]), int(parts[3]), int(parts[4])],
            "exam": int(parts[5]),
        })


def save_students():
    """Save the updated students list back to studentMarks.txt."""
    with open(FILE_PATH, "w", encoding="utf-8") as file:
        file.write(f"{len(students)}\n")
        for s in students:
            m = s["marks"]
            file.write(f"{s['code']},{s['name']},{m[0]},{m[1]},{m[2]},{s['exam']}\n")


# ---------- CALCULATIONS & FORMATTING ----------
def get_coursework_total(student):
    return sum(student["marks"])


def get_overall_mark(student):
    return get_coursework_total(student) + student["exam"]


def get_percentage(student):
    return (get_overall_mark(student) / TOTAL_MAX) * 100


def get_grade(percent):
    if percent >= 70:
        return "A"
    elif percent >= 60:
        return "B"
    elif percent >= 50:
        return "C"
    elif percent >= 40:
        return "D"
    return "F"


def format_student(student):
    pct = get_percentage(student)
    return (
        f"Name:               {student['name']}\n"
        f"Student Number:     {student['code']}\n"
        f"Coursework Total:   {get_coursework_total(student)} / {COURSEWORK_MAX}\n"
        f"Exam Mark:          {student['exam']} / {EXAM_MAX}\n"
        f"Overall Percentage: {pct:.1f}%\n"
        f"Grade:              {get_grade(pct)}\n"
    )


def format_student_list(student_list):
    if not student_list:
        return "No student records to display."
    output = ""
    for s in student_list:
        output += format_student(s) + ("-" * 42) + "\n"
    avg_pct = sum(get_percentage(s) for s in student_list) / len(student_list)
    output += f"\nNumber of students: {len(student_list)}\n"
    output += f"Average percentage: {avg_pct:.1f}%\n"
    return output


def show_output(text):
    """Display text inside the read-only output box."""
    output_box.config(state=NORMAL)
    output_box.delete("1.0", END)
    output_box.insert(END, text)
    output_box.config(state=DISABLED)


# ---------- SEARCH HELPERS ----------
def find_students(query):
    """Return students matching an exact student number or partial name."""
    query = query.strip().lower()
    return [
        s for s in students
        if query == str(s["code"]) or query in s["name"].lower()
    ]


def get_single_student():
    """Find exactly one student from the search box (used for Delete / Update)."""
    query = search_entry.get().strip()
    if not query:
        messagebox.showwarning("Search Required",
                               "Type a student name or number in the search box first.")
        return None

    matches = find_students(query)
    if not matches:
        messagebox.showinfo("Not Found", f"No student matches '{query}'.")
        return None
    if len(matches) > 1:
        names = ", ".join(s["name"] for s in matches)
        messagebox.showinfo("Be More Specific",
                            f"Multiple students match '{query}':\n{names}")
        return None
    return matches[0]


# ---------- CORE MENU ACTIONS (1 - 4) ----------
def view_all():
    show_output(format_student_list(students))


def view_individual():
    query = search_entry.get().strip()
    if not query:
        messagebox.showwarning("Search Required", "Enter a student name or number first.")
        return
    matches = find_students(query)
    if not matches:
        show_output(f"No student found matching '{query}'.")
    else:
        text = "".join(format_student(s) + ("-" * 42) + "\n" for s in matches)
        show_output(text)


def show_highest():
    if not students:
        show_output("No student records loaded.")
        return
    top_mark = max(get_overall_mark(s) for s in students)
    top_students = [s for s in students if get_overall_mark(s) == top_mark]
    text = "HIGHEST OVERALL MARK\n" + ("=" * 42) + "\n"
    text += "".join(format_student(s) + "\n" for s in top_students)
    show_output(text)


def show_lowest():
    if not students:
        show_output("No student records loaded.")
        return
    low_mark = min(get_overall_mark(s) for s in students)
    low_students = [s for s in students if get_overall_mark(s) == low_mark]
    text = "LOWEST OVERALL MARK\n" + ("=" * 42) + "\n"
    text += "".join(format_student(s) + "\n" for s in low_students)
    show_output(text)


# ---------- EXTENSION 5: SORT ----------
def sort_students():
    """Open a pop-up window to choose sort field and order."""
    win = Toplevel(root)
    win.title("Sort Student Records")
    win.geometry("300x300")
    win.resizable(False, False)
    win.config(bg=PANEL_COLOR)
    win.grab_set()

    sort_by = StringVar(value="percentage")
    order = StringVar(value="desc")

    Label(win, text="Sort By:", font=(FONT_NAME, 12, "bold"),
          bg=PANEL_COLOR, fg=ACCENT_COLOR).pack(pady=(14, 4))

    for text, val in [("Name", "name"), ("Student Number", "code"), ("Overall Percentage", "percentage")]:
        Radiobutton(win, text=text, variable=sort_by, value=val,
                    font=(FONT_NAME, 10), bg=PANEL_COLOR, fg=TEXT_COLOR,
                    selectcolor=OUTPUT_BG, activebackground=PANEL_COLOR,
                    activeforeground=ACCENT_COLOR).pack(anchor=W, padx=65)

    Label(win, text="Order:", font=(FONT_NAME, 12, "bold"),
          bg=PANEL_COLOR, fg=ACCENT_COLOR).pack(pady=(12, 4))

    for text, val in [("Ascending", "asc"), ("Descending", "desc")]:
        Radiobutton(win, text=text, variable=order, value=val,
                    font=(FONT_NAME, 10), bg=PANEL_COLOR, fg=TEXT_COLOR,
                    selectcolor=OUTPUT_BG, activebackground=PANEL_COLOR,
                    activeforeground=ACCENT_COLOR).pack(anchor=W, padx=65)

    def apply_sort():
        if sort_by.get() == "name":
            key_fn = lambda s: s["name"].lower()
        elif sort_by.get() == "code":
            key_fn = lambda s: s["code"]
        else:
            key_fn = get_percentage

        sorted_list = sorted(students, key=key_fn, reverse=(order.get() == "desc"))
        show_output(format_student_list(sorted_list))
        win.destroy()

    Button(win, text="Apply Sort", width=14, font=(FONT_NAME, 10, "bold"),
           bg=ACCENT_COLOR, fg="white", relief=FLAT, pady=5,
           command=apply_sort).pack(pady=16)


# ---------- EXTENSIONS 6 & 8: ADD / UPDATE ----------
def open_student_form(existing=None):
    """Shared pop-up form for adding a new student or updating an existing one."""
    win = Toplevel(root)
    win.title("Update Student" if existing else "Add Student")
    win.geometry("380x340")
    win.resizable(False, False)
    win.config(bg=PANEL_COLOR)
    win.grab_set()

    fields = [
        "Student Number (1000-9999):",
        "Student Name:",
        "Coursework 1 (0-20):",
        "Coursework 2 (0-20):",
        "Coursework 3 (0-20):",
        "Exam Mark (0-100):",
    ]
    entries = []
    for row, label_text in enumerate(fields):
        Label(win, text=label_text, font=(FONT_NAME, 10, "bold"),
              bg=PANEL_COLOR, fg=TEXT_COLOR).grid(row=row, column=0, padx=14, pady=8, sticky=W)
        entry = Entry(win, font=(FONT_NAME, 10), width=20,
                      bg=OUTPUT_BG, fg=TEXT_COLOR, relief=SOLID, bd=1)
        entry.grid(row=row, column=1, padx=10, pady=8)
        entries.append(entry)

    if existing:
        prefill = [existing["code"], existing["name"], *existing["marks"], existing["exam"]]
        for entry, val in zip(entries, prefill):
            entry.insert(0, str(val))

    
    def save_form():
        try:
            code = int(code_entry.get().strip())
            name = name_entry.get().strip()
            cw1 = int(cw1_entry.get().strip())
            cw2 = int(cw2_entry.get().strip())
            cw3 = int(cw3_entry.get().strip())
            exam = int(exam_entry.get().strip())
        except ValueError:
            messagebox.showerror("Invalid Input",
                                 "Student number and all marks must be whole numbers.",
                                 parent=win)
            return

        if not 1000 <= code <= 9999:
            messagebox.showerror("Invalid Input", "Student number must be 1000–9999.", parent=win)
            return
        if not name or "," in name:
            messagebox.showerror("Invalid Input", "Enter a valid name (no commas).", parent=win)
            return
        if any(not 0 <= m <= 20 for m in marks):
            messagebox.showerror("Invalid Input", "Coursework marks must be 0–20.", parent=win)
            return
        if not 0 <= exam <= EXAM_MAX:
            messagebox.showerror("Invalid Input", "Exam mark must be 0–100.", parent=win)
            return

        for other in students:
            if other["code"] == code and other is not existing:
                messagebox.showerror("Duplicate Code", "That student number already exists.", parent=win)
                return

        if existing:
            existing.update({"code": code, "name": name, "marks": marks, "exam": exam})
            status_msg = "Student record updated."
            target = existing
        else:
            target = {"code": code, "name": name, "marks": marks, "exam": exam}
            students.append(target)
            status_msg = "New student record added."

        save_students()
        win.destroy()
        show_output(f"{status_msg}\n\n{format_student(target)}")

    Button(win, text="Save Record", width=16, font=(FONT_NAME, 10, "bold"),
           bg=ACCENT_COLOR, fg="white", relief=FLAT, pady=6,
           command=save_form).grid(row=6, column=0, columnspan=2, pady=18)


def add_student():
    open_student_form()


def update_student():
    student = get_single_student()
    if student:
        open_student_form(student)


# ---------- EXTENSION 7: DELETE ----------
def delete_student():
    student = get_single_student()
    if not student:
        return
    if messagebox.askyesno("Confirm Delete",
                           f"Delete {student['name']} ({student['code']})?"):
        students.remove(student)
        save_students()
        show_output(f"Deleted {student['name']} ({student['code']}).\n\n"
                    f"Students remaining: {len(students)}")

# Left menu card (floats over the background image)
menu_frame = Frame(root, bg=PANEL_COLOR, padx=16, pady=14, bd=2, relief=RIDGE)
menu_frame.pack(side=LEFT, fill=Y, padx=(16, 8), pady=16)

Label(menu_frame, text="STUDENT MANAGER", font=(FONT_NAME, 15, "bold"),
      bg=PANEL_COLOR, fg=ACCENT_COLOR).pack(pady=(0, 10))

Label(menu_frame, text="Search (name or number):", font=(FONT_NAME, 10, "bold"),
      bg=PANEL_COLOR, fg=TEXT_COLOR).pack(anchor=W)

search_entry = Entry(menu_frame, font=(FONT_NAME, 11), width=25,
                     bg=OUTPUT_BG, fg=TEXT_COLOR, relief=SOLID, bd=1)
search_entry.pack(pady=(4, 12))
search_entry.bind("<Return>", lambda event: view_individual())

menu_buttons = [
    ("1. View All Students", view_all, ACCENT_COLOR, "white"),
    ("2. View Individual", view_individual, ACCENT_COLOR, "white"),
    ("3. Highest Overall Mark", show_highest, LILAC_BTN, TEXT_COLOR),
    ("4. Lowest Overall Mark", show_lowest, LILAC_BTN, TEXT_COLOR),
    ("5. Sort Records", sort_students, EXT_COLOR, "white"),
    ("6. Add Student", add_student, EXT_COLOR, "white"),
    ("7. Delete Student", delete_student, EXT_COLOR, "white"),
    ("8. Update Student", update_student, EXT_COLOR, "white"),
    ("Quit", root.destroy, DANGER_COLOR, "white"),
]

for label, cmd, bg_c, fg_c in menu_buttons:
    Button(menu_frame, text=label, width=24, font=(FONT_NAME, 10, "bold"),
           bg=bg_c, fg=fg_c, relief=FLAT, pady=5, command=cmd).pack(pady=3)

# Right scrollable output card (floats over the background image)
output_frame = Frame(root, bg=PANEL_COLOR, padx=6, pady=6, bd=2, relief=RIDGE)
output_frame.pack(side=RIGHT, fill=BOTH, expand=True, padx=(8, 16), pady=16)

scrollbar = Scrollbar(output_frame)
scrollbar.pack(side=RIGHT, fill=Y)

output_box = Text(output_frame, font=("Consolas", 11), bg=OUTPUT_BG, fg=TEXT_COLOR,
                  padx=14, pady=12, bd=0, wrap=WORD,
                  state=DISABLED, yscrollcommand=scrollbar.set)
output_box.pack(side=LEFT, fill=BOTH, expand=True)
scrollbar.config(command=output_box.yview)

show_output("Welcome to Student Manager!\nSelect an option from the left menu.\n"
            "Tip: Use the search box for options 2, 7, and 8.")

root.mainloop()