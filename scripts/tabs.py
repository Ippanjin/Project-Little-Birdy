# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 12:39:06 2019

@author: Omar
"""

import sys

try:
    import os
    os.chdir("D:\(PC)\Desktop\Coding\Python\Twitter prototype\github\Project-Little-Birdy\scripts")
except:
    pass

import twitter
import json
from urllib.parse import unquote
from woeid import alphSorted_woeid_list as woeid_data
import copy

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import gui_classes as gc
from retweets_tracker import track_tweets

data = [['Consumer key: ', 'OmSLZHzlAonPshptklKq40PXu'],
        ['Consumer secret: ', 'FDDapXwQavn1hJjXVNfftqEPqmnh6ppOSyTt4ljfSGOH8IsFt9'],
        ['OAUTH token: ', '1144962054475804672-1eRvXn1iWcEdOCZyq5mzhIn6L7echV'],
        ['OAUTH token secret: ', 'dapCBtw9xEbM5wHoPu0nuUB51CBho04ouac7a6IJ1AAer']]


def server_init(label):

    try:
        auth = twitter.oauth.OAuth(data[2], data[3], data[0], data[1])
        twitter_api = twitter.Twitter(auth=auth)
        label.config(text = "Connection status: connection success!")

    except:
        label.config(text = "Connection status: connection failure...")


global analysis_data

analysis_data = [[]]

def doNothing():
    print("Ok ok I wont...")

def quitProgram(root):
    root.quit()
    root.destroy()
    sys.exit()

###########################################
# Main program,
############################################



def main():
    # Setting up window , with variable as root
    root = tk.Tk()
    root.title(" Twitter Data Analysis")
    root.geometry("1000x700")

    # ***** Menu bar ***********
    menu = tk.Menu(root)
    root.config(menu=menu)

    subMenu = tk.Menu(menu, tearoff=0)
    menu.add_cascade(label="File", menu=subMenu) # below, we use lambda because its a hacker way around to pass func to command with parameters and ont exceute them instantly.
    subMenu.add_command(label="New Analysis...", command= lambda: gc.AnalysisTab(notebook, woeid_data))# gc is our defined gui_class as gc. I am calling a function call in command from class gui
    subMenu.add_command(label="Save Analysis as...", command = doNothing)
    subMenu.add_separator()
    subMenu.add_command(label="Exit", command = lambda: quitProgram(root))

    editMenu = tk.Menu(menu, tearoff=0)
    menu.add_cascade(label="Edit", menu=editMenu)
    editMenu.add_command(label="Advanced...", command = lambda: gc.AdvancedTab(notebook, data))

    # ***** Tool bar ***********

    toolbar = tk.Frame(root, bg="grey")
    # Right now when we click the option button , it does nothing in the main window.
    option1Button = tk.Button(toolbar, text="Option 1", command=doNothing) # This button is in the frame:toolbar, which is a top frame.
    option1Button.pack(side="left", padx=2, pady=2) # 2 pt padding with left most placement
    option2Button = tk.Button(toolbar, text="Option 2", command=doNothing)
    option2Button.pack(side="left", padx=2, pady=2)

    toolbar.pack(side="top", fill = "x")

    # ***** Status bar ****** the lowest /bottom most area of window
    statusbar = tk.Label(root, text="Disconnected from server...", bd=1, relief="sunken", anchor="w")
    statusbar.pack(side="bottom", fill="x")
    # *** end of status bar code ******

    notebook = gc.CustomNotebook(root,  close_button = True)
    notebook.pack(side="top", fill="both", expand=True)
    # Update the preview tweets in the active tab when enter is pressed - can be disabled.
    root.bind("<Return>", lambda event: notebook.tabs[notebook.index(notebook.select())].tweets_box.on_enter_press())
    """
    test_tab = gc.Tab(notebook, "Test")
    test_tab2 = gc.Tab(notebook, "Test2")


    labelFrame = tk.LabelFrame(test_tab.frame, text ="Testing stuff")
    some_frame = tk.Frame(labelFrame, width = 400, height = 400)
    some_frame.pack()
    labelFrame.pack(anchor= "nw")

    test_notebook = gc.FramedNotebook(some_frame, text = "FUCKSIES!", close_button = True)
    test_notebook.pack()

    test_button = tk.Button(some_frame, text = "Boom!", command = lambda: print(notebook.tabs[notebook.tabs.index(test_tab2)].tabName))
    test_button.place(relx = 0.5, rely=0.5, anchor = tk.CENTER)
    """


    while True:
        root.update()
        track_tweets()

if __name__ == '__main__':
    main()
