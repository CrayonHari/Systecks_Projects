import tkinter as tk
from tkinter import filedialog, messagebox
import ttkbootstrap as ttk
import cv2
from PIL import Image, ImageTk

class ImgtoSketch:
    def __init__(self, master):
        self.master = master
        master.title("Image-to-Sketch Converter")
        self.style = ttk.Style()
        self.style.theme_use('superhero')

        self.line_thickness = tk.IntVar()
        self.contrast = tk.IntVar()
        self.brightness = tk.IntVar()

        self.create_widgets()

    def create_widgets(self):
        self.title_label = ttk.Label(self.master, text="Image to Sketch Converter", font=("Helvetica", 24, "bold"))
        self.title_label.pack(pady=20)

        self.upload_button = ttk.Button(self.master, text="Upload an Image", command=self.browse_image)
        self.upload_button.pack(pady=10)

        self.main_frame = ttk.Frame(self.master)
        self.main_frame.pack()

        self.uploaded_image_label = ttk.Label(self.main_frame)
        self.uploaded_image_label.pack(padx=10, pady=10, side=tk.LEFT)

        self.sketch_image_label = ttk.Label(self.main_frame)
        self.sketch_image_label.pack(padx=10, pady=10, side=tk.RIGHT)

        self.button_frame = ttk.Frame(self.master)
        self.button_frame.pack(pady=10)

        self.save_button = ttk.Button(self.button_frame, text="Save to Computer", command=self.save_sketch)
        self.save_button.pack(pady=10)
        self.save_button.pack_forget()

    def browse_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.display_uploaded_image(file_path)
            self.add_parameter_sliders()

    def display_uploaded_image(self, file_path):
        self.original_image = cv2.imread(file_path)
        uploaded_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2RGB)
        uploaded_image = cv2.resize(uploaded_image, (300, 300))
        uploaded_image = Image.fromarray(uploaded_image)
        self.uploaded_photo = ImageTk.PhotoImage(uploaded_image)
        self.uploaded_image_label.configure(image=self.uploaded_photo)
        self.uploaded_image_label.image = self.uploaded_photo

    def add_parameter_sliders(self):
        for widget in self.button_frame.winfo_children():
            if isinstance(widget, (ttk.Scale, ttk.Label)):
                widget.destroy()

        self.line_thickness_label = ttk.Label(self.button_frame, text="Line Thickness:")
        self.line_thickness_label.pack(pady=5)

        self.line_thickness_scale = ttk.Scale(self.button_frame, from_=1, to=10, orient=tk.HORIZONTAL,
                                              variable=self.line_thickness)
        self.line_thickness_scale.set(5)
        self.line_thickness_scale.pack(pady=5)
        self.line_thickness_scale.bind("<ButtonRelease-1>", self.update_sketch)

        self.contrast_label = ttk.Label(self.button_frame, text="Contrast:")
        self.contrast_label.pack(pady=5)

        self.contrast_scale = ttk.Scale(self.button_frame, from_=0, to=100, orient=tk.HORIZONTAL,
                                        variable=self.contrast)
        self.contrast_scale.set(50)
        self.contrast_scale.pack(pady=5)
        self.contrast_scale.bind("<ButtonRelease-1>", self.update_sketch)

        self.brightness_label = ttk.Label(self.button_frame, text="Brightness:")
        self.brightness_label.pack(pady=5)

        self.brightness_scale = ttk.Scale(self.button_frame, from_=-100, to=100, orient=tk.HORIZONTAL,
                                          variable=self.brightness)
        self.brightness_scale.set(0)
        self.brightness_scale.pack(pady=5)
        self.brightness_scale.bind("<ButtonRelease-1>", self.update_sketch)

        self.save_button.pack(in_=self.button_frame)

        self.convert_to_sketch()

    def update_sketch(self, event):
        if self.line_thickness.get() % 2 == 0:
            self.line_thickness.set(self.line_thickness.get() + 1)
        if self.contrast.get() % 2 == 0:
            self.contrast.set(self.contrast.get() + 1)
        self.convert_to_sketch()

    def convert_to_sketch(self):
        try:
            line_thickness = self.line_thickness.get()
            contrast = self.contrast.get() / 50.0
            brightness = self.brightness.get()

            adjusted_image = cv2.convertScaleAbs(self.original_image, alpha=contrast, beta=brightness)

            gray_image = cv2.cvtColor(adjusted_image, cv2.COLOR_BGR2GRAY)
            invert_image = cv2.bitwise_not(gray_image)

            ksize = line_thickness if line_thickness % 2 != 0 else line_thickness + 1

            blur_image = cv2.GaussianBlur(invert_image, (ksize, ksize), 0)
            invert_blur = cv2.bitwise_not(blur_image)
            self.sketch = cv2.divide(gray_image, invert_blur, scale=256.0)
            self.sketch = cv2.GaussianBlur(self.sketch, (line_thickness, line_thickness), 0)
            self.sketch = cv2.cvtColor(self.sketch, cv2.COLOR_GRAY2RGB)
            self.sketch = cv2.resize(self.sketch, (300, 300))

            sketch_image = Image.fromarray(self.sketch)
            self.sketch_photo = ImageTk.PhotoImage(sketch_image)
            self.sketch_image_label.configure(image=self.sketch_photo)
            self.sketch_image_label.image = self.sketch_photo

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def save_sketch(self):
        try:
            if self.sketch is not None:
                sketch_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
                if sketch_path:
                    cv2.imwrite(sketch_path, self.sketch)
                    messagebox.showinfo("Success", "Sketch saved successfully!")
            else:
                messagebox.showwarning("Warning", "No sketch to save.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")


root = ttk.Window(themename='superhero')
root.minsize(700, 1)
root.maxsize(700, 1000)
app = ImgtoSketch(root)
root.mainloop()
