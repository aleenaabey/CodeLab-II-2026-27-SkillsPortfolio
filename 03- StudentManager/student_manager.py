import os
import json
from datetime import *
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk


# -------------------- Emerald Ocean & Soft Mint Theme --------------------

BG_COLOR = "#042f2e"
HEADER_BG = "#042f2e"
CARD_BG = "#ecfdf5"
INNER_BG = "#f0fdfa"
BORDER_OUTER = "#0f766e"
BORDER_INNER = "#2dd4bf"

TEAL_BTN = "#0d9488"
OCEAN_BTN = "#0891b2"
EMERALD_BTN = "#059669"
AMBER_BTN = "#f59e0b"
ROSE_BTN = "#e11d48"

TEXT_DARK = "#064e3b"
TEXT_MUTED = "#0f766e"
TEXT_LIGHT = "#ffffff"

UI_FONT = "Trebuchet MS"
MONO_FONT = "Consolas"

COURSEWORK_MAX = 60
EXAM_MAX = 100
TOTAL_MAX = 160


# -------------------- File Paths & Data --------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "studentMarks.txt")
JSON_FILE = os.path.join(BASE_DIR, "student_records.json")
REPORT_FILE = os.path.join(BASE_DIR, "class_report.txt")

students = []
last_size = (0, 0)
last_view_mode = "all"


# -------------------- Calculations --------------------

def get_cw_total(student):   # get_cw_total(student) It calculates the total coursework
    return student["cw1"] + student["cw2"] + student["cw3"]


def get_overall_mark(student): # get_overall_mark(student) It will show the overall mark that is out of 160
    return get_cw_total(student) + student["exam"]


def get_percentage(student):    # get_percentage(student) It is the percentage
    return (get_overall_mark(student) / TOTAL_MAX) * 100


def get_grade(percent):   # get_grade(percent) It is the grade of the student
    if percent >= 70:
        return "A"
    elif percent >= 60:
        return "B"
    elif percent >= 50:
        return "C"
    elif percent >= 40:
        return "D"
    else:
        return "F"


# -------------------- Text & JSON File Handling (Slides 132-154) --------------------

def load_students(): # load_students() reads studentMarks.txt and stores each student in the students list
    students.clear()
    if not os.path.exists(DATA_FILE):
        messagebox.showerror("File Not Found", "Could not find studentMarks.txt")
        return

    with open(DATA_FILE, "r", encoding="utf-8") as file_handler:
        lines = file_handler.readlines()

    for line in lines[1:]:
        clean = line.rstrip()
        if clean == "":
            continue
        parts = clean.split(",")
        if len(parts) == 6:
            students.append({
                "code": int(parts[0].strip()),
                "name": parts[1].strip(),
                "cw1": int(parts[2].strip()),
                "cw2": int(parts[3].strip()),
                "cw3": int(parts[4].strip()),
                "exam": int(parts[5].strip())
            })


def save_students(): # save_students() It writes the updated student count and records back to studentMarks.txt
    with open(DATA_FILE, "w", encoding="utf-8") as file_handler:
        file_handler.write(str(len(students)) + "\n")
        for s in students:
            line = f"{s['code']},{s['name']},{s['cw1']},{s['cw2']},{s['cw3']},{s['exam']}\n"
            file_handler.write(line)

    export_to_json()


def export_to_json():    # export_to_json() It will save all student records and class average into student_records.json
    today_now = datetime.now()
    total_pct = 0
    details_list = []

    for s in students:
        pct = get_percentage(s)
        total_pct += pct
        details_list.append({
            "code": s["code"],
            "name": s["name"],
            "cw1": s["cw1"],
            "cw2": s["cw2"],
            "cw3": s["cw3"],
            "coursework_total": get_cw_total(s),
            "exam": s["exam"],
            "overall_mark": get_overall_mark(s),
            "percentage": round(pct, 1),
            "grade": get_grade(pct)
        })

    if len(students) > 0:
        avg_pct = round(total_pct / len(students), 1)
    else:
        avg_pct = 0.0

    json_data = {
        "last_updated": f"{today_now:%d %B %Y}",
        "total_students": len(students),
        "average_percentage": avg_pct,
        "Student Details": details_list
    }

    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=4)


# -------------------- Output Formatting --------------------

def format_student(student):    # format_student() It formats one student details to show on the screen
    pct = get_percentage(student)
    cw_total = get_cw_total(student)

    if show_breakdown_var.get() == 1:
        cw_line = f"Coursework Total   : {cw_total} / {COURSEWORK_MAX}  (CW1: {student['cw1']}, CW2: {student['cw2']}, CW3: {student['cw3']})\n"
    else:
        cw_line = f"Coursework Total   : {cw_total} / {COURSEWORK_MAX}\n"

    return (
        f"Student Name       : {student['name']}\n"
        f"Student Number     : {student['code']}\n"
        + cw_line +
        f"Exam Mark          : {student['exam']} / {EXAM_MAX}\n"
        f"Overall Percentage : {pct:.1f}%\n"
        f"Student Grade      : {get_grade(pct)}\n"
    )


def format_student_list(student_list):    # format_student_list() It puts all students together and adds the class summary
    if len(student_list) == 0:
        return "No student records to display."

    output = ""
    total_pct = 0
    for s in student_list:
        output += format_student(s) + ("-" * 60) + "\n"
        total_pct += get_percentage(s)

    avg_pct = total_pct / len(student_list)
    output += "\nCLASS SUMMARY\n"
    output += "=" * 60 + "\n"
    output += f"Number of Students in Class : {len(student_list)}\n"
    output += f"Average Percentage Mark     : {avg_pct:.1f}%\n"
    return output


# -------------------- Main Window Setup --------------------

root = Tk()
root.title("Student Manager System")
root.geometry("980x640")
root.minsize(900, 580)
root.resizable(True, True)
root.config(bg=BG_COLOR)


# -------------------- Load Background & Excel Graph Images (Slides 60-68) --------------------

original_bg = None
for filename in os.listdir(BASE_DIR):
    lower = filename.lower()
    if lower.endswith((".png", ".jpg", ".jpeg", ".webp")):
        if lower.startswith("student_bg"):
            original_bg = Image.open(os.path.join(BASE_DIR, filename))
            break

if original_bg is not None:
    bg_photo = ImageTk.PhotoImage(original_bg.resize((980, 640)))
    bg_label = Label(root, image=bg_photo, bd=0)
    bg_label.image = bg_photo
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
else:
    bg_photo = None

# Load user's Excel graph image (grade_graph.png / student_graph.png / graph.png)
excel_graph_img = None
for filename in os.listdir(BASE_DIR):
    lower = filename.lower()
    if lower.endswith((".png", ".jpg", ".jpeg")):
        if lower.startswith(("grade_graph", "student_graph", "graph")):
            excel_graph_img = Image.open(os.path.join(BASE_DIR, filename))
            break


def resize_bg(event):    # resize_bg() It resizes the background, excel graph, and text size when the window changes
    global bg_photo, last_size
    if event.widget != root or event.width < 400 or event.height < 300:
        return
    w = event.width
    h = event.height
    if (w, h) == last_size:
        return
    last_size = (w, h)

    if original_bg is not None:
        resized = original_bg.resize((w, h))
        bg_photo = ImageTk.PhotoImage(resized)
        bg_label.config(image=bg_photo)
        bg_label.image = bg_photo

    if excel_graph_img is not None:
        gw = max(int(w * 0.40), 260)
        gh = max(int(h * 0.56), 200)
        resized_graph = excel_graph_img.resize((gw, gh))
        graph_photo = ImageTk.PhotoImage(resized_graph)
        graph_img_lbl.config(image=graph_photo)
        graph_img_lbl.image = graph_photo

    # Scale text box & title font sizes when window is maximized
    scale = min(w / 980, h / 640)
    if scale < 1.0:
        scale = 1.0
    if scale > 1.35:
        scale = 1.35

    text_sz = int(11 * scale)
    view_text.config(font=(MONO_FONT, text_sz))
    ind_text.config(font=(MONO_FONT, text_sz + 1))
    sort_text.config(font=(MONO_FONT, text_sz))
    analytics_text.config(font=(MONO_FONT, text_sz))
    hub_title_lbl.config(font=(UI_FONT, int(15 * scale), "bold"))


# -------------------- Helpers & Summary Refresh --------------------

def switch_to_frame(frame):    # switch_to_frame() It brings the chosen frame to the front
    frame.tkraise()


def refresh_summary_cards():    # refresh_summary_cards() It updates the total, average, highest, and lowest cards
    count = len(students)
    if count == 0:
        avg_str = "0.0%"
        top_str = "None"
        low_str = "None"
    else:
        total_pct = 0
        best = students[0]
        worst = students[0]
        for s in students:
            total_pct += get_percentage(s)
            if get_overall_mark(s) > get_overall_mark(best):
                best = s
            if get_overall_mark(s) < get_overall_mark(worst):
                worst = s

        avg_str = f"{(total_pct / count):.1f}%"
        top_str = f"{best['name']} ({get_percentage(best):.1f}%)"
        low_str = f"{worst['name']} ({get_percentage(worst):.1f}%)"

    hub_total_val.config(text=str(count))
    hub_avg_val.config(text=avg_str)
    hub_top_val.config(text=top_str)
    hub_low_val.config(text=low_str)

    view_total_val.config(text=str(count))
    view_avg_val.config(text=avg_str)
    view_top_val.config(text=top_str)
    view_low_val.config(text=low_str)


def refresh_student_menus():    # refresh_student_menus() It updates the dropdown menus after add, delete, or update
    options = []
    for s in students:
        options.append(f"{s['code']} - {s['name']}")
    if len(options) == 0:
        options = ["No Students"]

    for var, menu_widget in [
        (ind_var, ind_option_menu),
        (del_var, del_option_menu),
        (upd_var, upd_option_menu)
    ]:
        menu = menu_widget["menu"]
        menu.delete(0, "end")
        for item in options:
            menu.add_command(label=item, command=lambda val=item, v=var: v.set(val))
        var.set(options[0])


def find_matching_student(query_text, dropdown_val):    # find_matching_student() It finds one student from the search box or dropdown menu
    if len(students) == 0:
        return None

    q = query_text.strip().lower()
    if q != "":
        matches = []
        for s in students:
            if q == str(s["code"]) or q in s["name"].lower():
                matches.append(s)
        if len(matches) == 0:
            messagebox.showwarning("Not Found", f"No student found matching '{query_text}'.")
            return None
        if len(matches) > 1:
            messagebox.showinfo("Multiple Matches", "More than one student matches. Please type the full name or student number.")
            return None
        return matches[0]
    else:
        selected_code = int(dropdown_val.split(" - ")[0])
        for s in students:
            if s["code"] == selected_code:
                return s
    return None


def open_help():    # open_help() It opens a popup window with instructions on how to use the app
    win = Toplevel(root)
    win.title("Instructions")
    win.geometry("460x300")
    win.resizable(0, 0)
    win.configure(bg=BORDER_INNER, padx=2, pady=2)

    inner = Frame(win, bg=CARD_BG)
    inner.pack(fill=BOTH, expand=YES)

    Label(
        inner,
        text="How to Use Student Manager",
        font=(UI_FONT, 14, "bold"),
        bg=CARD_BG,
        fg=TEXT_DARK
    ).pack(pady=(14, 8))

    Label(
        inner,
        text=(
            "1-4: View all records (filter by grade), individual lookup,\n"
            "     highest score, or lowest score.\n"
            "5: Sort records ascending/descending by %, name, or ID.\n"
            "6: Add a new student (updates studentMarks.txt & JSON).\n"
            "7-8: Select or search a student to delete or update a field.\n"
            "9: View JSON Analytics alongside your Excel graph image."
        ),
        font=(UI_FONT, 10),
        bg=CARD_BG,
        fg=TEXT_DARK,
        justify=LEFT
    ).pack(padx=18, pady=6)

    Button(
        inner,
        text="Close",
        font=(UI_FONT, 10, "bold"),
        bg=TEAL_BTN,
        fg="white",
        width=12,
        pady=4,
        command=win.destroy
    ).pack(pady=12)


# -------------------- Menu Actions (1 - 9) --------------------

def quick_search(event=None):    # quick_search() It searches from the hub and opens the individual student page
    q = hub_search_entry.get().strip()
    if q == "":
        messagebox.showwarning("Search", "Enter a student name or number first.")
        return
    ind_search_entry.delete(0, END)
    ind_search_entry.insert(0, q)
    hub_search_entry.delete(0, END)
    switch_to_frame(ind_outer_frame)
    view_individual()


def show_in_view(title, text):    # show_in_view() It clears the text box and displays the new output
    view_title_lbl.config(text=title)
    view_text.config(state=NORMAL)
    view_text.delete("1.0", "end")
    view_text.insert(END, text)
    view_text.config(state=DISABLED)
    switch_to_frame(view_outer_frame)


# 1. View All Students (with Grade Filter)
def view_all(selected_grade=None):    # view_all() It shows all student records or filters them by the chosen grade
    global last_view_mode
    last_view_mode = "all"

    chosen = view_grade_var.get()
    if chosen == "All Grades":
        filtered = students
        title_txt = "1. ALL STUDENT RECORDS"
    else:
        filtered = []
        target_letter = chosen.replace("Grade ", "")
        for s in students:
            if get_grade(get_percentage(s)) == target_letter:
                filtered.append(s)
        title_txt = f"1. STUDENT RECORDS ({chosen.upper()})"

    show_in_view(title_txt, format_student_list(filtered))


def export_text_report():    # export_text_report() It saves the formatted class report into class_report.txt
    with open(REPORT_FILE, "w", encoding="utf-8") as file_handler:
        file_handler.write("STUDENT MANAGER - CLASS REPORT\n")
        file_handler.write(f"Generated: {datetime.now():%d %B %Y}\n")
        file_handler.write("=" * 60 + "\n\n")
        file_handler.write(format_student_list(students))
    messagebox.showinfo("Report Exported", "Saved formatted report to class_report.txt!")


# 2. View Individual Student
def open_individual_frame():    # open_individual_frame() It clears old search details and opens the individual page
    ind_search_entry.delete(0, END)
    ind_text.config(state=NORMAL)
    ind_text.delete("1.0", "end")
    ind_text.config(state=DISABLED)
    ind_grade_lbl.config(text="GRADE: --", bg=TEAL_BTN)
    ind_pct_lbl.config(text="--%")
    switch_to_frame(ind_outer_frame)


def view_individual(event=None):    # view_individual() It shows the selected student details and updates the grade badge colour
    student = find_matching_student(ind_search_entry.get(), ind_var.get())
    if student is None:
        return
    ind_text.config(state=NORMAL)
    ind_text.delete("1.0", "end")
    ind_text.insert(END, format_student(student))
    ind_text.config(state=DISABLED)

    pct = get_percentage(student)
    grade = get_grade(pct)
    if grade == "A":
        col = EMERALD_BTN
    elif grade == "B":
        col = OCEAN_BTN
    elif grade == "C":
        col = AMBER_BTN
    elif grade == "D":
        col = "#f97316"
    else:
        col = ROSE_BTN

    ind_grade_lbl.config(text="GRADE " + grade, bg=col)
    ind_pct_lbl.config(text=f"{pct:.1f}% Overall")


# 3. Highest Score
def show_highest():    # show_highest() It finds and shows the student with the highest overall mark
    global last_view_mode
    if len(students) == 0:
        show_in_view("3. HIGHEST OVERALL MARK", "No student records loaded.")
        return
    last_view_mode = "high"
    best = students[0]
    for s in students:
        if get_overall_mark(s) > get_overall_mark(best):
            best = s
    show_in_view("3. STUDENT WITH HIGHEST OVERALL MARK", format_student(best))


# 4. Lowest Score
def show_lowest():    # show_lowest() It finds and shows the student with the lowest overall mark
    global last_view_mode
    if len(students) == 0:
        show_in_view("4. LOWEST OVERALL MARK", "No student records loaded.")
        return
    last_view_mode = "low"
    worst = students[0]
    for s in students:
        if get_overall_mark(s) < get_overall_mark(worst):
            worst = s
    show_in_view("4. STUDENT WITH LOWEST OVERALL MARK", format_student(worst))


def on_breakdown_toggle():    # on_breakdown_toggle() It updates the view when the CW Details checkbox is clicked
    if last_view_mode == "all":
        view_all()
    elif last_view_mode == "high":
        show_highest()
    elif last_view_mode == "low":
        show_lowest()


# 5. Sort Student Records
def sort_by_name(s):    # sort_by_name() It returns the student name for sorting
    return s["name"].lower()


def sort_by_code(s):    # sort_by_code() It returns the student code for sorting
    return s["code"]


def apply_sort():    # apply_sort() It sorts the student list ascending or descending and displays it
    if len(students) == 0:
        messagebox.showinfo("Empty", "No student records to sort.")
        return

    reverse_order = (sort_order_var.get() == "desc")
    if sort_by_var.get() == "name":
        sorted_list = sorted(students, key=sort_by_name, reverse=reverse_order)
    elif sort_by_var.get() == "code":
        sorted_list = sorted(students, key=sort_by_code, reverse=reverse_order)
    else:
        sorted_list = sorted(students, key=get_percentage, reverse=reverse_order)

    sort_text.config(state=NORMAL)
    sort_text.delete("1.0", "end")
    sort_text.insert(END, format_student_list(sorted_list))
    sort_text.config(state=DISABLED)


def open_sort_frame():    # open_sort_frame() It runs sort and opens the sort page
    apply_sort()
    switch_to_frame(sort_outer_frame)


# 6. Add Student
def open_add_frame():    # open_add_frame() It clears all entry boxes and opens the add student page
    for e in [add_code_entry, add_name_entry, add_cw1_entry, add_cw2_entry, add_cw3_entry, add_exam_entry]:
        e.delete(0, END)
    switch_to_frame(add_outer_frame)
    add_code_entry.focus()


def add_student_record():    # add_student_record() It checks all inputs, adds the new student, and saves to files
    try:
        code = int(add_code_entry.get().strip())
        name = add_name_entry.get().strip()
        cw1 = int(add_cw1_entry.get().strip())
        cw2 = int(add_cw2_entry.get().strip())
        cw3 = int(add_cw3_entry.get().strip())
        exam = int(add_exam_entry.get().strip())
    except ValueError:
        messagebox.showerror("Invalid Input", "Student number and all marks must be whole numbers.")
        return

    if code < 1000 or code > 9999:
        messagebox.showerror("Invalid Input", "Student number must be between 1000 and 9999.")
        return
    if name == "" or "," in name:
        messagebox.showerror("Invalid Input", "Enter a valid name (no commas).")
        return
    if cw1 < 0 or cw1 > 20 or cw2 < 0 or cw2 > 20 or cw3 < 0 or cw3 > 20:
        messagebox.showerror("Invalid Input", "Coursework marks must be between 0 and 20.")
        return
    if exam < 0 or exam > 100:
        messagebox.showerror("Invalid Input", "Exam mark must be between 0 and 100.")
        return

    for s in students:
        if s["code"] == code:
            messagebox.showerror("Duplicate Code", "A student with that number already exists.")
            return

    new_student = {
        "code": code,
        "name": name,
        "cw1": cw1,
        "cw2": cw2,
        "cw3": cw3,
        "exam": exam
    }
    students.append(new_student)
    save_students()
    refresh_student_menus()
    refresh_summary_cards()

    messagebox.showinfo("Success", f"Added {name} to studentMarks.txt and student_records.json!")
    view_grade_var.set("All Grades")
    view_all()


# 7. Delete Student
def open_delete_frame():    # open_delete_frame() It clears the search box and opens the delete page
    del_search_entry.delete(0, END)
    switch_to_frame(del_outer_frame)


def delete_student_record():    # delete_student_record() It asks yes or no, removes the student, and updates the files
    target = find_matching_student(del_search_entry.get(), del_var.get())
    if target is None:
        return

    confirm = messagebox.askyesno(
        "Confirm Delete",
        f"Are you sure you want to delete {target['name']} ({target['code']})?"
    )
    if confirm:
        students.remove(target)
        save_students()
        refresh_student_menus()
        refresh_summary_cards()
        del_search_entry.delete(0, END)
        messagebox.showinfo("Deleted", f"Removed {target['name']} from studentMarks.txt.")
        view_grade_var.set("All Grades")
        view_all()


# 8. Update Student (with Field Sub-Menu)
def open_update_frame():    # open_update_frame() It clears the input boxes and opens the update page
    upd_search_entry.delete(0, END)
    upd_value_entry.delete(0, END)
    switch_to_frame(upd_outer_frame)


def update_student_record():    # update_student_record() It updates the chosen field and saves back to text and json files
    target = find_matching_student(upd_search_entry.get(), upd_var.get())
    if target is None:
        return

    field = upd_field_var.get()
    raw_val = upd_value_entry.get().strip()

    if field == "Name":
        if raw_val == "" or "," in raw_val:
            messagebox.showerror("Invalid Input", "Please enter a valid name (no commas).")
            return
        target["name"] = raw_val
    else:
        try:
            val = int(raw_val)
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a whole number for the mark.")
            return

        if field in ("CW1", "CW2", "CW3"):
            if val < 0 or val > 20:
                messagebox.showerror("Invalid Input", "Coursework mark must be between 0 and 20.")
                return
            if field == "CW1":
                target["cw1"] = val
            elif field == "CW2":
                target["cw2"] = val
            else:
                target["cw3"] = val
        elif field == "Exam":
            if val < 0 or val > 100:
                messagebox.showerror("Invalid Input", "Exam mark must be between 0 and 100.")
                return
            target["exam"] = val

    save_students()
    refresh_student_menus()
    refresh_summary_cards()
    upd_value_entry.delete(0, END)
    upd_search_entry.delete(0, END)
    messagebox.showinfo("Updated", f"Updated {target['name']} in studentMarks.txt and student_records.json!")
    show_in_view(f"8. UPDATED RECORD: {target['name']}", format_student(target))


# 9. Class Analytics & Excel Graph (Slides 60-68 & 147-154)
def open_analytics():    # open_analytics() It reads student_records.json and shows analytics with the excel graph
    export_to_json()

    with open(JSON_FILE, "r", encoding="utf-8") as file:
        info = json.load(file)

    grade_counts = {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0}
    total_cw_sum = 0
    total_exam_sum = 0
    pass_count = 0

    for student in info["Student Details"]:
        g = student["grade"]
        grade_counts[g] += 1
        total_cw_sum += student["coursework_total"]
        total_exam_sum += student["exam"]
        if student["percentage"] >= 40:
            pass_count += 1

    count = info["total_students"]
    if count > 0:
        avg_cw = total_cw_sum / count
        avg_exam = total_exam_sum / count
        pass_rate = (pass_count / count) * 100
    else:
        avg_cw = 0
        avg_exam = 0
        pass_rate = 0

    report = (
        f"JSON ANALYTICS SUMMARY\n"
        f"{'=' * 36}\n"
        f"Last Updated   : {info['last_updated']}\n"
        f"Total Students : {count}\n"
        f"Class Average  : {info['average_percentage']}%\n"
        f"Avg Coursework : {avg_cw:.1f} / 60\n"
        f"Avg Exam Mark  : {avg_exam:.1f} / 100\n"
        f"Pass Rate      : {pass_rate:.1f}% ({pass_count}/{count})\n\n"
        f"GRADE COUNTS\n"
        f"{'-' * 36}\n"
    )
    for g_letter in ["A", "B", "C", "D", "F"]:
        c_val = grade_counts[g_letter]
        if c_val == 1:
            unit = "student"
        else:
            unit = "students"
        report += f"  Grade {g_letter} : {c_val} {unit}\n"

    report += "\nALL STUDENTS (FROM JSON)\n" + ("-" * 36) + "\n"
    for student in info["Student Details"]:
        report += f"{student['code']} | {student['name']:<16} | {student['percentage']:>5}% ({student['grade']})\n"

    analytics_text.config(state=NORMAL)
    analytics_text.delete("1.0", "end")
    analytics_text.insert(END, report)
    analytics_text.config(state=DISABLED)
    switch_to_frame(analytics_outer_frame)


def quit_app():    # quit_app() It asks yes or no before closing the Student Manager window
    if messagebox.askyesno("Quit", "Are you sure you want to exit Student Manager?"):
        root.destroy()


# =========================================================
# TOP HEADER BAR
# =========================================================
top_frame = Frame(root, bg=HEADER_BG, padx=22, pady=10)
top_frame.pack(side=TOP, fill=X)

Label(
    top_frame,
    text="STUDENT MANAGER SYSTEM",
    font=(UI_FONT, 18, "bold"),
    bg=HEADER_BG,
    fg=BORDER_INNER
).pack(side=LEFT)

Button(
    top_frame,
    text="Help",
    font=(UI_FONT, 10, "bold"),
    bg=AMBER_BTN,
    fg=TEXT_DARK,
    padx=14,
    pady=3,
    relief=FLAT,
    cursor="hand2",
    command=open_help
).pack(side=RIGHT, padx=(10, 0))

today = datetime.now()
Label(
    top_frame,
    text=f"{today:%A, %d %B %Y}",
    font=(UI_FONT, 11, "bold"),
    bg=HEADER_BG,
    fg="#99f6e4"
).pack(side=RIGHT, padx=12)


# =========================================================
# CENTER PAGE BUILDER & SUMMARY STRIP
# =========================================================

def make_page():    # make_page() It creates the bordered center card frame for each screen
    outer = Frame(root, bg=BORDER_OUTER, padx=3, pady=3)
    outer.place(relx=0.5, rely=0.54, anchor=CENTER, relwidth=0.88, relheight=0.86)

    inner_b = Frame(outer, bg=BORDER_INNER, padx=2, pady=2)
    inner_b.pack(fill=BOTH, expand=YES)

    card = Frame(inner_b, bg=CARD_BG, padx=22, pady=12)
    card.pack(fill=BOTH, expand=YES)
    return outer, card


def create_summary_strip(parent):    # create_summary_strip() It builds the 4 summary cards at the top
    strip = Frame(parent, bg=CARD_BG)
    strip.pack(fill=X, pady=(0, 10))

    cards = []
    specs = [
        ("TOTAL STUDENTS", TEAL_BTN),
        ("CLASS AVERAGE", OCEAN_BTN),
        ("HIGHEST SCORE", EMERALD_BTN),
        ("LOWEST SCORE", ROSE_BTN),
    ]
    for title_txt, bar_col in specs:
        box = Frame(strip, bg=INNER_BG, bd=1, relief=SOLID)
        box.pack(side=LEFT, fill=X, expand=YES, padx=4)

        Frame(box, bg=bar_col, height=5).pack(fill=X)
        Label(box, text=title_txt, font=(UI_FONT, 9, "bold"), bg=INNER_BG, fg=TEXT_MUTED).pack(pady=(5, 1))
        val_lbl = Label(box, text="--", font=(UI_FONT, 12, "bold"), bg=INNER_BG, fg=TEXT_DARK)
        val_lbl.pack(pady=(0, 5))
        cards.append(val_lbl)

    return cards[0], cards[1], cards[2], cards[3]


# =========================================================
# PAGE 0: CENTERED MENU HUB
# =========================================================
hub_outer_frame, hub_card = make_page()

hub_title_lbl = Label(
    hub_card,
    text="CLASS OVERVIEW & CONTROL CENTER",
    font=(UI_FONT, 15, "bold"),
    bg=CARD_BG,
    fg=TEXT_DARK
)
hub_title_lbl.pack(pady=(0, 6))

hub_total_val, hub_avg_val, hub_top_val, hub_low_val = create_summary_strip(hub_card)

hub_search_row = Frame(hub_card, bg=INNER_BG, padx=14, pady=7, bd=1, relief=SOLID)
hub_search_row.pack(fill=X, pady=(0, 10))

Label(
    hub_search_row,
    text="Quick Student Lookup (Name or Code):",
    font=(UI_FONT, 11, "bold"),
    bg=INNER_BG,
    fg=TEXT_DARK
).pack(side=LEFT, padx=(0, 10))

hub_search_entry = Entry(hub_search_row, 
                         font=(UI_FONT, 11), 
                         width=26, 
                         bg="#ffffff", 
                         fg=TEXT_DARK)
hub_search_entry.pack(side=LEFT, padx=6, ipady=2)
hub_search_entry.bind("<Return>", quick_search)

Button(
    hub_search_row,
    text="Find Student",
    font=(UI_FONT, 10, "bold"),
    bg=TEAL_BTN,
    fg="white",
    padx=14,
    pady=4,
    relief=FLAT,
    cursor="hand2",
    command=quick_search
).pack(side=LEFT, padx=8)

Button(
    hub_card,
    text="Quit Application",
    font=(UI_FONT, 11, "bold"),
    bg=ROSE_BTN,
    fg="white",
    width=22,
    pady=4,
    relief=FLAT,
    cursor="hand2",
    command=quit_app
).pack(side=BOTTOM, pady=(8, 0))

hub_columns = Frame(hub_card, bg=CARD_BG)
hub_columns.pack(fill=BOTH, expand=YES, pady=2)

left_col = Frame(hub_columns, 
                 bg=INNER_BG, 
                 padx=16, pady=10,
                   bd=1, relief=SOLID)
left_col.pack(side=LEFT, fill=BOTH, expand=YES, padx=(0, 8))

Label(left_col,
       text="CORE MENU", 
       font=(UI_FONT, 12, "bold"), 
       bg=INNER_BG, 
       fg=TEAL_BTN).pack(pady=(0, 6))

for txt, cmd in [
    ("1. View All Student Records", view_all),
    ("2. View Individual Student Record", open_individual_frame),
    ("3. Show Highest Overall Mark", show_highest),
    ("4. Show Lowest Overall Mark", show_lowest),
]:
    Button(
        left_col,
        text=txt,
        font=(UI_FONT, 10, "bold"),
        bg=TEAL_BTN,
        fg="white",
        pady=6,
        relief=FLAT,
        cursor="hand2",
        command=cmd
    ).pack(fill=X, pady=4)

right_col = Frame(hub_columns, bg=INNER_BG, padx=16, pady=10, bd=1, relief=SOLID)
right_col.pack(side=RIGHT, fill=BOTH, expand=YES, padx=(8, 0))

Label(right_col, text="EXTENSIONS & ANALYTICS", font=(UI_FONT, 12, "bold"), bg=INNER_BG, fg=OCEAN_BTN).pack(pady=(0, 6))

for txt, cmd, col in [
    ("5. Sort Student Records", open_sort_frame, OCEAN_BTN),
    ("6. Add a Student Record", open_add_frame, EMERALD_BTN),
    ("7. Delete a Student Record", open_delete_frame, ROSE_BTN),
    ("8. Update a Student Record", open_update_frame, AMBER_BTN),
    ("9. Class Analytics & Graph (JSON)", open_analytics, "#0f766e"),
]:
    if col == AMBER_BTN:
        fg_c = TEXT_DARK
    else:
        fg_c = "white"
    Button(
        right_col,
        text=txt,
        font=(UI_FONT, 10, "bold"),
        bg=col,
        fg=fg_c,
        pady=5,
        relief=FLAT,
        cursor="hand2",
        command=cmd
    ).pack(fill=X, pady=3)


# =========================================================
# PAGE 1: VIEW RECORDS PAGE (Filter + Export + Summary Cards)
# =========================================================
view_outer_frame, view_card = make_page()

view_header = Frame(view_card, bg=CARD_BG)
view_header.pack(fill=X, pady=(0, 8))

view_title_lbl = Label(view_header, 
                       text="1. ALL STUDENT RECORDS", 
                       font=(UI_FONT, 14, "bold"), 
                       bg=CARD_BG, 
                       fg=TEXT_DARK)
view_title_lbl.pack(side=LEFT)

Button(
    view_header,
    text="Back to Menu",
    font=(UI_FONT, 10, "bold"),
    bg=HEADER_BG,
    fg="white",
    padx=12,
    pady=4,
    relief=FLAT,
    cursor="hand2",
    command=lambda: switch_to_frame(hub_outer_frame)
).pack(side=RIGHT)

Button(
    view_header,
    text="Export .txt",
    font=(UI_FONT, 10, "bold"),
    bg=OCEAN_BTN,
    fg="white",
    padx=10,
    pady=4,
    relief=FLAT,
    cursor="hand2",
    command=export_text_report
).pack(side=RIGHT, padx=6)

view_grade_var = StringVar(value="All Grades")
grade_filter_menu = OptionMenu(
    view_header,
    view_grade_var,
    "All Grades",
    "Grade A",
    "Grade B",
    "Grade C",
    "Grade D",
    "Grade F",
    command=view_all
)
grade_filter_menu.config(font=(UI_FONT, 9, "bold"), bg=INNER_BG, fg=TEXT_DARK)
grade_filter_menu.pack(side=RIGHT, padx=6)

show_breakdown_var = IntVar(value=1)
Checkbutton(
    view_header,
    text="CW Details",
    variable=show_breakdown_var,
    command=on_breakdown_toggle,
    font=(UI_FONT, 10, "bold"),
    bg=CARD_BG,
    fg=TEXT_DARK,
    selectcolor=INNER_BG
).pack(side=RIGHT, padx=6)

view_total_val, view_avg_val, view_top_val, view_low_val = create_summary_strip(view_card)

view_box = Frame(view_card, bg=BORDER_INNER, padx=2, pady=2)
view_box.pack(fill=BOTH, expand=YES)

view_scroll = Scrollbar(view_box)
view_scroll.pack(side=RIGHT, fill=Y)

view_text = Text(
    view_box,
    font=(MONO_FONT, 11),
    bg=INNER_BG,
    fg=TEXT_DARK,
    padx=18,
    pady=14,
    bd=0,
    wrap=WORD,
    state=DISABLED,
    yscrollcommand=view_scroll.set
)
view_text.pack(side=LEFT, fill=BOTH, expand=YES)
view_scroll.config(command=view_text.yview)


# =========================================================
# PAGE 2: INDIVIDUAL RECORD PAGE (Item 2)
# =========================================================
ind_outer_frame, ind_card = make_page()

ind_header = Frame(ind_card, bg=CARD_BG)
ind_header.pack(fill=X, pady=(0, 12))

Label(ind_header, 
      text="2. VIEW INDIVIDUAL STUDENT RECORD", 
      font=(UI_FONT, 15, "bold"),
        bg=CARD_BG, 
        fg=TEXT_DARK).pack(side=LEFT)
Button(ind_header,
        text="Back to Menu", 
        font=(UI_FONT, 10, "bold"), 
        bg=HEADER_BG, 
        fg="white", 
        padx=14, pady=4, relief=FLAT, 
        cursor="hand2", 
        command=lambda: switch_to_frame(hub_outer_frame)).pack(side=RIGHT)

ind_ctrl = Frame(ind_card, bg=INNER_BG, padx=16, pady=12, bd=1, relief=SOLID)
ind_ctrl.pack(fill=X, pady=(0, 12))

Label(ind_ctrl, text="Select Student:", font=(UI_FONT, 11, "bold"), bg=INNER_BG, fg=TEXT_DARK).grid(row=0, column=0, sticky=W, pady=4)
ind_var = StringVar()
ind_option_menu = OptionMenu(ind_ctrl, ind_var, "No Students")
ind_option_menu.config(width=28, font=(UI_FONT, 10), bg=CARD_BG, fg=TEXT_DARK)
ind_option_menu.grid(row=0, column=1, padx=12, pady=4, sticky=W)

Label(ind_ctrl, text="Or Search Name/Code:", font=(UI_FONT, 11, "bold"), bg=INNER_BG, fg=TEXT_DARK).grid(row=1, column=0, sticky=W, pady=4)
ind_search_entry = Entry(ind_ctrl, width=31, font=(UI_FONT, 11), bg="#ffffff", fg=TEXT_DARK)
ind_search_entry.grid(row=1, column=1, padx=12, pady=4, sticky=W)
ind_search_entry.bind("<Return>", view_individual)

Button(ind_ctrl, text="Show Record", font=(UI_FONT, 11, "bold"), bg=TEAL_BTN, fg="white", padx=16, pady=8, relief=FLAT, cursor="hand2", command=view_individual).grid(row=0, column=2, rowspan=2, padx=14)

ind_body = Frame(ind_card, bg=CARD_BG)
ind_body.pack(fill=BOTH, expand=YES)

# Grade Badge Box on the Left
ind_badge_box = Frame(ind_body, bg=INNER_BG, padx=18, pady=24, bd=1, relief=SOLID)
ind_badge_box.pack(side=LEFT, fill=Y, padx=(0, 12))

ind_grade_lbl = Label(
    ind_badge_box,
    text="GRADE: --",
    font=(UI_FONT, 16, "bold"),
    bg=TEAL_BTN,
    fg="white",
    width=11,
    pady=12
)
ind_grade_lbl.pack(pady=(25, 14))

ind_pct_lbl = Label(
    ind_badge_box,
    text="--%",
    font=(UI_FONT, 13, "bold"),
    bg=INNER_BG,
    fg=TEXT_DARK
)
ind_pct_lbl.pack()

# Student Details on the Right
ind_box = Frame(ind_body, bg=BORDER_INNER, padx=2, pady=2)
ind_box.pack(side=RIGHT, fill=BOTH, expand=YES)

ind_text = Text(ind_box, 
                font=(MONO_FONT, 12),
                  bg=INNER_BG, 
                  fg=TEXT_DARK,
                    padx=18, pady=18, bd=0, 
                    wrap=WORD, 
                    state=DISABLED)
ind_text.pack(fill=BOTH, expand=YES)


# =========================================================
# PAGE 3: SORT RECORDS PAGE (Item 5)
# =========================================================
sort_outer_frame, sort_card = make_page()

sort_header = Frame(sort_card, bg=CARD_BG)
sort_header.pack(fill=X, pady=(0, 10))

Label(sort_header,
       text="5. SORT STUDENT RECORDS", 
       font=(UI_FONT, 15, "bold"), 
       bg=CARD_BG, 
       fg=TEXT_DARK).pack(side=LEFT)
Button(sort_header,
        text="Back to Menu",
          font=(UI_FONT, 10, "bold"), 
          bg=HEADER_BG, 
          fg="white", padx=14, pady=4,
            relief=FLAT, cursor="hand2",
              command=lambda: switch_to_frame(hub_outer_frame)).pack(side=RIGHT)

sort_ctrl = Frame(sort_card, bg=INNER_BG, padx=14, pady=10, bd=1, relief=SOLID)
sort_ctrl.pack(fill=X, pady=(0, 10))

sort_by_var = StringVar(value="percentage")
sort_order_var = StringVar(value="desc")

Label(sort_ctrl, 
      text="Sort By:", 
      font=(UI_FONT, 11, "bold"), 
      bg=INNER_BG, 
      fg=TEAL_BTN).grid(row=0, column=0, sticky=W, padx=(0, 8))
Radiobutton(sort_ctrl, 
            text="Overall Percentage", 
            variable=sort_by_var, value="percentage",
              font=(UI_FONT, 10), 
              bg=INNER_BG, 
              fg=TEXT_DARK).grid(row=0, column=1, padx=6)
Radiobutton(sort_ctrl, 
            text="Name", 
            variable=sort_by_var, value="name", font=(UI_FONT, 10),
              bg=INNER_BG, 
              fg=TEXT_DARK).grid(row=0, column=2, padx=6)
Radiobutton(sort_ctrl, 
            text="Student Number", 
            variable=sort_by_var, 
            value="code", 
            font=(UI_FONT, 10),
              bg=INNER_BG, 
              fg=TEXT_DARK).grid(row=0, column=3, padx=6)

Label(sort_ctrl, 
      text="Order:", 
      font=(UI_FONT, 11, "bold"),
        bg=INNER_BG, 
        fg=TEAL_BTN).grid(row=1, column=0, sticky=W, padx=(0, 8), pady=4)
Radiobutton(sort_ctrl, 
            text="Descending (Highest First)", 
            variable=sort_order_var, value="desc", 
            font=(UI_FONT, 10), 
            bg=INNER_BG, 
            fg=TEXT_DARK).grid(row=1, column=1, padx=6, sticky=W)
Radiobutton(sort_ctrl, 
            text="Ascending (Lowest First)", 
            variable=sort_order_var, value="asc", 
            font=(UI_FONT, 10),
              bg=INNER_BG,
            fg=TEXT_DARK).grid(row=1, column=2, padx=6, sticky=W)

Button(sort_ctrl,
        text="Apply Sort",
        font=(UI_FONT, 10, "bold"),
          bg=OCEAN_BTN, 
          fg="white", padx=16, 
          pady=6, relief=FLAT, 
          cursor="hand2", 
          command=apply_sort).grid(row=0, column=4, rowspan=2, padx=16)

sort_box = Frame(sort_card, bg=BORDER_INNER, padx=2, pady=2)
sort_box.pack(fill=BOTH, expand=YES)

sort_scroll = Scrollbar(sort_box)
sort_scroll.pack(side=RIGHT, fill=Y)

sort_text = Text(sort_box, 
                 font=(MONO_FONT, 11), 
                 bg=INNER_BG, 
                 fg=TEXT_DARK, 
                 padx=18, pady=12, 
                 bd=0, wrap=WORD, 
                 state=DISABLED, 
                 yscrollcommand=sort_scroll.set)
sort_text.pack(side=LEFT, fill=BOTH, expand=YES)
sort_scroll.config(command=sort_text.yview)


# =========================================================
# PAGE 4: ADD STUDENT PAGE (Item 6)
# =========================================================
add_outer_frame, add_card = make_page()

add_header = Frame(add_card, bg=CARD_BG)
add_header.pack(fill=X, pady=(0, 14))

Label(add_header, 
      text="6. ADD A NEW STUDENT RECORD", 
      font=(UI_FONT, 15, "bold"),
        bg=CARD_BG, 
        fg=TEXT_DARK).pack(side=LEFT)
Button(add_header, 
       text="Back to Menu",
         font=(UI_FONT, 10, "bold"), 
         bg=HEADER_BG, 
         fg="white", padx=14,
           pady=4, relief=FLAT, 
           cursor="hand2", 
           command=lambda: switch_to_frame(hub_outer_frame)).pack(side=RIGHT)

add_form = Frame(add_card, 
                 bg=INNER_BG, 
                 padx=28, pady=22, 
                 bd=1, relief=SOLID)
add_form.place(relx=0.5, rely=0.55, anchor=CENTER)

Label(add_form,
       text="Student Number (1000-9999):", 
       font=(UI_FONT, 11, "bold"), 
       bg=INNER_BG, 
       fg=TEXT_DARK).grid(row=0, column=0, sticky=W, pady=7)
add_code_entry = Entry(add_form, 
                       font=(UI_FONT, 11), 
                       width=26, 
                       bg="#ffffff", 
                       fg=TEXT_DARK)
add_code_entry.grid(row=0, column=1, padx=14, pady=7)

Label(add_form, 
      text="Student Name:", 
      font=(UI_FONT, 11, "bold"), 
      bg=INNER_BG, 
      fg=TEXT_DARK).grid(row=1, column=0, sticky=W, pady=7)
add_name_entry = Entry(add_form, 
                       font=(UI_FONT, 11), 
                       width=26, 
                       bg="#ffffff", 
                       fg=TEXT_DARK)
add_name_entry.grid(row=1, column=1, padx=14, pady=7)

Label(add_form, 
      text="Coursework 1 (0-20):", 
      font=(UI_FONT, 11, "bold"),
        bg=INNER_BG, 
        fg=TEXT_DARK).grid(row=2, column=0, sticky=W, pady=7)
add_cw1_entry = Entry(add_form, 
                      font=(UI_FONT, 11), 
                      width=26, 
                      bg="#ffffff", 
                      fg=TEXT_DARK)
add_cw1_entry.grid(row=2, column=1, padx=14, pady=7)

Label(add_form, 
      text="Coursework 2 (0-20):", 
      font=(UI_FONT, 11, "bold"), 
      bg=INNER_BG, 
      fg=TEXT_DARK).grid(row=3, column=0, sticky=W, pady=7)
add_cw2_entry = Entry(add_form, 
                      font=(UI_FONT, 11), 
                      width=26, 
                      bg="#ffffff", 
                      fg=TEXT_DARK)
add_cw2_entry.grid(row=3, column=1, padx=14, pady=7)

Label(add_form, 
      text="Coursework 3 (0-20):", 
      font=(UI_FONT, 11, "bold"), 
      bg=INNER_BG, 
      fg=TEXT_DARK).grid(row=4, column=0, sticky=W, pady=7)
add_cw3_entry = Entry(add_form, 
                      font=(UI_FONT, 11), 
                      width=26, 
                      bg="#ffffff", 
                      fg=TEXT_DARK)
add_cw3_entry.grid(row=4, column=1, padx=14, pady=7)

Label(add_form,
       text="Exam Mark (0-100):", 
       font=(UI_FONT, 11, "bold"), 
       bg=INNER_BG, 
       fg=TEXT_DARK).grid(row=5, column=0, sticky=W, pady=7)
add_exam_entry = Entry(add_form, 
                       font=(UI_FONT, 11), 
                       width=26, 
                       bg="#ffffff", 
                       fg=TEXT_DARK)
add_exam_entry.grid(row=5, column=1, padx=14, pady=7)

Button(add_form, 
       text="Save New Student", 
       font=(UI_FONT, 11, "bold"), 
       bg=TEAL_BTN, 
       fg="white",
         width=22, pady=6, 
         relief=FLAT, cursor="hand2",
           command=add_student_record).grid(row=6, column=0, columnspan=2, pady=(16, 4))


# =========================================================
# PAGE 5: DELETE STUDENT PAGE (Item 7)
# =========================================================
del_outer_frame, del_card = make_page()

del_header = Frame(del_card, bg=CARD_BG)
del_header.pack(fill=X, pady=(0, 14))

Label(del_header, 
      text="7. DELETE A STUDENT RECORD", 
      font=(UI_FONT, 15, "bold"),
        bg=CARD_BG, 
        fg=TEXT_DARK).pack(side=LEFT)
Button(del_header, 
       text="Back to Menu", 
       font=(UI_FONT, 10, "bold"), 
       bg=HEADER_BG, 
       fg="white", 
       padx=14, pady=4, 
       relief=FLAT, 
       cursor="hand2", 
       command=lambda: switch_to_frame(hub_outer_frame)).pack(side=RIGHT)

del_form = Frame(del_card, 
                 bg=INNER_BG, 
                 padx=28, pady=28, 
                 bd=1, 
                 relief=SOLID)
del_form.place(relx=0.5, rely=0.52, anchor=CENTER)

Label(del_form, 
      text="Select Student:", 
      font=(UI_FONT, 11, "bold"), 
      bg=INNER_BG, 
      fg=TEXT_DARK).grid(row=0, column=0, sticky=W, pady=8)
del_var = StringVar()
del_option_menu = OptionMenu(del_form, del_var, "No Students")
del_option_menu.config(width=28, 
                       font=(UI_FONT, 10), 
                       bg=CARD_BG, 
                       fg=TEXT_DARK)
del_option_menu.grid(row=0, column=1, padx=14, pady=8)

Label(del_form, 
      text="Or Enter Name / Code:", 
      font=(UI_FONT, 11, "bold"), 
      bg=INNER_BG, 
      fg=TEXT_DARK).grid(row=1, column=0, sticky=W, pady=8)
del_search_entry = Entry(del_form, 
                         font=(UI_FONT, 11), 
                         width=30, 
                         bg="#ffffff", 
                         fg=TEXT_DARK)
del_search_entry.grid(row=1, column=1, padx=14, pady=8)

Button(del_form, 
       text="Delete Selected Student", 
       font=(UI_FONT, 11, "bold"),
         bg=ROSE_BTN, fg="white", 
         width=24, pady=6, relief=FLAT, 
         cursor="hand2", 
         command=delete_student_record).grid(row=2, column=0, columnspan=2, pady=(18, 4))


# =========================================================
# PAGE 6: UPDATE STUDENT PAGE WITH SUB-MENU (Item 8)
# =========================================================
upd_outer_frame, upd_card = make_page()

upd_header = Frame(upd_card, bg=CARD_BG)
upd_header.pack(fill=X, pady=(0, 12))

Label(upd_header, 
      text="8. UPDATE A STUDENT RECORD", 
      font=(UI_FONT, 15, "bold"), 
      bg=CARD_BG, 
      fg=TEXT_DARK).pack(side=LEFT)
Button(upd_header, 
       text="Back to Menu", 
       font=(UI_FONT, 10, "bold"), 
       bg=HEADER_BG, 
       fg="white", padx=14, pady=4, 
       relief=FLAT, cursor="hand2", 
       command=lambda: switch_to_frame(hub_outer_frame)).pack(side=RIGHT)

upd_form = Frame(upd_card, bg=INNER_BG, padx=28, pady=20, bd=1, relief=SOLID)
upd_form.place(relx=0.5, rely=0.55, anchor=CENTER)

Label(upd_form, 
      text="Select Student:", 
      font=(UI_FONT, 11, "bold"), 
      bg=INNER_BG, 
      fg=TEXT_DARK).grid(row=0, column=0, sticky=W, pady=6)
upd_var = StringVar()
upd_option_menu = OptionMenu(upd_form, upd_var, "No Students")
upd_option_menu.config(width=28, font=(UI_FONT, 10), bg=CARD_BG, fg=TEXT_DARK)
upd_option_menu.grid(row=0, column=1, padx=14, pady=6)

Label(upd_form, 
      text="Or Enter Name / Code:", 
      font=(UI_FONT, 11, "bold"), 
      bg=INNER_BG, 
      fg=TEXT_DARK).grid(row=1, column=0, sticky=W, pady=6)
upd_search_entry = Entry(upd_form, 
                         font=(UI_FONT, 11), 
                         width=30, 
                         bg="#ffffff", 
                         fg=TEXT_DARK)
upd_search_entry.grid(row=1, column=1, padx=14, pady=6)

Label(upd_form, 
      text="Field Sub-Menu:", 
      font=(UI_FONT, 11, "bold"), 
      bg=INNER_BG, 
      fg=TEXT_DARK).grid(row=2, column=0, sticky=NW, pady=8)
upd_field_var = StringVar(value="Exam")
upd_radio_frame = Frame(upd_form, bg=INNER_BG)
upd_radio_frame.grid(row=2, column=1, sticky=W, padx=14, pady=6)

for txt, val in [
    ("Student Name", "Name"),
    ("Coursework 1 (0-20)", "CW1"),
    ("Coursework 2 (0-20)", "CW2"),
    ("Coursework 3 (0-20)", "CW3"),
    ("Exam Mark (0-100)", "Exam")
]:
    Radiobutton(upd_radio_frame, 
                text=txt, 
                variable=upd_field_var, 
                value=val, 
                font=(UI_FONT, 10), 
                bg=INNER_BG, 
                fg=TEXT_DARK).pack(anchor=W)

Label(upd_form, 
      text="Enter New Value:", 
      font=(UI_FONT, 11, "bold"), 
      bg=INNER_BG, 
      fg=TEXT_DARK).grid(row=3, column=0, sticky=W, pady=8)
upd_value_entry = Entry(upd_form, 
                        font=(UI_FONT, 11), 
                        width=30, 
                        bg="#ffffff", 
                        fg=TEXT_DARK)
upd_value_entry.grid(row=3, column=1, padx=14, pady=8)

Button(upd_form, 
       text="Save Updated Record", 
       font=(UI_FONT, 11, "bold"), 
       bg=TEAL_BTN, 
       fg="white", 
       width=24, pady=6, 
       relief=FLAT, 
       cursor="hand2", 
       command=update_student_record).grid(row=4, column=0, columnspan=2, pady=(14, 4))


# =========================================================
# PAGE 7: CLASS ANALYTICS & EXCEL GRAPH (Slides 60-68 & 147-154)
# =========================================================
analytics_outer_frame, analytics_card = make_page()

ana_header = Frame(analytics_card, bg=CARD_BG)
ana_header.pack(fill=X, pady=(0, 10))

Label(ana_header,
       text="9. CLASS ANALYTICS & EXCEL GRAPH (JSON)", 
       font=(UI_FONT, 15, "bold"),
         bg=CARD_BG,
         fg=TEAL_BTN).pack(side=LEFT)
Button(ana_header, 
       text="Back to Menu", 
       font=(UI_FONT, 10, "bold"), 
       bg=HEADER_BG, 
       fg="white", 
       padx=14, pady=4, 
       relief=FLAT, cursor="hand2", 
       command=lambda: switch_to_frame(hub_outer_frame)).pack(side=RIGHT)

ana_split = Frame(analytics_card, bg=CARD_BG)
ana_split.pack(fill=BOTH, expand=YES)

analytics_box = Frame(ana_split, bg=BORDER_INNER, padx=2, pady=2)
analytics_box.pack(side=LEFT, fill=BOTH, expand=YES, padx=(0, 8))

analytics_scroll = Scrollbar(analytics_box)
analytics_scroll.pack(side=RIGHT, fill=Y)

analytics_text = Text(analytics_box, 
                      width=38, 
                      font=(MONO_FONT, 10), 
                      bg=INNER_BG, 
                      fg=TEXT_DARK,
                        padx=14, pady=12, 
                        bd=0, wrap=WORD, 
                        state=DISABLED, 
                        yscrollcommand=analytics_scroll.set)
analytics_text.pack(side=LEFT, fill=BOTH, expand=YES)
analytics_scroll.config(command=analytics_text.yview)

# Right Panel: Displays your Excel Graph Image
graph_box = Frame(ana_split, bg=BORDER_INNER, padx=2, pady=2)
graph_box.pack(side=RIGHT, fill=BOTH, expand=YES, padx=(8, 0))

if excel_graph_img is not None:
    init_g_photo = ImageTk.PhotoImage(excel_graph_img.resize((380, 340)))
    graph_img_lbl = Label(graph_box, image=init_g_photo, bg="#ffffff")
    graph_img_lbl.image = init_g_photo
else:
    graph_img_lbl = Label(
        graph_box,
        text="Save your Excel chart image as\n'grade_graph.png'\nin the 03- StudentManager folder!",
        font=(UI_FONT, 11, "bold"),
        bg="#ffffff",
        fg=TEXT_MUTED,
        justify=CENTER,
        padx=20,
        pady=20
    )
graph_img_lbl.pack(fill=BOTH, expand=YES)


# -------------------- Start Application --------------------
root.bind("<Configure>", resize_bg)    # It binds resize, loads text and json data, opens hub, and runs the app
load_students()
export_to_json()
refresh_student_menus()
refresh_summary_cards()
switch_to_frame(hub_outer_frame)
root.mainloop()