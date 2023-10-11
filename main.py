import customtkinter as ctk
from tkinter.messagebox import askyesno
from PIL import Image

class Page(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        ctk.CTkFrame.__init__(self, master=root, *args, **kwargs)
        
    def show(self):
        self.lift()

class mainMenu(Page):
    def __init__(self, controller, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        global cur_page
        cur_page = 'mainMenu'

        frame1 = ctk.CTkFrame(self)
        frame1.grid(row=0, column=0, sticky='nsew')
        
        bg1 = ctk.CTkImage(Image.open('assets/bg.png'), size=(900, 700))
        bg1label = ctk.CTkLabel(frame1, image = bg1, text = '')
        bg1label.grid(row=0, column=0)

        mm_settingsX = 410
        mm_settingsY = 610
        ms_settingsX = 450
        ms_settingsY = 610
        quitX = 485
        quitY = 610

        def modeSelection_button():
            global cur_page
            cur_page = 'modeSelection'
            page_stack.append('mainMenu')
            controller.pages['modeSelection'].show()
            
        def check_position(event):
            print( f'x: {event.x}, y: {event.y}')
            if page_stack == []:
                if event.x >= mm_settingsX - 20 and event.x <= mm_settingsX + 20 \
                and event.y >= mm_settingsY - 20 and event.y <= mm_settingsY + 20:
                    page_stack.append('mainMenu')
                    controller.pages['settings'].show()
                elif event.x >= quitX - 20 and event.x <= quitX + 20 \
                and event.y >= quitY - 20 and event.y <= quitY + 20:
                    if askyesno(title='Confirmation', message='Are you sure you want to quit?') == True:
                        root.destroy()
            if cur_page == 'modeSelection':
                if event.x >= ms_settingsX - 20 and event.x <= ms_settingsX + 20 \
                and event.y >= ms_settingsY - 20 and event.y <= ms_settingsY + 20:
                    page_stack.append('modeSelection')
                    controller.pages['settings'].show()

        root.bind('<Button-1>', check_position)

        modeSelection_image = ctk.CTkImage(Image.open("assets/modeSelection.png"), size=(95, 20))
        modeSelection_button = ctk.CTkButton(frame1, width=170, height=50, fg_color='#98a778', background_corner_colors=('#304c29','#35502c','#59743e','#59743e'), hover_color='#59743e', corner_radius=8, border_width=2, border_color='#FFFFFF', text='', image=modeSelection_image, command=modeSelection_button)
        modeSelection_button.grid(row=0, column=0, sticky='s', pady=(0,275))

class settings(Page):    
    def __init__(self, controller, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        label = ctk.CTkLabel(self, text="Settings")
        label.grid(row=0, column=0)

        def back_button():
            previous_page = page_stack.pop()
            controller.pages[previous_page].show()
        
        back_button = ctk.CTkButton(self, text="Back", command=back_button)
        back_button.grid(row=0, column=0)

class modeSelection(Page): #selects singleplayer or multiplayer
    def __init__(self, controller, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        global cur_page
        
        frame = ctk.CTkFrame(self)
        frame.grid(row=0, column=0, sticky='nsew')

        bg2 = ctk.CTkImage(Image.open('assets/bg2.png'), size=(900, 700))
        bg1label = ctk.CTkLabel(frame, image = bg2, text = '')
        bg1label.grid(row=0, column=0)

        def spOptions_button():
            controller.pages['spOptions'].show()
            
        def mpOptions_button():
            controller.pages['mpOptions'].show()

        def back_button():
            global cur_page
            cur_page = 'settings'
            previous_page = page_stack.pop()
            controller.pages[previous_page].show()
        
        back_button = ctk.CTkButton(frame, height=40, fg_color='#98a778', hover_color='#59743e', corner_radius=8, border_width=2, border_color='#FFFFFF', text="BACK", command=back_button)

        back_button.grid(row=0, column=0, padx=(0,520), pady=(0,494))
        
        spOptions_image = ctk.CTkImage(Image.open("assets/sp_button.png"), size=(245,245))
        mpOptions_image = ctk.CTkImage(Image.open("assets/mp_button.png"), size=(250,250))

        spOptions_button = ctk.CTkButton(frame, width=290, height=346, corner_radius=20, fg_color='#82925e', hover_color='#606c46', background_corner_colors=('#3f522b','#3f522b','#839b61','#3f522b'), border_width=2, border_color='#c7ced7', text="", image=spOptions_image, command=spOptions_button)
        mpOptions_button = ctk.CTkButton(frame, width=290, height=346, corner_radius=20, fg_color='#82925e', hover_color='#606c46', background_corner_colors=('#3f522b','#3f522b','#3f522b','#839b61'), border_width=2, border_color='#c7ced7', text="", image=mpOptions_image, command=mpOptions_button)

        spOptions_button.grid(row=0, column=0, padx=(0,382), pady=(36,0))
        mpOptions_button.grid(row=0, column=0, padx=(399,0), pady=(36,0))

class spOptions(Page): #screen to select generation style and grid size for singleplayer
    def __init__(self, controller, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = ctk.CTkLabel(self, text="Singleplayer Options")
        label.grid(row=0, column=0, padx=10, pady=10)

        def spGame_button():
            controller.pages['spGame'].show()

        c_frame = ctk.CTkFrame(self, width=600, height=600)
        c_frame.grid(row=1, column=1, sticky='nsew')

        def combobox_callback(choice):
            print("combobox dropdown clicked:", choice)

        combobox = ctk.CTkComboBox(c_frame, width=300, height=30, values=['Depth First Search', 'Hunt-and-Kill', 'Sidewinder'], command=combobox_callback)
        combobox.set('Select a generation algorithm')
        combobox.grid(row=0, column=0, padx=100, pady=50)

        slider = ctk.CTkSlider(c_frame)
        slider.grid(row=1, column=0, padx=100, pady=50)

        spGame_button = ctk.CTkButton(self, text="Start Game", command=spGame_button)

        spGame_button.grid(row=2, column=3, padx=10, pady=10)

class mpOptions(Page): #screen to select generation style and grid size for multiplayer
    def __init__(self, controller, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = ctk.CTkLabel(self, text="Multiplayer Options")
        label.grid(row=0, column=0, padx=10, pady=10)
        
        def mpGame_button():
            controller.pages['mpGame'].show()

        mpGame_button = ctk.CTkButton(self, text="Start Game", command=mpGame_button)

        mpGame_button.grid(row=0, column=0, padx=10, pady=10)

class spGame(Page): #singleplayer game screen
    def __init__(self, controller, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = ctk.CTkLabel(self, text="Singleplayer Game")
        label.grid(row=0, column=0, padx=10, pady=10)

        back_button = ctk.CTkButton(self, text="Back")
        back_button.grid(row=0, column=0, padx=10, pady=10)

class mpGame(Page): #multiplayer game screen
    def __init__(self, controller, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = ctk.CTkLabel(self, text="Multiplayer Game")
        label.grid(row=0, column=0, padx=10, pady=10)

        back_button = ctk.CTkButton(self, text="Back")
        back_button.grid(row=0, column=0, padx=10, pady=10)

class spResults(Page): #singleplayer results screen
    def __init__(self, controller, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = ctk.CTkLabel(self, text="Singleplayer Results")
        label.grid(row=0, column=0, padx=10, pady=10)

        back_button = ctk.CTkButton(self, text="Back")
        back_button.grid(row=0, column=0, padx=10, pady=10)

class mpResults(Page): #multiplayer results screen
    def __init__(self, controller, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = ctk.CTkLabel(self, text="Multiplayer Results")
        label.grid(row=0, column=0, padx=10, pady=10)
        
        back_button = ctk.CTkButton(self, text="Back")

class Window(ctk.CTkFrame): #create main window
    def __init__(self, *args, **kwargs):
        ctk.CTkFrame.__init__(self, *args, **kwargs)

        global page_stack, cur_page

        page_stack = []
        cur_page = ''

        #create a dictionary for all of the different selection pages
        self.pages = {}
        for Subclass in (mainMenu, settings, modeSelection, spOptions, mpOptions, spGame, mpGame, spResults, mpResults):
            self.pages[Subclass.__name__] = Subclass(self)
        
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