import csv
import json
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

DATA_FILE = "assignment_tracker.json"
COLUMNS = ("enrollment", "name", "assignment", "status", "marks", "remarks")


class Tracker(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Assignment Tracker")
        self.geometry("1000x620")
        self.students = {}
        self.records = []
        self.keys = set()
        self.load()
        self.make_variables()
        self.make_student_box()
        self.make_submission_box()
        self.make_table()
        self.refresh_students()
        self.refresh_table()

    def load(self):
        try:
            with open(DATA_FILE, encoding="utf-8") as handle:
                data = json.load(handle)
            self.students = dict(data["students"])
            self.records = list(data["records"])
        except (OSError, ValueError, KeyError, TypeError):
            self.students = {}
            self.records = []
        self.keys = {(r["enrollment"], r["assignment"].lower()) for r in self.records}

    def save(self):
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as handle:
                json.dump({"students": self.students, "records": self.records}, handle)
        except OSError as error:
            messagebox.showerror("Save failed", str(error))

    def make_variables(self):
        self.enroll_var = tk.StringVar()
        self.name_var = tk.StringVar()
        self.student_var = tk.StringVar()
        self.assignment_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Completed")
        self.marks_var = tk.StringVar()
        self.outof_var = tk.StringVar(value="20")
        self.late_var = tk.BooleanVar()
        self.filter_var = tk.StringVar(value="All")

    def make_student_box(self):
        box = ttk.LabelFrame(self, text="Student")
        box.pack(fill="x", padx=10, pady=5)
        ttk.Label(box, text="Enrollment").grid(row=0, column=0, padx=5, pady=5)
        ttk.Entry(box, textvariable=self.enroll_var, width=16).grid(row=0, column=1)
        ttk.Label(box, text="Name").grid(row=0, column=2, padx=5)
        ttk.Entry(box, textvariable=self.name_var, width=26).grid(row=0, column=3)
        ttk.Button(box, text="Add Student", command=self.add_student).grid(row=0, column=4, padx=10)

    def make_submission_box(self):
        box = ttk.LabelFrame(self, text="Submission")
        box.pack(fill="x", padx=10, pady=5)
        ttk.Label(box, text="Student").grid(row=0, column=0, padx=5, pady=5)
        self.student_box = ttk.Combobox(box, textvariable=self.student_var, state="readonly", width=28)
        self.student_box.grid(row=0, column=1)
        ttk.Label(box, text="Assignment").grid(row=0, column=2, padx=5)
        ttk.Entry(box, textvariable=self.assignment_var, width=24).grid(row=0, column=3)
        ttk.Radiobutton(box, text="Completed", variable=self.status_var, value="Completed").grid(row=1, column=0, pady=5)
        ttk.Radiobutton(box, text="Pending", variable=self.status_var, value="Pending").grid(row=1, column=1)
        ttk.Label(box, text="Marks").grid(row=1, column=2)
        ttk.Entry(box, textvariable=self.marks_var, width=8).grid(row=1, column=3, sticky="w")
        ttk.Label(box, text="Out of").grid(row=1, column=4)
        ttk.Entry(box, textvariable=self.outof_var, width=8).grid(row=1, column=5)
        ttk.Checkbutton(box, text="Late submission", variable=self.late_var).grid(row=1, column=6, padx=10)
        ttk.Label(box, text="Remarks").grid(row=2, column=0, padx=5)
        self.remarks_text = tk.Text(box, height=2, width=50)
        self.remarks_text.grid(row=2, column=1, columnspan=3, pady=5)
        ttk.Button(box, text="Add Submission", command=self.add_submission).grid(row=2, column=4, padx=5)
        ttk.Button(box, text="Update Marks", command=self.update_marks).grid(row=2, column=5, padx=5)

    def make_table(self):
        bar = ttk.Frame(self)
        bar.pack(fill="x", padx=10)
        ttk.Label(bar, text="Show:").pack(side="left")
        for label in ("All", "Pending", "Completed"):
            ttk.Radiobutton(bar, text=label, variable=self.filter_var, value=label,
                            command=self.refresh_table).pack(side="left", padx=5)
        ttk.Button(bar, text="Export CSV", command=self.export_csv).pack(side="right")
        holder = ttk.Frame(self)
        holder.pack(fill="both", expand=True, padx=10, pady=5)
        self.tree = ttk.Treeview(holder, columns=COLUMNS, show="headings", selectmode="browse")
        for column in COLUMNS:
            self.tree.heading(column, text=column.title())
            self.tree.column(column, width=130)
        scroll = ttk.Scrollbar(holder, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

    def refresh_students(self):
        self.student_box["values"] = [f"{key} - {name}" for key, name in sorted(self.students.items())]

    def visible_records(self):
        wanted = self.filter_var.get()
        return [(i, r) for i, r in enumerate(self.records) if wanted == "All" or r["status"] == wanted]

    def refresh_table(self):
        self.tree.delete(*self.tree.get_children())
        for index, record in self.visible_records():
            self.tree.insert("", "end", iid=str(index), values=[record[c] for c in COLUMNS])

    def parse_marks(self, text, out_of):
        try:
            limit = float(out_of)
            value = float(text)
        except ValueError:
            raise ValueError("Marks and Out of must be numbers")
        if not limit > 0 or not 0 <= value <= limit:
            raise ValueError("Marks must be between 0 and Out of")
        return int(value) if value.is_integer() else value, int(limit) if limit.is_integer() else limit

    def add_student(self):
        enrollment = self.enroll_var.get().strip()
        name = self.name_var.get().strip()
        if not enrollment.isalnum():
            messagebox.showerror("Invalid", "Enrollment must be letters and digits only")
        elif not name or not name.replace(" ", "").isalpha():
            messagebox.showerror("Invalid", "Name must contain only letters and spaces")
        elif enrollment in self.students:
            messagebox.showerror("Duplicate", "Student already exists")
        else:
            self.students[enrollment] = name
            self.save()
            self.refresh_students()
            self.enroll_var.set("")
            self.name_var.set("")

    def add_submission(self):
        chosen = self.student_var.get()
        assignment = self.assignment_var.get().strip()
        status = self.status_var.get()
        if not chosen:
            messagebox.showerror("Invalid", "Select a student first")
            return
        if not assignment:
            messagebox.showerror("Invalid", "Enter an assignment name")
            return
        enrollment = chosen.split(" - ")[0]
        if (enrollment, assignment.lower()) in self.keys:
            messagebox.showerror("Duplicate", "This submission already exists")
            return
        marks, out_of = "", None
        if status == "Completed":
            try:
                marks, out_of = self.parse_marks(self.marks_var.get(), self.outof_var.get())
            except ValueError as error:
                messagebox.showerror("Invalid", str(error))
                return
        notes = [self.remarks_text.get("1.0", "end-1c").strip()]
        if self.late_var.get():
            notes.append("Late submission")
        self.records.append({
            "enrollment": enrollment,
            "name": self.students[enrollment],
            "assignment": assignment,
            "status": status,
            "marks": marks,
            "remarks": "; ".join(n for n in notes if n),
            "out_of": out_of,
        })
        self.keys.add((enrollment, assignment.lower()))
        self.save()
        self.refresh_table()
        self.assignment_var.set("")
        self.marks_var.set("")
        self.remarks_text.delete("1.0", "end")
        self.late_var.set(False)

    def update_marks(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Invalid", "Select a row in the table first")
            return
        record = self.records[int(selected[0])]
        out_of = record.get("out_of") or self.outof_var.get()
        try:
            marks, out_of = self.parse_marks(self.marks_var.get(), out_of)
        except ValueError as error:
            messagebox.showerror("Invalid", str(error))
            return
        record["marks"] = marks
        record["out_of"] = out_of
        record["status"] = "Completed"
        self.save()
        self.refresh_table()

    def export_csv(self):
        path = filedialog.asksaveasfilename(defaultextension=".csv", initialfile="report.csv",
                                            filetypes=[("CSV files", "*.csv")])
        if not path:
            return
        try:
            with open(path, "w", newline="", encoding="utf-8") as handle:
                writer = csv.writer(handle)
                writer.writerow(COLUMNS)
                for _, record in self.visible_records():
                    writer.writerow([record[c] for c in COLUMNS])
        except OSError as error:
            messagebox.showerror("Export failed", str(error))
            return
        messagebox.showinfo("Exported", "Report saved to " + path)


if __name__ == "__main__":
    Tracker().mainloop()
