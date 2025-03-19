import tkinter as tk
from tkinter import messagebox
import random
import pyttsx3

class SpellingGame:
    def __init__(self, root):
        # Window
        self.root = root
        self.root.title("Spelling Game")
        self.root.geometry("800x500")

        #Variables
        self.num_words = 0  # Number of words
        self.words_list = []  # List of words
        self.modified_words = []  # List or words with hidden letters
        self.current_word_index = 0  # Tracking number of words entered
        self.score = 0  # User score

        #Text-to-speech for saying word
        self.engine = pyttsx3.init()

        #Start
        self.create_start_ui()

    # Starting UI
    def create_start_ui(self):
        self.clear_ui()
        self.label = tk.Label(self.root, text="Enter the number of words:", font=("", 30))
        self.label.pack()
        self.entry = tk.Entry(self.root, font=("Arial", 20))
        self.entry.pack()
        self.start_button = tk.Button(self.root, text="Enter", command=self.get_num_words, font=("", 20))
        self.start_button.pack()

    # UI for entering words after start_ui
    def create_word_input_ui(self):
        self.clear_ui()
        self.label = tk.Label(self.root, text="Enter a word:", font=("", 20))
        self.label.pack()
        self.entry = tk.Entry(self.root, font=("", 20))
        self.entry.pack()
        self.start_button = tk.Button(self.root, text="Next", command=self.get_words, font=("", 20))
        self.start_button.pack()

    # UI for guessing the word
    def create_guessing_ui(self):
        self.clear_ui()

        self.label = tk.Label(self.root, font=("", 20))
        self.label.pack()
        self.entry = tk.Entry(self.root, font=("", 20))
        self.entry.pack()
        button_frame = tk.Frame(self.root)
        button_frame.pack()
        self.start_button = tk.Button(button_frame, text="Enter", command=self.check_guess, font=("", 20))
        self.start_button.pack(side=tk.LEFT, padx=10)
        self.spelling_button = tk.Button(button_frame, text="Word", command=self.spell_word, font=("", 20))
        self.spelling_button.pack(side=tk.LEFT, padx=10)

    # UI for displaying results
    def create_results_ui(self):
        self.clear_ui()

        #Display score and correct answers
        result_text = f"Game Over\nYour score: {self.score}/{self.num_words}\n\n"
        for i, word in enumerate(self.words_list):
            result_text += f"Word {i+1}: {self.modified_words[i]} --> {word}\n"
        self.label = tk.Label(self.root, text=result_text, font=("", 20))
        self.label.pack()
        button_frame = tk.Frame(self.root)
        button_frame.pack()
        self.retry_button = tk.Button(button_frame, text="Retry", command=self.reset_for_retry, font=("", 20))
        self.retry_button.pack(side=tk.LEFT, padx=10)
        self.new_words_button = tk.Button(button_frame, text="New Words", command=self.create_start_ui, font=("", 20))
        self.new_words_button.pack(side=tk.LEFT, padx=10)

    # Clear UI elements
    def clear_ui(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # Get number of words from user with error checking
    def get_num_words(self):
        try:
            self.num_words = int(self.entry.get())
            if self.num_words <= 0:
                raise ValueError("Enter a positive number please.")

            # Clear list if new words
            self.words_list.clear()
            self.modified_words.clear()
            self.current_word_index = 0
            self.score = 0

            self.create_word_input_ui()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid positive number.")

    # Get words from the user
    def get_words(self):
        word = self.entry.get().strip().lower()
        if not word:
            messagebox.showerror("Error", "Please enter a word.")
            return

        self.words_list.append(word)
        self.entry.delete(0, tk.END)

        if len(self.words_list) == self.num_words:
            self.prepare_guessing_phase()


    def prepare_guessing_phase(self):
        self.modify_words()

        # Shuffle the words_list and modified_words together
        combined = list(zip(self.words_list, self.modified_words))
        random.shuffle(combined)
        self.words_list, self.modified_words = zip(*combined)
        # Convert tuples back to list
        self.words_list = list(self.words_list)
        self.modified_words = list(self.modified_words)

        self.create_guessing_ui()
        self.current_word_index = 0
        self.score = 0
        self.show_next_word()

    # Modify word by replacing a random letter with '_'
    def modify_words(self):
        self.modified_words.clear()
        for word in self.words_list:
            index = random.randint(0, len(word) - 1)
            modified_word = list(word)
            modified_word[index] = '_'
            self.modified_words.append("".join(modified_word))

    # Show next word
    def show_next_word(self):
        if self.current_word_index < len(self.modified_words):
            self.label.config(text=f"{self.modified_words[self.current_word_index]}")
            self.entry.delete(0, tk.END)
        else:
            self.create_results_ui()  # Show results when all words are guessed

    # Answer checker
    def check_guess(self):
        user_guess = self.entry.get().strip().lower()
        correct_word = self.words_list[self.current_word_index]

        if not user_guess:
            messagebox.showerror("Error", "Please enter a word.")
            return

        if user_guess == correct_word:
            self.score += 1

        self.current_word_index += 1
        self.show_next_word()

    # Reset with same initial words
    def reset_for_retry(self):
        self.current_word_index = 0
        self.score = 0
        self.prepare_guessing_phase()

    # Text to speach
    def ttspeach(self, word):
        self.engine.say(word)
        self.engine.runAndWait()

    def spell_word(self):
        if self.current_word_index < len(self.words_list):
            self.ttspeach(f"Spell the word: {self.words_list[self.current_word_index]}")



# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = SpellingGame(root)
    root.mainloop()