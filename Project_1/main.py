import tkinter as tk
import re
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


def generate():

    # validation for name  if flag not equal to 0 then pop msg all fields are mandatory.
    flag = 5

    if name.get().isalpha():
        name_msg.set("")
        flag -= 1
    elif len(name.get()) == 0:
        name_msg.set("*This field is mandatory")
    else:
        name_msg.set('*Name field must only contain alphabets')

    # validation for aicte  sample
    if aicte.get().isalnum() and (len(aicte.get()) == 26):
        aicte_msg.set("")
        flag -= 1
    elif len(aicte.get()) == 0:
        aicte_msg.set("*This field is mandatory")
    elif len(aicte.get()) != 26:
        aicte_msg.set("*AICTE ID must be 26 characters")
    else:
        aicte_msg.set("*AICTE ID doesn't contain symbols")

    # email
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if len(email.get()) == 0:
        email_msg.set("*This field is mandatory")
    elif re.fullmatch(pattern, email.get()):
        email_msg.set("")
        flag -= 1
    else:
        email_msg.set("*Invalid Email ID")

    # mobile
    if len(phone.get()) == 0:
        phone_msg.set("*This field is mandatory")
    elif (len(phone.get()) == 10) and phone.get().isnumeric():
        phone_msg.set("")
        flag -= 1
    else:
        phone_msg.set("*Invalid Mobile Number")

    # clg
    if len(clg.get()) == 0:
        clg_msg.set("*This field is mandatory")
    else:
        clg_msg.set("")
        flag -= 1

    if flag == 0:
        ttk.dialogs.dialogs.Messagebox.show_info('You have registered successfully', title="Success")

        c = canvas.Canvas("{}.pdf".format(name.get()), pagesize=(500, 250))
        c.roundRect(15, 15, 470, 220, radius=20, stroke=1, fill=0)
        c.setFont("Helvetica-Bold", 32)
        c.drawCentredString(x=250, y=200, text="Student Details")
        c.setFont("Helvetica-Bold", 18)
        c.drawString(x=30, y=155, text="Name")
        c.drawString(x=30, y=125, text="AICTE ID")
        c.drawString(x=30, y=95, text="Email")
        c.drawString(x=30, y=65, text="Mobile Number")
        c.drawString(x=30, y=35, text="College Name")

        c.drawString(x=180, y=155, text=":")
        c.drawString(x=180, y=125, text=":")
        c.drawString(x=180, y=95, text=":")
        c.drawString(x=180, y=65, text=":")
        c.drawString(x=180, y=35, text=":")

        c.setFont("Helvetica", 16)
        c.drawString(x=210, y=155, text=name.get())
        c.drawString(x=210, y=125, text=aicte.get())
        c.drawString(x=210, y=95, text=email.get())
        c.drawString(x=210, y=65, text=phone.get())
        c.drawString(x=210, y=35, text=clg.get())

        name_entry.delete(0, END)
        aicte_entry.delete(0, END)
        email_entry.delete(0, END)
        phone_entry.delete(0, END)
        clg_entry.delete(0, END)

        c.save()
        c.showPage()
        app.destroy()

    else:
        app.bell()

# creating window
app = ttk.Window(themename='morph')
app.title("SRF_Project_1")
app.geometry("540x800")
app.resizable(False,False)

# variables
name = tk.StringVar()
name_msg = tk.StringVar()
aicte = tk.StringVar()
aicte_msg = tk.StringVar()
email = tk.StringVar()
email_msg = tk.StringVar()
phone = tk.StringVar()
phone_msg = tk.StringVar()
clg = tk.StringVar()
clg_msg = tk.StringVar()

# creating labels, entries and button
heading = ttk.Label(master=app, text='Student Registration Form', padding=20, font=("Helvetica", 24), borderwidth=1, relief='groove', border=-10)
frame = ttk.Frame(master=app, padding=30)

name_label = ttk.Label(master=frame, text='Name', font=("Helvetica", 14))
name_entry = ttk.Entry(master=frame, textvariable=name, font=("Helvetica", 14))
name_error = ttk.Label(master=frame, textvariable=name_msg, font=("Helvetica", 8), foreground='red')

aicte_label = ttk.Label(master=frame, text='AICTE ID', font=("Helvetica", 14))
aicte_entry = ttk.Entry(master=frame, textvariable=aicte, font=("Helvetica", 14))
aicte_error = ttk.Label(master=frame, textvariable=aicte_msg, font=("Helvetica", 8), foreground='red')

email_label = ttk.Label(master=frame, text='Email Address', font=("Helvetica", 14))
email_entry = ttk.Entry(master=frame, textvariable=email, font=("Helvetica", 14))
email_error = ttk.Label(master=frame, textvariable=email_msg, font=("Helvetica", 8), foreground='red')

phone_label = ttk.Label(master=frame, text='Mobile Number', font=("Helvetica", 14))
phone_entry = ttk.Entry(master=frame, textvariable=phone, font=("Helvetica", 14))
phone_error = ttk.Label(master=frame, textvariable=phone_msg, font=("Helvetica", 8), foreground='red')

clg_label = ttk.Label(master=frame, text='College Name', font=("Helvetica", 14))
clg_entry = ttk.Entry(master=frame, textvariable=clg, font=("Helvetica", 14))
clg_error = ttk.Label(master=frame, textvariable=clg_msg, font=("Helvetica", 8), foreground='red')

btn = ttk.Button(master=app, text='Submit', command=generate, bootstyle=PRIMARY)

# packing all the widgets
heading.pack(pady=10)
frame.pack(pady=5)

name_label.pack(pady=5, anchor='w')
name_entry.pack(pady=5)
name_error.pack(anchor='w')

aicte_label.pack(pady=5, anchor='w')
aicte_entry.pack(pady=5)
aicte_error.pack(anchor='w')

email_label.pack(pady=5, anchor='w')
email_entry.pack(pady=5)
email_error.pack(anchor='w')

phone_label.pack(pady=5, anchor='w')
phone_entry.pack(pady=5)
phone_error.pack(anchor='w')

clg_label.pack(pady=5, anchor='w')
clg_entry.pack(pady=5)
clg_error.pack(anchor='w')

btn.pack(pady=5)

app.mainloop()
