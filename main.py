import customtkinter as ctk #for GUI
import algo
from tkinter.messagebox import askyesno #for pop-up box when exiting the program
from PIL import Image #to import images for buttons and backgrounds

class Page(ctk.CTkFrame): #all page classes (e.g. mainMenu, modeSelection etc.) inherit this class
    def __init__(self, *args, **kwargs):
        ctk.CTkFrame.__init__(self, master=root, *args, **kwargs)
        
    def show(self): #a function to raise all the widgets associated with a particular page to the top, displaying it on the window
        self.lift()

class mainMenu(Page):
    def __init__(self, controller, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        global cur_page
        cur_page = 'mainMenu' #set current page to 'mainMenu'

        frame_mm = ctk.CTkFrame(self) #create a frame for the menu
        frame_mm.grid(row=0, column=0, sticky='nsew')
        
        bg1 = ctk.CTkImage(Image.open('assets/bg.png'), size=(900, 700)) #import background image
        bg1label = ctk.CTkLabel(frame_mm, image = bg1, text = '') #create label to place background image
        bg1label.grid(row=0, column=0)

        #coordinates of various buttons
        mm_settingsX = 410
        mm_settingsY = 610
        ms_settingsX = 450
        ms_settingsY = 610
        quitX = 485
        quitY = 610

        #sets current page variable to 'modeSelection' and shows the widgets associated with the mode selection page
        def modeSelection_button():
            global cur_page
            cur_page = 'modeSelection'
            page_stack.append('mainMenu') #pushes 'mainMenu' to the page stack before showing the mode selection page
            controller.pages['modeSelection'].show() #shows widgets associated with the mode selection page
            
        def check_position(event): #checks the coordinates of any mouse click on the window, and according to parameters, redirects to either the settings page or terminates the program.
            print( f'x: {event.x}, y: {event.y}')
            if page_stack == []: #if the page stack is empty - meaning it points to nothing, then we are at the main menu, and the settings button is at 'mm_settingsX, mm_settingsY', the exit button is at 'quitX, quitY'
                if event.x >= mm_settingsX - 20 and event.x <= mm_settingsX + 20 \
                and event.y >= mm_settingsY - 20 and event.y <= mm_settingsY + 20:
                    page_stack.append('mainMenu') #pushes 'mainMenu' to the page stack before showing the settings page- this way when the back button is pressed in the settings, we recognise that the item on-top of the stack is mainMenu, and can direct back to the main menu.
                    controller.pages['settings'].show()
                elif event.x >= quitX - 20 and event.x <= quitX + 20 \
                and event.y >= quitY - 20 and event.y <= quitY + 20:
                    if askyesno(title='Confirmation', message='Are you sure you want to quit?') == True:
                        root.destroy()
            if cur_page == 'modeSelection': #if current page is the mode selection page, then the settings button is at 'ms_settingsX, ms_settingsY'
                if event.x >= ms_settingsX - 20 and event.x <= ms_settingsX + 20 \
                and event.y >= ms_settingsY - 20 and event.y <= ms_settingsY + 20:
                    page_stack.append('modeSelection') #pushes 'modeSelection' to the page stack before showing the settings page - this way when the back button is pressed in the settings, we recognise that the item on-top of the stack is modeSelection, and can direct back to the mode selection page.
                    controller.pages['settings'].show()

        root.bind('<Button-1>', check_position) #binds the left mouse click to the check_position() function

        modeSelection_image = ctk.CTkImage(Image.open("assets/modeSelection.png"), size=(95, 20)) #import image for button
        #button styling
        modeSelection_button = ctk.CTkButton(frame_mm, width=170, height=50, fg_color='#98a778', background_corner_colors=('#304c29','#35502c','#59743e','#59743e'), hover_color='#59743e', corner_radius=8, border_width=2, border_color='#FFFFFF', text='', image=modeSelection_image, command=modeSelection_button)
        modeSelection_button.grid(row=0, column=0, sticky='s', pady=(0,275))

class settings(Page):
    def __init__(self, controller, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        label = ctk.CTkLabel(self, text="Settings")
        label.grid(row=0, column=0)

        def back_button(): #directs to either the main menu or mode selection page depending on the contents of the page stack
            previous_page = page_stack.pop() #returns the top of the stack to identify the page previous to the settings page
            controller.pages[previous_page].show() #shows the page previous to the settings page
        
        back_button = ctk.CTkButton(self, text="Back", command=back_button) #back button styling WIP
        back_button.grid(row=0, column=0)

class modeSelection(Page): #selects singleplayer or multiplayer
    def __init__(self, controller, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        global cur_page
        
        frame_ms = ctk.CTkFrame(self) #creates frame for the mode selection page
        frame_ms.grid(row=0, column=0, sticky='nsew')

        bg2 = ctk.CTkImage(Image.open('assets/bg2.png'), size=(900, 700)) #
        bg2label = ctk.CTkLabel(frame_ms, image = bg2, text = '')
        bg2label.grid(row=0, column=0)

        def spOptions_button():
            controller.pages['spOptions'].show()
            
        def mpOptions_button():
            controller.pages['mpOptions'].show()

        def back_button():
            global cur_page
            cur_page = 'settings'
            previous_page = page_stack.pop()
            controller.pages[previous_page].show()
        
        back_button = ctk.CTkButton(frame_ms, height=40, fg_color='#98a778', hover_color='#59743e', corner_radius=8, border_width=2, border_color='#FFFFFF', text_color='#FFFFFF', font=('Upheaval TT (BRK)', 35), text="<", command=back_button)

        back_button.grid(row=0, column=0, padx=(0,520), pady=(0,494))
        
        spOptions_image = ctk.CTkImage(Image.open("assets/sp_button.png"), size=(245,245))
        mpOptions_image = ctk.CTkImage(Image.open("assets/mp_button.png"), size=(250,250))

        spOptions_button = ctk.CTkButton(frame_ms, width=290, height=346, corner_radius=20, fg_color='#82925e', hover_color='#606c46', background_corner_colors=('#3f522b','#3f522b','#839b61','#3f522b'), border_width=2, border_color='#c7ced7', text="", image=spOptions_image, command=spOptions_button)
        mpOptions_button = ctk.CTkButton(frame_ms, width=290, height=346, corner_radius=20, fg_color='#82925e', hover_color='#606c46', background_corner_colors=('#3f522b','#3f522b','#3f522b','#839b61'), border_width=2, border_color='#c7ced7', text="", image=mpOptions_image, command=mpOptions_button)

        spOptions_button.grid(row=0, column=0, padx=(0,382), pady=(36,0))
        mpOptions_button.grid(row=0, column=0, padx=(399,0), pady=(36,0))

class spOptions(Page): #screen to select generation style and grid size for singleplayer
    def __init__(self, controller, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        m_frame = ctk.CTkFrame(self)
        m_frame.grid(row=0, column=0, sticky='nsew')

        bg3 = ctk.CTkImage(Image.open('assets/bg3.png'), size=(900, 700)) 
        bg3label = ctk.CTkLabel(m_frame, image = bg3, text = '')
        bg3label.grid(row=0, column=0)

        s_frame = ctk.CTkFrame(m_frame, width=900, height=650, fg_color='#82925e', border_width=2, border_color='#c7ced7')
        s_frame.grid(row=0, column=0, padx=70, pady=(70,90))

        def combobox_callback(choice):
            global params
            if choice == -1:
                params[0] = int(get_current_value())
            else:
                params = [int(get_current_value()), choice]

        title_label = ctk.CTkLabel(s_frame, text='-Singleplayer Options-', text_color='#FFFFFF', font=('Upheaval TT (BRK)', 35))
        title_label.grid(row=0, column=0, padx = (0, 10), pady=(20, 300))

        combobox = ctk.CTkComboBox(s_frame, width=400, height=50, 
                                   values=['Depth First Search', 'Hunt-and-Kill', 'Sidewinder'], 
                                   font=('Upheaval TT (BRK)', 20), 
                                   dropdown_font=('Upheaval TT (BRK)', 20), 
                                   command=combobox_callback)
        combobox.set('Select a generation algorithm')
        combobox.grid(row=0, column=0, padx=100, pady=(0, 120))

        slider_value = ctk.DoubleVar()

        def get_current_value():
            value = '{: .0f}'.format(slider_value.get()*25+5)
            return value
        
        def format_value(value):
            return f'{value} x{value}'
        
        def slider_changed(event):
            slider_value_label.configure(text=format_value(get_current_value()))

        slider_label = ctk.CTkLabel(s_frame, text='> Grid size:', text_color='#FFFFFF', font=('Upheaval TT (BRK)', 30))
        slider_label.grid(row=0, column=0, padx = (0, 255), pady=(15, 0))

        slider_value_label = ctk.CTkLabel(s_frame, text=format_value(get_current_value()), text_color='#FFFFFF', font=('Upheaval TT (BRK)', 30))
        slider_value_label.grid(row=0, column=0, padx = (50, 0), pady=(15, 0))

        slider = ctk.CTkSlider(s_frame, width=400, button_color='#FFFFFF', button_hover_color='#cccccc', variable=slider_value, command=slider_changed)
        slider.grid(row=0, column=0, padx = (0, 0), pady=(110, 0))

        def spGame_button():
            combobox_callback(-1)
            sg.spGameCanvas()
            controller.pages['spGame'].show()

        spGame_button = ctk.CTkButton(s_frame, fg_color='#75a050', hover_color='#3d5329', text='START', text_color='#FFFFFF', font=('Upheaval TT (BRK)', 30), border_width=2, border_color='#c7ced7', command=spGame_button)
        spGame_button.grid(row=0, column=0, padx=10, pady=(230, 0))

class mpOptions(Page): #screen to select generation style and grid size for multiplayer
    def __init__(self, controller, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        m_frame = ctk.CTkFrame(self)
        m_frame.grid(row=0, column=0, sticky='nsew')

        bg3 = ctk.CTkImage(Image.open('assets/bg3.png'), size=(900, 700)) 
        bg3label = ctk.CTkLabel(m_frame, image = bg3, text = '')
        bg3label.grid(row=0, column=0)

        s_frame = ctk.CTkFrame(m_frame, width=900, height=650, fg_color='#82925e', border_width=2, border_color='#c7ced7')
        s_frame.grid(row=0, column=0, padx=70, pady=(70,90))

        def combobox_callback(choice):
            global params
            if choice == -1:
                params[0] = int(get_current_value())
            else:
                params = [int(get_current_value()), choice]

        title_label = ctk.CTkLabel(s_frame, text='-Multiplayer Options-', text_color='#FFFFFF', font=('Upheaval TT (BRK)', 35))
        title_label.grid(row=0, column=0, padx = (0, 10), pady=(20, 300))

        combobox = ctk.CTkComboBox(s_frame, width=400, height=50, 
                                   values=['Depth First Search', 'Hunt-and-Kill', 'Sidewinder'], 
                                   font=('Upheaval TT (BRK)', 20), 
                                   dropdown_font=('Upheaval TT (BRK)', 20), 
                                   command=combobox_callback)
        combobox.set('Select a generation algorithm')
        combobox.grid(row=0, column=0, padx=100, pady=(0, 120))

        slider_value = ctk.DoubleVar()

        def get_current_value():
            value = '{: .0f}'.format(slider_value.get()*25+5)
            return value
        
        def format_value(value):
            return f'{value} x{value}'
        
        def slider_changed(event):
            slider_value_label.configure(text=format_value(get_current_value()))

        slider_label = ctk.CTkLabel(s_frame, text='> Grid size:', text_color='#FFFFFF', font=('Upheaval TT (BRK)', 30))
        slider_label.grid(row=0, column=0, padx = (0, 255), pady=(15, 0))

        slider_value_label = ctk.CTkLabel(s_frame, text=format_value(get_current_value()), text_color='#FFFFFF', font=('Upheaval TT (BRK)', 30))
        slider_value_label.grid(row=0, column=0, padx = (50, 0), pady=(15, 0))

        slider = ctk.CTkSlider(s_frame, width=400, button_color='#FFFFFF', button_hover_color='#cccccc', variable=slider_value, command=slider_changed)
        slider.grid(row=0, column=0, padx = (0, 0), pady=(110, 0))

        def mpGame_button():
            combobox_callback(-1)
            mg.mpGameCanvas()
            controller.pages['mpGame'].show()

        mpGame_button = ctk.CTkButton(s_frame, fg_color='#75a050', hover_color='#3d5329', text='START', text_color='#FFFFFF', font=('Upheaval TT (BRK)', 30), border_width=2, border_color='#c7ced7', command=mpGame_button)
        mpGame_button.grid(row=0, column=0, padx=10, pady=(230, 0))

class spGame(Page): #singleplayer game screen
    def __init__(self, controller, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        label = ctk.CTkLabel(self, text="Singleplayer Game")
        label.grid(row=0, column=0, padx=10, pady=10)

    def spGameCanvas(self):

        game_frame = ctk.CTkFrame(self, width=600, height=600)
        game_frame.grid(row=1, column=0)

        algo.create_canvas(game_frame)
        algo.graph = algo.Graph(params[0])
     
        if params[1] == 'Depth First Search':
            algo.graph.DFS()
        elif params[1] == 'Hunt-and-Kill':
            algo.graph.Hunt_and_Kill()
        elif params[1] == 'Sidewinder':
            algo.graph.Sidewinder()
           
        algo.draw_maze(params[0])
        algo.draw_player('single')

class mpGame(Page): #multiplayer game screen
    def __init__(self, controller, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = ctk.CTkLabel(self, text="Multiplayer Game")
        label.grid(row=0, column=0, padx=10, pady=10)

    def mpGameCanvas(self):

        game_frame = ctk.CTkFrame(self, width=600, height=600)
        game_frame.grid(row=1, column=0)

        algo.create_canvas(game_frame)
        algo.graph = algo.Graph(params[0])
     
        if params[1] == 'Depth First Search':
            algo.graph.DFS()
        elif params[1] == 'Hunt-and-Kill':
            algo.graph.Hunt_and_Kill()
        elif params[1] == 'Sidewinder':
            algo.graph.Sidewinder()
           
        algo.draw_maze(params[0])
        algo.draw_player('multi')

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

        #variables for a dynamic back button
        global page_stack, cur_page, sg, mg
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
    #initialises the tkinter window
    root = ctk.CTk()
    main = Window(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("900x700") #window size
    root.wm_title('Hedge') #window title
    root.wm_iconbitmap('assets/icon.ico') #window icon
    #root.wm_resizable(False, False) #makes window a fixed size

    root.bind('<w>', algo.move_p1)
    root.bind('<a>', algo.move_p1)
    root.bind('<s>', algo.move_p1)
    root.bind('<d>', algo.move_p1)

    root.bind('<Up>', algo.move_p2)
    root.bind('<Left>', algo.move_p2)
    root.bind('<Down>', algo.move_p2)
    root.bind('<Right>', algo.move_p2)

    root.mainloop()

    