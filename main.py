import customtkinter as ctk
from tkinter import StringVar, END
import json
import time
from chatbot import chatbot_response

with open("questions.json", "r") as f:
    all_questions = json.load(f)


class LearningApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Learning Adventure")
        self.geometry("1400x800")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.current_subject = "Math 1"
        self.level = 1
        self.correct_answers = 0
        self.remaining_questions = 5
        self.current_difficulty = 1
        self.start_time = 0
        self.question_index = 0
        self.questions = all_questions.get(self.current_subject, [])
        self.configure_grid()
        self.create_header()
        self.create_menu()
        self.create_main_content()
        self.load_question()

    def configure_grid(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

    def create_header(self):
        self.header_frame = ctk.CTkFrame(self, height=60, fg_color="#1E1E1E", corner_radius=0)
        self.header_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")
        self.header_label = ctk.CTkLabel(
            self.header_frame,
            text="Learning Adventure",
            font=("Helvetica", 28, "bold"),
            text_color="white"
        )
        self.header_label.pack(side="left", padx=20)
        self.level_label = ctk.CTkLabel(
            self.header_frame,
            text=f"Level: {self.level}",
            font=("Helvetica", 16),
            text_color="white"
        )
        self.level_label.pack(side="right", padx=20)

    def create_menu(self):
        self.menu_frame = ctk.CTkFrame(self, width=200, fg_color="#2C2C2C")
        self.menu_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.menu_title = ctk.CTkLabel(
            self.menu_frame,
            text="Navigation",
            font=("Helvetica", 20, "bold"),
            text_color="#E0E0E0"
        )
        self.menu_title.pack(pady=20)
        for subject in ["Math 1", "Math 2", "Math 3", "Precalculus"]:
            ctk.CTkButton(
                self.menu_frame,
                text=subject,
                fg_color="#3B3B3B",
                hover_color="#505050",
                font=("Helvetica", 16),
                command=lambda sub=subject: self.change_subject(sub)
            ).pack(pady=10, padx=10, fill="x")

    def create_main_content(self):
        self.main_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="#1F1F1F")
        self.main_frame.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")
        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="Your Learning Journey Starts Here!",
            font=("Helvetica", 26, "bold"),
            text_color="#FFFFFF"
        )
        self.title_label.pack(pady=10)
        self.question_label = ctk.CTkLabel(
            self.main_frame,
            text="Question: Loading...",
            font=("Helvetica", 20),
            text_color="#B3B3B3"
        )
        self.question_label.pack(pady=10)
        self.answer_input = ctk.CTkEntry(
            self.main_frame,
            placeholder_text="Enter your answer here...",
            font=("Helvetica", 18),
            height=40,
            corner_radius=10
        )
        self.answer_input.pack(pady=20, ipadx=5, ipady=5)
        self.submit_button = ctk.CTkButton(
            self.main_frame,
            text="Submit Answer",
            fg_color="#27AE60",
            hover_color="#2ECC71",
            font=("Helvetica", 18),
            command=self.check_answer
        )
        self.submit_button.pack(pady=20)
        self.feedback_label = ctk.CTkLabel(
            self.main_frame,
            text="",
            font=("Helvetica", 18),
            text_color="green"
        )
        self.feedback_label.pack(pady=20)
        self.progress_bar = ctk.CTkProgressBar(
            self.main_frame,
            width=500,
            progress_color="#27AE60",
            corner_radius=10
        )
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=20)
        self.remaining_var = StringVar(value=f"Remaining Questions: {self.remaining_questions}")
        self.remaining_label = ctk.CTkLabel(
            self.main_frame,
            textvariable=self.remaining_var,
            font=("Helvetica", 16),
            text_color="#B3B3B3"
        )
        self.remaining_label.pack(pady=10)

    def load_question(self):
        self.remaining_var.set(f"Remaining Questions: {self.remaining_questions}")
        if self.question_index < len(self.questions):
            self.question = self.questions[self.question_index]
            self.question_label.configure(text=f"Q: {self.question['question']}")
            self.start_time = time.time()
        else:
            self.question_label.configure(text="You finished!")
            self.submit_button.configure(state="disabled")

    def check_answer(self):
        time_taken = int(time.time() - self.start_time)
        user_answer = self.answer_input.get()
        correct = 1 if user_answer.strip() == self.question["answer"] else 0
        self.feedback_label.configure(
            text="Correct! " if correct else f"❌ Correct answer: {self.question['answer']}",
            text_color="green" if correct else "red"
        )
        self.answer_input.delete(0, END)
        if correct:
            self.correct_answers += 1
            self.remaining_questions -= 1
            if self.remaining_questions == 0:
                self.level_up()
            self.question_index += 1  
        self.load_question()

    def level_up(self):
        self.level += 1
        self.remaining_questions = 5
        self.level_label.configure(text=f"Level: {self.level}")
        self.progress_bar.set(0)

    def change_subject(self, subject):
        self.current_subject = subject
        self.questions = all_questions.get(self.current_subject, [])
        self.level = 1
        self.correct_answers = 0
        self.remaining_questions = 5
        self.question_index = 0
        self.level_label.configure(text=f"Level: {self.level}")
        self.feedback_label.configure(text="")
        self.load_question()

if __name__ == "__main__":
    app = LearningApp()
    app.mainloop()