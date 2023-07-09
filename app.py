import ttkbootstrap as ttk
import customtkinter as ctk
import requests
import json


class App(ttk.Window):
    def __init__(self, theme):
        super().__init__(themename=theme)
        self.geometry("350x225")
        self.title("URL-Shortener")
        self.iconbitmap("images\logo.ico")
        self.var = ttk.StringVar()
        self.label = ttk.Label(self, text="URL", font=("helvetica", 15, "italic"))
        self.label.place(relx=0.5, rely=0.35, anchor="center")
        self.entry = ttk.Entry(
            self,
            textvariable=self.var,
            width=25,
            font=("helvetica", 12, "italic"),
            foreground="white",
            bootstyle="success",
        )
        self.submit_btn = ttk.Button(
            self,
            text="Submit",
            font=("helvetica", 14, "normal"),
            bootstyle="success-outline",
        )
        self.reset_btn = ttk.Button(
            self,
            text = 'Reset',
            font = ('helvetica',14,'normal'),
            bootstyle = 'success-outline'

        )
        self.quit_btn = ttk.Button(
            self,
            text = 'Quit',
            font = ('helvetica',14,'normal'),
            bootstyle = 'danger-outline'
        )
        self.clear_btn = ttk.Button(
            self,
            text = '',
            image
        )

        self.entry.place(relx=0.5, rely=0.5, anchor="center")
        self.entry.bind('<KeyRelease>',lambda _ : self.create(_))
        self.mainloop()
    def create(self,_):
        self.submit_btn.place(relx = 0.5,rely = 0.6,anchor='center')
        self.

if __name__ == "__main__":
    app = App("solar")
