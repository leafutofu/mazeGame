import customtkinter as tk

class Page(tk.CTkFrame):
    def __init__(self, *args, **kwargs):
        tk.CTkFrame.__init__(self, master=root, *args, **kwargs)
    
    def show(self):
        self.lift()

class mainMenu(Page):
    def __init__(self, controller, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = tk.CTkLabel(self, text="Main Menu")
        label.pack()

        def modeSelection_button():
            controller.pages['modeSelection'].show()
            
        def settings_button():
            controller.pages['settings'].show()

        modeSelection_button = tk.CTkButton(self, text="Play", command=modeSelection_button)
        settings_button = tk.CTkButton(self, text="Settings", command=settings_button)

        modeSelection_button.pack()
        settings_button.pack()
        

class settings(Page):    
    def __init__(self, controller, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = tk.CTkLabel(self, text="Settings")
        label.pack(side="top", fill="both", expand=True)

class modeSelection(Page): #selects singleplayer or multiplayer
    def __init__(self, controller, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = tk.CTkLabel(self, text="Mode Selection")
        label.pack()

        def singlePlayer_button():
            controller.pages['spOptions'].show()
            
        def multiPlayer_button():
            controller.pages['mpOptions'].show()
            
        singlePlayer_button = tk.CTkButton(self, text="Single Player", command=singlePlayer_button)
        multiPlayer_button = tk.CTkButton(self, text="Multi Player", command=multiPlayer_button)

        singlePlayer_button.pack()
        multiPlayer_button.pack()

class spOptions(Page): #screen to select generation style and grid size for singleplayer
    def __init__(self, controller, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = tk.CTkLabel(self, text="Singleplayer Options")
        label.pack(side="top", fill="both", expand=True)

class mpOptions(Page): #screen to select generation style and grid size for multiplayer
    def __init__(self, controller, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = tk.CTkLabel(self, text="Multiplayer Options")
        label.pack(side="top", fill="both", expand=True)

class spGame(Page): #singleplayer game screen
    def __init__(self, controller, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = tk.CTkLabel(self, text="Singleplayer Game")
        label.pack(side="top", fill="both", expand=True)

class mpGame(Page): #multiplayer game screen
    def __init__(self, controller, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = tk.CTkLabel(self, text="Multiplayer Game")
        label.pack(side="top", fill="both", expand=True)

class spResults(Page): #singleplayer results screen
    def __init__(self, controller, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = tk.CTkLabel(self, text="Singleplayer Results")
        label.pack(side="top", fill="both", expand=True)

class mpResults(Page): #multiplayer results screen
    def __init__(self, controller, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = tk.CTkLabel(self, text="Multiplayer Results")
        label.pack(side="top", fill="both", expand=True)

class Window(tk.CTkFrame):
    def __init__(self, *args, **kwargs):
        tk.CTkFrame.__init__(self, *args, **kwargs)

        self.pages = {}
        for Subclass in (mainMenu, settings, modeSelection, spOptions, mpOptions, spGame, mpGame, spResults, mpResults):
            self.pages[Subclass.__name__] = Subclass(self)
            
        mm, st, ms, so, mo, sg, mg, sr, mr = self.pages.values()

        container = tk.CTkFrame(self)
        container.pack(side="top", fill="both", expand=True)

        for window in self.pages.values():
            window.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        
        mm.show()
    

if __name__ == "__main__":
    root = tk.CTk()
    main = Window(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("400x400")
    root.mainloop()