import tkinter as tk
from tkinter import messagebox, ttk
import os
import sys
from dotenv import load_dotenv, set_key
import config

# Load environment variables from .env file
load_dotenv()

# Read API keys from environment variables
DEEPTR_RAPID_API = os.getenv("DEEPTR_RAPID_API", "")
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY", "")

# Default values from config.py
push_to_talk_key = config.push_to_talk_key
character = config.character

# Function to save to .env file
def save_to_env_file():
    set_key(".env", "DEEPTR_RAPID_API", DEEPTR_RAPID_API)
    set_key(".env", "DEEPGRAM_API_KEY", DEEPGRAM_API_KEY)

# Function to save to config.py
def save_to_config_py():
    with open('config.py', 'w') as f:
        f.write(f"push_to_talk_key = '{push_to_talk_key}'\n")
        f.write(f"character = {character}\n")

# Function to restart the program
def restart_program():
    python = sys.executable
    os.execl(python, python, *sys.argv)

# Function to save the settings
def save_settings():
    global push_to_talk_key, character, DEEPTR_RAPID_API, DEEPGRAM_API_KEY
    push_to_talk_key = push_to_talk_key_var.get()
    character = character_var.get()
    DEEPTR_RAPID_API = deeptr_api_var.get()
    DEEPGRAM_API_KEY = deepgram_api_var.get()

    if not DEEPTR_RAPID_API or not DEEPGRAM_API_KEY:
        messagebox.showerror("Error", "API keys are required!")
        return

    # Save settings to files
    save_to_env_file()
    save_to_config_py()
    
    # Restart program to apply settings
    restart_program()

# Function to start the program
def start_program():
    import main
    main.run()  # Assuming you have a function called `run()` in main.py

# Initialize the main window
root = tk.Tk()
root.title("Voice Program Configuration")
root.geometry("400x300")
root.configure(bg="#FFD700")  # Gold background for a colorful interface

# Variables for settings
push_to_talk_key_var = tk.StringVar(value=push_to_talk_key)
character_var = tk.StringVar(value=str(character))
deeptr_api_var = tk.StringVar(value=DEEPTR_RAPID_API)
deepgram_api_var = tk.StringVar(value=DEEPGRAM_API_KEY)

# Push-to-Talk Key
tk.Label(root, text="Push to Talk Key:", bg="#FFD700").grid(row=0, column=0, padx=10, pady=10)
push_to_talk_key_entry = tk.Entry(root, textvariable=push_to_talk_key_var)
push_to_talk_key_entry.grid(row=0, column=1, padx=10, pady=10)

# Character selection
tk.Label(root, text="Character:", bg="#FFD700").grid(row=1, column=0, padx=10, pady=10)
character_dropdown = ttk.Combobox(root, textvariable=character_var, values=[str(i) for i in range(1, 6)])
character_dropdown.grid(row=1, column=1, padx=10, pady=10)
character_dropdown.bind("<<ComboboxSelected>>", lambda event: character_var.set(character_dropdown.get()))

# DeepTranslate API Key
tk.Label(root, text="DeepTranslate API Key:", bg="#FFD700").grid(row=2, column=0, padx=10, pady=10)
deeptr_api_entry = tk.Entry(root, textvariable=deeptr_api_var)
deeptr_api_entry.grid(row=2, column=1, padx=10, pady=10)

# Deepgram API Key
tk.Label(root, text="Deepgram API Key:", bg="#FFD700").grid(row=3, column=0, padx=10, pady=10)
deepgram_api_entry = tk.Entry(root, textvariable=deepgram_api_var)
deepgram_api_entry.grid(row=3, column=1, padx=10, pady=10)

# Save Button
save_button = tk.Button(root, text="Save Settings", command=save_settings, bg="#32CD32", fg="white")
save_button.grid(row=4, column=0, columnspan=2, pady=10)

# Run Button
run_button = tk.Button(root, text="Run", command=start_program, bg="#1E90FF", fg="white")
run_button.grid(row=5, column=0, columnspan=2, pady=10)

# Start the main loop
root.mainloop()
