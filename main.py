import customtkinter as ctk
from tkinter.messagebox import askyesno
from PIL import Image

class Page(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        ctk.CTkFrame.__init__(self, master=root, *args, **kwargs)
        
    def show(self):
        self.lift()

    #def prev_page(self, page):
    #    if page == False:
    #        return previous_page
    #    elif page == str:
    #        previous_page = page

class mainMenu(Page):
    def __init__(self, controller, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        frame1 = ctk.CTkFrame(self)
        frame1.grid(row=0, column=0, sticky='nsew')
        
        bg1 = ctk.CTkImage(Image.open('assets/bg.png'), size=(900, 700))
        bg1label = ctk.CTkLabel(frame1, image = bg1, text = '')
        bg1label.grid(row=0, column=0)

        settingsX = 410
        settingsY = 610

        quitX = 485
        quitY = 610

        def modeSelection_button():
            page_stack.append('modeSelection')
            print(page_stack)
            controller.pages['modeSelection'].show()
            
        def check_position(event):
            print( f'x: {event.x}, y: {event.y}' )
            if page_stack == []:
                if event.x >= settingsX - 20 and event.x <= settingsX + 20 \
                and event.y >= settingsY - 20 and event.y <= settingsY + 20:
                    page_stack.append('mainMenu')
                    print(page_stack)
                    controller.pages['settings'].show()
                elif event.x >= quitX - 20 and event.x <= quitX + 20 \
                and event.y >= quitY - 20 and event.y <= quitY + 20:
                    if askyesno(title='Confirmation', message='Are you sure that you want to quit?') == True:
                        root.destroy()
            else:
                if event.x >= settingsX - 20 and event.x <= settingsX + 20 \
                and event.y >= settingsY - 20 and event.y <= settingsY + 20:
                    controller.pages['settings'].show()

        root.bind('<Button-1>', check_position)

        modeSelection_image = ctk.CTkImage(Image.open("assets/modeSelection.png"), size=(95, 20))

        modeSelection_button = ctk.CTkButton(frame1, 
                                             width=170,
                                             height=50,
                                             fg_color='#98a778',
                                             background_corner_colors=('#304c29','#35502c','#59743e','#59743e'),
                                             hover_color='#59743e',
                                             corner_radius=8,
                                             border_width=2,
                                             border_color='#FFFFFF',
                                             text='', image=modeSelection_image, command=modeSelection_button)

        modeSelection_button.grid(row=0, column=0, sticky='s', pady=(0,275))

class settings(Page):    
    def __init__(self, controller, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = ctk.CTkLabel(self, text="Settings")
        label.grid(row=0, column=0)

        print(f'settings {page_stack}')

        def back_button():
            previous_page = page_stack.pop()
            controller.pages[previous_page].show()
        
        back_button = ctk.CTkButton(self, text="Back", command=back_button)
        back_button.grid(row=0, column=0)

class modeSelection(Page): #selects singleplayer or multiplayer
    def __init__(self, controller, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        label = ctk.CTkLabel(self, text="Mode Selection")
        label.pack()

        def spOptions_button():
            controller.pages['spOptions'].show()
            
        def mpOptions_button():
            controller.pages['mpOptions'].show()

        settingsX = 410
        settingsY = 610
            
        spOptions_button = ctk.CTkButton(self, text="Single Player", command=spOptions_button)
        mpOptions_button = ctk.CTkButton(self, text="Multi Player", command=mpOptions_button)

        spOptions_button.pack()
        mpOptions_button.pack()
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

        global page_stack

        page_stack = []

        #create a dictionary for all of the different selection pages
        self.pages = {}
        #for Subclass in (mainMenu, settings, modeSelection, spOptions, mpOptions, spGame, mpGame, spResults, mpResults):
        for Subclass in (mpResults, spResults, mpGame, spGame, mpOptions, spOptions, modeSelection, settings, mainMenu):
            self.pages[Subclass.__name__] = Subclass(self)
        
        #mm, st, ms, so, mo, sg, mg, sr, mr = self.pages.values()
        mr, sr, mg, sg, mo, so, ms, st, mm = self.pages.values()
        
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