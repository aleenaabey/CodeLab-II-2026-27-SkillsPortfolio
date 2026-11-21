import os
from tkinter import *
from tkinter import messagebox

# Look for the data file next to this script so it works from any folder
FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         "studentMarks.txt")

COURSEWORK_MAX = 60     # 3 pieces of coursework, each out of 20
EXAM_MAX = 100
TOTAL_MAX = COURSEWORK_MAX + EXAM_MAX    # 160 marks available overall

# Each student is a dictionary; all students live in this list
students = []


# ---------------------------------------------------------------------------
# File handling
# ---------------------------------------------------------------------------
def loadStudents():
    """Read studentMarks.txt into the students list."""
    students.clear()
    try:
        with open(FILE_PATH, "r", encoding="utf-8") as fileHandler:
            lines = [line.strip() for line in fileHandler if line.strip()]
    except FileNotFoundError:
        messagebox.showerror("File not found", f"Could not find:\n{FILE_PATH}")
        return

    # lines[0] is the student count, the real data starts on the next line
    for line in lines[1:]:
        parts = line.split(",")
        students.append({
            "code": int(parts[0]),
            "name": parts[1].strip(),
            "marks": [int(parts[2]), int(parts[3]), int(parts[4])],
            "exam": int(parts[5]),
        })


def saveStudents():
    """Write the students list back to studentMarks.txt."""
    with open(FILE_PATH, "w", encoding="utf-8") as fileHandler:
        fileHandler.write(f"{len(students)}\n")
        for student in students:
            m = student["marks"]
            fileHandler.write(f"{student['code']},{student['name']},"
                              f"{m[0]},{m[1]},{m[2]},{student['exam']}\n")


# ---------------------------------------------------------------------------
# Calculations and formatting
# ---------------------------------------------------------------------------
def courseworkTotal(student):
    """Sum of the three coursework marks (out of 60)."""
    return sum(student["marks"])


def overallMark(student):
    """Coursework + exam (out of 160)."""
    return courseworkTotal(student) + student["exam"]


def percentage(student):
    """Overall percentage, based on the 160 marks available."""
    return overallMark(student) / TOTAL_MAX * 100


def grade(percent):
    """Convert a percentage into a letter grade."""
    if percent >= 70:
        return "A"
    elif percent >= 60:
        return "B"
    elif percent >= 50:
        return "C"
    elif percent >= 40:
        return "D"
    return "F"


def formatStudent(student):
    """Return the text block describing one student (used by every view)."""
    percent = percentage(student)
    return (f"Name:               {student['name']}\n"
            f"Student Number:     {student['code']}\n"
            f"Coursework Total:   {courseworkTotal(student)} / {COURSEWORK_MAX}\n"
            f"Exam Mark:          {student['exam']} / {EXAM_MAX}\n"
            f"Overall Percentage: {percent:.1f}%\n"
            f"Grade:              {grade(percent)}\n")


def formatList(studentList):
    """Format several students followed by the class summary."""
    if not studentList:
        return "No student records to show."
    text = ""
    for student in studentList:
        text += formatStudent(student) + "-" * 40 + "\n"
    average = sum(percentage(s) for s in studentList) / len(studentList)
    text += f"\nNumber of students: {len(studentList)}\n"
    text += f"Average percentage: {average:.1f}%\n"
    return text


def showText(text):
    """Display text in the read-only output area."""
    outputBox.config(state=NORMAL)
    outputBox.delete("1.0", END)
    outputBox.insert(END, text)
    outputBox.config(state=DISABLED)


# ---------------------------------------------------------------------------
# Searching
# ---------------------------------------------------------------------------
def findStudents(searchText):
    """Return every student whose number equals, or name contains, the text."""
    searchText = searchText.strip().lower()
    matches = []
    for student in students:
        if searchText == str(student["code"]) or searchText in student["name"].lower():
            matches.append(student)
    return matches


def getSingleStudent():
    """
    Use the search box to find exactly one student (for delete / update).
    Returns the student dictionary, or None after showing a warning.
    """
    searchText = searchEntry.get().strip()
    if searchText == "":
        messagebox.showwarning("Search needed",
                               "Type a student name or number in the search box first.")
        return None

    matches = findStudents(searchText)
    if len(matches) == 0:
        messagebox.showinfo("Not found", f"No student matches '{searchText}'.")
        return None
    if len(matches) > 1:
        names = ", ".join(s["name"] for s in matches)
        messagebox.showinfo("Be more specific",
                            f"More than one student matches: {names}")
        return None
    return matches[0]


# ---------------------------------------------------------------------------
# Menu actions 1 - 4
# ---------------------------------------------------------------------------
def viewAll():
    showText(formatList(students))


def viewIndividual():
    searchText = searchEntry.get().strip()
    if searchText == "":
        messagebox.showwarning("Search needed",
                               "Type a student name or number in the search box first.")
        return
    matches = findStudents(searchText)
    if not matches:
        showText(f"No student matches '{searchText}'.")
    else:
        text = ""
        for student in matches:
            text += formatStudent(student) + "-" * 40 + "\n"
        showText(text)


def showHighest():
    if not students:
        return
    best = max(overallMark(s) for s in students)
    # a list, in case two students tie for the top mark
    showText("HIGHEST OVERALL MARK\n\n" +
             "".join(formatStudent(s) + "\n" for s in students if overallMark(s) == best))


def showLowest():
    if not students:
        return
    worst = min(overallMark(s) for s in students)
    showText("LOWEST OVERALL MARK\n\n" +
             "".join(formatStudent(s) + "\n" for s in students if overallMark(s) == worst))


# ---------------------------------------------------------------------------
# Extension: sort
# ---------------------------------------------------------------------------
def sortStudents():
    """Pop-up window asking how to sort, then display the sorted records."""
    window = Toplevel(root)
    window.title("Sort student records")
    window.geometry("300x280")
    window.grab_set()                    # keep focus on this window

    sortBy = StringVar(value="percentage")
    order = StringVar(value="asc")

    Label(window, text="Sort by:", font=("Arial", 11, "bold")).pack(pady=(12, 2))
    Radiobutton(window, text="Name", variable=sortBy, value="name").pack(anchor=W, padx=60)
    Radiobutton(window, text="Student number", variable=sortBy, value="code").pack(anchor=W, padx=60)
    Radiobutton(window, text="Overall percentage", variable=sortBy, value="percentage").pack(anchor=W, padx=60)

    Label(window, text="Order:", font=("Arial", 11, "bold")).pack(pady=(12, 2))
    Radiobutton(window, text="Ascending", variable=order, value="asc").pack(anchor=W, padx=60)
    Radiobutton(window, text="Descending", variable=order, value="desc").pack(anchor=W, padx=60)

    def applySort():
        if sortBy.get() == "name":
            keyFunction = lambda s: s["name"].lower()
        elif sortBy.get() == "code":
            keyFunction = lambda s: s["code"]
        else:
            keyFunction = percentage
        # sorted() returns a new list so the original order is untouched
        result = sorted(students, key=keyFunction, reverse=(order.get() == "desc"))
        showText(formatList(result))
        window.destroy()

    Button(window, text="Sort", width=12, command=applySort).pack(pady=15)


# ---------------------------------------------------------------------------
# Extension: add / update (share one form)
# ---------------------------------------------------------------------------
def openStudentForm(existing=None):
    """
    Pop-up form used by both 'Add' (existing=None) and 'Update'
    (existing=the student being edited, so the boxes start filled in).
    """
    window = Toplevel(root)
    window.title("Update student" if existing else "Add student")
    window.geometry("340x370")
    window.grab_set()

    labels = ["Student number (1000-9999)", "Name", "Coursework 1 (0-20)",
              "Coursework 2 (0-20)", "Coursework 3 (0-20)", "Exam (0-100)"]
    entries = []
    for row, labelText in enumerate(labels):
        Label(window, text=labelText).grid(row=row, column=0, padx=12, pady=8, sticky=W)
        entry = Entry(window, width=18)
        entry.grid(row=row, column=1, padx=8, pady=8)
        entries.append(entry)

    if existing:
        values = [existing["code"], existing["name"], *existing["marks"], existing["exam"]]
        for entry, value in zip(entries, values):
            entry.insert(0, str(value))

    def saveForm():
        """Validate every box; only save if everything is acceptable."""
        try:
            code = int(entries[0].get())
            name = entries[1].get().strip()
            marks = [int(entries[2].get()), int(entries[3].get()), int(entries[4].get())]
            exam = int(entries[5].get())
        except ValueError:
            messagebox.showerror("Invalid input", "Numbers must be whole numbers.", parent=window)
            return

        if not 1000 <= code <= 9999:
            messagebox.showerror("Invalid input", "Student number must be 1000-9999.", parent=window)
            return
        if name == "" or "," in name:
            messagebox.showerror("Invalid input", "Enter a name (no commas).", parent=window)
            return
        if any(not 0 <= m <= 20 for m in marks):
            messagebox.showerror("Invalid input", "Coursework marks must be 0-20.", parent=window)
            return
        if not 0 <= exam <= EXAM_MAX:
            messagebox.showerror("Invalid input", "Exam mark must be 0-100.", parent=window)
            return
        # student numbers must be unique (ignore the student being edited)
        for other in students:
            if other["code"] == code and other is not existing:
                messagebox.showerror("Invalid input", "That student number is already used.", parent=window)
                return

        if existing:
            existing.update({"code": code, "name": name, "marks": marks, "exam": exam})
            message = "Student record updated."
            shown = existing
        else:
            shown = {"code": code, "name": name, "marks": marks, "exam": exam}
            students.append(shown)
            message = "Student record added."

        saveStudents()                   # keep the text file in step
        window.destroy()
        showText(message + "\n\n" + formatStudent(shown))

    Button(window, text="Save", width=12, command=saveForm).grid(row=6, column=0, columnspan=2, pady=18)


def addStudent():
    openStudentForm()


def updateStudent():
    student = getSingleStudent()
    if student:
        openStudentForm(student)


# ---------------------------------------------------------------------------
# Extension: delete
# ---------------------------------------------------------------------------
def deleteStudent():
    student = getSingleStudent()
    if student is None:
        return
    if messagebox.askyesno("Confirm delete",
                           f"Delete {student['name']} ({student['code']})?"):
        students.remove(student)
        saveStudents()
        showText(f"Deleted {student['name']}.\n\nStudents remaining: {len(students)}")


# ---------------------------------------------------------------------------
# Main window
# ---------------------------------------------------------------------------
root = Tk()
root.title("Student Manager")
root.geometry("900x560")

loadStudents()

# Left: search box and menu buttons
menuFrame = Frame(root, padx=12, pady=12)
menuFrame.pack(side=LEFT, fill=Y)

Label(menuFrame, text="STUDENT MANAGER", font=("Arial", 14, "bold")).pack(pady=(0, 10))
Label(menuFrame, text="Search (name or number):").pack(anchor=W)
searchEntry = Entry(menuFrame, width=26)
searchEntry.pack(pady=(0, 12))

menuItems = [
    ("1. View all student records", viewAll),
    ("2. View individual record", viewIndividual),
    ("3. Highest overall mark", showHighest),
    ("4. Lowest overall mark", showLowest),
    ("5. Sort student records", sortStudents),
    ("6. Add a student", addStudent),
    ("7. Delete a student", deleteStudent),
    ("8. Update a student", updateStudent),
    ("Quit", root.destroy),
]
for text, action in menuItems:
    Button(menuFrame, text=text, width=26, command=action).pack(pady=3)

# Right: read-only output area with a scroll bar
outputFrame = Frame(root, padx=8, pady=12)
outputFrame.pack(side=RIGHT, fill=BOTH, expand=True)

scrollBar = Scrollbar(outputFrame)
scrollBar.pack(side=RIGHT, fill=Y)
outputBox = Text(outputFrame, font=("Courier", 11), yscrollcommand=scrollBar.set,
                 state=DISABLED, wrap=WORD)
outputBox.pack(side=LEFT, fill=BOTH, expand=True)
scrollBar.config(command=outputBox.yview)

showText("Welcome! Choose an option from the menu.\n"
         "Use the search box for options 2, 7 and 8.")

root.mainloop()