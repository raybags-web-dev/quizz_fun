import tkinter as tk
from tkinter import ttk
import random
import time 

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz App")
        self.root.attributes('-fullscreen', True)
        self.root.bind("<Escape>", self.exit_fullscreen)

        self.current_question = None
        self.questions = []
        self.score = 0
        self.total_questions = 0
        self.correct_answers = 0
        self.incorrect_answers = 0
        self.rounds = 20
        self.round = 1
        self.timer = 60
        self.start_time = None
        self.repeat_button = None 

        # Add the result_label initialization here
        self.result_label = tk.Label(self.root, text="", font=("Helvetica", 30))
        self.result_label.pack(fill='both', expand=True, padx=20, pady=20)
        
        self.load_questions()
        self.create_gui()

    def load_questions(self):
        from quiz_data import quiz_data, clean_data
        self.questions = clean_data(quiz_data)
        self.total_questions = len(self.questions)

    def create_gui(self):
        self.question_label = tk.Label(self.root, text="", font=("Helvetica", 40), padx=20, pady=20)
        self.question_label.pack(fill='both', expand=True)

        self.option_buttons = []
        style = ttk.Style()
        style.configure("TButton", font=("Helvetica", 25), padding=10)
        for i in range(4):
            option_button = ttk.Button(self.root, text="", command=lambda i=i: self.check_answer(i), style="TButton")
            option_button.pack(fill='both', expand=True, padx=40, pady=(20, 0))
            self.option_buttons.append(option_button)

        self.round_label = tk.Label(self.root, text="", font=("Helvetica", 30))
        self.round_label.pack(side='bottom', pady=20)
        self.start_round()

    def start_round(self):
        if self.repeat_button:
            self.repeat_button.destroy()  # Destroy the "Repeat Quiz" button if it exists
        
        if self.round <= self.rounds:
            self.round_label.config(text=f"Round {self.round}/{self.rounds}")
            self.display_question()
            self.start_time = time.time()
        else:
            self.show_results()

    def display_question(self):
        if self.questions:
            self.current_question = random.choice(self.questions)
            self.questions.remove(self.current_question)  # Remove the displayed question
            self.question_label.config(text=self.current_question["question"], wraplength=1000)  # Adjust wraplength as needed
            options = self.current_question["options"]
            random.shuffle(options)
            for i in range(4):
                self.option_buttons[i].config(text=options[i].strip("'"))
        else:
            self.show_results()

    def check_answer(self, selected_option):
        if self.option_buttons[selected_option]["text"] == self.current_question["answer"]:
            self.correct_answers += 1
        else:
            self.incorrect_answers += 1
        self.score = (self.correct_answers / self.round) * 100
        self.round += 1
        self.start_round()

    def show_results(self):
        self.question_label.config(text=f"Quiz Complete!\nScore: {self.score:.2f}%")
        self.round_label.config(text="")
            
        # Determine if the user passed or failed
        if self.score >= 50:
            result_text = "PASSED"
        else:
            result_text = "FAILED"
        
        self.result_label.config(text=result_text)

        for button in self.option_buttons:
            button.destroy()
            
        for button in self.option_buttons:
            button.destroy()
        
        self.repeat_button = ttk.Button(self.root, text="Repeat Quiz", command=self.repeat_quiz, style="TButton")
        self.repeat_button.pack(fill='both', expand=True, padx=40, pady=20)

    def repeat_quiz(self):
        self.correct_answers = 0
        self.incorrect_answers = 0
        self.round = 1
        self.score = 0
        self.load_questions()
        
        # Remove the old option buttons
        for button in self.option_buttons:
            button.destroy()

        self.option_buttons = []  # Create new button instances

        # Configure the option buttons with new text and command
        if self.questions:
            options = self.current_question["options"]
            random.shuffle(options)
            for i in range(4):
                option_button = ttk.Button(self.root, text=options[i].strip("'"), command=lambda i=i: self.check_answer(i), style="TButton")
                option_button.pack(fill='both', expand=True, padx=40, pady=(20, 0))
                self.option_buttons.append(option_button)

        self.start_round()
        self.repeat_button.destroy()
        self.result_label.config(text="")


    def exit_fullscreen(self, event):
        self.root.attributes('-fullscreen', False)

    def reset_timer(self):
        self.root.after_cancel(self.timer)
        self.timer = 60

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
