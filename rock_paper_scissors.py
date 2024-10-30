import customtkinter as ctk
import random

# Set the appearance mode and color theme
ctk.set_appearance_mode("System")  # Modes: "System" (default), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (default), "green", "dark-blue"

class RockPaperScissorsGame(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Rock-Paper-Scissors Game")
        self.geometry("500x600")
        self.resizable(False, False)
        
        # Initialize scores
        self.user_score = 0
        self.computer_score = 0
        
        # Define choices
        self.choices = ["Rock", "Paper", "Scissors"]
        
        # Configure grid layout
        self.grid_columnconfigure(0, weight=1)
        
        # Create UI components
        self.create_widgets()
    
    def create_widgets(self):
        # Title Label
        title = ctk.CTkLabel(self, text="Rock-Paper-Scissors", font=ctk.CTkFont(size=24, weight="bold"))
        title.pack(pady=20)
        
        # Instruction Label
        instruction = ctk.CTkLabel(self, text="Choose Rock, Paper, or Scissors:", font=ctk.CTkFont(size=16))
        instruction.pack(pady=(10, 20))
        
        # Buttons Frame
        buttons_frame = ctk.CTkFrame(self)
        buttons_frame.pack(pady=10, padx=20, fill="x")
        buttons_frame.grid_columnconfigure((0,1,2), weight=1)
        
        # Rock Button
        rock_button = ctk.CTkButton(buttons_frame, text="Rock", font=ctk.CTkFont(size=16), command=lambda: self.play("Rock"))
        rock_button.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # Paper Button
        paper_button = ctk.CTkButton(buttons_frame, text="Paper", font=ctk.CTkFont(size=16), command=lambda: self.play("Paper"))
        paper_button.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        # Scissors Button
        scissors_button = ctk.CTkButton(buttons_frame, text="Scissors", font=ctk.CTkFont(size=16), command=lambda: self.play("Scissors"))
        scissors_button.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
        
        # Separator
        separator = ctk.CTkLabel(self, text="", height=2, fg_color="gray")
        separator.pack(fill="x", pady=20, padx=20)
        
        # Results Frame
        results_frame = ctk.CTkFrame(self)
        results_frame.pack(pady=10, padx=20, fill="x")
        results_frame.grid_columnconfigure(1, weight=1)
        
        # User Choice Label
        user_choice_label = ctk.CTkLabel(results_frame, text="Your Choice:", font=ctk.CTkFont(size=14, weight="bold"))
        user_choice_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)
        
        self.user_choice_value = ctk.CTkLabel(results_frame, text="-", font=ctk.CTkFont(size=14))
        self.user_choice_value.grid(row=0, column=1, sticky="w", padx=10, pady=5)
        
        # Computer Choice Label
        comp_choice_label = ctk.CTkLabel(results_frame, text="Computer's Choice:", font=ctk.CTkFont(size=14, weight="bold"))
        comp_choice_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)
        
        self.comp_choice_value = ctk.CTkLabel(results_frame, text="-", font=ctk.CTkFont(size=14))
        self.comp_choice_value.grid(row=1, column=1, sticky="w", padx=10, pady=5)
        
        # Result Label
        self.result_label = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=18, weight="bold"))
        self.result_label.pack(pady=20)
        
        # Scores Frame
        scores_frame = ctk.CTkFrame(self)
        scores_frame.pack(pady=10, padx=20, fill="x")
        scores_frame.grid_columnconfigure((0,1), weight=1)
        
        # User Score
        user_score_label = ctk.CTkLabel(scores_frame, text="Your Score:", font=ctk.CTkFont(size=14, weight="bold"))
        user_score_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)
        
        self.user_score_value = ctk.CTkLabel(scores_frame, text=str(self.user_score), font=ctk.CTkFont(size=14))
        self.user_score_value.grid(row=0, column=1, sticky="w", padx=10, pady=5)
        
        # Computer Score
        comp_score_label = ctk.CTkLabel(scores_frame, text="Computer's Score:", font=ctk.CTkFont(size=14, weight="bold"))
        comp_score_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)
        
        self.comp_score_value = ctk.CTkLabel(scores_frame, text=str(self.computer_score), font=ctk.CTkFont(size=14))
        self.comp_score_value.grid(row=1, column=1, sticky="w", padx=10, pady=5)
        
        # Play Again Button
        play_again_button = ctk.CTkButton(self, text="Reset Scores", font=ctk.CTkFont(size=14), command=self.reset_scores)
        play_again_button.pack(pady=20)
    
    def play(self, user_choice):
        # Update user's choice
        self.user_choice_value.configure(text=user_choice)
        
        # Generate computer's choice
        comp_choice = random.choice(self.choices)
        self.comp_choice_value.configure(text=comp_choice)
        
        # Determine the winner
        result = self.determine_winner(user_choice, comp_choice)
        self.result_label.configure(text=result)
        
        # Update scores
        if result == "You Win!":
            self.user_score += 1
            self.user_score_value.configure(text=str(self.user_score))
        elif result == "Computer Wins!":
            self.computer_score += 1
            self.comp_score_value.configure(text=str(self.computer_score))
        # No score update on tie
    
    def determine_winner(self, user, comp):
        if user == comp:
            return "It's a Tie!"
        elif (user == "Rock" and comp == "Scissors") or \
             (user == "Paper" and comp == "Rock") or \
             (user == "Scissors" and comp == "Paper"):
            return "You Win!"
        else:
            return "Computer Wins!"
    
    def reset_scores(self):
        confirm = ctk.CTkMessageBox.ask_yes_no(title="Reset Scores", message="Are you sure you want to reset the scores?")
        if confirm:
            self.user_score = 0
            self.computer_score = 0
            self.user_score_value.configure(text=str(self.user_score))
            self.comp_score_value.configure(text=str(self.computer_score))
            self.result_label.configure(text="")
            self.user_choice_value.configure(text="-")
            self.comp_choice_value.configure(text="-")
    
if __name__ == "__main__":
    app = RockPaperScissorsGame()
    app.mainloop()
