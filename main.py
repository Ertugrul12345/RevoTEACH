import customtkinter as ctk
from tkinter import StringVar, Toplevel, Text, END
import json
import time
from chatbot import chatbot_response

with open("questions.json", "r") as f:
    all_questions = json.load(f)

class LearningApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("RevoTeach")
        self.geometry("1000x700")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.current_subject = "Math 1"
        self.remaining_questions = 5
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
        ctk.CTkButton(
            self.menu_frame,
            text="Get Help",
            fg_color="#3B3B3B",
            hover_color="#505050",
            font=("Helvetica", 16),
            command=self.open_chatbot
        ).pack(pady=20, padx=10, fill="x")

    def create_main_content(self):
        self.main_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="#1F1F1F")
        self.main_frame.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")
        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="Question:",
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
            self.question_label.configure(text=f" {self.question['question']}")
            self.start_time = time.time()
        else:
            self.question_label.configure(text="🎉 You've completed all questions!")
            self.submit_button.configure(state="disabled")

    def check_answer(self):
        time_taken = int(time.time() - self.start_time)
        user_answer = self.answer_input.get()
        correct = 1 if user_answer.strip() == self.question["answer"] else 0
        self.feedback_label.configure(
            text="✅ Correct! Great job!" if correct else f"❌ Correct answer: {self.question['answer']}",
            text_color="green" if correct else "red"
        )
        self.answer_input.delete(0, END)
        if correct:
            self.remaining_questions -= 1
            self.question_index += 1
            if self.remaining_questions == 0:
                self.remaining_questions = 5
        self.load_question()

    def change_subject(self, subject):
        self.current_subject = subject
        self.questions = all_questions.get(self.current_subject, [])
        self.remaining_questions = 5
        self.question_index = 0
        self.feedback_label.configure(text="")
        self.load_question()

    def open_chatbot(self):
        chatbot_window = ctk.CTkToplevel(self)
        chatbot_window.title("Chatbot")
        chatbot_window.geometry("500x600")
        chatbot_window.configure(fg_color="#2C2C2C")

        chatbot_frame = ctk.CTkFrame(chatbot_window, corner_radius=10, fg_color="#1F1F1F")
        chatbot_frame.pack(fill="both", expand=True, padx=10, pady=10)

        chatbot_title = ctk.CTkLabel(
            chatbot_frame,
            text="Chatbot",
            font=("Helvetica", 24, "bold"),
            text_color="white"
        )
        chatbot_title.pack(pady=10)

        chatbot_display = ctk.CTkTextbox(
            chatbot_frame,
            height=400,
            corner_radius=10,
            fg_color="#1F1F1F",
            text_color="white"
        )
        chatbot_display.insert("1.0", "Bot: Hello! How can I assist you today?\n")
        chatbot_display.configure(state="disabled")
        chatbot_display.pack(pady=10, padx=10, fill="both", expand=True)

        chatbot_input = ctk.CTkEntry(
            chatbot_frame,
            placeholder_text="Type your message here...",
            font=("Helvetica", 16),
            height=40,
            corner_radius=10
        )
        chatbot_input.pack(pady=10, padx=10, fill="x")

        def send_message():
            user_message = chatbot_input.get()
            if user_message:
                chatbot_display.configure(state="normal")
                chatbot_display.insert("end", f"You: {user_message}\n")
                bot_response = chatbot_response(user_message)
                chatbot_display.insert("end", f"Bot: {bot_response}\n\n")
                chatbot_display.configure(state="disabled")
                chatbot_input.delete(0, END)
                chatbot_display.see("end")

        send_button = ctk.CTkButton(
            chatbot_frame,
            text="Send",
            fg_color="#27AE60",
            hover_color="#2ECC71",
            font=("Helvetica", 16),
            command=send_message
        )
        send_button.pack(pady=10)

if __name__ == "__main__":
    app = LearningApp()
    app.mainloop()
