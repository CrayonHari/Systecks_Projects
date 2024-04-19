import tkinter as tk
from tkinter import filedialog, messagebox
import ttkbootstrap as ttk
import pyttsx3


class TextToSpeechApp:
    def __init__(self, master):
        self.master = master
        master.title("Text-to-Speech Converter")

        # Apply ttkbootstrap style
        style = ttk.Style()
        self.segments = []

        # Text Input Field
        self.text_entry = ttk.Text(master, height=5, width=50)
        self.text_entry.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        # Voice Selection Dropdown
        self.voice_label = ttk.Label(master, text="Select Voice:")
        self.voice_label.grid(row=1, column=0)
        self.voice_var = tk.StringVar()
        self.voice_dropdown = ttk.Combobox(master, textvariable=self.voice_var)
        self.voice_dropdown['values'] = ['Male', 'Female']  # Add more voices as needed
        self.voice_dropdown.grid(row=1, column=1)
        self.voice_dropdown.set('Male')

        # Rate Slider
        self.rate_label = ttk.Label(master, text="Rate:")
        self.rate_label.grid(row=2, column=0)
        self.rate_slider = ttk.Scale(master, from_=0, to=200, orient="horizontal")
        self.rate_slider.grid(row=2, column=1)

        # Play Button
        self.play_button = ttk.Button(master, text="Play", command=self.play_text, width=12)
        self.play_button.grid(row=3, column=0, pady=10)

        # Save Audio Button
        self.save_button = ttk.Button(master, text="Save Audio", command=self.save_audio,width=12)
        self.save_button.grid(row=3, column=1, pady=10)

        # Initialize TTS engine
        self.engine = pyttsx3.init()

    def play_text(self):
        if not self.voice_dropdown.get():
            messagebox.showerror("Error", "Please select a voice.")
            return

        self.engine.stop()

        voice = self.voice_dropdown.get()
        voices = self.engine.getProperty('voices')
        if voice == 'Male':
            self.engine.setProperty('voice', voices[0].id)
        elif voice == 'Female':
            self.engine.setProperty('voice', voices[1].id)

        self.engine.setProperty('rate', int(self.rate_slider.get()))

        text = self.text_entry.get("1.0", tk.END)

        self.engine.say(text)
        self.engine.runAndWait()

    def save_audio(self):
        save_file_path = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("MP3 files", "*.mp3")])
        if save_file_path:
            text = self.text_entry.get("1.0", tk.END)
            self.engine.save_to_file(text, save_file_path)
            self.engine.runAndWait()
            messagebox.showinfo("Success", "Audio saved successfully!")


root = ttk.Window(themename='flatly')
app = TextToSpeechApp(root)
root.mainloop()
