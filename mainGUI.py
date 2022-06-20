'''
MECH ENG 4M03 - Capstone Project - Autonommous Snowblower Utilizing UWB Sensor Network
Developed By Capstone FY01

Solomon Ainodion -  ainodios@mcmaster.ca 
Guy-Marcel Fouedjio - fouedjig@mcmaster.ca 
Lawrence Mak - makl1@mcmaster.ca 
Sayanthan Paramananthan - params4@mcmaster.ca 
Prathmesh Shetty - shettp1@mcmaster.ca 

This small program allows us to visualize the tag data and understand the position of the snowblower in relation to the UWB anchor sensors
'''

#Import Statements 
#We are using Python's Tkinter Module to develop the GUI 
import tkinter as tk
from tkinter import Toplevel, ttk
from tkinter import Canvas, Frame, BOTH

#We are using Python's pySerial to communicate with the Shield/Board
#import serial
import struct
from typing import Container

#Private Variables - These variables are the few that are used everywhere in the program and have a significant value at every stage

#GUI
LARGE_FONT = ("Times", 12)

#GUI Window
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

#Serial Communication Setup Variables
#try:
   # ser = serial.Serial(
    #port='COM7',
   # baudrate = 115200,
   # parity=serial.PARITY_NONE,
   # stopbits=serial.STOPBITS_ONE,
   # bytesize=serial.EIGHTBITS,
    #timeout=1)

#except:
    #print("Serial Communication Not Established")


#Tkinter Frames Dealing With the Welcome Screen
'''
@class: capstoneGUI(tk.Tk) - Setups the GUI as Tkinter Frames and uses Tkinter Module in order to display the different screens
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class capstoneGUI(tk.Tk):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, *args, **kwargs
    @return - None
    '''    
    def __init__(self, *args, **kwargs):

        #Setups an instance of Tkinter
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        #Setups Custom Values and Geometry of the Screen
        tk.Tk.wm_title(self, "Capstone FY01")
        container.pack(side = "top", fill = "both", expand =True)
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)

        self.geometry('1280x720+320+180')

        #Setting Up the Frames - Screens to Transistions between
        self.frames = {} # Stores all the frames

        for F in (MainScreen, StartTrackingConfirmation, StopTrackingConfirmation, StartTracking, StopAllProcessesConfirmation, QuitClient):
            frame = F(container, self)
            self.frames[F] = frame #sets the welcomeScreen as the first frame to show
            frame.grid(row = 0, column = 0, sticky = "nsew")

        self.show_frame(MainScreen)

    '''
    @function: show_frame() - Transistions between the different frame by bring them up to the top
    @param -self, cont - Container of all the possible frames
    @return - None
    '''    
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()        

'''
@class: MainScreen(tk.Tk) - Tkinter Frame of the Main Screen (Starting Screen)
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class MainScreen(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''    
    def __init__(self, parent, controller):
        #Setting Up The Interactive Options such as Texts, Buttons and Entry Boxes
        
        #Init
        tk.Frame.__init__(self, parent)

        #Shape
        canvas = Canvas(self,height=WINDOW_HEIGHT,width=WINDOW_WIDTH,bg="white")
        canvas.pack()
        canvas.create_rectangle(WINDOW_WIDTH/2-300, WINDOW_HEIGHT-125, WINDOW_WIDTH/2+300, WINDOW_HEIGHT-50,outline="black", fill="white")
        canvas.create_rectangle(WINDOW_WIDTH/2-300, WINDOW_HEIGHT/2-250, WINDOW_WIDTH/2+300, WINDOW_HEIGHT/2+200,outline="black", fill="white")

        #Value Boxes
        #TopLeft Anchor
        canvas.create_rectangle(WINDOW_WIDTH/2-300, WINDOW_HEIGHT/2-250, WINDOW_WIDTH/2-200, WINDOW_HEIGHT/2-200,outline="black", fill="white")
        label = tk.Label(self, text = "Anchor 1", font = LARGE_FONT)
        label.place(x=WINDOW_WIDTH/2-275,y=WINDOW_HEIGHT/2-240)
        canvas.create_line(WINDOW_WIDTH/2-200, WINDOW_HEIGHT/2-200, WINDOW_WIDTH/2-50, WINDOW_HEIGHT/2-25, dash=(4, 2))        

        #BottomLeft Anchor
        canvas.create_rectangle(WINDOW_WIDTH/2-300, WINDOW_HEIGHT/2+150, WINDOW_WIDTH/2-200, WINDOW_HEIGHT/2+200,outline="black", fill="white")
        label = tk.Label(self, text = "Anchor 2", font = LARGE_FONT)
        label.place(x=WINDOW_WIDTH/2-275,y=WINDOW_HEIGHT/2+165)
        canvas.create_line(WINDOW_WIDTH/2-200, WINDOW_HEIGHT/2+150, WINDOW_WIDTH/2-50, WINDOW_HEIGHT/2+25, dash=(4, 2)) 

        #TopRight Anchor
        canvas.create_rectangle(WINDOW_WIDTH/2+200, WINDOW_HEIGHT/2-250, WINDOW_WIDTH/2+300, WINDOW_HEIGHT/2-200,outline="black", fill="white")
        label = tk.Label(self, text = "Anchor 4", font = LARGE_FONT)
        label.place(x=WINDOW_WIDTH/2+225,y=WINDOW_HEIGHT/2-240)
        canvas.create_line(WINDOW_WIDTH/2+200, WINDOW_HEIGHT/2-200, WINDOW_WIDTH/2+50, WINDOW_HEIGHT/2-25, dash=(4, 2)) 

        #BottomRight Anchor
        canvas.create_rectangle(WINDOW_WIDTH/2+200, WINDOW_HEIGHT/2+150, WINDOW_WIDTH/2+300, WINDOW_HEIGHT/2+200,outline="black", fill="white")
        label = tk.Label(self, text = "Anchor 3", font = LARGE_FONT)
        label.place(x=WINDOW_WIDTH/2+225,y=WINDOW_HEIGHT/2+165)
        canvas.create_line(WINDOW_WIDTH/2+200, WINDOW_HEIGHT/2+150, WINDOW_WIDTH/2+50, WINDOW_HEIGHT/2+25, dash=(4, 2)) 

        #Tag Window
        canvas.create_rectangle(WINDOW_WIDTH/2-50, WINDOW_HEIGHT/2-25, WINDOW_WIDTH/2+50, WINDOW_HEIGHT/2+25,outline="black", fill="white")
        label = tk.Label(self, text = "Tag", font = LARGE_FONT)
        label.place(x=WINDOW_WIDTH/2-15,y=WINDOW_HEIGHT/2-15)

        #Text
        label = tk.Label(self, text = "Capstone FY01 - Control System UI-v1.0", font = LARGE_FONT)
        label.place(x=WINDOW_WIDTH/2-140,y=10)
                      
        #Buttons
        preset_1_Box = ttk.Button(self, text = "Preset #1", command = quit)
        preset_1_Box.place(x=50,y=10, height = 25, width = 150)
        
        preset_2_Box = ttk.Button(self, text = "Preset #2", command = quit)
        preset_2_Box.place(x=250,y=10, height = 25, width = 150)

        quit_Box = ttk.Button(self, text = "Quit Client", command = lambda: controller.show_frame(QuitClient))
        quit_Box.place(x=WINDOW_WIDTH/2+450,y=10, height = 25, width = 150)

        startTrackingBox = ttk.Button(self, text = "Start Tracking", command = lambda: controller.show_frame(StartTrackingConfirmation))
        startTrackingBox.place(x=50,y=WINDOW_HEIGHT-125, height = 75, width = 200)

        emergencyStopBox = ttk.Button(self, text = "Emergency Stop", command = lambda: controller.show_frame(StopAllProcessesConfirmation))
        emergencyStopBox.place(x=WINDOW_WIDTH-250,y=WINDOW_HEIGHT-125, height = 75, width = 200)


'''
@class: StartTrackingConfirmation(tk.Tk) - Tkinter Frame of the Start Tracking Screen with Confirmation Message
@param - tk.Tk - Tkinter Reference
@return - None
'''     

class StartTrackingConfirmation(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''    
    def __init__(self, parent, controller):
        #Setting Up The Interactive Options such as Texts, Buttons and Entry Boxes
        
        #Init
        tk.Frame.__init__(self, parent)

        #Shape
        canvas = Canvas(self,height=WINDOW_HEIGHT,width=WINDOW_WIDTH,bg="white")
        canvas.pack()
        canvas.create_rectangle(WINDOW_WIDTH/2-300, WINDOW_HEIGHT-125, WINDOW_WIDTH/2+300, WINDOW_HEIGHT-50,outline="black", fill="white")
        
        #Text
        label = tk.Label(self, text = "Capstone FY01 - Control System UI-v1.0", font = LARGE_FONT)
        label.place(x=WINDOW_WIDTH/2-140,y=10)

        #Question
        label = tk.Label(self, text = "Are you sure to start tracking?", font = LARGE_FONT)
        label.place(x = WINDOW_WIDTH/2-100,y = WINDOW_HEIGHT-120)
                      
        #Buttons
        yes_Box = ttk.Button(self, text = "Yes", command = lambda: controller.show_frame(StartTracking))
        yes_Box.place(x = WINDOW_WIDTH/2-200,y = WINDOW_HEIGHT-75, height = 25, width = 150)

        no_Box = ttk.Button(self, text = "No", command = lambda: controller.show_frame(MainScreen))
        no_Box.place(x = WINDOW_WIDTH/2+50,y = WINDOW_HEIGHT-75, height = 25, width = 150)

'''
@class: StopTrackingConfirmation(tk.Tk) - Tkinter Frame of the Stop Tracking Screen with Confirmation Message
@param - tk.Tk - Tkinter Reference
@return - None
'''     

class StopTrackingConfirmation(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''    
    def __init__(self, parent, controller):
        #Setting Up The Interactive Options such as Texts, Buttons and Entry Boxes
        
        #Init
        tk.Frame.__init__(self, parent)

        #Shape
        canvas = Canvas(self,height=WINDOW_HEIGHT,width=WINDOW_WIDTH,bg="white")
        canvas.pack()
        canvas.create_rectangle(WINDOW_WIDTH/2-300, WINDOW_HEIGHT-125, WINDOW_WIDTH/2+300, WINDOW_HEIGHT-50,outline="black", fill="white")
        
        #Text
        label = tk.Label(self, text = "Capstone FY01 - Control System UI-v1.0", font = LARGE_FONT)
        label.place(x=WINDOW_WIDTH/2-140,y=10)

        #Question
        label = tk.Label(self, text = "Are you sure to stop tracking?", font = LARGE_FONT)
        label.place(x = WINDOW_WIDTH/2-100,y = WINDOW_HEIGHT-120)
                      
        #Buttons
        yes_Box = ttk.Button(self, text = "Yes", command = lambda: controller.show_frame(MainScreen))
        yes_Box.place(x = WINDOW_WIDTH/2-200,y = WINDOW_HEIGHT-75, height = 25, width = 150)

        no_Box = ttk.Button(self, text = "No", command = lambda: controller.show_frame(StartTracking))
        no_Box.place(x = WINDOW_WIDTH/2+50,y = WINDOW_HEIGHT-75, height = 25, width = 150)


'''
@class: StartTracking(tk.Tk) - Tkinter Frame of the Start Tracking Screen
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class StartTracking(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''    
    def __init__(self, parent, controller):
        #Setting Up The Interactive Options such as Texts, Buttons and Entry Boxes

        #Init
        tk.Frame.__init__(self, parent)

        #Shape
        canvas = Canvas(self,height=WINDOW_HEIGHT,width=WINDOW_WIDTH,bg="white")
        canvas.pack()
        canvas.create_rectangle(WINDOW_WIDTH/2-300, WINDOW_HEIGHT-125, WINDOW_WIDTH/2+300, WINDOW_HEIGHT-50,outline="black", fill="white")
        canvas.create_rectangle(WINDOW_WIDTH/2-300, WINDOW_HEIGHT/2-250, WINDOW_WIDTH/2+300, WINDOW_HEIGHT/2+200,outline="black", fill="white")

        #Value Boxes
        #TopLeft Anchor
        canvas.create_rectangle(WINDOW_WIDTH/2-300, WINDOW_HEIGHT/2-250, WINDOW_WIDTH/2-200, WINDOW_HEIGHT/2-200,outline="black", fill="white")
        canvas.create_line(WINDOW_WIDTH/2-200, WINDOW_HEIGHT/2-200, WINDOW_WIDTH/2-50, WINDOW_HEIGHT/2-25, dash=(4, 2))        

        #BottomLeft Anchor
        canvas.create_rectangle(WINDOW_WIDTH/2-300, WINDOW_HEIGHT/2+150, WINDOW_WIDTH/2-200, WINDOW_HEIGHT/2+200,outline="black", fill="white")
        canvas.create_line(WINDOW_WIDTH/2-200, WINDOW_HEIGHT/2+150, WINDOW_WIDTH/2-50, WINDOW_HEIGHT/2+25, dash=(4, 2)) 

        #TopRight Anchor
        canvas.create_rectangle(WINDOW_WIDTH/2+200, WINDOW_HEIGHT/2-250, WINDOW_WIDTH/2+300, WINDOW_HEIGHT/2-200,outline="black", fill="white")
        canvas.create_line(WINDOW_WIDTH/2+200, WINDOW_HEIGHT/2-200, WINDOW_WIDTH/2+50, WINDOW_HEIGHT/2-25, dash=(4, 2)) 

        #BottomRight Anchor
        canvas.create_rectangle(WINDOW_WIDTH/2+200, WINDOW_HEIGHT/2+150, WINDOW_WIDTH/2+300, WINDOW_HEIGHT/2+200,outline="black", fill="white")
        canvas.create_line(WINDOW_WIDTH/2+200, WINDOW_HEIGHT/2+150, WINDOW_WIDTH/2+50, WINDOW_HEIGHT/2+25, dash=(4, 2)) 

        #Tag Window
        canvas.create_rectangle(WINDOW_WIDTH/2-50, WINDOW_HEIGHT/2-25, WINDOW_WIDTH/2+50, WINDOW_HEIGHT/2+25,outline="black", fill="white")
        label = tk.Label(self, text = "Tag", font = LARGE_FONT)
        label.place(x=WINDOW_WIDTH/2-15,y=WINDOW_HEIGHT/2-15)

        #Text
        label = tk.Label(self, text = "Capstone FY01 - Control System UI-v1.0", font = LARGE_FONT)
        label.place(x=WINDOW_WIDTH/2-140,y=10)
                      
        #Buttons
        startTrackingBox = ttk.Button(self, text = "Stop Tracking", command = lambda: controller.show_frame(StopTrackingConfirmation))
        startTrackingBox.place(x=50,y=WINDOW_HEIGHT-125, height = 75, width = 200)

        emergencyStopBox = ttk.Button(self, text = "Emergency Stop", command = lambda: controller.show_frame(StopAllProcessesConfirmation))
        emergencyStopBox.place(x=WINDOW_WIDTH-250,y=WINDOW_HEIGHT-125, height = 75, width = 200)

'''
@class: StopAllProcessesConfirmation(tk.Tk) - Tkinter Frame of the Emergency Stop Process
@param - tk.Tk - Tkinter Reference
@return - None
'''     
class StopAllProcessesConfirmation(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''    
    def __init__(self, parent, controller):
        #Setting Up The Interactive Options such as Texts, Buttons and Entry Boxes
        
        #Init
        tk.Frame.__init__(self, parent)

        #Shape
        canvas = Canvas(self,height=WINDOW_HEIGHT,width=WINDOW_WIDTH,bg="white")
        canvas.pack()
        canvas.create_rectangle(WINDOW_WIDTH/2-300, WINDOW_HEIGHT-125, WINDOW_WIDTH/2+300, WINDOW_HEIGHT-50,outline="black", fill="white")
        
        #Text
        label = tk.Label(self, text = "Capstone FY01 - Control System UI-v1.0", font = LARGE_FONT)
        label.place(x=WINDOW_WIDTH/2-140,y=10)

        #Question
        label = tk.Label(self, text = "Are you sure to stop all processes?", font = LARGE_FONT)
        label.place(x = WINDOW_WIDTH/2-100,y = WINDOW_HEIGHT-120)
                      
        #Buttons
        yes_Box = ttk.Button(self, text = "Yes", command = lambda: controller.show_frame(MainScreen))
        yes_Box.place(x = WINDOW_WIDTH/2-200,y = WINDOW_HEIGHT-75, height = 25, width = 150)

        no_Box = ttk.Button(self, text = "No", command = lambda: controller.show_frame())
        no_Box.place(x = WINDOW_WIDTH/2+50,y = WINDOW_HEIGHT-75, height = 25, width = 150)

'''
@class: QuitClient(tk.Tk) - Tkinter Frame of the Quit Client with Confirmation Message
@param - tk.Tk - Tkinter Reference
@return - None
'''     

class QuitClient(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''    
    def __init__(self, parent, controller):
        #Setting Up The Interactive Options such as Texts, Buttons and Entry Boxes
        
        #Init
        tk.Frame.__init__(self, parent)

        #Shape
        canvas = Canvas(self,height=WINDOW_HEIGHT,width=WINDOW_WIDTH,bg="white")
        canvas.pack()
        canvas.create_rectangle(WINDOW_WIDTH/2-300, WINDOW_HEIGHT-125, WINDOW_WIDTH/2+300, WINDOW_HEIGHT-50,outline="black", fill="white")
        
        #Text
        label = tk.Label(self, text = "Capstone FY01 - Control System UI-v1.0", font = LARGE_FONT)
        label.place(x=WINDOW_WIDTH/2-140,y=10)

        #Question
        label = tk.Label(self, text = "Are you sure to quit the client?", font = LARGE_FONT)
        label.place(x = WINDOW_WIDTH/2-100,y = WINDOW_HEIGHT-120)
                      
        #Buttons
        yes_Box = ttk.Button(self, text = "Yes", command = quit)
        yes_Box.place(x = WINDOW_WIDTH/2-200,y = WINDOW_HEIGHT-75, height = 25, width = 150)

        no_Box = ttk.Button(self, text = "No", command = lambda: controller.show_frame(MainScreen))
        no_Box.place(x = WINDOW_WIDTH/2+50,y = WINDOW_HEIGHT-75, height = 25, width = 150)

#Tkinter Reference Lines - Launching the Applet
app = capstoneGUI()
app.mainloop()