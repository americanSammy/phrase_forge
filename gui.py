# gui.py
import subprocess
import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox, ttk
from analyzer import Analyzer
from translator import Translator
import plotly.express as px
import plotly.graph_objects as go
import os
import logging

# Configure the logging settings
logging.basicConfig(filename='phraseforge.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class MessageAnalyzerGUI:
    def __init__(self, master):
        self.master = master
        master.title("PhraseForge")
        master.geometry("1200x900")
        master.configure(bg="white")

        # GUI components
        self.label = tk.Label(master, text="Upload chat.db file:", font=("Arial", 24), bg="white")
        self.label.pack(pady=20)

        self.browse_button = tk.Button(master, text="Browse", command=self.browse_file, font=("Arial", 21))
        self.browse_button.pack(side=tk.LEFT, padx=20, pady=20)

        self.language_var = tk.StringVar()
        self.language_var.set("Select Language")

        self.language_dropdown = ttk.Combobox(master, textvariable=self.language_var, values=["Portuguese", "Spanish", "French", "Italian"])
        self.language_dropdown.pack(side=tk.LEFT, padx=10, pady=20)

        self.translate_button = tk.Button(master, text="Translate", command=self.translate_words, font=("Arial", 21), state=tk.DISABLED)
        self.translate_button.pack(side=tk.LEFT, padx=10, pady=20)

        self.result_text = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=70, height=20, font=("Arial", 18))
        self.result_text.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

        self.generate_button = tk.Button(master, text="Generate Bubble Chart", command=self.generate_bubble_chart, font=("Arial", 21), state=tk.DISABLED)
        self.generate_button.pack(pady=20)

        self.view_log_button = tk.Button(master, text="View Log", command=self.view_log, font=("Arial", 21))
        self.view_log_button.pack(side=tk.LEFT, padx=10, pady=20)

    def view_log(self):
        try:
            log_file_path = os.path.join(os.getcwd(), 'phraseforge.log')
            subprocess.Popen(['open', '-t', log_file_path])  # Use 'open -t' on macOS to open in the default text editor
        except Exception as e:
            logging.error(f"An error occurred while opening the log file: {e}")
            self.show_error(f"An error occurred while opening the log file: {e}")

    def browse_file(self):
        try:
            initial_dir = os.path.expanduser("~/Library/Messages/")
            file_path = filedialog.askopenfilename(
                filetypes=[("SQLite Database", "*.db")],
                initialdir=initial_dir
            )
            if file_path:
                logging.info(f"Selected chat.db file: {file_path}")
                self.analyze_chat_db(file_path)
        except Exception as e:
            logging.error(f"Error while selecting file: {e}")
            self.show_error(f"Error while selecting file: {e}")

    def analyze_chat_db(self, chat_db_path):
        try:
            common_words = Analyzer.analyze_chat_db(chat_db_path)
            logging.info("Chat analysis completed successfully.")

            # Display the most common words in the result_text widget
            result_text_content = "Most Common 300 Words:\n\n"
            for word, count in common_words:
                result_text_content += f"{word.capitalize()}: {count}\n"

            self.result_text.delete(1.0, tk.END)  # Clear existing content
            self.result_text.insert(tk.END, result_text_content)

            # Store common words for later use
            self.common_words = common_words

            # Enable the Generate Bubble Chart button and Translate button
            self.generate_button.config(state=tk.NORMAL)
            self.translate_button.config(state=tk.NORMAL)

        except Exception as e:
            logging.error(f"An error occurred during analysis: {e}")
            self.show_error(f"An error occurred: {e}")

    def generate_bubble_chart(self):
        try:
            # Generate and display the bubble chart using the stored common words
            if hasattr(self, 'common_words'):
                self.generate_word_cloud(self.common_words)
                logging.info("Bubble chart generated successfully.")
            else:
                self.show_info("Please analyze the chat.db file first.")

        except Exception as e:
            logging.error(f"An error occurred during bubble chart generation: {e}")
            self.show_error(f"An error occurred: {e}")

    def generate_word_cloud(self, common_words):
        # Extract words and counts from common_words
        words, counts = zip(*common_words)

        # Create a Bubble Chart using Plotly Express
        fig = px.scatter(x=words, y=counts, size=counts, size_max=50, text=words, hover_name=words)

        # Configure the layout
        fig.update_layout(
            title="Word Cloud Bubble Chart",
            xaxis_title="Words",
            yaxis_title="Count",
            xaxis=dict(type='category'),  # Ensure words are treated as categories
        )

        # Display the Bubble Chart
        fig.show()

    def translate_words(self):
        try:
            if hasattr(self, 'common_words') and self.common_words:
                selected_language = self.language_var.get()
                if selected_language == "Select Language":
                    self.show_info("Please select a language for translation.")
                    return

                translated_words = Translator.translate_to_language(self.common_words, selected_language)

                # Display the translated words side by side with the original words
                result_text_content = "Original Words\t\t\tTranslated Words\n\n"
                for (original_word, count), translated_word in zip(self.common_words, translated_words):
                    result_text_content += f"{original_word.capitalize()}: {count}\t\t\t{translated_word.capitalize()}\n"

                self.result_text.delete(1.0, tk.END)  # Clear existing content
                self.result_text.insert(tk.END, result_text_content)

            else:
                self.show_info("Please analyze the chat.db file first.")

        except Exception as e:
            logging.error(f"An error occurred during translation: {e}")
            self.show_error(f"An error occurred during translation: {e}")

    def show_info(self, message):
        messagebox.showinfo("Info", message)

    def show_error(self, message):
        messagebox.showerror("Error", message)
