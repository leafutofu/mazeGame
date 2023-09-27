import customtkinter as ctk
from tkinter import *
from PIL import Image
import os

class Page(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        ctk.CTkFrame.__init__(self, master=root, *args, **kwargs)
        
    def show(self):
        self.lift() 

class mainMenu(Page):
    def __init__(self, controller, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        frame1 = ctk.CTkFrame(self)
        frame1.grid(row=0, column=0, sticky='nsew')
        
        bg1 = ctk.CTkImage(Image.open('assets/bg.png'), size=(900, 700))
        bg1label = ctk.CTkLabel(frame1, image = bg1, text = '')
        bg1label.grid(row=0, column=0)

        label = ctk.CTkLabel(frame1, text="Main Menu")
        label.grid(row=0, column=0)

        def modeSelection_button():
            controller.pages['modeSelection'].show()
            
        def settings_button():
            controller.pages['settings'].show()

        modeSelection_button = ctk.CTkButton(frame1, text="Play", command=modeSelection_button)
        settings_button = ctk.CTkButton(frame1, text="Settings", command=settings_button)

        modeSelection_button.grid(row=0, column=0)
        settings_button.grid(row=0, column=0, sticky='s', pady=10)
        

class settings(Page):    
    def __init__(self, controller, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = ctk.CTkLabel(self, text="Settings")
        label.pack(side="top", fill="both", expand=True)

class modeSelection(Page): #selects singleplayer or multiplayer
    def __init__(self, controller, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)


        label = ctk.CTkLabel(self, text="Mode Selection")
        label.pack()

        def spOptions_button():
            controller.pages['spOptions'].show()
            
        def mpOptions_button():
            controller.pages['mpOptions'].show()

        def settings_button():
            controller.pages['settings'].show()
            
        spOptions_button = ctk.CTkButton(self, text="Single Player", command=spOptions_button)
        mpOptions_button = ctk.CTkButton(self, text="Multi Player", command=mpOptions_button)
        settings_button = ctk.CTkButton(self, text="Settings", command=settings_button)

        spOptions_button.pack()
        mpOptions_button.pack()
        settings_button.pack()

class spOptions(Page): #screen to select generation style and grid size for singleplayer
    def __init__(self, controller, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = ctk.CTkLabel(self, text="Singleplayer Options")
        label.pack(side="top", fill="both", expand=True)

        def spGame_button():
            controller.pages['spGame'].show()

        spGame_button = ctk.CTkButton(self, text="Start Game", command=spGame_button)

        spGame_button.pack()

class mpOptions(Page): #screen to select generation style and grid size for multiplayer
    def __init__(self, controller, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = ctk.CTkLabel(self, text="Multiplayer Options")
        label.pack(side="top", fill="both", expand=True)
        
        def mpGame_button():
            controller.pages['mpGame'].show()

        mpGame_button = ctk.CTkButton(self, text="Start Game", command=mpGame_button)

        mpGame_button.pack()

class spGame(Page): #singleplayer game screen
    def __init__(self, controller, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = ctk.CTkLabel(self, text="Singleplayer Game")
        label.pack(side="top", fill="both", expand=True)

        back_button = ctk.CTkButton(self, text="Back")
        back_button.pack()

class mpGame(Page): #multiplayer game screen
    def __init__(self, controller, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = ctk.CTkLabel(self, text="Multiplayer Game")
        label.pack(side="top", fill="both", expand=True)

        back_button = ctk.CTkButton(self, text="Back")
        back_button.pack()

class spResults(Page): #singleplayer results screen
    def __init__(self, controller, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = ctk.CTkLabel(self, text="Singleplayer Results")
        label.pack(side="top", fill="both", expand=True)

        back_button = ctk.CTkButton(self, text="Back")
        back_button.pack()

class mpResults(Page): #multiplayer results screen
    def __init__(self, controller, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = ctk.CTkLabel(self, text="Multiplayer Results")
        label.pack(side="top", fill="both", expand=True)
        
        back_button = ctk.CTkButton(self, text="Back")

class Window(ctk.CTkFrame): #create main window
    def __init__(self, *args, **kwargs):
        ctk.CTkFrame.__init__(self, *args, **kwargs)

        #create a dictionary for all of the different selection pages
        self.pages = {}
        for Subclass in (mainMenu, settings, modeSelection, spOptions, mpOptions, spGame, mpGame, spResults, mpResults):
            self.pages[Subclass.__name__] = Subclass(self)
        
        print(self.pages.values())
        
        mm, st, ms, so, mo, sg, mg, sr, mr = self.pages.values()
        
        #creating a container frame to contain the widgets of each page
        container = ctk.CTkFrame(self)
        container.pack(side="top", fill="both", expand=True)

        #place all of the widgets onto the frame
        for window in self.pages.values():
            window.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        
        #show the first set of widgets - the main menu widgets on startup
        mm.show()
    

if __name__ == "__main__":
    root = ctk.CTk()
    main = Window(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("900x700")
    root.wm_title('Hedge')
    root.wm_iconbitmap('assets/icon.ico')
    root.wm_resizable(False, False)
    root.mainloop()