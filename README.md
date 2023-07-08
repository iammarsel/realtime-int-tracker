# Realtime Interface Bandwidth Utilization Tracker

## A program that creates an SSH connection with Networking Routers and Switches and displays the activity of every interface on that device in realtime, with an ability to compare multiple devices running at the same time

This project is part of my work at Williams Communcations as a Software Developer, assisting Networking Engineers in automation of daily tasks and analysis of devices that are part of our framework. This application is meant to be used for comparing different device speeds, changes over time, and any unexpected down time, using a convenient and user-friendly GUI design. Here are the statistics we are able to see in the application:
- All current interfaces in a table format
- TX/RX Speeds of each interface updating every 5 seconds
- Ability to have multiple SSH connections at the same time to compare the interfaces' bandwidth tables 

## Here is a display of how the application requests user input and shows the scrolling table GUI using Python and tkinter

<p align = center>
<img src="/demo_content/pic1.PNG" alt="" width="350" height="250" border="10" />
<img src="/demo_content/pic2.PNG" alt="" width="350" height="250" border="10" />
<img src="/demo_content/pic3.PNG" alt="" width="350" height="250" border="10" />
<img src="/demo_content/pic4.PNG" alt="" width="350" height="250" border="10" />

</p>

## How to use this app properly

The way to test this project would be to clone this project, install dependencies for Python, and test with any Cisco Router or Switch. The command that is running in the background is "sh int". Here is a step by step for the installation:

1. Clone this project
2. Install Python and required dependencing through pip, which are tkinter, matplotlib, numpy, customtkinter
3. Run the application and input the required data, including IP, username, password, and the update time.
## How to tweak this project for your own uses

Connect the same way as shown in the demo!

## Find a bug?

If you found an issue or would like to submit an improvement to this project, please submit an issue using the issues tab above. If you would like to submit a PR with a fix, reference the issue you created!

## Known issues

None

## Like this project?

Please consider leaving a star and a follow!