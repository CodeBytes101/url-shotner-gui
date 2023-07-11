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
        self.var = ttk.Variable(value="")
        self.result_var = ttk.Variable()
        self.r = 0
        self.label_frame = ttk.Labelframe(self, text="Short-URL", bootstyle="success")
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
            width=30,
            font=("helvetica", 11, "italic"),
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
            self, text="Quit", bootstyle="danger-outline", command=self.destroy
        )
        self.result_label = ttk.Label(
            self.label_frame,
            text="",
            font=("helvetica", 16, "italic"),
            textvariable=self.result_var,
            bootstyle="success",
            border=3,
            foreground="white",
        )
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
            threading.Thread(target=self.link_shorten).start()
            self.animate()

    def animate(self):
        if self.load and self.result_var.get() == "":
            self.r -= 1.5
            self.load.configure(image=ImageTk.PhotoImage(self.load_img.rotate(self.r)))
            self.after(1, self.load_animate)

        elif self.result_var.get() != "":
            self.load.place_forget()
            self.label_frame.place(relx=0.5, rely=0.55, anchor="center")
            self.result_label.place(relx=0.5, rely=0.5, anchor="center")

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
            self.label_frame.configure(text="Info", bootstyle="warning")
            self.result_var.configure(color="Yellow")
            self.result_var.set("Something Went Wrong")

        else:
            self.result_var.set(response)


if __name__ == "__main__":
    app = App("solar")
