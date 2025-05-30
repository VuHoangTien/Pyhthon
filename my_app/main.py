import tkinter as tk
from views.Login_Gui import logingui

if __name__ == "__main__":
    root = tk.Tk()
    app = logingui(master=root)
    app.mainloop() 