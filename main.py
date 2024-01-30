import customtkinter as ctk #for GUI
#import pywinstyles
import time
import algo
from tkinter.messagebox import askyesno #for pop-up box when exiting the program
from PIL import Image, ImageTk #to import images for buttons and backgrounds

theme = 'system'
ctk.set_appearance_mode(theme)
ctk.set_default_color_theme("assets/HEDGE.json")

if theme == 'light':
    bg1 = ctk.CTkImage(Image.open('assets/grad1bg.png'), size=(1920, 1080)) #import background image
    bg2 = ctk.CTkImage(Image.open('assets/bg1.png'), size=(900, 700))
    bg_game = ctk.CTkImage(Image.open('assets/grad1game.png'), size=(1920, 1080))
else:
    bg1 = ctk.CTkImage(Image.open('assets/grad2bg.png'), size=(1920, 1080)) #import background image
    bg2 = ctk.CTkImage(Image.open('assets/bg2.png'), size=(900, 700))
    bg_game = ctk.CTkImage(Image.open('assets/grad2game.png'), size=(1920, 1080))

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

        m_frame = ctk.CTkFrame(self) #create a frame for the menu
        m_frame.pack(side='top', expand=True, fill = 'both')
        
        self.bg1label = ctk.CTkLabel(m_frame, image = bg1, text = '') #create label to place background image
        self.bg1label.place(relx=0.5, rely=0.5, anchor='center')

        s_frame = ctk.CTkFrame(m_frame, height=700, width=900, corner_radius=0)
        s_frame.place(relx=0.5, rely=0.5, anchor='center')

        self.bg2label = ctk.CTkLabel(s_frame, image = bg2, text = '')
        self.bg2label.place(relx=0.5, rely=0.5, anchor='center')

        title = ctk.CTkLabel(s_frame, text='HEDGE', font=('Upheaval TT (BRK)', 120))
        title.place(relx=0.5, rely=0.38, anchor='center')

        #quit_button_label = ctk.CTkLabel(sframe, image = ctk.CTkImage(Image.open('assets/quit.png'), size=(43, 43)), text = '')
        #quit_button_label.place(relx=0.54, rely=0.875, anchor='center')

        #settings_button_label = ctk.CTkLabel(sframe, image = ctk.CTkImage(Image.open('assets/settings.png'), size=(43, 43)), text = '')
        #settings_button_label.place(relx=0.46, rely=0.875, anchor='center')        

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
            print(event)
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

        #button styling
        modeSelection_button = ctk.CTkButton(s_frame, width=170, height=50, corner_radius=8, border_width=2, text_color='#FFFFFF', font=('Upheaval TT (BRK)', 40), text='PLAY', command=modeSelection_button)
        modeSelection_button.place(relx=0.5, rely=0.57, anchor='center')

class settings(Page):
    def __init__(self, controller, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        self.bg1label = ctk.CTkLabel(self, image = bg1, text = '') #create label to place background image
        self.bg1label.place(relx=0.5, rely=0.5, anchor='center')


        def back_button(): #directs to either the main menu or mode selection page depending on the contents of the page stack
            previous_page = page_stack.pop() #returns the top of the stack to identify the page previous to the settings page
            controller.pages[previous_page].show() #shows the page previous to the settings page
        
        back_button = ctk.CTkButton(self, height=40, fg_color='#98a778', bg_color='#96ab72', hover_color='#59743e', corner_radius=8, border_width=2, border_color='#FFFFFF', text_color='#FFFFFF', font=('Upheaval TT (BRK)', 25), text="< BACK", command=back_button)
        back_button.place(relx=0.3, rely=0.2, anchor='center')

class modeSelection(Page): #selects singleplayer or multiplayer
    def __init__(self, controller, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        global cur_page

        self.bg1label = ctk.CTkLabel(self, image = bg1, text = '') #create label to place background image
        self.bg1label.place(relx=0.5, rely=0.5, anchor='center')
        
        frame_ms = ctk.CTkFrame(self, width=900, height=700) #creates frame for the mode selection page
        frame_ms.place(relx=0.5, rely=0.5, anchor='center')

        def spOptions_button():
            controller.pages['spOptions'].show()
            
        def mpOptions_button():
            controller.pages['mpOptions'].show()

        def back_button():
            global cur_page
            cur_page = 'settings'
            previous_page = page_stack.pop()
            controller.pages[previous_page].show()
        
        back_button = ctk.CTkButton(frame_ms, height=40, corner_radius=8, border_width=3, text_color='#FFFFFF', font=('Upheaval TT (BRK)', 25), text="< BACK", command=back_button)

        back_button.grid(row=0, column=0, padx=(0,537), pady=(0,494))
        
        spOptions_image = ctk.CTkImage(Image.open("assets/sp_button.png"), size=(245,245))
        mpOptions_image = ctk.CTkImage(Image.open("assets/mp_button.png"), size=(250,250))

        spOptions_button = ctk.CTkButton(frame_ms, width=290, height=346, corner_radius=20, text="", border_width=5, image=spOptions_image, command=spOptions_button)
        mpOptions_button = ctk.CTkButton(frame_ms, width=290, height=346, corner_radius=20, text="", border_width=5, image=mpOptions_image, command=mpOptions_button)

        spOptions_button.grid(row=0, column=0, padx=(0,399), pady=(36,0))
        mpOptions_button.grid(row=0, column=0, padx=(399,0), pady=(36,0))

class spOptions(Page): #screen to select generation style and grid size for singleplayer
    def __init__(self, controller, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        global sp_time_start

        self.bg1label = ctk.CTkLabel(self, image = bg1, text = '') #create label to place background image
        self.bg1label.place(relx=0.5, rely=0.5, anchor='center')

        m_frame = ctk.CTkFrame(self, width=900, height=700)
        m_frame.place(relx=0.5, rely=0.5, anchor='center')

        s_frame = ctk.CTkFrame(m_frame, width=675, height=380, border_width=5, corner_radius=15)
        s_frame.place(relx=0.5, rely=0.55, anchor='center')

        def combobox_callback(choice):
            global sp_params
            if choice == 0:
                sp_params = [] #creates sp_params if combobox is not selected and the start game button is pressed
            elif choice == -1:
                sp_params[0] = int(get_current_value())
            else:
                sp_params = [int(get_current_value()), choice]

        title_label = ctk.CTkLabel(s_frame, text='-Singleplayer Options-', font=('Upheaval TT (BRK)', 35), text_color='#FFFFFF')
        title_label.place(relx=0.5, rely=0.12, anchor='center')

        combobox = ctk.CTkComboBox(s_frame, width=400, height=50, 
                                   values=['Depth First Search', 'Hunt-and-Kill', 'Sidewinder'], 
                                   font=('Upheaval TT (BRK)', 20), 
                                   dropdown_font=('Upheaval TT (BRK)', 20),
                                   command=combobox_callback)
        combobox.set('Select a generation algorithm')
        combobox.place(relx=0.5, rely=0.31, anchor='center')

        slider_value = ctk.DoubleVar()

        def get_current_value():
            value = '{: .0f}'.format(slider_value.get()*25+5)
            return value
        
        def format_value(value):
            return f'{value} x{value}'
        
        def slider_changed(event):
            slider_value_label.configure(text=format_value(get_current_value()))

        slider_label = ctk.CTkLabel(s_frame, text='> Grid size:', font=('Upheaval TT (BRK)', 30))
        slider_label.place(relx=0.3, rely=0.51, anchor='center')

        slider_value_label = ctk.CTkLabel(s_frame, text=format_value(get_current_value()), text_color='#FFFFFF', font=('Upheaval TT (BRK)', 30))
        slider_value_label.place(relx=0.55, rely=0.51, anchor='center')

        slider = ctk.CTkSlider(s_frame, width=400, button_color='#FFFFFF', button_hover_color='#cccccc', variable=slider_value, command=slider_changed)
        slider.place(relx=0.5, rely=0.66, anchor='center')

        combobox_error_message = ctk.CTkLabel(m_frame, text='', text_color='#e53935', font=('Upheaval TT (BRK)', 15))
        combobox_error_message.grid(row=0, column=0, padx=(0,260), pady=(465, 0))

        def spGame_button():
            global sp_time_start
            if sp_params != []:
                combobox_callback(-1)
                sg.spGameCanvas()
                sp_time_start = time.time()
                controller.pages['spGame'].show()
                combobox_error_message.configure(text='')
            else:
                combobox_error_message.configure(text='error : no maze generation algorithm selected')
                
        spGame_button = ctk.CTkButton(s_frame, height=40, fg_color='#75a050', hover_color='#3d5329', text='START', text_color='#FFFFFF', font=('Upheaval TT (BRK)', 30), border_width=2, border_color='#c7ced7', command=spGame_button)
        spGame_button.place(relx=0.5, rely=0.84, anchor='center')

        def back_button():
            combobox_error_message.configure(text='')
            controller.pages['modeSelection'].show()
        
        back_button = ctk.CTkButton(m_frame, height=40, corner_radius=8, border_width=3, text_color='#FFFFFF', font=('Upheaval TT (BRK)', 25), text="< BACK", command=back_button)
        back_button.grid(row=0, column=0, padx=(0,536), pady=(0,494))

        combobox_callback(0)

class mpOptions(Page): #screen to select generation style and grid size for multiplayer
    def __init__(self, controller, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        self.bg1label = ctk.CTkLabel(self, image = bg1, text = '') #create label to place background image
        self.bg1label.place(relx=0.5, rely=0.5, anchor='center')
        
        m_frame = ctk.CTkFrame(self, width=900, height=700)
        m_frame.place(relx=0.5, rely=0.5, anchor='center')

        s_frame = ctk.CTkFrame(m_frame, width=675, height=380, border_width=5, corner_radius=15)
        s_frame.place(relx=0.5, rely=0.55, anchor='center')

        def combobox_callback(choice):
            global mp_params
            if choice == 0:
                mp_params = [] #creates mp_params if combobox is not selected and the start game button is pressed
            elif choice == -1:
                mp_params[0] = int(get_current_value())
            else:
                mp_params = [int(get_current_value()), choice]

        title_label = ctk.CTkLabel(s_frame, text='-Multiplayer Options-', font=('Upheaval TT (BRK)', 35), text_color='#FFFFFF')
        title_label.place(relx=0.5, rely=0.12, anchor='center')

        combobox = ctk.CTkComboBox(s_frame, width=400, height=50, 
                                   values=['Depth First Search', 'Hunt-and-Kill', 'Sidewinder'], 
                                   font=('Upheaval TT (BRK)', 20), 
                                   dropdown_font=('Upheaval TT (BRK)', 20),
                                   command=combobox_callback)
        combobox.set('Select a generation algorithm')
        combobox.place(relx=0.5, rely=0.31, anchor='center')

        slider_value = ctk.DoubleVar()

        def get_current_value():
            value = '{: .0f}'.format(slider_value.get()*25+5)
            return value
        
        def format_value(value):
            return f'{value} x{value}'
        
        def slider_changed(event):
            slider_value_label.configure(text=format_value(get_current_value()))

        slider_label = ctk.CTkLabel(s_frame, text='> Grid size:', font=('Upheaval TT (BRK)', 30))
        slider_label.place(relx=0.3, rely=0.51, anchor='center')

        slider_value_label = ctk.CTkLabel(s_frame, text=format_value(get_current_value()), text_color='#FFFFFF', font=('Upheaval TT (BRK)', 30))
        slider_value_label.place(relx=0.55, rely=0.51, anchor='center')

        slider = ctk.CTkSlider(s_frame, width=400, button_color='#FFFFFF', button_hover_color='#cccccc', variable=slider_value, command=slider_changed)
        slider.place(relx=0.5, rely=0.66, anchor='center')

        combobox_error_message = ctk.CTkLabel(m_frame, text='', text_color='#e53935', font=('Upheaval TT (BRK)', 15))
        combobox_error_message.grid(row=0, column=0, padx=(0,260), pady=(465, 0))

        def mpGame_button():
            if mp_params != []:
                combobox_callback(-1)
                mg.mpGameCanvas()
                controller.pages['mpGame'].show()
                combobox_error_message.configure(text='')
            else:
                combobox_error_message.configure(text='error : no maze generation algorithm selected')

        mpGame_button = ctk.CTkButton(s_frame, height=40, fg_color='#75a050', hover_color='#3d5329', text='START', text_color='#FFFFFF', font=('Upheaval TT (BRK)', 30), border_width=2, border_color='#c7ced7', command=mpGame_button)
        mpGame_button.place(relx=0.5, rely=0.84, anchor='center')

        def back_button():
            combobox_error_message.configure(text='')
            controller.pages['modeSelection'].show()

        back_button = ctk.CTkButton(m_frame, height=40, corner_radius=8, border_width=3, text_color='#FFFFFF', font=('Upheaval TT (BRK)', 25), text="< BACK", command=back_button)

        #back_button.grid(row=0, column=0, padx=(0,460), pady=(0,494))
        back_button.grid(row=0, column=0, padx=(0,536), pady=(0,494))

        combobox_callback(0)

class spGame(Page): #singleplayer game screen
    def __init__(self, controller, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        self.controller = controller

        self.bg1label = ctk.CTkLabel(self, image = bg_game, text = '') #create label to place background image
        self.bg1label.place(relx=0.5, rely=0.5, anchor='center')

        title_frame = ctk.CTkFrame(self)
        title_frame.place(relx=0.5, rely=0.1, anchor='center')
        title = ctk.CTkLabel(title_frame, text=" HEDGE ", text_color='#4a6f3e', font=('Upheaval TT (BRK)', 80))
        subheading = ctk.CTkLabel(title_frame, text="SINGLEPLAYER ", text_color='#FFFFFF', font=('Upheaval TT (BRK)', 40, 'italic'))
        title.pack()
        subheading.pack()
        
        #frame to contain gui information on left
        left_frame = ctk.CTkFrame(self, height=228, width=380)
        left_frame.place(relx=0.15, rely=0.495, anchor='center')
        
        left_image = ctk.CTkImage(Image.open("assets/game_left.png"), size=(191, 227))
        left_image_label = ctk.CTkLabel(left_frame, text='', image=left_image)
        left_image_label.place(relx=0, rely=0.5, anchor='w')

        self.algo_label = ctk.CTkLabel(left_frame, text='', text_color='#FFFFFF', font=('Upheaval TT (BRK)', 35, 'italic'))
        self.grid_label = ctk.CTkLabel(left_frame, text='', text_color='#FFFFFF', font=('Upheaval TT (BRK)', 35, 'italic'))
        self.algo_label.place(x=150, rely=0.11)
        self.grid_label.place(x=150, rely=0.61)

        #

        right_frame = ctk.CTkFrame(self, height=228, width=380)
        right_frame.place(relx=0.85, rely=0.495, anchor='center')

        right_image = ctk.CTkImage(Image.open('assets/sg_right.png'), size=(233, 227))
        right_image_label = ctk.CTkLabel(right_frame, text='', image=right_image)
        right_image_label.place(x=380, rely=0.5, anchor='e')
    
        self.step_label = ctk.CTkLabel(right_frame, text='', text_color='#FFFFFF', font=('Upheaval TT (BRK)', 45, 'italic'))
        self.time_label = ctk.CTkLabel(right_frame, text='', text_color='#4a6f3e', font=('Upheaval TT (BRK)', 45, 'italic'))
        self.step_label.place(x=180, rely=0.145, anchor='e')
        self.time_label.place(x=100, rely=0.655, anchor='w')

        #
        #a temporary back button
        def back_button():
            self.update = False
            controller.pages['spOptions'].show()
        
        back_button = ctk.CTkButton(self, height=40, font=('Upheaval TT (BRK)', 15), text="demo bck", command=back_button)
        back_button.place(relx=0.2, rely=0.1, anchor='center')
        #
        #

    def spGameCanvas(self):
        global sp_time_end
        self.update = True

        game_frame = ctk.CTkFrame(self, width=600, height=600)
        game_frame.place(relx=0.5, rely=0.5, anchor='center')

        algo.create_canvas(game_frame)
        algo.graph = algo.Graph(sp_params[0])

        self.grid_label.configure(text=f'{sp_params[0]} x {sp_params[0]}')
     
        if sp_params[1] == 'Depth First Search':
            algo.graph.DFS()
            self.algo_label.configure(text='DFS')
        elif sp_params[1] == 'Hunt-and-Kill':
            algo.graph.Hunt_and_Kill()
            self.algo_label.configure(text='Hunt - Kill')
        elif sp_params[1] == 'Sidewinder':
            algo.graph.Sidewinder()
            self.algo_label.configure(text='Sidewinder')
         
        algo.draw_maze()
        algo.draw_player('single')
        algo.p1moves = 0

        def spUpdate():
            global sp_time_end
            if algo.detect_win('single'):
                self.update = False
                sp_time_end = time.time()
                sr.results()
                self.controller.pages['spResults'].show()
            if self.update == True:
                self.step_label.configure(text=f'{algo.get_moves("single")}  ')
                self.time_label.configure(text=f'{round(time.time()-sp_time_start, 1)}  ')
                root.after(100, spUpdate)

        root.after(0, spUpdate)

class mpGame(Page): #multiplayer game screen
    def __init__(self, controller, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        self.controller = controller

        label = ctk.CTkLabel(self, text="Multiplayer Game", text_color='#FFFFFF', font=('Upheaval TT (BRK)', 25))
        label.grid(row=0, column=0, padx=10, pady=10)

        def back_button():
            controller.pages['mpOptions'].show()
        
        back_button = ctk.CTkButton(self, height=40, fg_color='#98a778', hover_color='#59743e', corner_radius=8, border_width=2, border_color='#FFFFFF', text_color='#FFFFFF', font=('Upheaval TT (BRK)', 15), text="demo bck", command=back_button)

        back_button.grid(row=0, column=0, padx=(0,465))  

    def mpGameCanvas(self):

        self.update = True

        game_frame = ctk.CTkFrame(self, width=600, height=600)
        game_frame.grid(row=1, column=0, padx = 150)

        algo.create_canvas(game_frame)
        algo.graph = algo.Graph(mp_params[0])
     
        if mp_params[1] == 'Depth First Search':
            algo.graph.DFS()
        elif mp_params[1] == 'Hunt-and-Kill':
            algo.graph.Hunt_and_Kill()
        elif mp_params[1] == 'Sidewinder':
            algo.graph.Sidewinder()
           
        algo.draw_maze()
        algo.draw_player('multi')

        algo.p1moves = 0
        algo.p2moves = 0

        def mpUpdate():
            if algo.detect_win('multi') != False:
                self.update = False
                self.controller.pages['mpResults'].show()
            if self.update == True:
                root.after(100, mpUpdate)

        root.after(0, mpUpdate)

class spResults(Page): #singleplayer results screen
    def __init__(self, controller, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = ctk.CTkLabel(self, text="Singleplayer Results")
        label.grid(row=0, column=1, padx=10, pady=10)
    
    def results(self):
        steps = ctk.CTkLabel(self, text=f'Moves = {algo.get_moves("single")}', font=('Upheaval TT (BRK)', 25))
        steps.grid(row=1, column=1)
        time = ctk.CTkLabel(self, text=f'Time = {round(sp_time_end - sp_time_start, 3)} s', font=('Upheaval TT (BRK)', 25))
        time.grid(row=2, column=1)

class mpResults(Page): #multiplayer results screen
    def __init__(self, controller, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = ctk.CTkLabel(self, text="Multiplayer Results")
        label.grid(row=0, column=0, padx=10, pady=10)
        
class Window(ctk.CTkFrame): #create main window
    def __init__(self, *args, **kwargs):
        ctk.CTkFrame.__init__(self, *args, **kwargs)

        #variables for a dynamic back button
        global page_stack, cur_page, sg, mg, sr, mr
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

        #place all of the widgets into the frame
        for window in self.pages.values():
            window.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        
        #show the first set of widgets - the main menu widgets on startup
        mm.show()

        #
        #
        # Temp 
        secondary_window = ctk.CTkToplevel()
        secondary_window.title("Controls")
        secondary_window.config(width=300, height=200)
        secondary_window.focus()
        #
        #
        #

        def switch_theme():
            global theme
            if theme == 'light':
                theme = 'dark'
                mm.bg2label.configure(image=ctk.CTkImage(Image.open('assets/bg2.png'), size=(900, 700)))
                mm.bg1label.configure(image=ctk.CTkImage(Image.open('assets/grad2bg.png'), size=(1920, 1080)))
                st.bg1label.configure(image=ctk.CTkImage(Image.open('assets/grad2bg.png'), size=(1920, 1080)))
                ms.bg1label.configure(image=ctk.CTkImage(Image.open('assets/grad2bg.png'), size=(1920, 1080)))
                so.bg1label.configure(image=ctk.CTkImage(Image.open('assets/grad2bg.png'), size=(1920, 1080)))
                mo.bg1label.configure(image=ctk.CTkImage(Image.open('assets/grad2bg.png'), size=(1920, 1080)))
                sg.bg1label.configure(image=ctk.CTkImage(Image.open('assets/grad2game.png'), size=(1920, 1080)))
            else:
                theme = 'light'
                mm.bg2label.configure(image=ctk.CTkImage(Image.open('assets/bg1.png'), size=(900, 700)))
                mm.bg1label.configure(image=ctk.CTkImage(Image.open('assets/grad1bg.png'), size=(1920, 1080)))
                st.bg1label.configure(image=ctk.CTkImage(Image.open('assets/grad1bg.png'), size=(1920, 1080)))
                ms.bg1label.configure(image=ctk.CTkImage(Image.open('assets/grad1bg.png'), size=(1920, 1080)))
                so.bg1label.configure(image=ctk.CTkImage(Image.open('assets/grad1bg.png'), size=(1920, 1080)))
                mo.bg1label.configure(image=ctk.CTkImage(Image.open('assets/grad1bg.png'), size=(1920, 1080)))
                sg.bg1label.configure(image=ctk.CTkImage(Image.open('assets/grad1game.png'), size=(1920, 1080)))
            ctk.set_appearance_mode(theme)

        #
        #
        # Temp
        theme_button = ctk.CTkButton(secondary_window, text='switch theme', command=switch_theme)
        theme_button.place(relx = 0.5, rely = 0.5, anchor = 'center')
        #
        #
        #

if __name__ == "__main__":
    #initialises the tkinter window
    root = ctk.CTk()
    #pywinstyles.apply_style(root, "acrylic")
    main = Window(root)
    main.pack(side="top", fill="both", expand=True)
    root.geometry("1600x900") #window size
    root.minsize(1500, 900)
    root.title('Hedge') #window title
    root.iconbitmap('assets/icon.ico') #window icon
    #root.wm_resizable(False, False) #makes window a fixed size

    root.bind('<w>', algo.move_p1)
    root.bind('<a>', algo.move_p1)
    root.bind('<s>', algo.move_p1)
    root.bind('<d>', algo.move_p1)

    root.bind('<Up>', algo.move_p2)
    root.bind('<Left>', algo.move_p2)
    root.bind('<Down>', algo.move_p2)
    root.bind('<Right>', algo.move_p2)

    def toggle_fullscreen(event=None):
        global fullscreen
        if fullscreen:
            root.attributes("-fullscreen", False)
            fullscreen = False
        else:
            root.attributes("-fullscreen", True)
            fullscreen = True
    def end_fullscreen(event=None):
        global fullscreen
        root.attributes("-fullscreen", False)
        fullscreen = False

    fullscreen = False
    root.bind("<F11>", toggle_fullscreen)
    root.bind("<Escape>", end_fullscreen)
    
    root.mainloop()

    