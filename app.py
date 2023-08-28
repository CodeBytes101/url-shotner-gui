import ttkbootstrap as ttk
from PIL import Image, ImageTk
import requests
import threading
from tkinter import ttk as tk
import customtkinter as ctk
import pyperclip
import os


def image_parser(path: str, size: tuple):
    img = Image.open(path).resize(size)
    return ImageTk.PhotoImage(img)


class App(ttk.Window):
    def __init__(self, theme):
        super().__init__(themename=theme)
        self.geometry("525x375")
        self.maxsize(width=525, height=375)
        self.minsize(width=525, height=375)
        self.x = -0.4
        threading.Thread(target=self.link_fetcher).start()
        self.shorturls = []
        self.toggle_frame = tk.Frame(self, height=325, width=240, bootstyle="dark")
        self.table = ttk.Treeview(
            self.toggle_frame, columns=("URL's"), show="headings", bootstyle="info"
        )
        self.table.heading("URL's", text="URL's")
        self.back_btn = ctk.CTkButton(
            self.toggle_frame,
            text="",
            image=image_parser(r"images\back.png", (18, 18)),
            height=18,
            fg_color="#0B5162",
            width=15,
            corner_radius=10,
            command=self.animate_backward,
        )
        self.selected_url = ""
        self.toggle_frame.place(relx=self.x, rely=0.52, anchor="center")
        self.toggle_btn = ctk.CTkButton(
            self,
            text="",
            image=image_parser("images\menu.png", (20, 20)),
            fg_color="#002B36",
            height=20,
            width=20,
            command=self.animate_forward,
        )
        self.toggle_btn.place(relx=0.05, rely=0.05, anchor="center")
        self.table.place(relx=0.5, rely=0.53, anchor="center")
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
        self.endpoint = "https://sizl.ink/api/url/add"
        self.authentication = os.environ.get(
            "URL_TOKEN"
        )  # save your api key under the name of URLTOKEN into the system environment variables
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
            bootstyle="success-outline",  # type: ignore
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
            bootstyle="danger-outline",  # type: ignore
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
        self.entry.bind("<KeyRelease>", lambda _: self.submit_btn.place(relx=0.5, rely=0.7, anchor="center")
)
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
        self.result_label.configure(font=16, foreground="white")

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

    def link_shorten(self):
        headers = {
            "Authorization": f"Bearer {self.authentication}",
            "Content-Type": "application/json",
        }
        payload = {"url": self.var.get()}
        response = requests.post(self.endpoint, json=payload, headers=headers)
        status = response.status_code
        response = response.json().get("shorturl")
        if status != 200:
            threading.Thread(target=self.link_fetcher).start()
            self.label_frame.configure(bootstyle="warning", text="Error")
            self.result_label.configure(font=9, foreground="yellow")

            if status == 403:
                self.result_var.set("Service Unavailable")
        else:
            self.result_var.set(response)

    def animate_forward(self):
        self.toggle_btn.place_forget()
        if self.x < 0.26:
            self.x += 0.01
            self.toggle_frame.lift()
            self.toggle_frame.place(relx=self.x, rely=0.5, anchor="center")
            self.after(1, self.animate_forward)
        self.back_btn.place(relx=0.93, rely=0.06, anchor="center")

    def animate_backward(self):
        if self.x >= -0.4:
            self.x -= 0.01
            self.toggle_frame.place(relx=self.x, rely=0.5, anchor="center")
            self.after(1, self.animate_backward)
        self.back_btn.place_forget()
        self.toggle_btn.place(relx=0.05, rely=0.05, anchor="center")

    def link_fetcher(self):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.authentication}",
        }
        response = requests.get("https://sizl.ink/api/urls", headers=headers)
        data = (response.json()).get("data").get("urls")
        try:
            for i in data:
                self.shorturls.append(i.get("shorturl"))
            for i in self.shorturls:
                self.table.insert("", index="end", values=(i))
        except:
            print("Error")


if __name__ == "__main__":
    app = App("solar")
