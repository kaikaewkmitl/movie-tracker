import tkinter as tk
from tkinter.font import Font

from tmdb_api.api import p

p()

root = tk.Tk()
root.title("movie tracker")
root.geometry("800x800")

myFont = Font(
    family="Noteworthy",
    size=30,
    weight="bold"
)

frame1 = tk.Frame(root)
frame1.pack(pady=10)

myList = tk.Listbox(frame1,
                    font=myFont,
                    width=25,
                    height=5,
                    bg="white",
                    bd=0,
                    fg="blue",
                    highlightthickness=0,
                    selectbackground="black",
                    activestyle="none"
                    )
myList.pack(side=tk.LEFT)

stuff = ["eat food", "sleep", "learn math", "asdfasf", "apsadfsdafple", "pie"]

for s in stuff:
    myList.insert(tk.END, s)

scrollbar = tk.Scrollbar(frame1)
scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)

myList.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=myList.yview)

root.mainloop()
