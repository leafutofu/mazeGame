import customtkinter as ctk #for GUI
import algo
import time #for timing
from tkinter.messagebox import askyesno #for pop-up box when exiting the program
from PIL import Image #to import images for buttons and backgrounds
from queue import PriorityQueue #for a* search

theme = ''
ctk.set_default_color_theme("assets/HEDGE.json")

if theme == 'light':
    bg1 = ctk.CTkImage(Image.open('assets/grad1bg.png'), size=(1920, 1080)) #import background image
    bg2 = ctk.CTkImage(Image.open('assets/bg1.png'), size=(900, 700))
    bg_set = ctk.CTkImage(Image.open('assets/grad1set.png'), size=(1920, 1080))
    bg_game = ctk.CTkImage(Image.open('assets/grad1game.png'), size=(1920, 1080))
    bg_res = ctk.CTkImage(Image.open('assets/grad1res.png'), size=(1920, 1080))
    canvas_colour = '#82925e'
    line_colour = '#FFFFFF'
else:
    bg1 = ctk.CTkImage(Image.open('assets/grad2bg.png'), size=(1920, 1080)) #import background image
    bg2 = ctk.CTkImage(Image.open('assets/bg2.png'), size=(900, 700))
    bg_set = ctk.CTkImage(Image.open('assets/grad2set.png'), size=(1920, 1080))
    bg_game = ctk.CTkImage(Image.open('assets/grad2game.png'), size=(1920, 1080))
    bg_res = ctk.CTkImage(Image.open('assets/grad2res.png'), size=(1920, 1080))
    canvas_colour = '#16291d'
    line_colour = '#afbf8b'

class Page(ctk.CTkFrame): #all page classes (e.g. mainMenu, modeSelection etc.) inherit this class
    def __init__(self, *args, **kwargs):
        ctk.CTkFrame.__init__(self, master=root, *args, **kwargs)

    def show(self): #a function to raise all the widgets associated with a particular page to the top, displaying it on the window
        self.lift()

class mainMenu(Page):
    def __init__(self, controller, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

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
            algo.play_click_sound()
            controller.pages['modeSelection'].show() #shows widgets associated with the mode selection page

        def check_position(event): #checks the coordinates of any mouse click on the window, and according to parameters, redirects to either the settings page or terminates the program.
            if event.x >= mm_settingsX - 20 and event.x <= mm_settingsX + 20 \
            and event.y >= mm_settingsY - 20 and event.y <= mm_settingsY + 20:
                controller.pages['settings'].show()
            elif event.x >= quitX - 20 and event.x <= quitX + 20 \
            and event.y >= quitY - 20 and event.y <= quitY + 20:
                if askyesno(title='Confirmation', message='Are you sure you want to quit?') == True:
                    root.destroy()

        root.bind('<Button-1>', check_position) #binds the left mouse click to the check_position() function

        #button styling
        modeSelection_button = ctk.CTkButton(s_frame, width=170, height=50, corner_radius=8, border_width=2, text_color='#FFFFFF', font=('Upheaval TT (BRK)', 40), text='PLAY', command=modeSelection_button)
        modeSelection_button.place(relx=0.5, rely=0.57, anchor='center')

class settings(Page):
    def __init__(self, controller, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        self.m_frame = ctk.CTkFrame(self, width=1920, height=1080)
        self.m_frame.place(relx=0.5, rely=0.5, anchor='center')

        self.bg1label = ctk.CTkLabel(self.m_frame, image = bg_set, text='') #create label to place background image
        self.bg1label.place(relx=0.5, rely=0.5, anchor='center')

        self.frame = ctk.CTkFrame(self.m_frame, width=440, height=600)
        self.frame.place(x=530, rely=0.5, anchor='center')
        
        self.info_frame = ctk.CTkFrame(self.m_frame, width = 650, height=540, corner_radius=12, bg_color=('#bfcba4','#34473b'))
        self.info_frame.place(x=1295, rely=0.52, anchor='center')
        self.info_frame.pack_propagate(0)

        self.info_label = ctk.CTkLabel(self.info_frame, text='')
        self.info_label.place(relx=0.48, rely=0, anchor='n')

        title_label = ctk.CTkLabel(self.frame, text='Settings', font=('Upheaval TT (BRK)', 50))
        title_label.place(x=0, y=0, anchor='nw')
        title_label2 = ctk.CTkLabel(self.frame, text='+ information ', font=('Upheaval TT (BRK)', 35, 'italic'), text_color=('#FFFFFF','#506d5a'))
        title_label2.place(x=100, y=40, anchor='nw')

        #

        radiobutton_value = ctk.StringVar(value="off")

        def radiobutton_event():
            selection = radiobutton_value.get()
            if selection == 'theme':
                self.info_label.configure(image=ctk.CTkImage(Image.open('assets/theme.png'), size=(600, 520)))
            elif selection == 'gen':
                self.info_label.configure(image=ctk.CTkImage(Image.open('assets/gen.png'), size=(600, 530)))
            elif selection == 'ret':
                self.info_label.configure(image=ctk.CTkImage(Image.open('assets/ret.png'), size=(605, 505)))
            elif selection == 'sound':
                self.info_label.configure(image=ctk.CTkImage(Image.open('assets/sound.png'), size=(600, 470)))

        theme_button = ctk.CTkRadioButton(self.frame, text='', variable=radiobutton_value,
                            value='theme', width=8, command=radiobutton_event)
        gen_button = ctk.CTkRadioButton(self.frame, text='', variable=radiobutton_value,
                            value='gen', width=8, command=radiobutton_event)
        ret_button = ctk.CTkRadioButton(self.frame, text='', variable=radiobutton_value,
                            value='ret', width=8, command=radiobutton_event)
        sound_button = ctk.CTkRadioButton(self.frame, text='', variable=radiobutton_value,
                            value='sound', width=8, command=radiobutton_event)

        theme_button.place(x=10, y=122, anchor='nw')
        gen_button.place(x=10, y=182, anchor='nw')
        ret_button.place(x=10, y=242, anchor='nw')
        sound_button.place(x=10, y=302, anchor='nw')

        #CHANGE THEME
        def theme_switch_event():
            theme_button.invoke()
            main.switch_theme()
        theme_switch_var = ctk.StringVar(value='dark')
        theme_switch = ctk.CTkSwitch(self.frame, text='    Theme', font=('Upheaval TT (BRK)', 20), text_color='#FFFFFF', command=theme_switch_event,
                                 variable=theme_switch_var, onvalue='light', offvalue='dark',
                                 switch_width=50, switch_height=27) #true is imperfect
        theme_switch.place(x=60, y=120, anchor='nw')

        #Generate Imperfect mazes with multiple solutions
        def gen_switch_event():
            gen_button.invoke()
            if gen_switch_var.get() == 'on':
                main.sg.imperfect = True
                main.mg.imperfect = True
            elif gen_switch_var.get() == 'off':
                main.sg.imperfect = False
                main.mg.imperfect = False
        gen_switch_var = ctk.StringVar(value='off')
        gen_switch = ctk.CTkSwitch(self.frame, text='    Generate imperfect mazes', font=('Upheaval TT (BRK)', 20), text_color='#FFFFFF', command=gen_switch_event,
                                 variable=gen_switch_var, onvalue='on', offvalue='off',
                                 switch_width=50, switch_height=27) #true is imperfect
        gen_switch.place(x=60, y=180, anchor='nw')

        #MODE - PRESS Q TO RETURN TO START
        def ret_switch_event():
            ret_button.invoke()
            if ret_switch_var.get() == 'on':
                algo.ret_start_allowed = True
            elif ret_switch_var.get() == 'off':
                algo.ret_start_allowed = False
        ret_switch_var = ctk.StringVar(value='off')
        ret_switch = ctk.CTkSwitch(self.frame, text='    Allow return to start', font=('Upheaval TT (BRK)', 20), text_color='#FFFFFF', command=ret_switch_event,
                                 variable=ret_switch_var, onvalue='on', offvalue='off',
                                 switch_width=50, switch_height=27)
        ret_switch.place(x=60, y=240, anchor='nw')

        #Turn off game sound
        def sound_switch_event():
            sound_button.invoke()
            if sound_switch_var.get() == 'on':
                algo.sound_allowed = True
            elif sound_switch_var.get() == 'off':
                algo.sound_allowed = False
        sound_switch_var = ctk.StringVar(value='on')
        sound_switch = ctk.CTkSwitch(self.frame, text='    Player move sound', font=('Upheaval TT (BRK)', 20), text_color='#FFFFFF', command=sound_switch_event,
                                 variable=sound_switch_var, onvalue='on', offvalue='off',
                                 switch_width=50, switch_height=27)
        sound_switch.place(x=60, y=300, anchor='nw')
        
        #

        def tutorial_button():
            theme_button.deselect()
            gen_button.deselect()
            ret_button.deselect()
            sound_button.deselect()
            self.info_label.configure(image=ctk.CTkImage(Image.open('assets/tut2.png'), size=(610, 525)))

        tutorial_button = ctk.CTkButton(self.frame, height=70, width=300, corner_radius=10, border_width=0, font=('Upheaval TT (BRK)', 30), text="🛈 HOW TO PLAY", command=tutorial_button)
        tutorial_button.place(x=30, y=400, anchor='nw')

        def back_button(): #directs to either the main menu or mode selection page depending on the contents of the page stack
            algo.play_click_sound()
            controller.pages['mainMenu'].show() #shows the page previous to the settings page
        
        back_button = ctk.CTkButton(self.frame, height=40, corner_radius=8, border_width=2, font=('Upheaval TT (BRK)', 25), text="< BACK", command=back_button)
        back_button.place(x=0, y=550, anchor='nw')

class modeSelection(Page): #selects singleplayer or multiplayer
    def __init__(self, controller, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        self.bg1label = ctk.CTkLabel(self, image = bg1, text = '') #create label to place background image
        self.bg1label.place(relx=0.5, rely=0.5, anchor='center')
        
        frame_ms = ctk.CTkFrame(self, width=900, height=700) #creates frame for the mode selection page
        frame_ms.place(relx=0.5, rely=0.5, anchor='center')

        def spOptions_button():
            algo.play_click_sound()
            controller.pages['spOptions'].show()
            
        def mpOptions_button():
            algo.play_click_sound()
            controller.pages['mpOptions'].show()

        def back_button():
            algo.play_click_sound()
            controller.pages['mainMenu'].show()
        
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

        self.bg1label = ctk.CTkLabel(self, image = bg1, text = '') #create label to place background image
        self.bg1label.place(relx=0.5, rely=0.5, anchor='center')

        m_frame = ctk.CTkFrame(self, width=900, height=700)
        m_frame.place(relx=0.5, rely=0.5, anchor='center')

        s_frame = ctk.CTkFrame(m_frame, width=675, height=380, border_width=5, corner_radius=15)
        s_frame.place(relx=0.5, rely=0.55, anchor='center')

        def combobox_callback(choice):
            if choice == 0:
                self.sp_params = [] #creates sp_params if combobox is not selected and the start game button is pressed
            elif choice == -1:
                self.sp_params[0] = int(get_current_value())
            else:
                self.sp_params = [int(get_current_value()), choice]

        title_label = ctk.CTkLabel(s_frame, text='-Singleplayer Options-', font=('Upheaval TT (BRK)', 35), text_color='#FFFFFF')
        title_label.place(relx=0.5, rely=0.12, anchor='center')

        combobox = ctk.CTkComboBox(s_frame, width=400, height=50,
                                   state="readonly",
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
            algo.play_click_sound()
            if self.sp_params != []:
                combobox_callback(-1)
                main.sg.spGameCanvas('new')
                algo.pmode = '' #set the mode for algo file to be singleplayer to prevent checking overlap in move_p1()
                controller.pages['spGame'].show()
                combobox_error_message.configure(text='')
                slider.set(0)
                slider_value_label.configure(text=format_value(get_current_value()))
                combobox.set('Select a generation algorithm')
            else:
                combobox_error_message.configure(text='error : no maze generation algorithm selected')
                
        spGame_button = ctk.CTkButton(s_frame, height=40, fg_color='#75a050', hover_color='#3d5329', text='START', text_color='#FFFFFF', font=('Upheaval TT (BRK)', 30), border_width=2, command=spGame_button)
        spGame_button.place(relx=0.5, rely=0.84, anchor='center')

        def back_button():
            slider.set(0)
            combobox.set('Select a generation algorithm')
            slider_value_label.configure(text=format_value(get_current_value()))
            algo.play_click_sound()
            combobox_error_message.configure(text='')
            controller.pages['modeSelection'].show()
            self.sp_params = []
        
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
            if choice == 0:
                self.mp_params = [] #creates sp_params if combobox is not selected and the start game button is pressed
            elif choice == -1:
                self.mp_params[0] = int(get_current_value())
            else:
                self.mp_params = [int(get_current_value()), choice]

        title_label = ctk.CTkLabel(s_frame, text='-Multiplayer Options-', font=('Upheaval TT (BRK)', 35), text_color='#FFFFFF')
        title_label.place(relx=0.5, rely=0.12, anchor='center')

        combobox = ctk.CTkComboBox(s_frame, width=400, height=50,
                                   state="readonly",
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
            algo.play_click_sound()
            if self.mp_params != []:
                combobox_callback(-1)
                main.mg.mpGameCanvas('new')
                algo.pmode = 'multi'
                controller.pages['mpGame'].show()
                combobox_error_message.configure(text='')
                slider.set(0)
                slider_value_label.configure(text=format_value(get_current_value()))
                combobox.set('Select a generation algorithm')
            else:
                combobox_error_message.configure(text='error : no maze generation algorithm selected')
                
        mpGame_button = ctk.CTkButton(s_frame, height=40, fg_color='#75a050', hover_color='#3d5329', text='START', text_color='#FFFFFF', font=('Upheaval TT (BRK)', 30), border_width=2, command=mpGame_button)
        mpGame_button.place(relx=0.5, rely=0.84, anchor='center')

        def back_button():
            slider.set(0)
            combobox.set('Select a generation algorithm')
            slider_value_label.configure(text=format_value(get_current_value()))
            algo.play_click_sound()
            combobox_error_message.configure(text='')
            controller.pages['modeSelection'].show()
            self.mp_params = []
        
        back_button = ctk.CTkButton(m_frame, height=40, corner_radius=8, border_width=3, text_color='#FFFFFF', font=('Upheaval TT (BRK)', 25), text="< BACK", command=back_button)
        back_button.grid(row=0, column=0, padx=(0,536), pady=(0,494))

        combobox_callback(0)

class spGame(Page): #singleplayer game screen   
    def __init__(self, controller, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        self.controller = controller
        self.imperfect = False

        self.bg1label = ctk.CTkLabel(self, image = bg_game, text = '') #create label to place background image
        self.bg1label.place(relx=0.5, rely=0.5, anchor='center')

        self.title_frame = ctk.CTkFrame(self)
        self.title_frame.place(relx=0.5, rely=0.1, anchor='center')
        title = ctk.CTkLabel(self.title_frame, text=" HEDGE ", text_color='#82925e', font=('Upheaval TT (BRK)', 50))
        subheading = ctk.CTkLabel(self.title_frame, text="SINGLEPLAYER ", text_color='#FFFFFF', font=('Upheaval TT (BRK)', 30, 'italic'))
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
        self.time_label = ctk.CTkLabel(right_frame, text='', text_color='#82925e', font=('Upheaval TT (BRK)', 50, 'italic'))
        #6f3e4a
        self.step_label.place(x=100, rely=0.145, anchor='w')
        self.time_label.place(x=100, rely=0.645, anchor='w')

        self.progress = ctk.CTkProgressBar(self, width=600, height=5, corner_radius=5, progress_color='#a1d0d1')
        self.progress.set(0)
        self.progress.place(relx=0.5, rely=0.9, anchor='center')

        #
        #temporary demonstration stuff
        def back_button():
            self.update = False
            controller.pages['spOptions'].show()
        
        back_button = ctk.CTkButton(self, height=40, font=('Upheaval TT (BRK)', 15), text="demo bck", command=back_button)
        back_button.place(relx=0.2, rely=0.1, anchor='center')

        def skip_button():
            self.update = False
            self.sp_time_end = time.time()
            main.r.results('single')
            controller.pages['Results'].show()

        skip_button = ctk.CTkButton(self, height=40, font=('Upheaval TT (BRK)', 15), text="demo skip", command=skip_button)
        skip_button.place(relx=0.8, rely=0.1, anchor='center')
            
        #
        #
    def createNewMaze(self):
        self.game_frame = ctk.CTkFrame(self, width=600, height=600)
        self.game_frame.place(relx=0.5, rely=0.5, anchor='center')

        algo.create_canvas(self.game_frame, canvas_colour)
        algo.graph = algo.Graph(main.so.sp_params[0])

        self.grid_label.configure(text=f'{main.so.sp_params[0]} x {main.so.sp_params[0]} ')
     
        if main.so.sp_params[1] == 'Depth First Search':
            algo.graph.DFS()
            self.algo_label.configure(text='DFS')
        elif main.so.sp_params[1] == 'Hunt-and-Kill':
            algo.graph.Hunt_and_Kill()
            self.algo_label.configure(text='Hunt - Kill')
        elif main.so.sp_params[1] == 'Sidewinder':
            algo.graph.Sidewinder()
            self.algo_label.configure(text='Sidewinder ')

        if self.imperfect:
            algo.graph.Imperfect()
        
        algo.draw_maze(algo.canvas_m, line_colour)
        

    def spGameCanvas(self, mode):
        self.update = True
        self.sp_time_start = time.time()

        algo.p2 = None

        self.retry_label = ctk.CTkLabel(self.title_frame, text='repeated', text_color='#ca4754', font=('Upheaval TT (BRK)', 15))
        self.retry_label.pack()

        if mode == 'new':
            self.createNewMaze()
            self.retry_label.pack_forget()
        elif mode == 'retry':
            self.retry_label.pack()
            algo.canvas_m.delete(algo.p1)


        algo.draw_player('single')
        algo.p1moves = 0

        def spUpdate():
            if algo.detect_win('single'):
                self.update = False
                self.sp_time_end = time.time()
                main.r.results('single')
                self.controller.pages['Results'].show()
                self.retry_label.pack_forget()
                main.so.sp_params[1] = ''
            if self.update == True:
                print(f'params in: {main.so.sp_params[0]}, {algo.node_player(algo.p1)}')
                print(f'solve_maze progress returning: {main.r.solve_maze(main.so.sp_params[0], algo.node_player(algo.p1))}')
                print(f'divisor returning: {(2*main.so.sp_params[0])}')
                self.progress.set(1-(main.r.solve_maze(main.so.sp_params[0], algo.node_player(algo.p1))/(2*main.so.sp_params[0]))) #h() is heuristic function
                self.step_label.configure(text=f'{algo.get_moves("single")}  ')
                self.time_label.configure(text=f'{round(time.time()-self.sp_time_start, 1)}  ')
                root.after(100, spUpdate)

        root.after(0, spUpdate)

class mpGame(Page): #multiplayer game screen
    def __init__(self, controller, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        self.controller = controller
        self.imperfect = False

        self.bg1label = ctk.CTkLabel(self, image = bg_game, text = '') #create label to place background image
        self.bg1label.place(relx=0.5, rely=0.5, anchor='center')

        self.title_frame = ctk.CTkFrame(self)
        self.title_frame.place(relx=0.5, rely=0.1, anchor='center')
        title = ctk.CTkLabel(self.title_frame, text=" HEDGE ", text_color='#82925e', font=('Upheaval TT (BRK)', 50))
        subheading = ctk.CTkLabel(self.title_frame, text="MULTIPLAYER ", text_color='#FFFFFF', font=('Upheaval TT (BRK)', 30, 'italic'))
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

        #right_frame = ctk.CTkFrame(self, height=228, width=380)
        #right_frame.place(relx=0.85, rely=0.495, anchor='center')

        #right_image = ctk.CTkImage(Image.open('assets/sg_right.png'), size=(233, 227))
        #right_image_label = ctk.CTkLabel(right_frame, text='', image=right_image)
        #right_image_label.place(x=380, rely=0.5, anchor='e')
    
        #self.step_label = ctk.CTkLabel(right_frame, text='', text_color='#FFFFFF', font=('Upheaval TT (BRK)', 45, 'italic'))
        #self.time_label = ctk.CTkLabel(right_frame, text='', text_color='#4a6f3e', font=('Upheaval TT (BRK)', 50, 'italic'))
        #6f3e4a
        #self.step_label.place(x=100, rely=0.145, anchor='w')
        #self.time_label.place(x=100, rely=0.645, anchor='w')

        self.progress1 = ctk.CTkProgressBar(self, width=600, height=5, corner_radius=5, progress_color='#c77373')
        self.progress1.set(0)
        self.progress1.place(relx=0.5, rely=0.9, anchor='center')
        self.progress2 = ctk.CTkProgressBar(self, width=600, height=5, corner_radius=5,  progress_color='#f4e59d')
        self.progress2.set(0)
        self.progress2.place(relx=0.5, rely=0.92, anchor='center')


        #
        #a temporary back button
        def back_button():
            self.update = False
            controller.pages['mpOptions'].show()
        
        back_button = ctk.CTkButton(self, height=40, font=('Upheaval TT (BRK)', 15), text="demo bck", command=back_button)
        back_button.place(relx=0.2, rely=0.1, anchor='center')

        def skip_button():
            self.update = False
            self.sp_time_end = time.time()
            main.r.results('multi')
            controller.pages['Results'].show()

        skip_button = ctk.CTkButton(self, height=40, font=('Upheaval TT (BRK)', 15), text="demo skip", command=skip_button)
        skip_button.place(relx=0.8, rely=0.1, anchor='center')
        #
        #

    def createNewMaze(self):
        self.game_frame = ctk.CTkFrame(self, width=600, height=600)
        self.game_frame.place(relx=0.5, rely=0.5, anchor='center')

        algo.create_canvas(self.game_frame, canvas_colour)
        algo.graph = algo.Graph(main.mo.mp_params[0])

        self.grid_label.configure(text=f'{main.mo.mp_params[0]} x {main.mo.mp_params[0]} ')
     
        if main.mo.mp_params[1] == 'Depth First Search':
            algo.graph.DFS()
            self.algo_label.configure(text='DFS')
        elif main.mo.mp_params[1] == 'Hunt-and-Kill':
            algo.graph.Hunt_and_Kill()
            self.algo_label.configure(text='Hunt - Kill')
        elif main.mo.mp_params[1] == 'Sidewinder':
            algo.graph.Sidewinder()
            self.algo_label.configure(text='Sidewinder ')

        if self.imperfect:
            algo.graph.Imperfect()
        
        algo.draw_maze(algo.canvas_m, line_colour)

    def mpGameCanvas(self, mode):
        self.update = True
        self.mp_time_start = time.time()

        self.retry_label = ctk.CTkLabel(self.title_frame, text='repeated', text_color='#ca4754', font=('Upheaval TT (BRK)', 15))
        self.retry_label.pack()

        if mode == 'new':
            self.createNewMaze()
            self.retry_label.pack_forget()
        elif mode == 'retry':
            self.retry_label.pack()
            algo.canvas_m.delete(algo.p1)
            algo.canvas_m.delete(algo.p2)

        algo.draw_player('multi')
        algo.p1moves = 0
        algo.p2moves = 0
        
        def mpUpdate():
            win_list = algo.detect_win('multi')
            if win_list[0]:
                self.update = False
                main.r.results('multi', -1, win_list)
                self.controller.pages['Results'].show()
                self.retry_label.pack_forget()
                main.mo.mp_params[1] = ''
                algo.order_list = []
            if self.update == True:
                self.progress1.set(1-(main.r.solve_maze(main.mo.mp_params[0], algo.node_player(algo.p1))/(2*main.mo.mp_params[0]))) #h() is heuristic function
                self.progress2.set(1-(main.r.solve_maze(main.mo.mp_params[0], algo.node_player(algo.p2))/(2*main.mo.mp_params[0])))
                

                root.after(100, mpUpdate)

        root.after(0, mpUpdate)

class Results(Page): #singleplayer results screen
    def __init__(self, controller, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.controller = controller
        self.path2 = {}

        self.bg1label = ctk.CTkLabel(self, image = bg_res, text = '') #create label to place background image
        self.bg1label.place(relx=0.5, rely=0.5, anchor='center')

    def return_button(self):
        algo.play_click_sound()
        main.so.sp_params = []
        main.mo.mp_params = []
        self.controller.pages['modeSelection'].show()

    def retry_button(self):
        algo.play_click_sound()
        if self.mode == 'single':
            main.sg.spGameCanvas('retry')
            self.controller.pages['spGame'].show()
        if self.mode == 'multi':
            main.mg.mpGameCanvas('retry')
            self.controller.pages['mpGame'].show()
    
    def solve_maze(self, size, start_node, mode=None):
        self.mode = mode
        queue = PriorityQueue()
        if self.mode == 'disp':
            search_colours = algo.get_colour_gradient('#473d5a', '#004f5a', 2*size-1)
        start = start_node
        self.path = {}  

        g_score = [float('inf') for _ in range(algo.graph.num_nodes)]
        g_score[start] = 0
        f_score = [float('inf') for _ in range(algo.graph.num_nodes)]
        f_score[start] = algo.h(start)

        queue.put((f_score[start], algo.h(start), start))
        self.end = False
        def astar_loop():
            print('in loop')
            if not queue.empty():
                cur_node = queue.get()[2]
                if cur_node+1 == size**2: # reached end
                    self.path2 = {}
                    path_node = size**2 - 1
                    while path_node != 0:
                        self.path2[self.path[path_node]] = path_node
                        path_node = self.path[path_node]
                    if self.mode == 'disp':
                        self.results('draw', self.path2)
                    else:
                        print(f'solve_maze returning: {len(self.path2)}')
                        return len(self.path2)
                else:
                    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]#EWSN
                    for dy, dx in directions:
                        node = cur_node + dy * size + dx
                        p = True
                        if dx == 1 and (cur_node+1) % size == 0:
                            p = False
                        if dx == -1 and cur_node % size == 0:
                            p = False
                        if dy == 1 and (node+1) > size**2:
                            p = False
                        if dy == -1 and cur_node < size:    
                            p = False
                        if p == True:
                            if algo.graph.detect_wall(cur_node, node) == False:
                                child_node = node
                                temp_g_score = g_score[cur_node] + 1
                                temp_f_score = temp_g_score + algo.h(child_node)
                                
                                if self.mode == 'disp':
                                    index = algo.h(child_node)
                                    algo.cloned.tag_lower(algo.cloned.create_rectangle(0+child_node%size*algo.w, 0+child_node//size*algo.w, child_node%size*algo.w + algo.w-0, child_node//size*algo.w + algo.w-0, tags='del', width = 0, fill=search_colours[index]))
                                
                                if temp_f_score < f_score[child_node]:
                                    g_score[child_node]= temp_g_score
                                    f_score[child_node]= temp_f_score
                                    queue.put((temp_f_score, algo.h(child_node), child_node))
                                    self.path[child_node]=cur_node
                    root.after(1, astar_loop)
        root.after(0, astar_loop)

    def results(self, mode, path=None, win_list=None):

        self.mode = mode
        
        self.m_frame = ctk.CTkFrame(self, width=1280, height=650)
        self.m_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        results_frame = ctk.CTkFrame(self.m_frame, width=500, height=650)
        results_frame.place(relx=0.2, rely=0.5, anchor='center')
        self.path2 = {}
        
        if self.mode == 'single':
            self.size = main.so.sp_params[0]

            title = ctk.CTkLabel(results_frame, text='GAME STATS:', text_color='#FFFFFF', font=('Upheaval TT (BRK)', 70))
            title.place(x=10, y=0)

            steps = ctk.CTkLabel(results_frame, text=f'Steps Made: {algo.get_moves("single")}', font=('Upheaval TT (BRK)', 33))
            steps.place(x=10, y=190)

            time_taken = ctk.CTkLabel(results_frame, text=f'Time Taken: {round(main.sg.sp_time_end - main.sg.sp_time_start, 1)} s', font=('Upheaval TT (BRK)', 33))
            time_taken.place(x=10, y=230)
        elif self.mode == 'multi':
            self.size = main.mo.mp_params[0]
            print(win_list)

        canvas_frame = ctk.CTkFrame(self.m_frame, width=600, height = 600)
        algo.clone_canvas(algo.canvas_m, canvas_frame, canvas_colour, line_colour)
        algo.cloned.tag_lower(algo.cloned.create_rectangle(600-algo.w, 600-algo.w, 600, 600, width = 0, fill='#005b27'))

        button_frame = ctk.CTkFrame(self.m_frame, width=600, height = 600, fg_color=('#96a672', '#16291d'))
        button_frame.place(relx=0.7625, rely=0.5, anchor='center')

        def draw_path(path2):
            size = self.size
            print(f'draw_path using: {path2}')
            path_colours = algo.get_colour_gradient('#473d5a', '#004f5a', len(path2))
            for index, node in enumerate(path2.keys()):
                algo.cloned.create_rectangle(0+node%size*algo.w, 0+node//size*algo.w, node%size*algo.w + algo.w -0, node//size*algo.w + algo.w-0, width=0, fill=path_colours[index])
            algo.cloned.delete(algo.cloned.gettags("del"))
            algo.draw_maze(algo.cloned, line_colour)
            algo_steps = ctk.CTkLabel(results_frame, text=f'Optimal Path: {len(path2)} Steps', font=('Upheaval TT (BRK)', 33))
            algo_steps.place(x=10, y=300)

        if self.mode == 'draw':
            draw_path(path)

        def show_canvas():
            algo.play_click_sound()
            button_frame.place_forget()
            canvas_frame.place(relx=0.7625, rely=0.5, anchor='center')
            self.solve_maze(self.size, 0, 'disp')

        button = ctk.CTkButton(button_frame, height=35, text='Reveal solution', font=('Upheaval TT (BRK)', 25), command=show_canvas)
        button.place(x=300, y=300, anchor='center')

        return_button = ctk.CTkButton(results_frame, corner_radius=8, border_width=3, height=60, width=200, fg_color=('#96a672','#2a4f38'), text='New Game', font=('Upheaval TT (BRK)', 35), command=self.return_button)
        return_button.place(x=10, y=565)

        retry_button = ctk.CTkButton(results_frame, corner_radius=8, border_width=3, height=60, width=200, text='Retry', font=('Upheaval TT (BRK)', 35), command=self.retry_button)
        retry_button.place(x=265, y=565)
        
class Window(ctk.CTkFrame): #create main window
    def __init__(self, *args, **kwargs):
        ctk.CTkFrame.__init__(self, *args, **kwargs)

        #create a dictionary for all of the different selection pages
        self.pages = {}
        for Subclass in (mainMenu, settings, modeSelection, spOptions, mpOptions, spGame, mpGame, Results):
            self.pages[Subclass.__name__] = Subclass(self)
        
        self.mm, self.st, self.ms, self.so, self.mo, self.sg, self.mg, self.r = self.pages.values()
        
        #creating a container frame to contain the widgets of each page
        container = ctk.CTkFrame(self)
        container.pack(side="top", fill="both", expand=True)

        #place all of the widgets into the frame
        for window in self.pages.values():
            window.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        
        #show the first set of widgets - the main menu widgets on startup
        self.mm.show()

    def switch_theme(self):
        global theme, canvas_colour, line_colour
        if theme == 'light':
            theme = 'dark'
            canvas_colour = '#16291d'
            line_colour = '#afbf8b'
            self.mm.bg2label.configure(image=ctk.CTkImage(Image.open('assets/bg2.png'), size=(900, 700)))
            self.mm.bg1label.configure(image=ctk.CTkImage(Image.open('assets/grad2bg.png'), size=(1920, 1080)))
            self.st.bg1label.configure(image=ctk.CTkImage(Image.open('assets/grad2set.png'), size=(1920, 1080)))
            self.ms.bg1label.configure(image=ctk.CTkImage(Image.open('assets/grad2bg.png'), size=(1920, 1080)))
            self.so.bg1label.configure(image=ctk.CTkImage(Image.open('assets/grad2bg.png'), size=(1920, 1080)))
            self.mo.bg1label.configure(image=ctk.CTkImage(Image.open('assets/grad2bg.png'), size=(1920, 1080)))
            self.sg.bg1label.configure(image=ctk.CTkImage(Image.open('assets/grad2game.png'), size=(1920, 1080)))
            self.mg.bg1label.configure(image=ctk.CTkImage(Image.open('assets/grad2game.png'), size=(1920, 1080)))
            self.r.bg1label.configure(image=ctk.CTkImage(Image.open('assets/grad2res.png'), size=(1920, 1080)))
        else:
            theme = 'light'
            canvas_colour = '#82925e'
            line_colour = '#FFFFFF'
            self.mm.bg2label.configure(image=ctk.CTkImage(Image.open('assets/bg1.png'), size=(900, 700)))
            self.mm.bg1label.configure(image=ctk.CTkImage(Image.open('assets/grad1bg.png'), size=(1920, 1080)))
            self.st.bg1label.configure(image=ctk.CTkImage(Image.open('assets/grad1set.png'), size=(1920, 1080)))
            self.ms.bg1label.configure(image=ctk.CTkImage(Image.open('assets/grad1bg.png'), size=(1920, 1080)))
            self.so.bg1label.configure(image=ctk.CTkImage(Image.open('assets/grad1bg.png'), size=(1920, 1080)))
            self.mo.bg1label.configure(image=ctk.CTkImage(Image.open('assets/grad1bg.png'), size=(1920, 1080)))
            self.sg.bg1label.configure(image=ctk.CTkImage(Image.open('assets/grad1game.png'), size=(1920, 1080)))
            self.mg.bg1label.configure(image=ctk.CTkImage(Image.open('assets/grad1game.png'), size=(1920, 1080)))
            self.r.bg1label.configure(image=ctk.CTkImage(Image.open('assets/grad1res.png'), size=(1920, 1080)))
        ctk.set_appearance_mode(theme)

if __name__ == "__main__":
    #initialises the tkinter window
    root = ctk.CTk()
    main = Window(root)
    main.pack(side="top", fill="both", expand=True)
    root.geometry("1600x900") #window size
    root.minsize(1500, 900)
    root.title('Hedge') #window title
    root.iconbitmap('assets/icon.ico') #window icon

    root.bind('<w>', algo.move_p1)
    root.bind('<W>', algo.move_p1)

    root.bind('<a>', algo.move_p1)
    root.bind('<A>', algo.move_p1)

    root.bind('<s>', algo.move_p1)
    root.bind('<S>', algo.move_p1)

    root.bind('<d>', algo.move_p1)
    root.bind('<D>', algo.move_p1)


    root.bind('<Up>', algo.move_p2)
    root.bind('<Left>', algo.move_p2)
    root.bind('<Down>', algo.move_p2)
    root.bind('<Right>', algo.move_p2)

    root.bind('<q>', algo.return_start)
    root.bind('<Q>', algo.return_start)

    root.bind('</>', algo.return_start)

    
    def toggle_fullscreen(event=None):
        global fullscreen
        if fullscreen:
            root.attributes("-fullscreen", False)
            fullscreen = False
        else:
            root.attributes("-fullscreen", True)
            fullscreen = True

    fullscreen = False
    root.bind("<F11>", toggle_fullscreen)

    root.mainloop()