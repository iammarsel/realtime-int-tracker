from tkinter import *
from netmiko import ConnectHandler
from customtkinter import *
set_appearance_mode("System")
set_default_color_theme("green")

window = ()
window.title("Realtime Interface Table Tracker")
window.geometry("300x300")

ios_l2 = {
    'device_type': 'cisco_ios',
    'username': '',
    'ip': '',
    'password': '',
    'conn_timeout': 9999999
}

pause = False
font = {'family': 'Times New Roman',
        'weight': 'bold',
        'size': 22
        }
ssh = ""

class Table:
    def __init__(self,root,data):
         
        # code for creating table
        for i in range(data):
            for j in range(len(data[0])):
                 
                self.e = Entry(root, width=250,
                               font=('Arial',16,'bold'))
                 
                self.e.grid(row=i, column=j)
                self.e.insert(END, data[i][j])



def update_window(win):
    ints_command = ssh.send_command(f"sh int | i up | rate")
    ints_command = ints_command.split("\n")
    data_list = []
    for i,line in enumerate(ints_command):
        if "Gigabit" in line:
            rx,tx = ints_command[i+1].split()[4],ints_command[i+2].split()[4]
            data_list.append([line[0:21],rx,tx])
    t = Table(win,data_list)
    win.update()
    window.after(int(update_timer.get())*1000, update_window(win))

def newTrack():
    ios_l2['ip'] = device_ip.get()
    ios_l2['username'] = device_username.get()
    ios_l2['password'] = device_password.get()
    global ssh
    ssh = ConnectHandler(**ios_l2)
    ints_command = ssh.send_command(f"sh int | i up | rate")
    ints_command = ints_command.split("\n")
    
    newWindow = Toplevel(window)
 
    newWindow.title(ios_l2['ip'])
 
    newWindow.geometry("750x750")
 
    data_list = []
    for i,line in enumerate(ints_command):
        if "Gigabit" in line:
            rx,tx = ints_command[i+1].split()[4],ints_command[i+2].split()[4]
            data_list.append([line[0:21],rx,tx])
    t = Table(newWindow,data_list)
    
    window.after(int(update_timer.get())*1000,update_window(newWindow))
        
greeting = Label(window, text="Realtime Interface Table Tracker")
greeting.place(relx=0.5, rely=0.1, anchor=CENTER)


device_ip = Entry(window, placeholder_text="IP Address",
                     width=120,
                     height=25,
                     border_width=2,
                     corner_radius=10)
device_ip.place(relx=0.5, rely=0.2, anchor=CENTER)

device_username = Entry(window, placeholder_text="Username",
                           width=120,
                           height=25,
                           border_width=2,
                           corner_radius=10)
device_username.place(relx=0.5, rely=0.3, anchor=CENTER)
device_password = Entry(window, placeholder_text="Password", show="*",
                           width=120,
                           height=25,
                           
                           border_width=2,
                           corner_radius=10)
device_password.place(relx=0.5, rely=0.4, anchor=CENTER)

update_timer = Entry(window, placeholder_text="Refresh Time (s)",
                           width=120,
                           height=25,
                           border_width=2,
                           corner_radius=10)
update_timer.place(relx=0.5, rely=0.5, anchor=CENTER)

load_button = Button(window, text="Start Tracking", command=newTrack,
                        fg_color="#119149", hover_color="#45ba78")
load_button.place(relx=0.5, rely=0.7, anchor=CENTER)

window.mainloop()