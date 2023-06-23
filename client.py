import socket
from threading import Thread
from tkinter import *

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

nickname = input("Enter your nickname: ")

ip_address = "127.0.0.1"
port = 8000

conn = client.connect((ip_address, port))

print("Connected to the server")

class GUI:
    def __init__(self):
        self.Window = Tk()
        self.Window.withdraw()

        self.login = Toplevel()
        self.login.title("Login")
        self.login.resizable(width = False, height = False)
        self.login.configure(width = 400, height = 300)

        self.pls = Label(
            self.login,
            text = "Please login to continue",
            justify = CENTER,
            font = "Helvetica 14 bold")
        self.pls.place(relheight = 0.15, relx = 0.25, rely = 0.05)

        self.name_label = Label(self.login, text = "Name", font = "Helvetica 12")
        self.name_label.place(relheight = 0.4, relx = 0.1, rely = 0.075)

        self.name_entry = Entry(self.login, font = "Helvetica 14")
        self.name_entry.place(relwidth = 0.4, relheight = 0.12, relx = 0.35, rely = 0.2)
        self.name_entry.focus()

        self.button = Button(
            self.login,
            text = "Continue",
            font = "Helvetica 14 bold",
            command = lambda: self.go(self.name_entry.get())
        )
        self.button.place(relx = 0.4, rely = 0.5)

        self.Window.mainloop()

    def go(self, name):
        self.login.destroy()
        self.layout(name)

        thread = Thread(target = self.receive)
        thread.start()

    def receive(self):
        while True:
            try:
                message = client.recv(2048).decode("utf-8")
                if message == "nickname":
                    client.send(self.name.encode("utf-8"))
                else:
                    self.show_msg(message)
            except:
                print("An error occured!")
                client.close()
                break

    def write(self):
        self.text.config(state = DISABLED)
        while True:
            msg = f"{self.name}: {self.msg}"
            client.send(msg.encode("utf-8"))
            self.show_msg(msg)
            break

    def layout(self, name):
        self.name = name

        self.Window.deiconify()
        self.Window.title("Quiz")
        self.Window.resizable(width = False, height = False)
        self.Window.configure(width = 470, height = 550, bg = "#17202A")

        self.head = Label(
            self.Window,
            bg = "#17202A",
            fg = "#EAECEE",
            text = self.name,
            font = "Helvetica 13 bold",
            pady = 5
        )
        self.head.place(relwidth = 1)

        self.line = Label(self.Window, width = 450, bg = "#ABB2B9")
        self.line.place(relwidth = 1, relheight = 0.012, rely = 0.07)

        self.text = Text(
            self.Window,
            width = 20,
            height = 2,
            bg = "#17202A",
            fg = "#EAECEE",
            font = "Helvetica 14",
            padx = 5,
            pady = 5
        )
        self.text.place(relwidth = 1, relheight = 0.745, rely = 0.08)

        self.bottom_label = Label(self.Window, height = 80, bg = "#ABB2B9")
        self.bottom_label.place(relwidth = 1, rely = 0.825)

        self.entry = Entry(self.bottom_label, bg = "#2C3E50", fg = "#EAECEE", font = "Helvetica 13")
        self.entry.place(relwidth = 0.74, relheight = 0.06, relx = 0.011, rely = 0.008)
        self.entry.focus()

        self.send_button = Button(
            self.bottom_label,
            text = "Send",
            font = "Helvetica 10 bold",
            width = 20,
            bg = "#ABB2B9",
            command = lambda: self.send(self.entry.get())
        )
        self.send_button.place(relwidth = 0.22, relheight = 0.06, relx = 0.77, rely = 0.008)

        self.text.config(cursor = "arrow")

        scroll_bar = Scrollbar(self.text)
        scroll_bar.place(relheight = 1, relx = 0.974)
        scroll_bar.config(command = self.text.yview)

    def send(self, msg):
        self.text.config(state = DISABLED)
        self.msg = msg
        self.entry.delete(0, END)

        send_thread = Thread(target = self.write)
        send_thread.start()

    def show_msg(self, msg):
        self.text.config(state = NORMAL)
        self.text.insert(END, f"{msg}\n\n")
        self.text.config(state = DISABLED)
        self.text.see(END)

g = GUI()