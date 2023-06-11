import tkinter as tk

window = tk.Tk()

def settings():
    top_level = tk.Toplevel(window)
    top_level.title("Top level")
    tk.Label(top_level, text="elo").pack()

tk.Label(window, text="Hello World!").pack()
tk.Button(window, text="Settings", command=settings).pack()
window.mainloop()