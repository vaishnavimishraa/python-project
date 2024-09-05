 import tkinter as tk
from tkinter import ttk, messagebox
import csv
import random

class QuestionPaperSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Question Paper Simulator")
        self.root.geometry("800x500")  # Increased window size
        self.root.configure(bg="#f0f0f0")  # Changed background color

        self.subjects = []
        self.questions = {}
        self.selected_questions = {}
        self.total_marks = 0

        self.load_subjects()
        self.create_widgets()

    def load_subjects(self):
        try:
            with open("subjects.csv", 'r') as file:
                reader = csv.reader(file)
                self.subjects = next(reader)  # Read the first row containing subjects
        except FileNotFoundError:
            messagebox.showerror("Error", "Subjects file not found.")

    def load_questions(self, subject):
        try:
            with open(f"{subject}.csv", 'r') as file:
                reader = csv.DictReader(file)
                self.questions[subject] = [row for row in reader]
        except FileNotFoundError:
            messagebox.showerror("Error", f"Questions file for {subject} not found.")

    def select_questions(self):
        self.selected_questions = {}
        self.total_marks = 0
        for subject in self.subjects:
            if subject in self.questions:
                selected = random.sample(self.questions[subject], k=5)  # Select 5 random questions per subject
                self.selected_questions[subject] = selected
                self.total_marks += len(selected)  # Add the marks of selected questions

    def submit_answers(self):
      total_score = 0
      for subject in self.selected_questions:
          subject_score = 0
          for question_idx, question in enumerate(self.selected_questions[subject], start=1):
              answer = self.answers[question_idx].get()  # Get the user's answer using question index
              if answer == question['Answer']:  # Compare with the correct answer
                  subject_score += 1
          total_score += subject_score
          messagebox.showinfo("Result", f"Score in {subject}: {subject_score}/{len(self.selected_questions[subject])}")
      messagebox.showinfo("Total Result", f"Total Score: {total_score}/{self.total_marks}")


    def create_widgets(self):
     title_frame = tk.Frame(self.root, bg="#9370db", pady=10)
     title_frame.pack(fill=tk.X)

     title_label = tk.Label(title_frame, text="Question Paper Simulator", font=("Arial", 24, "bold"), bg="#9370db", fg="white")
     title_label.pack()

     subject_frame = tk.Frame(self.root, bg="#f0f0f0", pady=10)
     subject_frame.pack()

     subject_label = tk.Label(subject_frame, text="Choose Subject:", font=("Arial", 12), bg="#f0f0f0")
     subject_label.grid(row=0, column=0, padx=10)

     self.subject_var = tk.StringVar()
     self.subject_var.set(self.subjects[0] if self.subjects else "No subjects available")  # Default value

     subject_menu = ttk.OptionMenu(subject_frame, self.subject_var, *self.subjects)
     subject_menu.grid(row=0, column=1, padx=10)

     load_button = tk.Button(subject_frame, text="Load Questions", command=self.load_selected_questions, font=("Arial", 12))
     load_button.grid(row=0, column=2, padx=10)

     question_frame = tk.Frame(self.root, bg="#f0f0f0")
     question_frame.pack(pady=20)

     self.question_scroll = tk.Scrollbar(question_frame)
     self.question_scroll.pack(side=tk.RIGHT, fill=tk.Y)

     self.question_canvas = tk.Canvas(question_frame, bg="#f0f0f0", yscrollcommand=self.question_scroll.set, width=700, height=300)
     self.question_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

     self.question_scroll.config(command=self.question_canvas.yview)

     self.question_inner_frame = tk.Frame(self.question_canvas, bg="#f0f0f0")
     self.question_canvas.create_window((0, 0), window=self.question_inner_frame, anchor="nw")

     self.submit_button = tk.Button(question_frame, text="Submit Answers", command=self.submit_answers, font=("Arial", 14, "bold"), bg="#9370db", fg="white", width=40)  # Adjusted width
     

    def load_selected_questions(self):
        subject = self.subject_var.get()
        if subject not in self.questions:
            self.load_questions(subject)
            self.select_questions()
            self.render_questions()
            self.submit_button.pack(pady=10)
        else:
            self.select_questions()
            self.render_questions()
            self.submit_button.pack(pady=10)

    def render_questions(self):
         for widget in self.question_inner_frame.winfo_children():
             widget.destroy()

         self.answers = {}
         selected_questions = self.selected_questions.get(self.subject_var.get(), [])
         for idx, question in enumerate(selected_questions, start=1):
             question_label = tk.Label(self.question_inner_frame, text=f"{idx}. {question['Question']}", font=("Arial", 12), bg="#f0f0f0")
             question_label.pack(anchor="w", padx=10, pady=5)

             answer_var = tk.StringVar()
             answer_option = ttk.Combobox(self.question_inner_frame, textvariable=answer_var, values=["True", "False"], font=("Arial", 12))
             answer_option.pack(anchor="w", padx=10, pady=5)
             answer_option.current(0)

             # Using the index of the question as the key
             self.answers[idx] = answer_var  

         # Update the scroll region of the canvas
         self.question_inner_frame.update_idletasks()
         self.question_canvas.config(scrollregion=self.question_canvas.bbox("all"))



def main():
    root = tk.Tk()
    app = QuestionPaperSimulator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
