from tkinter import *
from netmiko import ConnectHandler
from customtkinter import *
import threading
import time

set_appearance_mode("Dark")
set_default_color_theme("green")



ios_l2 = {
    'device_type': 'cisco_ios',
    'username': '',
    'ip': '',
    'password': '',
    'conn_timeout': 9999999
}

class Table:
    def __init__(self, root, data):
        for i in range(len(data)):
            for j in range(len(data[i])):
                e = CTkEntry(root, width=250, font=('Arial', 16, 'bold'))
                e.grid(row=i, column=j)
                e.insert(END, data[i][j])


def update_window(win,ssh):
    data_list = []
    ints_command = ssh.send_command("sh int | i up | rate")
    ints_command = ints_command.split("\n")
    for i, line in enumerate(ints_command):
        if "Gigabit" in line:
            rx, tx = ints_command[i+1].split()[4], ints_command[i+2].split()[4]
            data_list.append([line[0:21], rx, tx])
    t = Table(win, data_list)
    window.after(int(update_timer.get())*1000,update_window,win,ssh)
def create_window():
        try:
            newWindow = CTkToplevel(window)
            newWindow.title(ios_l2['ip'])
            newWindow.geometry("750x750")
            ssh = ConnectHandler(**ios_l2)
            update_window(newWindow,ssh)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
        

def newTrack():
    ios_l2['ip'] = device_ip.get()
    ios_l2['username'] = device_username.get()
    ios_l2['password'] = device_password.get()
    threading.Thread(target=create_window).start()

window = CTk()
window.title("Realtime Interface Table Tracker")
window.geometry("300x300")

greeting = CTkLabel(window, text="Realtime Interface Table Tracker")
greeting.place(relx=0.5, rely=0.1, anchor=CENTER)

device_ip = CTkEntry(window, placeholder_text="IP Address",
                     width=120,
                     height=25,
                     border_width=2,
                     corner_radius=10)
device_ip.place(relx=0.5, rely=0.2, anchor=CENTER)

device_username = CTkEntry(window, placeholder_text="Username",
                           width=120,
                           height=25,
                           border_width=2,
                           corner_radius=10)
device_username.place(relx=0.5, rely=0.3, anchor=CENTER)
device_password = CTkEntry(window, placeholder_text="Password", show="*",
                           width=120,
                           height=25,
                           
                           border_width=2,
                           corner_radius=10)
device_password.place(relx=0.5, rely=0.4, anchor=CENTER)

update_timer = CTkEntry(window, placeholder_text="Refresh Time (s)",
                           width=120,
                           height=25,
                           border_width=2,
                           corner_radius=10)
update_timer.place(relx=0.5, rely=0.5, anchor=CENTER)

load_button = CTkButton(window, text="Start Tracking", command=newTrack)
load_button.place(relx=0.5, rely=0.7, anchor=CENTER)

window.mainloop()