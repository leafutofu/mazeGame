import customtkinter as ctk  # For the GUI.
import algo  # Import key algorithms.
import time  # For timing the players.
from tkinter.messagebox import askyesno  # For pop-up box when exiting the program.
from PIL import Image  # To import images for buttons and backgrounds.
from queue import PriorityQueue  # For A* search.

theme = ''  # Define theme.
ctk.set_default_color_theme("assets/HEDGE.json")  # Set overall theme to custom json file.

if theme == 'light':
    # Import background images.
    bg1 = ctk.CTkImage(Image.open('assets/grad1bg.png'), size=(1920, 1080)) 
    bg2 = ctk.CTkImage(Image.open('assets/bg1.png'), size=(900, 700))
    bg_set = ctk.CTkImage(Image.open('assets/grad1set.png'), size=(1920, 1080))
    bg_game = ctk.CTkImage(Image.open('assets/grad1game.png'), size=(1920, 1080))
    bg_res = ctk.CTkImage(Image.open('assets/grad1res.png'), size=(1920, 1080))
    # Define the canvas background colour and the wall colour.
    canvas_colour = '#82925e' 
    line_colour = '#FFFFFF'
else:
    # Import background images.
    bg1 = ctk.CTkImage(Image.open('assets/grad2bg.png'), size=(1920, 1080))
    bg2 = ctk.CTkImage(Image.open('assets/bg2.png'), size=(900, 700))
    bg_set = ctk.CTkImage(Image.open('assets/grad2set.png'), size=(1920, 1080))
    bg_game = ctk.CTkImage(Image.open('assets/grad2game.png'), size=(1920, 1080))
    bg_res = ctk.CTkImage(Image.open('assets/grad2res.png'), size=(1920, 1080))
    # Define the canvas background colour and the wall colour.
    canvas_colour = '#16291d'
    line_colour = '#afbf8b'

# The parent class that all page classes inherit.
class Page(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        ctk.CTkFrame.__init__(self, master=root, *args, **kwargs)

    def show(self):  # A function to raise all the widgets associated with a particular page to the top, displaying it on the window.
        self.lift()

# The Main Menu page class - a child of the Page class.
class mainMenu(Page):
    def __init__(self, controller, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)  # Inherits the page class.

        m_frame = ctk.CTkFrame(self)  # Create a frame for the menu.
        m_frame.pack(side='top', expand=True, fill = 'both')
        
        self.bg1label = ctk.CTkLabel(m_frame, image = bg1, text = '')  # Create label to place background image.
        self.bg1label.place(relx=0.5, rely=0.5, anchor='center')

        s_frame = ctk.CTkFrame(m_frame, height=700, width=900, corner_radius=0)
        s_frame.place(relx=0.5, rely=0.5, anchor='center')

        self.bg2label = ctk.CTkLabel(s_frame, image = bg2, text = '')  # Create label to place 2nd background image (for buttons).
        self.bg2label.place(relx=0.5, rely=0.5, anchor='center')

        title = ctk.CTkLabel(s_frame, text='HEDGE', font=('Upheaval TT (BRK)', 120))
        title.place(relx=0.5, rely=0.38, anchor='center')      

        # Coordinates of various buttons.
        mm_settingsX = 410
        mm_settingsY = 610
        quitX = 485
        quitY = 610

        # Sets current page variable to 'modeSelection' and shows the widgets associated with the mode selection page.
        def modeSelection_button():
            algo.play_click_sound()
            controller.pages['modeSelection'].show()  # Shows widgets associated with the mode selection page.

        # Checks the coordinates of any mouse click on the window, and according to parameters, 
        # redirects to either the settings page or terminates the program.
        def check_position(event):
            if event.x >= mm_settingsX - 20 and event.x <= mm_settingsX + 20 \
            and event.y >= mm_settingsY - 20 and event.y <= mm_settingsY + 20:
                controller.pages['settings'].show()
            elif event.x >= quitX - 20 and event.x <= quitX + 20 \
            and event.y >= quitY - 20 and event.y <= quitY + 20:
                if askyesno(title='Confirmation', message='Are you sure you want to quit?') == True:
                    root.destroy()

        # Binds the left mouse click to the check_position() function.
        root.bind('<Button-1>', check_position)

        # Button styling.
        modeSelection_button = ctk.CTkButton(s_frame, width=170, height=50, corner_radius=8, 
                                             border_width=2, text_color='#FFFFFF', 
                                             font=('Upheaval TT (BRK)', 40), text='PLAY', 
                                             command=modeSelection_button)
        modeSelection_button.place(relx=0.5, rely=0.57, anchor='center')

# The Settings page class - a child of the Page class.
class settings(Page):
    def __init__(self, controller, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)  # Inherits the page class.

        # Main frame - contains all widgets.
        self.m_frame = ctk.CTkFrame(self, width=1920, height=1080)
        self.m_frame.place(relx=0.5, rely=0.5, anchor='center')

        self.bg1label = ctk.CTkLabel(self.m_frame, image = bg_set, text='')  # Create label to place background image.
        self.bg1label.place(relx=0.5, rely=0.5, anchor='center')

        # Frame to contain switches on the left.
        self.frame = ctk.CTkFrame(self.m_frame, width=440, height=600)
        self.frame.place(x=530, rely=0.5, anchor='center')
        
        # Frame to contain information on the right.
        self.info_frame = ctk.CTkFrame(self.m_frame, width = 650, height=540, corner_radius=12, bg_color=('#bfcba4','#34473b'))
        self.info_frame.place(x=1295, rely=0.52, anchor='center')
        self.info_frame.pack_propagate(0)

        # Label to place images - for the info_frame which will allow information in the form of images to be displayed.
        self.info_label = ctk.CTkLabel(self.info_frame, text='')
        self.info_label.place(relx=0.48, rely=0, anchor='n')

        # Title.
        title_label = ctk.CTkLabel(self.frame, text='Settings', font=('Upheaval TT (BRK)', 50))
        title_label.place(x=0, y=0, anchor='nw')
        title_label2 = ctk.CTkLabel(self.frame, text='+ information ', 
                                    font=('Upheaval TT (BRK)', 35, 'italic'), 
                                    text_color=('#FFFFFF','#506d5a'))
        title_label2.place(x=100, y=40, anchor='nw')

        # The radiobutton value.
        radiobutton_value = ctk.StringVar(value="off")

        # When any of the 4 radiobuttons are selected, the corresponding image is shown.
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

        # Change Theme.
        def theme_switch_event():
            theme_button.invoke()  # Invokes the radiobutton to show the information about this particular switch.
            main.switch_theme()
        theme_switch_var = ctk.StringVar(value='dark')
        theme_switch = ctk.CTkSwitch(self.frame, text='    Theme', 
                                     font=('Upheaval TT (BRK)', 20), 
                                     text_color='#FFFFFF', command=theme_switch_event,
                                     variable=theme_switch_var, onvalue='light', offvalue='dark',
                                     switch_width=50, switch_height=27)
        theme_switch.place(x=60, y=120, anchor='nw')

        # Generate Imperfect mazes with multiple solutions.
        def gen_switch_event():
            gen_button.invoke()  # Invokes the radiobutton to show the information about this particular switch.
            if gen_switch_var.get() == 'on':
                main.sg.imperfect = True
                main.mg.imperfect = True
            elif gen_switch_var.get() == 'off':
                main.sg.imperfect = False
                main.mg.imperfect = False
        gen_switch_var = ctk.StringVar(value='off')
        gen_switch = ctk.CTkSwitch(self.frame, text='    Generate imperfect mazes', 
                                   font=('Upheaval TT (BRK)', 20), text_color='#FFFFFF', 
                                   command=gen_switch_event,
                                 variable=gen_switch_var, onvalue='on', offvalue='off',
                                 switch_width=50, switch_height=27)
        gen_switch.place(x=60, y=180, anchor='nw')

        # Allows returning to start by pressing Q.
        def ret_switch_event():
            ret_button.invoke()  # Invokes the radiobutton to show the information about this particular switch.
            if ret_switch_var.get() == 'on':
                algo.ret_start_allowed = True
            elif ret_switch_var.get() == 'off':
                algo.ret_start_allowed = False
        ret_switch_var = ctk.StringVar(value='off')
        ret_switch = ctk.CTkSwitch(self.frame, text='    Allow return to start', 
                                   font=('Upheaval TT (BRK)', 20), text_color='#FFFFFF', 
                                   command=ret_switch_event,
                                 variable=ret_switch_var, onvalue='on', offvalue='off',
                                 switch_width=50, switch_height=27)
        ret_switch.place(x=60, y=240, anchor='nw')

        # Turn off game sound.
        def sound_switch_event():
            sound_button.invoke()  # Invokes the radiobutton to show the information about this particular switch.
            if sound_switch_var.get() == 'on':
                algo.sound_allowed = True
            elif sound_switch_var.get() == 'off':
                algo.sound_allowed = False
        sound_switch_var = ctk.StringVar(value='on')
        sound_switch = ctk.CTkSwitch(self.frame, text='    Player move sound', 
                                     font=('Upheaval TT (BRK)', 20), text_color='#FFFFFF', 
                                     command=sound_switch_event,
                                 variable=sound_switch_var, onvalue='on', offvalue='off',
                                 switch_width=50, switch_height=27)
        sound_switch.place(x=60, y=300, anchor='nw')

        # Displays tutorial on how to play the game.
        def tutorial_button():
            theme_button.deselect()
            gen_button.deselect()
            ret_button.deselect()
            sound_button.deselect()
            self.info_label.configure(image=ctk.CTkImage(Image.open('assets/tut2.png'), size=(610, 525)))

        tutorial_button = ctk.CTkButton(self.frame, height=70, width=300, 
                                        corner_radius=10, border_width=0, 
                                        font=('Upheaval TT (BRK)', 30), 
                                        text="🛈 HOW TO PLAY", command=tutorial_button)
        tutorial_button.place(x=30, y=400, anchor='nw')

        # Back to main menu.
        def back_button():
            algo.play_click_sound()
            controller.pages['mainMenu'].show()
        
        back_button = ctk.CTkButton(self.frame, height=40, corner_radius=8, 
                                    border_width=2, font=('Upheaval TT (BRK)', 25), 
                                    text="< BACK", command=back_button)
        back_button.place(x=0, y=550, anchor='nw')

# The Mode Selection page class - a child of the Page class.
class modeSelection(Page):  # Selects singleplayer or multiplayer.
    def __init__(self, controller, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)  # Inherits the page class.

        self.bg1label = ctk.CTkLabel(self, image = bg1, text = '')  # Create label to place background image.
        self.bg1label.place(relx=0.5, rely=0.5, anchor='center')
        
        frame_ms = ctk.CTkFrame(self, width=900, height=700)  # Creates frame for the mode selection page.
        frame_ms.place(relx=0.5, rely=0.5, anchor='center')

        # Redirects to singleplayer options page.
        def spOptions_button():
            algo.play_click_sound()
            controller.pages['spOptions'].show()
        
        # Redirects to multiplayer options page.
        def mpOptions_button():
            algo.play_click_sound()
            controller.pages['mpOptions'].show()

        # Redirects to previous page.
        def back_button():
            algo.play_click_sound()
            controller.pages['mainMenu'].show()
        
        back_button = ctk.CTkButton(frame_ms, height=40, corner_radius=8, 
                                    border_width=3, text_color='#FFFFFF', 
                                    font=('Upheaval TT (BRK)', 25), text="< BACK", command=back_button)

        back_button.grid(row=0, column=0, padx=(0,537), pady=(0,494))
        
        # Load images for the buttons
        spOptions_image = ctk.CTkImage(Image.open("assets/sp_button.png"), size=(245,245))
        mpOptions_image = ctk.CTkImage(Image.open("assets/mp_button.png"), size=(250,250))

        spOptions_button = ctk.CTkButton(frame_ms, width=290, height=346, 
                                         corner_radius=20, text="", border_width=5, 
                                         image=spOptions_image, command=spOptions_button)
        mpOptions_button = ctk.CTkButton(frame_ms, width=290, height=346, 
                                         corner_radius=20, text="", border_width=5, 
                                         image=mpOptions_image, command=mpOptions_button)

        spOptions_button.grid(row=0, column=0, padx=(0,399), pady=(36,0))
        mpOptions_button.grid(row=0, column=0, padx=(399,0), pady=(36,0))

# The Singleplayer Options page class - a child of the Page class.
class spOptions(Page): # Screen to select generation style and grid size for singleplayer.
    def __init__(self, controller, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)  # Inherits the page class.

        self.bg1label = ctk.CTkLabel(self, image = bg1, text = '')  # Create label to place background image.
        self.bg1label.place(relx=0.5, rely=0.5, anchor='center')

        m_frame = ctk.CTkFrame(self, width=900, height=700)
        m_frame.place(relx=0.5, rely=0.5, anchor='center')

        s_frame = ctk.CTkFrame(m_frame, width=675, height=380, border_width=5, corner_radius=15)
        s_frame.place(relx=0.5, rely=0.55, anchor='center')

        # Defines the parameters list
        self.params = []

        # Called for every interation with the drop down box.
        def combobox_callback(choice):
            # Redefines the params list when a choice is made.
            # It gets the current slider value and the choice of the drop down box.
            self.params = [int(get_current_value()), choice]

        title_label = ctk.CTkLabel(s_frame, text='-Singleplayer Options-', font=('Upheaval TT (BRK)', 35), text_color='#FFFFFF')
        title_label.place(relx=0.5, rely=0.12, anchor='center')

        # The drop down menu.
        combobox = ctk.CTkComboBox(s_frame, width=400, height=50,
                                   state="readonly",
                                   values=['Depth First Search', 'Hunt-and-Kill', 'Sidewinder'], 
                                   font=('Upheaval TT (BRK)', 20), 
                                   dropdown_font=('Upheaval TT (BRK)', 20),
                                   command=combobox_callback)
        combobox.set('Select a generation algorithm')
        combobox.place(relx=0.5, rely=0.31, anchor='center')

        """
        To implement the slider, we need to update the displayed value of the slider going to the
        gui every time the slider is changed.
        We also need to get the final slider value when the user presses the start button.
        
        To do this, a slider value is defined, three functions are created:
            - get_current_value()
            - format_value()
            - slider_changed()
        
        The slider_changed() function is called every time the user interacts with the slider,
        it changes the displayed value of the maze size on the GUI
        It calls the get_current_value() function, and formats the output using the format_value() function.
        
        When the start game button is pressed, in order to get the current slider value,
        we update the parameter list passed to the game object.
        
        """

        slider_value = ctk.DoubleVar()

        # Returns current slider value.
        def get_current_value():
            value = '{: .0f}'.format(slider_value.get()*25+5)
            return value
        
        # Formats the value to be displayed on the GUI
        def format_value(value):
            return f'{value} x{value}'
        
        # Called every time the slider is changed - updates the label on the GUI.
        def slider_changed(event):
            slider_value_label.configure(text=format_value(get_current_value()))

        slider_label = ctk.CTkLabel(s_frame, text='> Grid size:', font=('Upheaval TT (BRK)', 30))
        slider_label.place(relx=0.3, rely=0.51, anchor='center')

        slider_value_label = ctk.CTkLabel(s_frame, text=format_value(get_current_value()), 
                                          text_color='#FFFFFF', font=('Upheaval TT (BRK)', 30))
        slider_value_label.place(relx=0.55, rely=0.51, anchor='center')

        # Slider for maze size.
        slider = ctk.CTkSlider(s_frame, width=400, button_color='#FFFFFF', 
                               button_hover_color='#cccccc', variable=slider_value, command=slider_changed)
        slider.place(relx=0.5, rely=0.66, anchor='center')

        # Displays an error message on the GUI when nothing is selected in the drop down and the play button is pressed.
        combobox_error_message = ctk.CTkLabel(m_frame, text='', 
                                              text_color='#e53935', 
                                              font=('Upheaval TT (BRK)', 15))
        combobox_error_message.grid(row=0, column=0, padx=(0,260), pady=(465, 0))

        # Called when the play button is pressed.
        def spGame_button():
            algo.play_click_sound()
            """
            If the parameters are selected:
            -Update the current slider value.
            -Call the function in the next page to start the maze generation.
            -Set the mode for algo file to be singleplayer to prevent checking overlap in move_p1() (pmode).
            -Show the singleplayer game page
            """
            if self.params != []:
                self.params[0] = int(get_current_value())
                main.sg.spGameCanvas('new')
                algo.pmode = ''
                controller.pages['spGame'].show()
                # Reset error message.
                combobox_error_message.configure(text='')
            else:
                combobox_error_message.configure(text='error : no maze generation algorithm selected')
                
        spGame_button = ctk.CTkButton(s_frame, height=40, fg_color='#75a050', 
                                      hover_color='#3d5329', text='START', 
                                      text_color='#FFFFFF', font=('Upheaval TT (BRK)', 30), 
                                      border_width=2, command=spGame_button)
        spGame_button.place(relx=0.5, rely=0.84, anchor='center')

        def back_button():
            algo.play_click_sound()
            combobox_error_message.configure(text='')
            controller.pages['modeSelection'].show()
        
        back_button = ctk.CTkButton(m_frame, height=40, corner_radius=8, 
                                    border_width=3, text_color='#FFFFFF', 
                                    font=('Upheaval TT (BRK)', 25), 
                                    text="< BACK", command=back_button)
        back_button.grid(row=0, column=0, padx=(0,536), pady=(0,494))

# The Singleplayer Game page class - a child of the Page class.
class spGame(Page):  # Singleplayer game screen.
    def __init__(self, controller, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)  # Inherits the page class.

        self.controller = controller  # Controller for changing pages.
        self.imperfect = False  # Determines whether imperfect mazes are generated (settings).

        self.bg1label = ctk.CTkLabel(self, image = bg_game, text = '')  # Create label to place background image.
        self.bg1label.place(relx=0.5, rely=0.5, anchor='center')

        # Title.
        self.title_frame = ctk.CTkFrame(self)
        self.title_frame.place(relx=0.5, rely=0.1, anchor='center')
        title = ctk.CTkLabel(self.title_frame, text=" HEDGE ", 
                             text_color='#82925e', font=('Upheaval TT (BRK)', 50))
        subheading = ctk.CTkLabel(self.title_frame, text="SINGLEPLAYER ", 
                                  text_color='#FFFFFF', font=('Upheaval TT (BRK)', 30, 'italic'))
        title.pack()
        subheading.pack()
        
        # Frame to contain GUI information on the left.
        left_frame = ctk.CTkFrame(self, height=228, width=380)
        left_frame.place(relx=0.15, rely=0.495, anchor='center')
        
        # Styling.
        left_image = ctk.CTkImage(Image.open("assets/game_left.png"), size=(191, 227))
        left_image_label = ctk.CTkLabel(left_frame, text='', image=left_image)
        left_image_label.place(relx=0, rely=0.5, anchor='w')

        # Info about algorithm and maze size on GUI.
        self.algo_label = ctk.CTkLabel(left_frame, text='', text_color='#FFFFFF', 
                                       font=('Upheaval TT (BRK)', 35, 'italic'))
        self.grid_label = ctk.CTkLabel(left_frame, text='', text_color='#FFFFFF', 
                                       font=('Upheaval TT (BRK)', 35, 'italic'))
        self.algo_label.place(x=150, rely=0.11)
        self.grid_label.place(x=150, rely=0.61)

        # Frame to contain GUI information on the right.
        right_frame = ctk.CTkFrame(self, height=228, width=380)
        right_frame.place(relx=0.85, rely=0.495, anchor='center')

        # Styling.
        right_image = ctk.CTkImage(Image.open('assets/sg_right.png'), size=(233, 227))
        right_image_label = ctk.CTkLabel(right_frame, text='', image=right_image)
        right_image_label.place(x=380, rely=0.5, anchor='e')
    
        # Displays the steps made so far and the time elapsed.
        self.step_label = ctk.CTkLabel(right_frame, text='', text_color='#FFFFFF', 
                                       font=('Upheaval TT (BRK)', 45, 'italic'))
        self.time_label = ctk.CTkLabel(right_frame, text='', text_color='#82925e', 
                                       font=('Upheaval TT (BRK)', 50, 'italic'))
        self.step_label.place(x=100, rely=0.145, anchor='w')
        self.time_label.place(x=100, rely=0.645, anchor='w')

        # Progress bar - utilises the manhattan distance between the player's current position and the goal.
        self.progress = ctk.CTkProgressBar(self, width=600, height=5, 
                                           corner_radius=5, progress_color='#a1d0d1')
        self.progress.set(0)
        self.progress.place(relx=0.5, rely=0.9, anchor='center')

        # Called when the back button is pressed.
        def back_button():
            self.update = False
            controller.pages['spOptions'].show()
            # Styling.
            self.retry_label.pack_forget()
        
        back_button = ctk.CTkButton(self, height=40, corner_radius=8, border_width=3, 
                                    text_color='#FFFFFF', font=('Upheaval TT (BRK)', 25), 
                                    text="QUIT", command=back_button)
        back_button.place(relx=0.1, rely=0.1, anchor='center')
            
    def createNewMaze(self):
        """
        Creates a maze using algo.py and the parameters passed from singleplayer options
        Only called when a new game is played.
        """
        self.game_frame = ctk.CTkFrame(self, width=600, height=600)
        self.game_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        # Displays the canvas created in the algo file.
        algo.create_canvas(self.game_frame, canvas_colour)
        # Creates a graph object - this is the foundation of the maze.
        algo.graph = algo.Graph(main.so.params[0])

        self.grid_label.configure(text=f'{main.so.params[0]} x {main.so.params[0]} ')
     
        # Generates a maze depending on the algorithm selected.
        if main.so.params[1] == 'Depth First Search':
            algo.graph.DFS()  # Calls DFS() on the graph object to generate a DFS maze.
            self.algo_label.configure(text='DFS ')  # Configures the label on the GUI
        elif main.so.params[1] == 'Hunt-and-Kill':
            algo.graph.Hunt_and_Kill()  # Calls Hunt_and_Kill() on the graph object to generate a hunt and kill maze.
            self.algo_label.configure(text='Hunt - Kill')  # Configures the label on the GUI
        elif main.so.params[1] == 'Sidewinder':
            algo.graph.Sidewinder()  # Calls Sidewinder() on the graph object to generate a sidewinder maze.
            self.algo_label.configure(text='Sidewinder ')  # Configures the label on the GUI

        if self.imperfect:
            # If the imperfect maze switch is toggled on in settings, then make the graph imperfect.
            algo.graph.Imperfect()
        
        # Draw the maze on the canvas.
        algo.draw_maze(algo.canvas_m, line_colour)
        

    def spGameCanvas(self, mode):
        """
        A function that is called only when the play button is pressed 
        - NOT called at initialisation - which ensures that the game update loop only activates when 
        a player presses play in an options menu.
        """

        # Starts the update loop.
        self.update = True
        # Starts the time.
        self.sp_time_start = time.time()

        # No player 2 in singleplayer.
        algo.p2 = None

        # Styling.
        self.retry_label = ctk.CTkLabel(self.title_frame, text='repeated', 
                                        text_color='#ca4754', font=('Upheaval TT (BRK)', 15))
        self.retry_label.pack()

        if mode == 'new':
            # When a new maze is generated.
            # Calls the createNewMaze() function
            self.createNewMaze()
            # Styling.
            self.retry_label.pack_forget()
        elif mode == 'retry':
            # Removes the previous player sprite.
            algo.canvas_m.delete(algo.p1)
            # Styling.
            self.retry_label.pack()

        # Draws the player.
        algo.draw_player('single')
        # Sets the player's moves to 0.
        algo.p1moves = 0

        # Update function - called every 100ms.
        def spUpdate():
            """
            Constantly detects for wins using algo.py.
            If a win is detected, stop updating
            If a win is not detected then keep updating
            """
            # If a win is detected.
            if algo.detect_win('single'): 
                self.update = False
                self.sp_time_end = time.time()  # Stops the time.
                main.r.results('single')  # Call results page so it can display the relevant information.
                self.controller.pages['Results'].show()  # Shows the result page.
                # Styling.
                self.retry_label.pack_forget()

            # If not won yet, refresh the elements on the GUI.
            if self.update == True:
                # Update the progress bar.
                self.progress.set(1-(algo.h('single')/(2*main.so.params[0])))  # h() is heuristic function.
                # Update the step label and the time label.
                self.step_label.configure(text=f'{algo.get_moves("single")}  ')
                self.time_label.configure(text=f'{round(time.time()-self.sp_time_start, 1)}  ')
                
                root.after(100, spUpdate)

        root.after(0, spUpdate)  # First run of the loop

# The Multiplayer Options page class - a child of the Page class.
class mpOptions(Page): # Screen to select generation style and grid size for multiplayer.
    def __init__(self, controller, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)  # Inherits the page class.

        self.bg1label = ctk.CTkLabel(self, image = bg1, text = '')  # Create label to place background image.
        self.bg1label.place(relx=0.5, rely=0.5, anchor='center')

        m_frame = ctk.CTkFrame(self, width=900, height=700)
        m_frame.place(relx=0.5, rely=0.5, anchor='center')

        s_frame = ctk.CTkFrame(m_frame, width=675, height=380, border_width=5, corner_radius=15)
        s_frame.place(relx=0.5, rely=0.55, anchor='center')

        # Defines the parameters list
        self.params = [None, None, None]

        # Called for every interation with the drop down box.
        def combobox_callback(choice):
            # Redefines the params list when a choice is made.
            # It gets the current slider value, the choice of the drop down box, and the win condition.
            self.params = [int(get_current_value()), choice, condition_switch_var.get()]

        title_label = ctk.CTkLabel(s_frame, text='-Multiplayer Options-', font=('Upheaval TT (BRK)', 35), text_color='#FFFFFF')
        title_label.place(relx=0.5, rely=0.12, anchor='center')

        # The drop down menu.
        combobox = ctk.CTkComboBox(s_frame, width=400, height=50,
                                   state="readonly",
                                   values=['Depth First Search', 'Hunt-and-Kill', 'Sidewinder'], 
                                   font=('Upheaval TT (BRK)', 20), 
                                   dropdown_font=('Upheaval TT (BRK)', 20),
                                   command=combobox_callback)
        combobox.set('Select a generation algorithm')
        combobox.place(relx=0.5, rely=0.31, anchor='center')

        """
        To implement the slider, we need to update the displayed value of the slider going to the
        gui every time the slider is changed.
        We also need to get the final slider value when the user presses the start button.
        
        To do this, a slider value is defined, three functions are created:
            - get_current_value()
            - format_value()
            - slider_changed()
        
        The slider_changed() function is called every time the user interacts with the slider,
        it changes the displayed value of the maze size on the GUI
        It calls the get_current_value() function, and formats the output using the format_value() function.
        
        When the start game button is pressed, in order to get the current slider value, 
        we update the parameter list passed to the game object.
        
        """

        slider_value = ctk.DoubleVar()
        
        # Returns current slider value.
        def get_current_value():
            value = '{: .0f}'.format(slider_value.get()*25+5)
            return value
        
        # Formats the value to be displayed on the GUI
        def format_value(value):
            return f'{value} x{value}'
        
        # Called every time the slider is changed - updates the label on the GUI.
        def slider_changed(event):
            slider_value_label.configure(text=format_value(get_current_value()))

        slider_label = ctk.CTkLabel(s_frame, text='> Grid size:', font=('Upheaval TT (BRK)', 30))
        slider_label.place(relx=0.3, rely=0.51, anchor='center')

        slider_value_label = ctk.CTkLabel(s_frame, text=format_value(get_current_value()), 
                                          text_color='#FFFFFF', font=('Upheaval TT (BRK)', 30))
        slider_value_label.place(relx=0.55, rely=0.51, anchor='center')

        # Slider for maze size.
        slider = ctk.CTkSlider(s_frame, width=400, button_color='#FFFFFF', 
                               button_hover_color='#cccccc', variable=slider_value, 
                               command=slider_changed)
        slider.place(relx=0.5, rely=0.66, anchor='center')

        # Called every time the switch is changed.
        def condition_switch_event():
            if condition_switch_var.get() == 'steps':
                self.params[2] = 'steps'
            else:
                self.params[2] = 'speed'
        
        # Switch to change win condition.
        condition_switch_var = ctk.StringVar(value='speed')
        condition_switch = ctk.CTkSwitch(s_frame, text='', command=condition_switch_event, 
                                         variable=condition_switch_var, onvalue='steps', offvalue='speed', 
                                         switch_width=50, switch_height=27)
        condition_switch.place(relx=0.34, rely=0.84, anchor='center')

        condition_label_1 = ctk.CTkLabel(s_frame, text='Fastest', font=('Upheaval TT (BRK)', 15))
        condition_label_1.place(relx=0.2, rely=0.84, anchor='center')
        condition_label_2 = ctk.CTkLabel(s_frame, text='Least Steps', font=('Upheaval TT (BRK)', 15))
        condition_label_2.place(relx=0.43, rely=0.84, anchor='center')

        # Displays an error message on the GUI when nothing is selected in the drop down and the play button is pressed.
        combobox_error_message = ctk.CTkLabel(m_frame, text='', text_color='#e53935', font=('Upheaval TT (BRK)', 15))
        combobox_error_message.grid(row=0, column=0, padx=(0,260), pady=(465, 0))

        # Called when the play button is pressed.
        def mpGame_button():
            algo.play_click_sound()
            """
            If the parameters are selected:
            -Update the current slider value.
            -Call the function in the next page to start the maze generation.
            -Set the mode for algo.py move_player functions in order for them to check for overlaps (pmode).
            -Show the multiplayer game page
            """
            if self.params != [None, None, None]: #if the parameters are selected
                self.params[0] = int(get_current_value())
                main.mg.mpGameCanvas('new')
                algo.pmode = 'multi'
                controller.pages['mpGame'].show()
                # Reset error message.
                combobox_error_message.configure(text='')
            else:
                combobox_error_message.configure(text='error : no maze generation algorithm selected')
                
        mpGame_button = ctk.CTkButton(s_frame, height=40, fg_color='#75a050', 
                                      hover_color='#3d5329', text='START', 
                                      text_color='#FFFFFF', font=('Upheaval TT (BRK)', 30), 
                                      border_width=2, command=mpGame_button)
        mpGame_button.place(relx=0.7, rely=0.84, anchor='center')

        def back_button():
            algo.play_click_sound()
            combobox_error_message.configure(text='')
            controller.pages['modeSelection'].show()
        
        back_button = ctk.CTkButton(m_frame, height=40, corner_radius=8, 
                                    border_width=3, text_color='#FFFFFF', 
                                    font=('Upheaval TT (BRK)', 25), 
                                    text="< BACK", command=back_button)
        back_button.grid(row=0, column=0, padx=(0,536), pady=(0,494))

# The Singleplayer Game page class - a child of the Page class.
class mpGame(Page):  # Multiplayer game screen.
    def __init__(self, controller, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)  # Inherits the page class.

        self.controller = controller  # Controller for changing pages.
        self.imperfect = False  # Determines whether imperfect mazes are generated (settings).

        self.bg1label = ctk.CTkLabel(self, image = bg_game, text = '')  # Create label to place background image.
        self.bg1label.place(relx=0.5, rely=0.5, anchor='center')

        # Title.
        self.title_frame = ctk.CTkFrame(self)
        self.title_frame.place(relx=0.5, rely=0.1, anchor='center')
        title = ctk.CTkLabel(self.title_frame, text=" HEDGE ", 
                             text_color='#82925e', 
                             font=('Upheaval TT (BRK)', 50))
        subheading = ctk.CTkLabel(self.title_frame, text="MULTIPLAYER ", 
                                  text_color='#FFFFFF', 
                                  font=('Upheaval TT (BRK)', 30, 'italic'))
        title.pack()
        subheading.pack()
        
        # Frame to contain GUI information on the left.
        left_frame = ctk.CTkFrame(self, height=228, width=380)
        left_frame.place(relx=0.15, rely=0.495, anchor='center')
        
        # Styling.
        left_image = ctk.CTkImage(Image.open("assets/game_left.png"), size=(191, 227))
        left_image_label = ctk.CTkLabel(left_frame, text='', image=left_image)
        left_image_label.place(relx=0, rely=0.5, anchor='w')

        # Info about algorithm and maze size on GUI.
        self.algo_label = ctk.CTkLabel(left_frame, text='', 
                                       text_color='#FFFFFF', 
                                       font=('Upheaval TT (BRK)', 35, 'italic'))
        self.grid_label = ctk.CTkLabel(left_frame, text='', 
                                       text_color='#FFFFFF', 
                                       font=('Upheaval TT (BRK)', 35, 'italic'))
        self.algo_label.place(x=150, rely=0.11)
        self.grid_label.place(x=150, rely=0.61)

        # Frame to contain GUI information on the right.
        right_frame = ctk.CTkFrame(self, height=330, width=380)
        right_frame.place(relx=0.85, rely=0.495, anchor='center')

        # Styling.
        right_image = ctk.CTkImage(Image.open('assets/mg_right.png'), size=(231, 329))
        right_image_label = ctk.CTkLabel(right_frame, text='', image=right_image)
        right_image_label.place(x=380, rely=0.5, anchor='e')

        # Displays the steps made so far and the time elapsed.
        self.p1_step_label = ctk.CTkLabel(right_frame, text='', 
                                          text_color='#FFFFFF', 
                                          font=('Upheaval TT (BRK)', 45, 'italic'))
        self.p2_step_label = ctk.CTkLabel(right_frame, text='', 
                                          text_color='#FFFFFF', 
                                          font=('Upheaval TT (BRK)', 45, 'italic'))
        self.time_label = ctk.CTkLabel(right_frame, text='', text_color='#82925e', font=('Upheaval TT (BRK)', 50, 'italic'))
        self.p1_step_label.place(x=100, rely=0.145, anchor='w')
        self.p2_step_label.place(x=100, rely=0.337, anchor='w')
        self.time_label.place(x=100, rely=0.755, anchor='w')

        # Progress bars - utilises the manhattan distance between the players' current positions and the goal.
        self.progress1 = ctk.CTkProgressBar(self, width=600, height=5, corner_radius=5, progress_color='#c77373')
        self.progress1.set(0)
        self.progress1.place(relx=0.5, rely=0.9, anchor='center')
        self.progress2 = ctk.CTkProgressBar(self, width=600, height=5, corner_radius=5,  progress_color='#f4e59d')
        self.progress2.set(0)
        self.progress2.place(relx=0.5, rely=0.92, anchor='center')

        # Called when the back button is pressed.
        def back_button():
            self.update = False
            controller.pages['mpOptions'].show()
            # Styling.
            self.retry_label.pack_forget()
            # Clears list of winners.
            algo.order_list = []
        
        back_button = ctk.CTkButton(self, height=40, corner_radius=8, 
                                    border_width=3, text_color='#FFFFFF', 
                                    font=('Upheaval TT (BRK)', 25), text="QUIT", command=back_button)
        back_button.place(relx=0.1, rely=0.1, anchor='center')


    def createNewMaze(self):
        """
        Creates a maze using algo.py and the parameters passed from multiplayer options
        Only called when a new game is played.
        """
        self.game_frame = ctk.CTkFrame(self, width=600, height=600)
        self.game_frame.place(relx=0.5, rely=0.5, anchor='center')

        # Displays the canvas created in the algo file.
        algo.create_canvas(self.game_frame, canvas_colour)
        # Creates a graph object - this is the foundation of the maze.
        algo.graph = algo.Graph(main.mo.params[0])

        self.grid_label.configure(text=f'{main.mo.params[0]} x {main.mo.params[0]} ')

        # Generates a maze depending on the algorithm selected.
        if main.mo.params[1] == 'Depth First Search':
            algo.graph.DFS()  # Calls DFS() on the graph object to generate a DFS maze.
            self.algo_label.configure(text='DFS ')  # Configures the label on the GUI
        elif main.mo.params[1] == 'Hunt-and-Kill':
            algo.graph.Hunt_and_Kill()  # Calls Hunt_and_Kill() on the graph object to generate a hunt and kill maze.
            self.algo_label.configure(text='Hunt - Kill')  # Configures the label on the GUI
        elif main.mo.params[1] == 'Sidewinder':
            algo.graph.Sidewinder()  # Calls Sidewinder() on the graph object to generate a sidewinder maze.
            self.algo_label.configure(text='Sidewinder ')  # Configures the label on the GUI

        if self.imperfect:
            # If the imperfect maze switch is toggled on in settings, then make the graph imperfect.
            algo.graph.Imperfect()

        # Draw the maze on the canvas.
        algo.draw_maze(algo.canvas_m, line_colour)

    def mpGameCanvas(self, mode):
        """
        A function that is called only when the play button is pressed 
        - NOT called at initialisation - which ensures that the game update loop only activates when 
        a player presses play in an options menu.
        """

        # Starts the update loop.
        self.update = True
        # Starts the time.
        self.mp_time_start = time.time()

        # Styling.
        self.retry_label = ctk.CTkLabel(self.title_frame, text='repeated', 
                                        text_color='#ca4754', font=('Upheaval TT (BRK)', 15))
        self.retry_label.pack()

        if mode == 'new':
            # When a new maze is generated.
            # Calls the createNewMaze() function
            self.createNewMaze()
            # Styling.
            self.retry_label.pack_forget()
        elif mode == 'retry':
            # Removes the previous players' sprites.
            algo.canvas_m.delete(algo.p1)
            algo.canvas_m.delete(algo.p2)
            # Styling.
            self.retry_label.pack()

        # Draws the player.
        algo.draw_player('multi')
        # Sets the players' moves to 0.
        algo.p1moves = 0
        algo.p2moves = 0
        
        # Update function - called every 100ms.
        def mpUpdate():
            """
            Constantly detects for wins using algo.py.
            If a win is detected, stop updating
            If a win is not detected then keep updating
            """
            win_list = algo.detect_win('multi')
            # If a win is detected.
            if win_list[0]:
                self.update = False
                main.r.results('multi', win_list)  # Call results page so it can display the relevant information.
                self.controller.pages['Results'].show()  # Shows the result page.
                # Styling.
                self.retry_label.pack_forget()
                # Reset the order_list.
                algo.order_list = []
            
            # If not won yet, refresh the elements on the GUI.
            if self.update == True:
                # Update the progress bars.
                self.progress1.set(1-(algo.h('multi')[0]/(2*main.mo.params[0])))  # h() is heuristic function.
                self.progress2.set(1-(algo.h('multi')[1]/(2*main.mo.params[0])))
                # Update the step labels and the time label.
                self.p1_step_label.configure(text=f'{algo.get_moves("multi")[0]}  ')
                self.p2_step_label.configure(text=f'{algo.get_moves("multi")[1]}  ')
                self.time_label.configure(text=f'{round(time.time()-self.mp_time_start, 1)}  ')
                
                root.after(100, mpUpdate)

        root.after(0, mpUpdate) #first run of the loop

# The Results page class - a child of the Page class.
class Results(Page):
    def __init__(self, controller, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.controller = controller

        # Defines the path tuple that will contain the list of shortest paths.
        self.path2 = {}

        self.bg1label = ctk.CTkLabel(self, image = bg_res, text = '')  # Create label to place background image.
        self.bg1label.place(relx=0.5, rely=0.5, anchor='center')

    def return_button(self): # Returns to the respective game option selection page when 'new game' button is pressed.
        algo.play_click_sound()
        if self.mode == 'single':
            self.controller.pages['spOptions'].show()
        if self.mode == 'multi':
            self.controller.pages['mpOptions'].show()

    def retry_button(self): # Returns to the same maze for reattempt.
        algo.play_click_sound()
        if self.mode == 'single':
            main.sg.spGameCanvas('retry')  # Calls the function in the singleplayer game object in retry mode.
            self.controller.pages['spGame'].show()
        if self.mode == 'multi':
            main.mg.mpGameCanvas('retry')  # Calls the function in the multiplayer game object in retry mode.
            self.controller.pages['mpGame'].show()
    
    def home_button(self):  # Returns to home - the main menu.
        algo.play_click_sound()
        self.controller.pages['mainMenu'].show()
    
    def results(self, mode, win_list=None):
        """
        Called when the game is finished - NOT at initialisation
        """
        self.mode = mode
        
        self.m_frame = ctk.CTkFrame(self, width=1280, height=650)
        self.m_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        # Frame to display results on the left.
        results_frame = ctk.CTkFrame(self.m_frame, width=500, height=650)
        results_frame.place(relx=0.2, rely=0.5, anchor='center')
        self.path2 = {} #path of solved solution
        
        # Displaying different information depending on the mode.
        if self.mode == 'single':
            # Size of maze.
            size = main.so.params[0]

            title = ctk.CTkLabel(results_frame, text='GAME STATS:', text_color='#FFFFFF', 
                                 font=('Upheaval TT (BRK)', 70))
            title.place(x=10, y=0)

            steps = ctk.CTkLabel(results_frame, text=f'Steps Made: {algo.get_moves("single")}', 
                                 font=('Upheaval TT (BRK)', 33))
            steps.place(x=10, y=190)

            # Calculates the time taken for the player to reach the end.
            time_taken = ctk.CTkLabel(results_frame, 
                                      text=f'Time Taken: {round(main.sg.sp_time_end - main.sg.sp_time_start, 1)} s', 
                                      font=('Upheaval TT (BRK)', 33))
            time_taken.place(x=10, y=230)
        
        elif self.mode == 'multi':
            # Size of maze.
            size = main.mo.params[0]
            # Gets player1 and player2 times.
            p1_time_end = win_list[0][1] if win_list[0][0] == 'p1' else win_list[1][1]
            p2_time_end = win_list[1][1] if win_list[0][0] == 'p1' else win_list[0][1]

            # If comparing speed.
            if main.mo.params[2] == 'speed':
                if win_list[0][0] == 'p1':
                    title_text = 'RED WINS!'
                    text_color = '#c77373'
                else:
                    title_text = 'YELLOW WINS!'
                    text_color = '#f4e59d'
            else:  # Else if comparing least moves.
                moves = algo.get_moves("multi")
                if moves[0] < moves[1]:
                    title_text = 'RED WINS!'
                    text_color = '#c77373'
                elif moves[0] > moves[1]:
                    title_text = 'YELLOW WINS!'
                    text_color = '#f4e59d'
                else:  # In the event of a draw.
                    title_text = 'DRAW!'
                    text_color = '#FFFFFF'

            # Place various labels on the GUI.
            title = ctk.CTkLabel(results_frame, text=title_text, 
                                 text_color=text_color, font=('Upheaval TT (BRK)', 70))
            title.place(x=10, y=0)
                            
            p1_label = ctk.CTkLabel(results_frame, 
                                    text=f'Player 1: RED', text_color='#c77373', 
                                    font=('Upheaval TT (BRK)', 33))
            p1_label.place(x=10, y=130)
            p1_steps = ctk.CTkLabel(results_frame, 
                                    text=f'Steps: {algo.get_moves("multi")[0]}', 
                                    font=('Upheaval TT (BRK)', 33))
            p1_steps.place(x=50, y=160)
            p1_time = ctk.CTkLabel(results_frame, 
                                   text=f'Time: {round(p1_time_end - main.mg.mp_time_start, 2)} s', 
                                   font=('Upheaval TT (BRK)', 33))
            p1_time.place(x=50, y=190)

            p2_label = ctk.CTkLabel(results_frame, text=f'Player 2: YELLOW', 
                                    text_color='#f4e59d', font=('Upheaval TT (BRK)', 33))
            p2_label.place(x=10, y=230)
            p2_steps = ctk.CTkLabel(results_frame, 
                                    text=f'Steps: {algo.get_moves("multi")[1]}', 
                                    font=('Upheaval TT (BRK)', 33))
            p2_steps.place(x=50, y=260)
            p2_time = ctk.CTkLabel(results_frame, 
                                   text=f'Time: {round(p2_time_end - main.mg.mp_time_start, 2)} s', 
                                   font=('Upheaval TT (BRK)', 33))
            p2_time.place(x=50, y=290)

        # Frame on the right - contains the solved maze when requested.
        canvas_frame = ctk.CTkFrame(self.m_frame, width=600, height = 600)
        algo.clone_canvas(algo.canvas_m, canvas_frame, canvas_colour, line_colour)  # Clones the game canvas.
        # Styling.
        algo.cloned.tag_lower(algo.cloned.create_rectangle(600-algo.w, 600-algo.w, 600, 600, width = 0, fill='#005b27'))

        button_frame = ctk.CTkFrame(self.m_frame, width=600, height = 600, fg_color=('#96a672', '#16291d'))
        button_frame.place(relx=0.7625, rely=0.5, anchor='center')
 
        # Called when the 'reveal solution' button is pressed.
        def solve_maze():
            # Priority queue for A* algorithm.
            queue = PriorityQueue()
            # Get a gradient of colours for visualising searching.
            search_colours = algo.get_colour_gradient('#473d5a', '#005b27', 2*size-1)
            # Start node.
            start = 0
            self.path = {}  

            g_score = [float('inf') for _ in range(algo.graph.num_nodes)]
            g_score[start] = 0
            f_score = [float('inf') for _ in range(algo.graph.num_nodes)]
            f_score[start] = algo.h('a*', start)

            queue.put((f_score[start],algo.h('a*', start),start))
            self.end = False
            def astar_loop():
                if not queue.empty():
                    cur_node = queue.get()[2]
                    if cur_node+1 == size**2:
                        draw_path()
                        pass
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
                                    temp_f_score = temp_g_score + algo.h('a*', child_node)
                                    
                                    # Draws the search cells.
                                    index = algo.h('a*', child_node)
                                    algo.cloned.tag_lower(algo.cloned.create_rectangle(0+child_node%size*algo.w, 
                                                                                       0+child_node//size*algo.w, 
                                                                                       child_node%size*algo.w + algo.w-0, 
                                                                                       child_node//size*algo.w + algo.w-0, 
                                                                                       tags='del', width = 0, 
                                                                                       fill=search_colours[index]))
                                    
                                    if temp_f_score < f_score[child_node]:
                                        g_score[child_node]= temp_g_score
                                        f_score[child_node]= temp_f_score
                                        queue.put((temp_f_score, algo.h('a*', child_node), child_node))
                                        self.path[child_node]=cur_node
                        root.after(1, astar_loop)
            root.after(0, astar_loop)

            # Draws the path of the shortest path.
            def draw_path():
                self.path2 = {}
                node = size**2 - 1
                while node != 0:
                    self.path2[self.path[node]] = node
                    node = self.path[node]
                path_colours = algo.get_colour_gradient('#473d5a', '#004f5a', len(self.path2))
                for index, node in enumerate(self.path2.keys()):
                    algo.cloned.create_rectangle(0+node%size*algo.w, 
                                                 0+node//size*algo.w, 
                                                 node%size*algo.w + algo.w -0, 
                                                 node//size*algo.w + algo.w-0, 
                                                 width=0, fill=path_colours[index])
                algo.cloned.delete(algo.cloned.gettags("del"))
                algo.draw_maze(algo.cloned, line_colour)
                algo_steps = ctk.CTkLabel(results_frame, 
                                          text=f'Optimal Path: {len(self.path2)} Steps', 
                                          text_color=('#608f90','#a1d0d1'), font=('Upheaval TT (BRK)', 33))
                
                # Displays more info when the solution is revealed - the difference between their solution and the optimal one.
                if self.mode == 'single':
                    algo_steps.place(x=10, y=300)
                    difference = ctk.CTkLabel(results_frame, 
                                              text=f'Difference: {algo.get_moves("single")-len(self.path2)} Steps', 
                                              font=('Upheaval TT (BRK)', 33))
                    difference.place(x=10, y=340)                
                else:
                    algo_steps.place(x=10, y=350)
                    p1_diff = ctk.CTkLabel(results_frame, 
                                           text=f'Red Difference: {algo.get_moves("multi")[0]-len(self.path2)}', 
                                           font=('Upheaval TT (BRK)', 33))
                    p1_diff.place(x=10, y=410)
                    p2_diff = ctk.CTkLabel(results_frame, 
                                           text=f'Yellow Difference: {algo.get_moves("multi")[1]-len(self.path2)}', 
                                           font=('Upheaval TT (BRK)', 33))
                    p2_diff.place(x=10, y=440)

        # Called when the 'reveal solution' button is pressed.
        def show_canvas():
            algo.play_click_sound()
            button_frame.place_forget()
            canvas_frame.place(relx=0.7625, rely=0.5, anchor='center')
            solve_maze()

        # Reveal solution button.
        button = ctk.CTkButton(button_frame, height=35, text='Reveal solution', 
                               font=('Upheaval TT (BRK)', 25), command=show_canvas)
        button.place(x=300, y=300, anchor='center')

        return_button = ctk.CTkButton(results_frame, corner_radius=8, border_width=3, 
                                      height=60, width=200, fg_color=('#96a672','#2a4f38'), 
                                      text='New Game', font=('Upheaval TT (BRK)', 35), command=self.return_button)
        return_button.place(x=10, y=565)

        retry_button = ctk.CTkButton(results_frame, corner_radius=8, border_width=3, 
                                     height=60, width=100, text='REDO', 
                                     font=('Upheaval TT (BRK)', 35), command=self.retry_button)
        retry_button.place(x=245, y=565)

        home_button = ctk.CTkButton(results_frame, corner_radius=8, border_width=3, 
                                    height=60, width=100, text='HOME', 
                                    font=('Upheaval TT (BRK)', 35), command=self.home_button)
        home_button.place(x=380, y=565)
class Window(ctk.CTkFrame): # Create main window.
    def __init__(self, *args, **kwargs):
        ctk.CTkFrame.__init__(self, *args, **kwargs)

        # Create a dictionary for all of the different selection pages.
        self.pages = {}
        for Subclass in (mainMenu, settings, modeSelection, 
                         spOptions, mpOptions, spGame, 
                         mpGame, Results):
            self.pages[Subclass.__name__] = Subclass(self)
        
        self.mm, self.st, self.ms, self.so, self.mo, self.sg, self.mg, self.r = self.pages.values()
        
        # Creating a container frame to contain the widgets of each page.
        container = ctk.CTkFrame(self)
        container.pack(side="top", fill="both", expand=True)

        # Place all of the widgets into the frame.
        for window in self.pages.values():
            window.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        
        # Show the first set of widgets - the main menu widgets on startup.
        self.mm.show()

    def switch_theme(self):  # Function to switch theme.
        global theme, canvas_colour, line_colour
        if theme == 'light':
            theme = 'dark'
            canvas_colour = '#16291d'
            line_colour = '#afbf8b'
            # Change all background images.
            self.mm.bg2label.configure(image=ctk.CTkImage(Image.open('assets/bg2.png'), 
                                                          size=(900, 700)))
            self.mm.bg1label.configure(image=ctk.CTkImage(Image.open('assets/grad2bg.png'), 
                                                          size=(1920, 1080)))
            self.st.bg1label.configure(image=ctk.CTkImage(Image.open('assets/grad2set.png'), 
                                                          size=(1920, 1080)))
            self.ms.bg1label.configure(image=ctk.CTkImage(Image.open('assets/grad2bg.png'), 
                                                          size=(1920, 1080)))
            self.so.bg1label.configure(image=ctk.CTkImage(Image.open('assets/grad2bg.png'), 
                                                          size=(1920, 1080)))
            self.mo.bg1label.configure(image=ctk.CTkImage(Image.open('assets/grad2bg.png'), 
                                                          size=(1920, 1080)))
            self.sg.bg1label.configure(image=ctk.CTkImage(Image.open('assets/grad2game.png'), 
                                                          size=(1920, 1080)))
            self.mg.bg1label.configure(image=ctk.CTkImage(Image.open('assets/grad2game.png'), 
                                                          size=(1920, 1080)))
            self.r.bg1label.configure(image=ctk.CTkImage(Image.open('assets/grad2res.png'), 
                                                         size=(1920, 1080)))
        else:
            theme = 'light'
            canvas_colour = '#82925e'
            line_colour = '#FFFFFF'
            # Change all background images.
            self.mm.bg2label.configure(image=ctk.CTkImage(Image.open('assets/bg1.png'), 
                                                          size=(900, 700)))
            self.mm.bg1label.configure(image=ctk.CTkImage(Image.open('assets/grad1bg.png'), 
                                                          size=(1920, 1080)))
            self.st.bg1label.configure(image=ctk.CTkImage(Image.open('assets/grad1set.png'), 
                                                          size=(1920, 1080)))
            self.ms.bg1label.configure(image=ctk.CTkImage(Image.open('assets/grad1bg.png'), 
                                                          size=(1920, 1080)))
            self.so.bg1label.configure(image=ctk.CTkImage(Image.open('assets/grad1bg.png'), 
                                                          size=(1920, 1080)))
            self.mo.bg1label.configure(image=ctk.CTkImage(Image.open('assets/grad1bg.png'), 
                                                          size=(1920, 1080)))
            self.sg.bg1label.configure(image=ctk.CTkImage(Image.open('assets/grad1game.png'), 
                                                          size=(1920, 1080)))
            self.mg.bg1label.configure(image=ctk.CTkImage(Image.open('assets/grad1game.png'), 
                                                          size=(1920, 1080)))
            self.r.bg1label.configure(image=ctk.CTkImage(Image.open('assets/grad1res.png'), 
                                                         size=(1920, 1080)))
        # Change the theme of widgets.
        ctk.set_appearance_mode(theme)

if __name__ == "__main__":
    # Initialises the tkinter window.
    root = ctk.CTk()
    main = Window(root)
    main.pack(side="top", fill="both", expand=True)
    root.geometry("1600x900")  # Window size at launch (resizable).
    root.minsize(1500, 900) # Minimum window size.
    root.title('Hedge') # Window title.
    root.iconbitmap('assets/icon.ico') # Window icon.

    # Keyboard bindings.
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

    # Function to toggle fullscreen using the f11 key.
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

    # Game event loop.
    root.mainloop()