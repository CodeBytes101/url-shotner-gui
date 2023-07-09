import ttkbootstrap as ttk
from PIL import Image, ImageTk
import requests
import threading
import customtkinter as ctk


class App(ttk.Window):
    def __init__(self, theme):
        super().__init__(themename=theme)
        self.geometry("500x350")
        self.title("URL-Shortener")
        self.iconbitmap("images\logo.ico")
        self.var = ttk.StringVar()
        self.result_var = ttk.StringVar(value="")
        self.r = 0
        self.load_img = Image.open("images\loading.png").resize((25, 25))
        self.load = ctk.CTkLabel(
            self, text="", image=ImageTk.PhotoImage(self.load_img.rotate(self.r))
        )
        self.endpoint = "https://api-ssl.bitly.com/v4/shorten"
        self.authentication = "41dd6d539c0cb4b23d427a23ca9f992906073e02"
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
            bootstyle="success-outline",
            command=self.submit_handler,
        )
        self.reset_btn = ttk.Button(
            self,
            text="Reset",
            bootstyle="success-outline",
        )
        self.quit_btn = ttk.Button(
            self,
            text="Quit",
            bootstyle="danger-outline",
        )
        self.result_label = ttk.Label(self, text="", textvariable=self.result_var)
        self.entry.place(relx=0.5, rely=0.5, anchor="center")
        self.entry.bind("<KeyRelease>", lambda _: self.create(_))
        self.mainloop()

    def submit_handler(self):
        if self.var.get() != "":
            self.label.place_forget()
            self.submit_btn.place_forget()
            self.entry.place_configure(rely=0.3)
            self.entry.configure(state="readonly")
            self.load.place(relx=0.5, rely=0.6, anchor="center")
            self.load_animate()
            threading.Thread(target=self.link_shorten)

    def load_animate(self):
        if self.load and self.result_var.get() == "":
            self.r -= 1.5
            self.load.configure(image=ImageTk.PhotoImage(self.load_img.rotate(self.r)))
            self.after(1, self.load_animate)
        else:
            self.load.place_forget()
            self.result_label.place(relx=0.5, rely=0.55, anchor="center")

    def create(self, _):
        self.submit_btn.place(relx=0.5, rely=0.7, anchor="center")

    def link_shorten(self):
        headers = {
            "Authorization": f"Bearer {self.authentication}",
            "Content-Type": "application/json",
        }
        payload = {"long_url": self.var}
        response = requests.post(self.endpoint, json=payload, headers=headers)
        self.result_var.set(response.json().get("link"))


if __name__ == "__main__":
    app = App("solar")
