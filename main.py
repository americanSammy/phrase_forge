# main.py
import tkinter as tk
from gui import MessageAnalyzerGUI

def main():
    root = tk.Tk()
    gui = MessageAnalyzerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
