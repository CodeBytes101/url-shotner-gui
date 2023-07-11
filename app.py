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
        self.geometry("525x375")
        self.maxsize(width=525, height=375)
        self.minsize(width=525, height=375)
        self.title("URL-Shortener")
        self.iconbitmap("images\logo.ico")
        self.var = ttk.Variable(value="")
        self.result_var = ttk.Variable(value="")
        self.r = 0
        self.btn_frame = ttk.Frame(self, width=150, height=125)
        self.label_frame = ttk.Labelframe(
            self, text="Short-URL", bootstyle="success", height=130, width=380
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
            command=self.reset,
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
        self.quit_btn.pack(side="left", pady=20)
        self.reset_btn.pack(side="left", pady=20, padx=10)
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

    def reset(self):
        self.result_var.set("")
        self.var.set("")
        self.btn_frame.place_forget()
        self.label_frame.place_forget()
        self.entry.configure(state="normal")
        self.entry.place_configure(relx=0.5, rely=0.5, anchor="center")
        self.label.place(relx=0.5, rely=0.35, anchor="center")
        self.label_frame.configure(bootstyle="success", text="Short-URL")
        self.result_label.configure(font=12, foreground="white")

    def animate(self):
        if self.load and self.result_var.get() == "":
            self.r -= 1.5
            self.load.configure(image=ImageTk.PhotoImage(self.load_img.rotate(self.r)))
            self.after(1, self.animate)

        elif self.result_var.get() != "":
            self.load.place_forget()
            self.label_frame.place(relx=0.5, rely=0.5, anchor="center")
            self.result_label.place(relx=0.5, rely=0.5, anchor="center")
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
            self.result_var.set("Enter a valid URL")
        else:
            self.result_var.set(response)


if __name__ == "__main__":
    app = App("solar")
