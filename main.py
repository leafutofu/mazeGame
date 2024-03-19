import customtkinter as ctk  # For the GUI.
import algo  # Import key algorithms.
import time  # For timing the players.
from tkinter.messagebox import askyesno  # For pop-up box when exiting the program.
from PIL import Image  # To import images for buttons and backgrounds.
from queue import PriorityQueue  # For A* search.

theme = ''  # Define theme.
ctk.set_default_color_theme("assets/HEDGE.json")  # Set overall theme to custom json file.

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
        self._bglabel = None

    # A function to raise all the widgets associated with a particular page to the top, displaying it on the window.
    def show(self):
        self.lift()

    # Getter of bglabel - a ctkinter label used to display background images
    @property
    def bglabel(self):
        return self._bglabel
    
    # Setter of bglabel
    @bglabel.setter
    def bglabel(self, bglabel):
        self._bglabel = bglabel

# The Main Menu page class - a child of the Page class.
class mainMenu(Page):
    def __init__(self, controller, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)  # Inherits the page class.
        self._controller = controller

        self.__m_frame = ctk.CTkFrame(self)  # Create a frame for the menu.
        self.__m_frame.pack(side='top', expand=True, fill = 'both')
        
        self._bglabel = ctk.CTkLabel(self.__m_frame, image = bg1, text = '')  # Create label to place background image.
        self._bglabel.place(relx=0.5, rely=0.5, anchor='center')

        self.__s_frame = ctk.CTkFrame(self.__m_frame, height=700, width=900, corner_radius=0)
        self.__s_frame.place(relx=0.5, rely=0.5, anchor='center')

        self._bg2label = ctk.CTkLabel(self.__s_frame, image = bg2, text = '')  # Create label to place 2nd background image (for buttons).
        self._bg2label.place(relx=0.5, rely=0.5, anchor='center')

        self.__title = ctk.CTkLabel(self.__s_frame, text='HEDGE', font=('Upheaval TT (BRK)', 120))
        self.__title.place(relx=0.5, rely=0.38, anchor='center')      

        # Coordinates of various buttons.
        self._mm_settingsX = 410
        self._mm_settingsY = 610
        self._quitX = 485
        self._quitY = 610

        # Binds the left mouse click to the check_position() function.
        root.bind('<Button-1>', self.__check_position)

        # Button styling.
        self.__modeSelection_button = ctk.CTkButton(self.__s_frame, width=170, height=50, corner_radius=8, 
                                                    border_width=2, text_color='#FFFFFF', font=('Upheaval TT (BRK)', 40), 
                                                    text='PLAY', command=self.__modeSelection_button)
        self.__modeSelection_button.place(relx=0.5, rely=0.57, anchor='center')
    
    # Checks the coordinates of any mouse click on the window, and according to parameters, redirects to either the settings page or terminates the program.
    def __check_position(self, event):
        if (event.x >= self._mm_settingsX - 20 and event.x <= self._mm_settingsX + 20 
            and event.y >= self._mm_settingsY - 20 and event.y <= self._mm_settingsY + 20):
            self._controller.pages['settings'].show()
        elif (event.x >= self._quitX - 20 and event.x <= self._quitX + 20 
              and event.y >= self._quitY - 20 and event.y <= self._quitY + 20 and
                askyesno(title='Confirmation', message='Are you sure you want to quit?') == True):
                root.destroy()
            
    # Sets current page variable to 'modeSelection' and shows the widgets associated with the mode selection page.
    def __modeSelection_button(self):
        algo.play_click_sound()
        self._controller.pages['modeSelection'].show()  # Shows widgets associated with the mode selection page.

    # Getter of bg2label
    @property
    def bg2label(self):
        return self._bg2label
    
    # Setter of bg2label
    @bg2label.setter
    def bg2label(self, bg2label):
        self._bg2label = bg2label

# The Settings page class - a child of the Page class.
class settings(Page):
    def __init__(self, controller, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)  # Inherits the page class.
        self._controller = controller

        # Main frame - contains all widgets.
        self.__m_frame = ctk.CTkFrame(self, width=1920, height=1080)
        self.__m_frame.place(relx=0.5, rely=0.5, anchor='center')

        self._bglabel = ctk.CTkLabel(self.__m_frame, image = bg_set, text='')  # Create label to place background image.
        self._bglabel.place(relx=0.5, rely=0.5, anchor='center')

        # Frame to contain switches on the left.
        self.__frame = ctk.CTkFrame(self.__m_frame, width=440, height=600)
        self.__frame.place(x=530, rely=0.5, anchor='center')
        
        # Frame to contain information on the right.
        self.__info_frame = ctk.CTkFrame(self.__m_frame, width = 650, height=540, corner_radius=12, bg_color=('#bfcba4','#34473b'))
        self.__info_frame.place(x=1295, rely=0.52, anchor='center')
        self.__info_frame.pack_propagate(0)

        # Label to place images - for the info_frame which will allow information in the form of images to be displayed.
        self.__info_label = ctk.CTkLabel(self.__info_frame, text='')
        self.__info_label.place(relx=0.48, rely=0, anchor='n')

        # Title.
        self.__title_label = ctk.CTkLabel(self.__frame, text='Settings', font=('Upheaval TT (BRK)', 50))
        self.__title_label.place(x=0, y=0, anchor='nw')

        # Title.
        self.__title_label2 = ctk.CTkLabel(self.__frame, text='+ information ', font=('Upheaval TT (BRK)', 35, 'italic'), text_color=('#FFFFFF','#506d5a'))
        self.__title_label2.place(x=100, y=40, anchor='nw')

        # The radiobutton value.
        self._radiobutton_value = ctk.StringVar(value="off")
        
        # The radiobuttons.
        self.__theme_button = ctk.CTkRadioButton(self.__frame, text='', variable=self._radiobutton_value,
                            value='theme', width=8, command=self.__radiobutton_event)
        self.__gen_button = ctk.CTkRadioButton(self.__frame, text='', variable=self._radiobutton_value,
                            value='gen', width=8, command=self.__radiobutton_event)
        self.__ret_button = ctk.CTkRadioButton(self.__frame, text='', variable=self._radiobutton_value,
                            value='ret', width=8, command=self.__radiobutton_event)
        self.__sound_button = ctk.CTkRadioButton(self.__frame, text='', variable=self._radiobutton_value,
                            value='sound', width=8, command=self.__radiobutton_event)

        self.__theme_button.place(x=10, y=122, anchor='nw')
        self.__gen_button.place(x=10, y=182, anchor='nw')
        self.__ret_button.place(x=10, y=242, anchor='nw')
        self.__sound_button.place(x=10, y=302, anchor='nw')

        # The Tutorial Button.
        self.__tutorial_button = ctk.CTkButton(self.__frame, height=70, width=300, corner_radius=10, border_width=0, font=('Upheaval TT (BRK)', 30), text="🛈 HOW TO PLAY", command=self.__tutorial_button)
        self.__tutorial_button.place(x=30, y=400, anchor='nw')

        # The switch variables.
        self._theme_switch_var = ctk.StringVar(value='dark')
        self._gen_switch_var = ctk.StringVar(value='off')
        self._ret_switch_var = ctk.StringVar(value='off')
        self._sound_switch_var = ctk.StringVar(value='on')

        # The switches.
        self.__theme_switch = ctk.CTkSwitch(self.__frame, text='    Theme', font=('Upheaval TT (BRK)', 20), text_color='#FFFFFF', command=self.__theme_switch_event,
                                variable=self._theme_switch_var, onvalue='light', offvalue='dark',
                                switch_width=50, switch_height=27)
        self.__theme_switch.place(x=60, y=120, anchor='nw')

        self.__gen_switch = ctk.CTkSwitch(self.__frame, text='    Generate imperfect mazes', font=('Upheaval TT (BRK)', 20), text_color='#FFFFFF', command=self.__gen_switch_event,
                                variable=self._gen_switch_var, onvalue='on', offvalue='off',
                                switch_width=50, switch_height=27)
        self.__gen_switch.place(x=60, y=180, anchor='nw')

        self.__ret_switch = ctk.CTkSwitch(self.__frame, text='    Allow return to start', font=('Upheaval TT (BRK)', 20), text_color='#FFFFFF', command=self.__ret_switch_event,
                                variable=self._ret_switch_var, onvalue='on', offvalue='off',
                                switch_width=50, switch_height=27)
        self.__ret_switch.place(x=60, y=240, anchor='nw')

        self.__sound_switch = ctk.CTkSwitch(self.__frame, text='    Player move sound', font=('Upheaval TT (BRK)', 20), text_color='#FFFFFF', command=self.__sound_switch_event,
                                variable=self._sound_switch_var, onvalue='on', offvalue='off',
                                switch_width=50, switch_height=27)
        self.__sound_switch.place(x=60, y=300, anchor='nw')

        # Back button.
        self.__back_button = ctk.CTkButton(self.__frame, height=40, corner_radius=8, border_width=2, font=('Upheaval TT (BRK)', 25), text="< BACK", command=self.__back_button)
        self.__back_button.place(x=0, y=550, anchor='nw')

    # When any of the 4 radiobuttons are selected, the corresponding image is shown.
    def __radiobutton_event(self):
            selection = self._radiobutton_value.get()
            if selection == 'theme':
                self.__info_label.configure(image=ctk.CTkImage(Image.open('assets/theme.png'), size=(600, 520)))
            elif selection == 'gen':
                self.__info_label.configure(image=ctk.CTkImage(Image.open('assets/gen.png'), size=(600, 530)))
            elif selection == 'ret':
                self.__info_label.configure(image=ctk.CTkImage(Image.open('assets/ret.png'), size=(605, 505)))
            elif selection == 'sound':
                self.__info_label.configure(image=ctk.CTkImage(Image.open('assets/sound.png'), size=(600, 470)))
    
    # Change Theme.
    def __theme_switch_event(self):
        self.__theme_button.invoke()  # Invokes the radiobutton to show the information about this particular switch.
        main.switch_theme()

    # Generate Imperfect mazes with multiple solutions.
    def __gen_switch_event(self):
        self.__gen_button.invoke()  # Invokes the radiobutton to show the information about this particular switch.
        if self._gen_switch_var.get() == 'on':
            main.sg.imperfect = True
            main.mg.imperfect = True
        elif self._gen_switch_var.get() == 'off':
            main.sg.imperfect = False
            main.mg.imperfect = False

    # Allows returning to start by pressing Q.
    def __ret_switch_event(self):
        self.__ret_button.invoke()  # Invokes the radiobutton to show the information about this particular switch.
        if self._ret_switch_var.get() == 'on':
            algo.ret_start_allowed = True
        elif self._ret_switch_var.get() == 'off':
            algo.ret_start_allowed = False

    # Turn off game sound.
    def __sound_switch_event(self):
        self.__sound_button.invoke()  # Invokes the radiobutton to show the information about this particular switch.
        if self._sound_switch_var.get() == 'on':
            algo.sound_allowed = True
        elif self._sound_switch_var.get() == 'off':
            algo.sound_allowed = False

    # Displays tutorial on how to play the game.
    def __tutorial_button(self):
        self.__theme_button.deselect()
        self.__gen_button.deselect()
        self.__ret_button.deselect()
        self.__sound_button.deselect()
        self.__info_label.configure(image=ctk.CTkImage(Image.open('assets/tut2.png'), size=(610, 525)))

    # Back to main menu.
    def __back_button(self):
        algo.play_click_sound()
        self._controller.pages['mainMenu'].show()

# The Mode Selection page class - a child of the Page class.
class modeSelection(Page):  # Selects singleplayer or multiplayer.
    def __init__(self, controller, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)  # Inherits the page class.
        self._controller = controller

        self._bglabel = ctk.CTkLabel(self, image = bg1, text = '')  # Create label to place background image.
        self._bglabel.place(relx=0.5, rely=0.5, anchor='center')
        
        self.__m_frame = ctk.CTkFrame(self, width=900, height=700)  # Creates frame for the mode selection page.
        self.__m_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        self.__back_button = ctk.CTkButton(self.__m_frame, height=40, corner_radius=8, border_width=3, text_color='#FFFFFF', font=('Upheaval TT (BRK)', 25), text="< BACK", command=self.__back_button)

        self.__back_button.grid(row=0, column=0, padx=(0,537), pady=(0,494))
        
        # Load images for the buttons
        self.__spOptions_image = ctk.CTkImage(Image.open("assets/sp_button.png"), size=(245,245))
        self.__mpOptions_image = ctk.CTkImage(Image.open("assets/mp_button.png"), size=(250,250))

        self.__spOptions_button = ctk.CTkButton(self.__m_frame, width=290, height=346, corner_radius=20, text="", border_width=5, image=self.__spOptions_image, command=self.__spOptions_button)
        self.__mpOptions_button = ctk.CTkButton(self.__m_frame, width=290, height=346, corner_radius=20, text="", border_width=5, image=self.__mpOptions_image, command=self.__mpOptions_button)

        self.__spOptions_button.grid(row=0, column=0, padx=(0,399), pady=(36,0))
        self.__mpOptions_button.grid(row=0, column=0, padx=(399,0), pady=(36,0))

    # Redirects to singleplayer options page.
    def __spOptions_button(self):
        algo.play_click_sound()
        self._controller.pages['spOptions'].show()
    
    # Redirects to multiplayer options page.
    def __mpOptions_button(self):
        algo.play_click_sound()
        self._controller.pages['mpOptions'].show()

    # Redirects to previous page.
    def __back_button(self):
        algo.play_click_sound()
        self._controller.pages['mainMenu'].show()

# The Singleplayer Options page class - a child of the Page class.
class spOptions(Page): # Screen to select generation style and grid size for singleplayer.
    def __init__(self, controller, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)  # Inherits the page class.
        self._controller = controller

        self._bglabel = ctk.CTkLabel(self, image = bg1, text = '')  # Create label to place background image.
        self._bglabel.place(relx=0.5, rely=0.5, anchor='center')

        self.__m_frame = ctk.CTkFrame(self, width=900, height=700)
        self.__m_frame.place(relx=0.5, rely=0.5, anchor='center')

        self.__s_frame = ctk.CTkFrame(self.__m_frame, width=675, height=380, border_width=5, corner_radius=15)
        self.__s_frame.place(relx=0.5, rely=0.55, anchor='center')

        # Defines the parameters list
        self._params = []

        self.__title_label = ctk.CTkLabel(self.__s_frame, text='-Singleplayer Options-', font=('Upheaval TT (BRK)', 35), text_color='#FFFFFF')
        self.__title_label.place(relx=0.5, rely=0.12, anchor='center')

        # The drop down menu.
        self.__combobox = ctk.CTkComboBox(self.__s_frame, width=400, height=50,
                                   state="readonly",
                                   values=['Depth First Search', 'Hunt-and-Kill', 'Sidewinder'], 
                                   font=('Upheaval TT (BRK)', 20), 
                                   dropdown_font=('Upheaval TT (BRK)', 20),
                                   command=self.__combobox_callback)
        self.__combobox.set('Select a generation algorithm')
        self.__combobox.place(relx=0.5, rely=0.31, anchor='center')

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
        
        When the start game button is pressed, in order to get the current slider value, we update the parameter list passed to the game object.
        
        """

        self._slider_value = ctk.DoubleVar()

        self.__slider_label = ctk.CTkLabel(self.__s_frame, text='> Grid size:', font=('Upheaval TT (BRK)', 30))
        self.__slider_label.place(relx=0.3, rely=0.51, anchor='center')

        self.__slider_value_label = ctk.CTkLabel(self.__s_frame, text=self.__format_value(self.__get_current_value()), text_color='#FFFFFF', font=('Upheaval TT (BRK)', 30))
        self.__slider_value_label.place(relx=0.55, rely=0.51, anchor='center')

        # Slider for maze size.
        self.__slider = ctk.CTkSlider(self.__s_frame, width=400, button_color='#FFFFFF', button_hover_color='#cccccc', variable=self._slider_value, command=self.__slider_changed)
        self.__slider.place(relx=0.5, rely=0.66, anchor='center')

        # Displays an error message on the GUI when nothing is selected in the drop down and the play button is pressed.
        self.__combobox_error_message = ctk.CTkLabel(self.__m_frame, text='', text_color='#e53935', font=('Upheaval TT (BRK)', 15))
        self.__combobox_error_message.grid(row=0, column=0, padx=(0,260), pady=(465, 0))
                
        self.__spGame_button = ctk.CTkButton(self.__s_frame, height=40, fg_color='#75a050', hover_color='#3d5329', text='START', text_color='#FFFFFF', font=('Upheaval TT (BRK)', 30), border_width=2, command=self.__spGame_button)
        self.__spGame_button.place(relx=0.5, rely=0.84, anchor='center')
        
        back_button = ctk.CTkButton(self.__m_frame, height=40, corner_radius=8, border_width=3, text_color='#FFFFFF', font=('Upheaval TT (BRK)', 25), text="< BACK", command=self.__back_button)
        back_button.grid(row=0, column=0, padx=(0,536), pady=(0,494))
    
    # Called for every interation with the drop down box.
    def __combobox_callback(self, choice):
        # Redefines the params list when a choice is made.
        # It gets the current slider value and the choice of the drop down box.
        self._params = [int(self.__get_current_value()), choice]

    # Returns current slider value.
    def __get_current_value(self):
        value = '{: .0f}'.format(self._slider_value.get()*25+5)
        return value
    
    # Formats the value to be displayed on the GUI
    def __format_value(self, value):
        return f'{value} x{value}'
    
    # Called every time the slider is changed - updates the label on the GUI.
    def __slider_changed(self, event):
        self.__slider_value_label.configure(text=self.__format_value(self.__get_current_value()))

    # Called when the play button is pressed.
    def __spGame_button(self):
        """
        If the parameters are selected:
        -Update the current slider value.
        -Call the function in the next page to start the maze generation.
        -Set the mode for algo file to be singleplayer to prevent checking overlap in move_p1() (pmode).
        -Show the singleplayer game page
        """
        if self.params != []:
            algo.play_start_sound()
            self._params[0] = int(self.__get_current_value())
            main.sg.spGameCanvas('new')
            algo.pmode = ''
            self._controller.pages['spGame'].show()
            # Reset error message.
            self.__combobox_error_message.configure(text='')
        else:
            algo.play_click_sound()
            self.__combobox_error_message.configure(text='error : no maze generation algorithm selected')

    def __back_button(self):
        algo.play_click_sound()
        self.__combobox_error_message.configure(text='')
        self._controller.pages['modeSelection'].show()

    # Getter of params
    @property
    def params(self):
        return self._params

# The Singleplayer Game page class - a child of the Page class.
class spGame(Page):  # Singleplayer game screen.
    def __init__(self, controller, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)  # Inherits the page class.

        self._controller = controller  # Controller for changing pages.
        self._imperfect = False  # Determines whether imperfect mazes are generated (settings).

        self._bglabel = ctk.CTkLabel(self, image = bg_game, text = '')  # Create label to place background image.
        self._bglabel.place(relx=0.5, rely=0.5, anchor='center')

        # Title.
        self.__title_frame = ctk.CTkFrame(self)
        self.__title_frame.place(relx=0.5, rely=0.1, anchor='center')
        self.__title = ctk.CTkLabel(self.__title_frame, text=" HEDGE ", text_color='#82925e', font=('Upheaval TT (BRK)', 50))
        self.__subheading = ctk.CTkLabel(self.__title_frame, text="SINGLEPLAYER ", text_color='#FFFFFF', font=('Upheaval TT (BRK)', 30, 'italic'))
        self.__title.pack()
        self.__subheading.pack()
        
        # Frame to contain GUI information on the left.
        self.__left_frame = ctk.CTkFrame(self, height=228, width=380)
        self.__left_frame.place(relx=0.15, rely=0.495, anchor='center')
        
        # Styling.
        self.__left_image = ctk.CTkImage(Image.open("assets/game_left.png"), size=(191, 227))
        self.__left_image_label = ctk.CTkLabel(self.__left_frame, text='', image=self.__left_image)
        self.__left_image_label.place(relx=0, rely=0.5, anchor='w')

        # Displayed info about algorithm and maze size on GUI.
        self.__algo_label = ctk.CTkLabel(self.__left_frame, text='', text_color='#FFFFFF', font=('Upheaval TT (BRK)', 35, 'italic'))
        self.__grid_label = ctk.CTkLabel(self.__left_frame, text='', text_color='#FFFFFF', font=('Upheaval TT (BRK)', 35, 'italic'))
        self.__algo_label.place(x=150, rely=0.11)
        self.__grid_label.place(x=150, rely=0.61)

        # Frame to contain GUI information on the right.
        self.__right_frame = ctk.CTkFrame(self, height=228, width=380)
        self.__right_frame.place(relx=0.85, rely=0.495, anchor='center')

        # Styling.
        self.__right_image = ctk.CTkImage(Image.open('assets/sg_right.png'), size=(233, 227))
        self.__right_image_label = ctk.CTkLabel(self.__right_frame, text='', image=self.__right_image)
        self.__right_image_label.place(x=380, rely=0.5, anchor='e')
    
        # Displays the steps made so far and the time elapsed.
        self.__step_label = ctk.CTkLabel(self.__right_frame, text='', text_color='#FFFFFF', font=('Upheaval TT (BRK)', 45, 'italic'))
        self.__time_label = ctk.CTkLabel(self.__right_frame, text='', text_color='#82925e', font=('Upheaval TT (BRK)', 50, 'italic'))
        self.__step_label.place(x=100, rely=0.145, anchor='w')
        self.__time_label.place(x=100, rely=0.645, anchor='w')

        # Progress bar - utilises the manhattan distance between the player's current position and the goal.
        self.__progress = ctk.CTkProgressBar(self, width=600, height=5, corner_radius=5, progress_color='#a1d0d1')
        self.__progress.set(0)
        self.__progress.place(relx=0.5, rely=0.9, anchor='center')

        # Back button.
        self.__back_button = ctk.CTkButton(self, height=40, corner_radius=8, border_width=3, text_color='#FFFFFF', font=('Upheaval TT (BRK)', 25), text="QUIT", command=self.__back_button)
        self.__back_button.place(relx=0.1, rely=0.1, anchor='center')
            
    def _createNewMaze(self):
        """
        Creates a maze using algo.py and the parameters passed from singleplayer options
        Only called when a new game is played.
        """
        self.__game_frame = ctk.CTkFrame(self, width=600, height=600)
        self.__game_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        # Displays the canvas created in the algo file.
        algo.create_canvas(self.__game_frame, canvas_colour)
        # Creates a graph object - this is the foundation of the maze.
        algo.graph = algo.Graph(main.so.params[0])

        self.__grid_label.configure(text=f'{main.so.params[0]} x {main.so.params[0]} ')
     
        # Generates a maze depending on the algorithm selected.
        if main.so.params[1] == 'Depth First Search':
            algo.graph.DFS()  # Calls DFS() on the graph object to generate a DFS maze.
            self.__algo_label.configure(text='DFS ')  # Configures the label on the GUI
        elif main.so.params[1] == 'Hunt-and-Kill':
            algo.graph.Hunt_and_Kill()  # Calls Hunt_and_Kill() on the graph object to generate a hunt and kill maze.
            self.__algo_label.configure(text='Hunt - Kill')  # Configures the label on the GUI
        elif main.so.params[1] == 'Sidewinder':
            algo.graph.Sidewinder()  # Calls Sidewinder() on the graph object to generate a sidewinder maze.
            self.__algo_label.configure(text='Sidewinder ')  # Configures the label on the GUI

        if self._imperfect:
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
        self._update = True
        # Starts the time.
        self._sp_time_start = time.time()

        # No player 2 in singleplayer.
        algo.p2 = None

        # Styling.
        self.__retry_label = ctk.CTkLabel(self.__title_frame, text='repeated', text_color='#ca4754', font=('Upheaval TT (BRK)', 15))
        self.__retry_label.pack()

        if mode == 'new':
            # When a new maze is generated.
            # Calls the createNewMaze() function
            self._createNewMaze()
            # Styling.
            self.__retry_label.pack_forget()
        elif mode == 'retry':
            # Removes the previous player sprite.
            algo.canvas_m.delete(algo.p1)
            # Styling.
            self.__retry_label.pack()

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
                self._update = False
                self._sp_time_end = time.time()  # Stops the time.
                main.r.results('single')  # Call results page so it can display the relevant information.
                self._controller.pages['Results'].show()  # Shows the result page.
                # Styling.
                self.__retry_label.pack_forget()

            # If not won yet, refresh the elements on the GUI.
            if self._update == True:
                # Update the progress bar.
                self.__progress.set(1-(algo.h('single')/(2*main.so.params[0])))  # h() is heuristic function.
                # Update the step label and the time label.
                self.__step_label.configure(text=f'{algo.get_moves("single")}  ')
                self.__time_label.configure(text=f'{round(time.time()-self.sp_time_start, 1)}  ')
                
                root.after(100, spUpdate)

        root.after(0, spUpdate)  # First run of the loop

    # Called when the back button is pressed.
    def __back_button(self):
        algo.play_click_sound()
        self._update = False
        self._controller.pages['spOptions'].show()
        # Styling.
        self.__retry_label.pack_forget()

    # Getter of 'sp_time_start'
    @property
    def sp_time_start(self):
        return self._sp_time_start
    
    # Getter of 'sp_time_end'
    @property
    def sp_time_end(self):
        return self._sp_time_end

# The Multiplayer Options page class - a child of the Page class.
class mpOptions(Page): # Screen to select generation style and grid size for multiplayer.
    def __init__(self, controller, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)  # Inherits the page class.
        self._controller = controller

        self._bglabel = ctk.CTkLabel(self, image = bg1, text = '')  # Create label to place background image.
        self._bglabel.place(relx=0.5, rely=0.5, anchor='center')

        self.__m_frame = ctk.CTkFrame(self, width=900, height=700)
        self.__m_frame.place(relx=0.5, rely=0.5, anchor='center')

        self.__s_frame = ctk.CTkFrame(self.__m_frame, width=675, height=380, border_width=5, corner_radius=15)
        self.__s_frame.place(relx=0.5, rely=0.55, anchor='center')

        # Defines the parameters list
        self._params = [None, None, None]

        self.__title_label = ctk.CTkLabel(self.__s_frame, text='-Multiplayer Options-', font=('Upheaval TT (BRK)', 35), text_color='#FFFFFF')
        self.__title_label.place(relx=0.5, rely=0.12, anchor='center')

        # The drop down menu.
        self.__combobox = ctk.CTkComboBox(self.__s_frame, width=400, height=50,
                                   state="readonly",
                                   values=['Depth First Search', 'Hunt-and-Kill', 'Sidewinder'], 
                                   font=('Upheaval TT (BRK)', 20), 
                                   dropdown_font=('Upheaval TT (BRK)', 20),
                                   command=self.__combobox_callback)
        self.__combobox.set('Select a generation algorithm')
        self.__combobox.place(relx=0.5, rely=0.31, anchor='center')

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
        
        When the start game button is pressed, in order to get the current slider value, we update the parameter list passed to the game object.
        
        """

        self._slider_value = ctk.DoubleVar()

        self.__slider_label = ctk.CTkLabel(self.__s_frame, text='> Grid size:', font=('Upheaval TT (BRK)', 30))
        self.__slider_label.place(relx=0.3, rely=0.51, anchor='center')

        self.__slider_value_label = ctk.CTkLabel(self.__s_frame, text=self.__format_value(self.__get_current_value()), text_color='#FFFFFF', font=('Upheaval TT (BRK)', 30))
        self.__slider_value_label.place(relx=0.55, rely=0.51, anchor='center')

        # Slider for maze size.
        self.__slider = ctk.CTkSlider(self.__s_frame, width=400, button_color='#FFFFFF', button_hover_color='#cccccc', variable=self._slider_value, command=self.__slider_changed)
        self.__slider.place(relx=0.5, rely=0.66, anchor='center')
        
        # Switch to change win condition.
        self._condition_switch_var = ctk.StringVar(value='speed')
        self.__condition_switch = ctk.CTkSwitch(self.__s_frame, text='', command=self.__condition_switch_event, variable=self._condition_switch_var, onvalue='steps', offvalue='speed', 
                                         switch_width=50, switch_height=27)
        self.__condition_switch.place(relx=0.34, rely=0.84, anchor='center')

        self.__condition_label_1 = ctk.CTkLabel(self.__s_frame, text='Fastest', font=('Upheaval TT (BRK)', 15))
        self.__condition_label_1.place(relx=0.2, rely=0.84, anchor='center')
        self.__condition_label_2 = ctk.CTkLabel(self.__s_frame, text='Least Steps', font=('Upheaval TT (BRK)', 15))
        self.__condition_label_2.place(relx=0.43, rely=0.84, anchor='center')

        # Displays an error message on the GUI when nothing is selected in the drop down and the play button is pressed.
        self.__combobox_error_message = ctk.CTkLabel(self.__m_frame, text='', text_color='#e53935', font=('Upheaval TT (BRK)', 15))
        self.__combobox_error_message.grid(row=0, column=0, padx=(0,260), pady=(465, 0))

        self.__mpGame_button = ctk.CTkButton(self.__s_frame, height=40, fg_color='#75a050', hover_color='#3d5329', text='START', text_color='#FFFFFF', font=('Upheaval TT (BRK)', 30), border_width=2, command=self.mpGame_button)
        self.__mpGame_button.place(relx=0.7, rely=0.84, anchor='center')
        
        self.__back_button = ctk.CTkButton(self.__m_frame, height=40, corner_radius=8, border_width=3, text_color='#FFFFFF', font=('Upheaval TT (BRK)', 25), text="< BACK", command=self.__back_button)
        self.__back_button.grid(row=0, column=0, padx=(0,536), pady=(0,494))

    # Called for every interation with the drop down box.
    def __combobox_callback(self, choice):
        # Redefines the params list when a choice is made.
        # It gets the current slider value, the choice of the drop down box, and the win condition.
        self._params = [int(self.__get_current_value()), choice, self._condition_switch_var.get()]

    # Returns current slider value.
    def __get_current_value(self):
        value = '{: .0f}'.format(self._slider_value.get()*25+5)
        return value
    
    # Formats the value to be displayed on the GUI
    def __format_value(self, value):
        return f'{value} x{value}'
    
    # Called every time the slider is changed - updates the label on the GUI.
    def __slider_changed(self, event):
        self.__slider_value_label.configure(text=self.__format_value(self.__get_current_value()))
    
    # Called every time the switch is changed.
    def __condition_switch_event(self):
        if self._condition_switch_var.get() == 'steps':
            self._params[2] = 'steps'
        else:
            self._params[2] = 'speed'

    # Called when the play button is pressed.
    def mpGame_button(self):
        """
        If the parameters are selected:
        -Update the current slider value.
        -Call the function in the next page to start the maze generation.
        -Set the mode for algo.py move_player functions in order for them to check for overlaps (pmode).
        -Show the multiplayer game page
        """
        if self._params != [None, None, None]: #if the parameters are selected
            algo.play_start_sound()
            self._params[0] = int(self.__get_current_value())
            main.mg.mpGameCanvas('new')
            algo.pmode = 'multi'
            self._controller.pages['mpGame'].show()
            # Reset error message.
            self.__combobox_error_message.configure(text='')
        else:
            algo.click_sound()
            self.__combobox_error_message.configure(text='error : no maze generation algorithm selected')
            
    def __back_button(self):
        algo.play_click_sound()
        self.__combobox_error_message.configure(text='')
        self._controller.pages['modeSelection'].show()
    
    # Getter of params
    @property
    def params(self):
        return self._params
        
# The Multiplayer Game page class - a child of the Page class.
class mpGame(Page):  # Multiplayer game screen.
    def __init__(self, controller, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)  # Inherits the page class.

        self._controller = controller  # Controller for changing pages.
        self._imperfect = False  # Determines whether imperfect mazes are generated (settings).

        self._bglabel = ctk.CTkLabel(self, image = bg_game, text = '')  # Create label to place background image.
        self._bglabel.place(relx=0.5, rely=0.5, anchor='center')

        # Title.
        self.__title_frame = ctk.CTkFrame(self)
        self.__title_frame.place(relx=0.5, rely=0.1, anchor='center')
        self.__title = ctk.CTkLabel(self.__title_frame, text=" HEDGE ", text_color='#82925e', font=('Upheaval TT (BRK)', 50))
        self.__subheading = ctk.CTkLabel(self.__title_frame, text="MULTIPLAYER ", text_color='#FFFFFF', font=('Upheaval TT (BRK)', 30, 'italic'))
        self.__title.pack()
        self.__subheading.pack()
        
        # Frame to contain GUI information on the left.
        self.__left_frame = ctk.CTkFrame(self, height=228, width=380)
        self.__left_frame.place(relx=0.15, rely=0.495, anchor='center')
        
        # Styling.
        self.__left_image = ctk.CTkImage(Image.open("assets/game_left.png"), size=(191, 227))
        self.__left_image_label = ctk.CTkLabel(self.__left_frame, text='', image=self.__left_image)
        self.__left_image_label.place(relx=0, rely=0.5, anchor='w')

        # Info about algorithm and maze size on GUI.
        self.__algo_label = ctk.CTkLabel(self.__left_frame, text='', text_color='#FFFFFF', font=('Upheaval TT (BRK)', 35, 'italic'))
        self.__grid_label = ctk.CTkLabel(self.__left_frame, text='', text_color='#FFFFFF', font=('Upheaval TT (BRK)', 35, 'italic'))
        self.__algo_label.place(x=150, rely=0.11)
        self.__grid_label.place(x=150, rely=0.61)

        # Frame to contain GUI information on the right.
        self.__right_frame = ctk.CTkFrame(self, height=330, width=380)
        self.__right_frame.place(relx=0.85, rely=0.495, anchor='center')

        # Styling.
        self.__right_image = ctk.CTkImage(Image.open('assets/mg_right.png'), size=(231, 329))
        self.__right_image_label = ctk.CTkLabel(self.__right_frame, text='', image=self.__right_image)
        self.__right_image_label.place(x=380, rely=0.5, anchor='e')

        # Displays the steps made so far and the time elapsed.
        self.__p1_step_label = ctk.CTkLabel(self.__right_frame, text='', text_color='#FFFFFF', font=('Upheaval TT (BRK)', 45, 'italic'))
        self.__p2_step_label = ctk.CTkLabel(self.__right_frame, text='', text_color='#FFFFFF', font=('Upheaval TT (BRK)', 45, 'italic'))
        self.__time_label = ctk.CTkLabel(self.__right_frame, text='', text_color='#82925e', font=('Upheaval TT (BRK)', 50, 'italic'))
        self.__p1_step_label.place(x=100, rely=0.145, anchor='w')
        self.__p2_step_label.place(x=100, rely=0.337, anchor='w')
        self.__time_label.place(x=100, rely=0.755, anchor='w')

        # Progress bars - utilises the manhattan distance between the players' current positions and the goal.
        self.__progress1 = ctk.CTkProgressBar(self, width=600, height=5, corner_radius=5, progress_color='#c77373')
        self.__progress1.set(0)
        self.__progress1.place(relx=0.5, rely=0.9, anchor='center')
        self.__progress2 = ctk.CTkProgressBar(self, width=600, height=5, corner_radius=5,  progress_color='#f4e59d')
        self.__progress2.set(0)
        self.__progress2.place(relx=0.5, rely=0.92, anchor='center')
        
        self.__back_button = ctk.CTkButton(self, height=40, corner_radius=8, border_width=3, text_color='#FFFFFF', font=('Upheaval TT (BRK)', 25), text="QUIT", command=self.__back_button)
        self.__back_button.place(relx=0.1, rely=0.1, anchor='center')

    def _createNewMaze(self):
        """
        Creates a maze using algo.py and the parameters passed from multiplayer options
        Only called when a new game is played.
        """
        self.__game_frame = ctk.CTkFrame(self, width=600, height=600)
        self.__game_frame.place(relx=0.5, rely=0.5, anchor='center')

        # Displays the canvas created in the algo file.
        algo.create_canvas(self.__game_frame, canvas_colour)
        # Creates a graph object - this is the foundation of the maze.
        algo.graph = algo.Graph(main.mo.params[0])

        self.__grid_label.configure(text=f'{main.mo.params[0]} x {main.mo.params[0]} ')

        # Generates a maze depending on the algorithm selected.
        if main.mo.params[1] == 'Depth First Search':
            algo.graph.DFS()  # Calls DFS() on the graph object to generate a DFS maze.
            self.__algo_label.configure(text='DFS ')  # Configures the label on the GUI
        elif main.mo.params[1] == 'Hunt-and-Kill':
            algo.graph.Hunt_and_Kill()  # Calls Hunt_and_Kill() on the graph object to generate a hunt and kill maze.
            self.__algo_label.configure(text='Hunt - Kill')  # Configures the label on the GUI
        elif main.mo.params[1] == 'Sidewinder':
            algo.graph.Sidewinder()  # Calls Sidewinder() on the graph object to generate a sidewinder maze.
            self.__algo_label.configure(text='Sidewinder ')  # Configures the label on the GUI

        if self._imperfect:
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
        self._update = True
        # Starts the time.
        self._mp_time_start = time.time()

        # Styling.
        self.__retry_label = ctk.CTkLabel(self.__title_frame, text='repeated', text_color='#ca4754', font=('Upheaval TT (BRK)', 15))
        self.__retry_label.pack()

        if mode == 'new':
            # When a new maze is generated.
            # Calls the createNewMaze() function
            self._createNewMaze()
            # Styling.
            self.__retry_label.pack_forget()
        elif mode == 'retry':
            # Removes the previous players' sprites.
            algo.canvas_m.delete(algo.p1)
            algo.canvas_m.delete(algo.p2)
            # Styling.
            self.__retry_label.pack()

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
            self._win_list = algo.detect_win('multi')
            # If a win is detected.
            if self._win_list[0]:
                self._update = False
                main.r.results('multi', self._win_list)  # Call results page so it can display the relevant information.
                self._controller.pages['Results'].show()  # Shows the result page.
                # Styling.
                self.__retry_label.pack_forget()
                # Reset the order_list.
                algo.order_list = []
            
            # If not won yet, refresh the elements on the GUI.
            if self._update == True:
                # Update the progress bars.
                self.__progress1.set(1-(algo.h('multi')[0]/(2*main.mo.params[0])))  # h() is heuristic function.
                self.__progress2.set(1-(algo.h('multi')[1]/(2*main.mo.params[0])))
                # Update the step labels and the time label.
                self.__p1_step_label.configure(text=f'{algo.get_moves("multi")[0]}  ')
                self.__p2_step_label.configure(text=f'{algo.get_moves("multi")[1]}  ')
                self.__time_label.configure(text=f'{round(time.time()-self.mp_time_start, 1)}  ')
                
                root.after(100, mpUpdate)

        root.after(0, mpUpdate) #first run of the loop

    # Called when the back button is pressed.
    def __back_button(self):
        self._update = False
        self._controller.pages['mpOptions'].show()
        # Styling.
        self.__retry_label.pack_forget()
        # Clears list of winners.
        algo.order_list = []
    
    # Getter of 'mp_time_start'
    @property
    def mp_time_start(self):
        return self._mp_time_start

# The Results page class - a child of the Page class.
class Results(Page):
    def __init__(self, controller, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self._controller = controller

        self._bglabel = ctk.CTkLabel(self, image = bg_res, text = '')  # Create label to place background image.
        self._bglabel.place(relx=0.5, rely=0.5, anchor='center')

    def __return_button(self): # Returns to the respective game option selection page when 'new game' button is pressed.
        algo.play_click_sound()
        if self._mode == 'single':
            self._controller.pages['spOptions'].show()
        if self._mode == 'multi':
            self._controller.pages['mpOptions'].show()

    def __retry_button(self): # Returns to the same maze for reattempt.
        algo.play_click_sound()
        if self._mode == 'single':
            main.sg.spGameCanvas('retry')  # Calls the function in the singleplayer game object in retry mode.
            self._controller.pages['spGame'].show()
        if self._mode == 'multi':
            main.mg.mpGameCanvas('retry')  # Calls the function in the multiplayer game object in retry mode.
            self._controller.pages['mpGame'].show()
    
    def __home_button(self):  # Returns to home - the main menu.
        algo.play_click_sound()
        self._controller.pages['mainMenu'].show()
    
    def results(self, mode, win_list=None):
        """
        Called when the game is finished - NOT at initialisation
        """
        self._mode = mode
        self._win_list = win_list
        
        self.__m_frame = ctk.CTkFrame(self, width=1280, height=650)
        self.__m_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        # Frame to display results on the left.
        self.__results_frame = ctk.CTkFrame(self.__m_frame, width=500, height=650)
        self.__results_frame.place(relx=0.2, rely=0.5, anchor='center')
        self._path2 = {} #path of solved solution
        
        # Displaying different information depending on the mode.
        if self._mode == 'single':
            # Size of maze.
            self._size = main.so.params[0]

            algo.play_win_sound()

            title = ctk.CTkLabel(self.__results_frame, text='GAME STATS:', text_color='#FFFFFF', font=('Upheaval TT (BRK)', 70))
            title.place(x=10, y=0)

            steps = ctk.CTkLabel(self.__results_frame, text=f'Steps Made: {algo.get_moves("single")}', font=('Upheaval TT (BRK)', 33))
            steps.place(x=10, y=190)

            # Calculates the time taken for the player to reach the end.
            time_taken = ctk.CTkLabel(self.__results_frame, text=f'Time Taken: {round(main.sg.sp_time_end - main.sg.sp_time_start, 1)} s', font=('Upheaval TT (BRK)', 33))
            time_taken.place(x=10, y=230)
        
        elif self._mode == 'multi':
            # Size of maze.
            self._size = main.mo.params[0]

            # Gets player1 and player2 times.
            self._p1_time_end = self._win_list[0][1] if self._win_list[0][0] == 'p1' else self._win_list[1][1]
            self._p2_time_end = self._win_list[1][1] if self._win_list[0][0] == 'p1' else self._win_list[0][1]

            # If comparing speed.
            if main.mo.params[2] == 'speed':
                if self._win_list[0][0] == 'p1':
                    self.__title_text = 'RED WINS!'
                    self.__text_color = '#c77373'
                else:
                    self.__title_text = 'YELLOW WINS!'
                    self.__text_color = '#f4e59d'
            else:  # Else if comparing least moves.
                self._moves = algo.get_moves("multi")
                if self._moves[0] < self._moves[1]:
                    algo.play_win_sound()
                    self.__title_text = 'RED WINS!'
                    self.__text_color = '#c77373'
                elif self._moves[0] > self._moves[1]:
                    algo.play_win_sound()
                    self.__title_text = 'YELLOW WINS!'
                    self.__text_color = '#f4e59d'
                else:  # In the event of a draw.
                    algo.play_win_sound('draw')
                    self.__title_text = 'DRAW!'
                    self.__text_color = '#FFFFFF'

            # Place various labels on the GUI.
            self.__title = ctk.CTkLabel(self.__results_frame, text=self.__title_text, text_color=self.__text_color, font=('Upheaval TT (BRK)', 70))
            self.__title.place(x=10, y=0)
                            
            self.__p1_label = ctk.CTkLabel(self.__results_frame, text=f'Player 1: RED', text_color='#c77373', font=('Upheaval TT (BRK)', 33))
            self.__p1_label.place(x=10, y=130)
            self.__p1_steps = ctk.CTkLabel(self.__results_frame, text=f'Steps: {algo.get_moves("multi")[0]}', font=('Upheaval TT (BRK)', 33))
            self.__p1_steps.place(x=50, y=160)
            self.__p1_time = ctk.CTkLabel(self.__results_frame, text=f'Time: {round(self._p1_time_end - main.mg.mp_time_start, 2)} s', font=('Upheaval TT (BRK)', 33))
            self.__p1_time.place(x=50, y=190)

            self.__p2_label = ctk.CTkLabel(self.__results_frame, text=f'Player 2: YELLOW', text_color='#f4e59d', font=('Upheaval TT (BRK)', 33))
            self.__p2_label.place(x=10, y=230)
            self.__p2_steps = ctk.CTkLabel(self.__results_frame, text=f'Steps: {algo.get_moves("multi")[1]}', font=('Upheaval TT (BRK)', 33))
            self.__p2_steps.place(x=50, y=260)
            self.__p2_time = ctk.CTkLabel(self.__results_frame, text=f'Time: {round(self._p2_time_end - main.mg.mp_time_start, 2)} s', font=('Upheaval TT (BRK)', 33))
            self.__p2_time.place(x=50, y=290)

        # Frame on the right - contains the solved maze when requested.
        self.__canvas_frame = ctk.CTkFrame(self.__m_frame, width=600, height = 600)
        algo.clone_canvas(algo.canvas_m, self.__canvas_frame, canvas_colour, line_colour)  # Clones the game canvas.
        # Styling.
        algo.cloned.tag_lower(algo.cloned.create_rectangle(600-algo.w, 600-algo.w, 600, 600, width = 0, fill='#005b27'))

        self.__button_frame = ctk.CTkFrame(self.__m_frame, width=600, height = 600, fg_color=('#96a672', '#16291d'))
        self.__button_frame.place(relx=0.7625, rely=0.5, anchor='center')


        # Reveal solution button.
        button = ctk.CTkButton(self.__button_frame, height=35, text='Reveal solution', font=('Upheaval TT (BRK)', 25), command=self.__show_canvas)
        button.place(x=300, y=300, anchor='center')

        return_button = ctk.CTkButton(self.__results_frame, corner_radius=8, border_width=3, height=60, width=200, fg_color=('#96a672','#2a4f38'), text='New Game', font=('Upheaval TT (BRK)', 35), command=self.__return_button)
        return_button.place(x=10, y=565)

        retry_button = ctk.CTkButton(self.__results_frame, corner_radius=8, border_width=3, height=60, width=100, text='REDO', font=('Upheaval TT (BRK)', 35), command=self.__retry_button)
        retry_button.place(x=245, y=565)

        home_button = ctk.CTkButton(self.__results_frame, corner_radius=8, border_width=3, height=60, width=100, text='HOME', font=('Upheaval TT (BRK)', 35), command=self.__home_button)
        home_button.place(x=380, y=565)

    # Called when the 'reveal solution' button is pressed.
    def _solve_maze(self):
        # Priority queue for A* algorithm.
        queue = PriorityQueue()
        # Get a gradient of colours for visualising searching.
        search_colours = algo.get_colour_gradient('#473d5a', '#005b27', 2*self._size-1)
        # Start node.
        start = 0
        self._path = {}

        g_score = [float('inf') for _ in range(algo.graph.num_nodes)]
        g_score[start] = 0
        f_score = [float('inf') for _ in range(algo.graph.num_nodes)]
        f_score[start] = algo.h('a*', start)

        queue.put((f_score[start], algo.h('a*', start), start))

        def astar_loop():
            if not queue.empty():
                cur_node = queue.get()[2]
                if cur_node+1 == self._size**2:
                    draw_path()
                    pass
                else:
                    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]#EWSN
                    for dy, dx in directions:
                        child_node = cur_node + dy * self._size + dx
                        p = True
                        if dx == 1 and (cur_node+1) % self._size == 0:
                            p = False
                        if dx == -1 and cur_node % self._size == 0:
                            p = False
                        if dy == 1 and (child_node+1) > self._size**2:
                            p = False
                        if dy == -1 and cur_node < self._size:    
                            p = False
                        if p == True:
                            if algo.graph.detect_wall(cur_node, child_node) == False:
                                temp_g_score = g_score[cur_node] + 1
                                temp_f_score = temp_g_score + algo.h('a*', child_node)
                                
                                # Draws the search cells.
                                index = algo.h('a*', child_node)
                                algo.cloned.tag_lower(algo.cloned.create_rectangle(0+child_node%self._size*algo.w, 
                                                                                   0+child_node//self._size*algo.w, 
                                                                                   child_node%self._size*algo.w + algo.w-0, 
                                                                                   child_node//self._size*algo.w + algo.w-0, 
                                                                                   tags='del', width = 0, 
                                                                                   fill=search_colours[index]))
                                
                                if temp_f_score < f_score[child_node]:
                                    g_score[child_node] = temp_g_score
                                    f_score[child_node] = temp_f_score
                                    queue.put((temp_f_score, algo.h('a*', child_node), child_node))
                                    self._path[child_node] = cur_node
                    root.after(1, astar_loop)
        root.after(0, astar_loop)

        # Draws the path of the shortest path.
        def draw_path():

            node = self._size**2 - 1
            while node != 0:
                self._path2[self._path[node]] = node
                node = self._path[node]
            path_colours = algo.get_colour_gradient('#473d5a', '#004f5a', len(self._path2))
            for index, node in enumerate(self._path2.keys()):
                algo.cloned.create_rectangle(0+node%self._size*algo.w, 0+node//self._size*algo.w, node%self._size*algo.w + algo.w -0, node//self._size*algo.w + algo.w-0, width=0, fill=path_colours[index])
            algo.cloned.delete(algo.cloned.gettags("del"))
            algo.draw_maze(algo.cloned, line_colour)
            self.__algo_steps = ctk.CTkLabel(self.__results_frame, text=f'Optimal Path: {len(self._path2)} Steps', text_color=('#608f90','#a1d0d1'), font=('Upheaval TT (BRK)', 33))
            
            # Displays more info when the solution is revealed - the difference between their solution and the optimal one.
            if self._mode == 'single':
                self.__algo_steps.place(x=10, y=300)
                self.__difference = ctk.CTkLabel(self.__results_frame, text=f'Difference: {algo.get_moves("single")-len(self._path2)} Steps', font=('Upheaval TT (BRK)', 33))
                self.__difference.place(x=10, y=340)                
            else:
                self.__algo_steps.place(x=10, y=350)
                self.__p1_diff = ctk.CTkLabel(self.__results_frame, text=f'Red Difference: {algo.get_moves("multi")[0]-len(self._path2)}', font=('Upheaval TT (BRK)', 33))
                self.__p1_diff.place(x=10, y=410)
                self.__p2_diff = ctk.CTkLabel(self.__results_frame, text=f'Yellow Difference: {algo.get_moves("multi")[1]-len(self._path2)}', font=('Upheaval TT (BRK)', 33))
                self.__p2_diff.place(x=10, y=440)

    # Called when the 'reveal solution' button is pressed.
    def __show_canvas(self):
        algo.play_click_sound()
        self.__button_frame.place_forget()
        self.__canvas_frame.place(relx=0.7625, rely=0.5, anchor='center')
        self._solve_maze()
        
class Window(ctk.CTkFrame): # Create main window.
    def __init__(self, *args, **kwargs):
        ctk.CTkFrame.__init__(self, *args, **kwargs)

        # Create a dictionary for all of the different selection pages.
        self.pages = {}
        for Subclass in (mainMenu, settings, modeSelection, spOptions, mpOptions, spGame, mpGame, Results):
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
            self.mm.bg2label.configure(image=ctk.CTkImage(Image.open('assets/bg2.png'), size=(900, 700)))
            self.mm.bglabel.configure(image=ctk.CTkImage(Image.open('assets/grad2bg.png'), size=(1920, 1080)))
            self.st.bglabel.configure(image=ctk.CTkImage(Image.open('assets/grad2set.png'), size=(1920, 1080)))
            self.ms.bglabel.configure(image=ctk.CTkImage(Image.open('assets/grad2bg.png'), size=(1920, 1080)))
            self.so.bglabel.configure(image=ctk.CTkImage(Image.open('assets/grad2bg.png'), size=(1920, 1080)))
            self.mo.bglabel.configure(image=ctk.CTkImage(Image.open('assets/grad2bg.png'), size=(1920, 1080)))
            self.sg.bglabel.configure(image=ctk.CTkImage(Image.open('assets/grad2game.png'), size=(1920, 1080)))
            self.mg.bglabel.configure(image=ctk.CTkImage(Image.open('assets/grad2game.png'), size=(1920, 1080)))
            self.r.bglabel.configure(image=ctk.CTkImage(Image.open('assets/grad2res.png'), size=(1920, 1080)))
        else:
            theme = 'light'
            canvas_colour = '#82925e'
            line_colour = '#FFFFFF'
            # Change all background images.
            self.mm.bg2label.configure(image=ctk.CTkImage(Image.open('assets/bg1.png'), size=(900, 700)))
            self.mm.bglabel.configure(image=ctk.CTkImage(Image.open('assets/grad1bg.png'), size=(1920, 1080)))
            self.st.bglabel.configure(image=ctk.CTkImage(Image.open('assets/grad1set.png'), size=(1920, 1080)))
            self.ms.bglabel.configure(image=ctk.CTkImage(Image.open('assets/grad1bg.png'), size=(1920, 1080)))
            self.so.bglabel.configure(image=ctk.CTkImage(Image.open('assets/grad1bg.png'), size=(1920, 1080)))
            self.mo.bglabel.configure(image=ctk.CTkImage(Image.open('assets/grad1bg.png'), size=(1920, 1080)))
            self.sg.bglabel.configure(image=ctk.CTkImage(Image.open('assets/grad1game.png'), size=(1920, 1080)))
            self.mg.bglabel.configure(image=ctk.CTkImage(Image.open('assets/grad1game.png'), size=(1920, 1080)))
            self.r.bglabel.configure(image=ctk.CTkImage(Image.open('assets/grad1res.png'), size=(1920, 1080)))
        # Change the theme of widgets.
        ctk.set_appearance_mode(theme)

if __name__ == "__main__":
    # Initialises the tkinter window.
    root = ctk.CTk()
    main = Window(root)
    algo.play_startup_sound()
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
        if root.attributes("-fullscreen"):
            root.attributes("-fullscreen", False)
        else:
            root.attributes("-fullscreen", True)
    root.bind("<F11>", toggle_fullscreen)

    # Game event loop.
    root.mainloop()