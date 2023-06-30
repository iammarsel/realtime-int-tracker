from tkinter import *
from netmiko import ConnectHandler
from customtkinter import *
set_appearance_mode("System")
set_default_color_theme("green")

window = CTk()
window.title("Realtime Interface Table Tracker")
window.geometry("1000x700")

ios_l2 = {
    'device_type': 'cisco_ios',
    'username': '',
    'ip': '',
    'password': '',
    'conn_timeout': 9999999
}

pause = False
index = 0
toggle_text = "Pause"
font = {'family': 'Times New Roman',
        'weight': 'bold',
        'size': 22
        }
int_table = {"1":[4,2],"2":[1,1],"3":[9,9]}
ints_command = "" 
ssh = ""
class ScrollableInterfaceFrame(CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.label_list = []
    def add_int(self, item, image=None):
        label = CTkLabel(self, text=item, image=image, compound="left", padx=5, anchor="w")
        label.grid(row=len(self.label_list), column=0, pady=(0, 10), sticky="w")
        self.label_list.append(label)

    def remove_int(self, item):
        for label in self.label_list:
            if item == label.cget("text"):
                label.destroy()
                self.label_list.remove(label)
                return

def onChange():
    global pause
    pause ^= True
    if pause:
        pause_button.configure(
            text="Continue", fg_color="#119149", hover_color="#45ba78")
       
    else:
        pause_button.configure(
            text="Pause", fg_color="#c74c3c", hover_color="#9c2b1c")
        window.after(3000,update_table)

def update_table():
    global int_table, ssh
    ints_command = ssh.send_command(f"sh int | i up | rate")
    ints_command = ints_command.split("\n")
    scrollable_interface_frame = ScrollableInterfaceFrame(window, width=500, height=500, corner_radius=5)
    scrollable_interface_frame.place(relx=0.6, rely=0.4, anchor=CENTER)
    for i,line in enumerate(ints_command):
        if "Gigabit" in line:
            rx,tx = ints_command[i+1].split()[4],ints_command[i+2].split()[4]
            int_table[line[0:21]] = [rx,tx]
    for k,v in int_table.items():  # add all current ints
        scrollable_interface_frame.add_int(f"{k}               RX: {v[0]:,} bits/sec              TX: {v[1]:,} bits/sec")
    if not pause:
        window.after(3000, update_table)

def create_window():
    ios_l2['ip'] = device_ip.get()
    ios_l2['username'] = device_username.get()
    ios_l2['password'] = device_password.get()
    ssh = ""
    try:
        ssh = ConnectHandler(**ios_l2)
        ints_command = ssh.send_command(f"sh int | i up | rate")
        ints_command = ints_command.split("\n")
        newWindow = Toplevel(window)
        newWindow.title(ios_l2['ip'])
        newWindow.geometry("700x700")
        scrollable_interface_frame = ScrollableInterfaceFrame(window, width=500, height=500, corner_radius=5)
        scrollable_interface_frame.place(relx=0.6, rely=0.4, anchor=CENTER)
        window.after(3000,update_table)
    except:
        print("error creating a table")
        return
    
    ios_l2['ip'] = device_ip.get()
    ios_l2['username'] = device_username.get()
    ios_l2['password'] = device_password.get()
    ssh = ConnectHandler(**ios_l2)
    #try:
    ints_command = ssh.send_command(f"sh int | i up | rate")
    ints_command = ints_command.split("\n")
    print(ints_command)
    print(int_table)
    global pause_button
    exit_button = CTkButton(newWindow, text="Stop Tracking", command=onChange, fg_color="#c74c3c", hover_color="#9c2b1c")
    exit_button.place(relx=0.4, rely=0.8, anchor=CENTER)
    if not pause:
        window.after(3000,update_table)
    """          
    except KeyboardInterrupt:
        print('Interrupted by user')
    except:
        print('error found at', device_ip)
    """
greeting = CTkLabel(window, text="Load Device and Track Speed using Graph")
greeting.place(relx=0.2, rely=0.1, anchor=CENTER)


device_ip = CTkEntry(window, placeholder_text="IP Address",
                     width=120,
                     height=25,
                     border_width=2,
                     corner_radius=10)
device_ip.place(relx=0.2, rely=0.2, anchor=CENTER)

device_username = CTkEntry(window, placeholder_text="Username",
                           width=120,
                           height=25,
                           border_width=2,
                           corner_radius=10)
device_username.place(relx=0.2, rely=0.3, anchor=CENTER)
device_password = CTkEntry(window, placeholder_text="Password", show="*",
                           width=120,
                           height=25,
                           border_width=2,
                           corner_radius=10)
device_password.place(relx=0.2, rely=0.4, anchor=CENTER)

load_button = CTkButton(window, text="Start Tracking", command=create_window,
                        fg_color="#119149", hover_color="#45ba78")
load_button.place(relx=0.2, rely=0.5, anchor=CENTER)
window.mainloop()