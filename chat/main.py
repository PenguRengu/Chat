"""
main.py
create on 5/17/19
"""
### Imports
import tkinter as tk
import tkinter.messagebox as msgbox
from tkinter import filedialog
from socket import *
from threading import Thread
from time import sleep

### Variables
name = "Forgot to set display name"

### Functions
def send_to_server(msg):
    s = socket(AF_INET, SOCK_STREAM)
    s.connect(("localhost", 9897))
    s.send(msg.encode("utf-8"))
    resp = str(s.recv(7766))[2:-1]
    s.close()
    return resp

def check_messages():
    global text
    while True:
        text.delete("1.0",tk.END)
        recv_split = send_to_server("msg").split("|")
        
        for r in recv_split:
            if r.split(":")[0] == "file":
                recv_split.remove(r)
        
        text.insert(tk.END, "|".join(recv_split).replace("|","\n"))
        sleep(1)

def send_file():
    filename = filedialog.askopenfilename()
    with open(filename, "r") as file:
        send_to_server(name + " sent file: " + filename.split("/")[-1])
        send_to_server("file:" + file.read().replace("\n", "/n/"))

def download_file():
    recv_split = send_to_server("msg").split("|")

    files = []

    for r in recv_split:
        if r.split(":")[0] == "file":
            files.append(r)
    
    if len(files) <= 0:
        msgbox.showerror("No file was uploaded")
        return
    
    filename = filedialog.askopenfilename()
    with open(filename, "w") as file:
        file.write(files[-1].split(":")[1].replace("/n/", "\n"))

def change_display_name(w, e):
    global name
    name = e.get()
    w.destroy()
def change_display_name_dialog():
    dialog = tk.Tk()
    dialog.title("Display Name")
    dialog.geometry("200x100")

    l = tk.Label(dialog, text="Display Name:")
    l.pack(fill=tk.X)

    name_entry = tk.Entry(dialog)
    name_entry.pack(fill=tk.X)

    ok_button = tk.Button(dialog, text="Ok", command=lambda: change_display_name(dialog, name_entry))
    ok_button.pack(fill=tk.X)


### Main
if __name__ == "__main__":
    change_display_name_dialog()

    root = tk.Tk()
    root.geometry("600x600")
    root.title("Chat")

    text = tk.Text(root)
    text.pack(fill=tk.BOTH)

    entry = tk.Entry(root)
    entry.pack(fill=tk.X)

    send_button = tk.Button(root, text="Send", command=lambda: send_to_server(name + "> " + entry.get()))
    send_button.pack(fill=tk.X)

    send_file_button = tk.Button(root, text="Send File", command=send_file)
    send_file_button.pack(fill=tk.X)

    download_file_button = tk.Button(root, text="Download File", command=download_file)
    download_file_button.pack(fill=tk.X)

    change_display_name_button = tk.Button(root, text="Change Display Name", command=change_display_name_dialog)
    change_display_name_button.pack(fill=tk.X)

    t = Thread(target=check_messages)
    t.start()

    root.mainloop()