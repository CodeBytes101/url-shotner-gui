import ttkbootstrap as ttk
from PIL import Image, ImageTk
import requests
import threading
import customtkinter as ctk
import pyperclip


def image_parser(path: str, size: tuple):
    img = Image.open(path).resize(size)
    return ImageTk.PhotoImage(img)


class App(ttk.Window):
    def __init__(self, theme):
        super().__init__(themename=theme)
        self.geometry("500x350")
        self.maxsize(width=500, height=350)
        self.minsize(width=500, height=350)
        self.title("URL-Shortener")
        self.iconbitmap("images\logo.ico")
        self.var = ttk.Variable(value="")
        self.result_var = ttk.Variable()
        self.r = 0
        self.btn_frame = ttk.Frame(self)
        self.label_frame = ttk.Labelframe(
            self, text="Short-URL", bootstyle="success", height=150, width=360
        )
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
            width=40,
            font=("helvetica", 11, "italic"),
            foreground="white",
            bootstyle="success",
        )
        self.copy_btn = ctk.CTkButton(
            self.label_frame,
            text="",
            image=image_parser("images\copy.png", (16, 16)),
            height=16,
            width=16,
            fg_color="#002B36",
            command=lambda: pyperclip.copy(self.result_var.get()),
        )

        self.submit_btn = ttk.Button(
            self,
            text="Submit",
            bootstyle="success-outline",
            command=self.submit_handler,
        )
        self.reset_btn = ttk.Button(
            self.btn_frame,
            text="Reset",
            bootstyle="success-outline",
        )
        self.quit_btn = ttk.Button(
            self.btn_frame,
            text="Quit",
            bootstyle="danger-outline",
            command=self.destroy,
        )
        self.result_label = ttk.Label(
            self.label_frame,
            text="",
            font=("helvetica", 16, "italic"),
            textvariable=self.result_var,
            bootstyle="success",
            foreground="white",
        )
        self.quit_btn.place(relx=0.45, rely=85, anchor="center")
        self.reset_btn.place(relx=0.65, rely=0.85, anchor="center")
        self.entry.place(relx=0.5, rely=0.5, anchor="center")
        self.entry.bind("<KeyRelease>", lambda _: self.create(_))
        self.mainloop()

    def submit_handler(self, event=None):
        if self.var.get() != "":
            self.label.place_forget()
            self.submit_btn.place_forget()
            self.entry.place_configure(rely=0.2)
            self.entry.configure(state="readonly")
            self.load.place(relx=0.5, rely=0.6, anchor="center")
            threading.Thread(target=self.link_shorten).start()
            self.animate()

    def animate(self):
        if self.load and self.result_var.get() == "":
            self.r -= 1.5
            self.load.configure(image=ImageTk.PhotoImage(self.load_img.rotate(self.r)))
            self.after(1, self.animate)

        elif self.result_var.get() != "":
            self.load.place_forget()
            self.label_frame.place(relx=0.5, rely=0.6, anchor="center")
            self.result_label.place(relx=0.5, rely=0.38, anchor="center")
            self.copy_btn.place(relx=0.95, rely=0.05, anchor="center")
            self.btn_frame.place(relx=0.5, rely=0.85, anchor="center")

    def create(self, _):
        self.submit_btn.place(relx=0.5, rely=0.7, anchor="center")

    def link_shorten(self):
        headers = {
            "Authorization": f"Bearer {self.authentication}",
            "Content-Type": "application/json",
        }
        payload = {"long_url": self.var.get()}
        response = requests.post(self.endpoint, json=payload, headers=headers)
        status = response.status_code
        response = response.json().get("link")
        if status != 200:
            self.label_frame.configure(bootstyle="warning", text="Error")
            self.result_label.configure(font=9, foreground="yellow")
        self.result_var.set(response)


if __name__ == "__main__":
    app = App("solar")
