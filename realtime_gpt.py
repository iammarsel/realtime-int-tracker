from tkinter import *
from netmiko import ConnectHandler
import threading
import time

window = Tk()
window.title("Realtime Interface Table Tracker")
window.geometry("300x300")

ios_l2 = {
    'device_type': 'cisco_ios',
    'username': '',
    'ip': '',
    'password': '',
    'conn_timeout': 9999999
}

interface_data = []

class Table:
    def __init__(self, root, data):
        for i in range(len(data)):
            for j in range(len(data[i])):
                e = Entry(root, width=250, font=('Arial', 16, 'bold'))
                e.grid(row=i, column=j)
                e.insert(END, data[i][j])

def update_window(win):
    while True:
        try:
            ints_command = ssh.send_command("sh int | i up | rate")
            ints_command = ints_command.split("\n")
            data_list = []
            for i, line in enumerate(ints_command):
                if "Gigabit" in line:
                    rx, tx = ints_command[i+1].split()[4], ints_command[i+2].split()[4]
                    data_list.append([line[0:21], rx, tx])
            global interface_data
            interface_data = data_list
        except Exception as e:
            print(f"An error occurred: {str(e)}")
        
        time.sleep(5)

def newTrack():
    ios_l2['ip'] = device_ip.get()
    ios_l2['username'] = device_username.get()
    ios_l2['password'] = device_password.get()
    global ssh
    ssh = ConnectHandler(**ios_l2)

    newWindow = Toplevel(window)
    newWindow.title(ios_l2['ip'])
    newWindow.geometry("750x750")

    global interface_data
    t = Table(newWindow, interface_data)
    
    threading.Thread(target=update_window, args=(newWindow,)).start()

greeting = Label(window, text="Realtime Interface Table Tracker")
greeting.place(relx=0.5, rely=0.1, anchor=CENTER)

device_ip = Entry(window, width=120 )
device_ip.place(relx=0.5, rely=0.2, anchor=CENTER)

device_username = Entry(window, width=120)
device_username.place(relx=0.5, rely=0.3, anchor=CENTER)

device_password = Entry(window, show="*", width=120)
device_password.place(relx=0.5, rely=0.4, anchor=CENTER)

load_button = Button(window, text="Start Tracking", command=newTrack)
load_button.place(relx=0.5, rely=0.5, anchor=CENTER)

window.mainloop()