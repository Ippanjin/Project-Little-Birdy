
import sys
import twitter
import json
from woeid import alphSorted_woeid_list as woeid_data
import copy
from PIL import Image, ImageTk



import tkinter as tk
from tkinter import ttk
from tkinter import messagebox



def getIndex(listbox):
    items = []
    for i in listbox.curselection():
        items.append(listbox.get(i))

    print(items)



root = tk.Tk()
root.title(" Twitter Data Analysis")
root.geometry("1000x700")

listbox = tk.Listbox(root)
listbox.pack()
listbox.bind("<<ListboxSelect>>", lambda _ : print(fuckshit(listbox)))

combobox = ttk.Combobox(root)
combobox['values'] = ("tard", "shit")
combobox.pack()
combobox.bind("<<ComboboxSelected>>", lambda _ : print("FUCK!"))

listbox.insert(tk.END, "a list entry")

for item in ["one", "two", "three", "four"]:
    listbox.insert(tk.END, item)



image = Image.open('File.png')
render = ImageTk.PhotoImage(image)

labelFrame = tk.LabelFrame(root, text ="Testing stuff")
some_frame = tk.Frame(labelFrame, width = 400, height = 400)
some_frame.pack()
labelFrame.place(x = 100, y = 100)

button = tk.Button(labelFrame, text = "FUCK", width = 100)
button.pack()

print(help(listbox))

label = tk.Label(root, image = render)
label.place(x = 0, y = 200)

tk.mainloop()
