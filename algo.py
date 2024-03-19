import customtkinter as ctk
import numpy as np
import random
import time
from pygame import mixer

mixer.init()  # Initialises the pygame mixer to play sounds.

def play_click_sound():
    # Plays a clicking sound whenever called.
    mixer.music.load("assets/click.mp3") 
    mixer.music.play(loops=0)

def play_win_sound(case=None):
    # Plays a sound when the game ends
    if case == 'draw':
        mixer.music.load("assets/draw.mp3") 
        mixer.music.play(loops=0)
    else:
        mixer.music.load("assets/win.mp3") 
        mixer.music.play(loops=0)

def play_start_sound():
    # Plays a sound whenever the user starts a game.
    mixer.music.load("assets/start.mp3") 
    mixer.music.play(loops=0)

def play_startup_sound():
    # Plays a sound on startup
    mixer.music.load("assets/startup.mp3") 
    mixer.music.play(loops=0)

# Determines whether to play the move sound whenever a player moves.
sound_allowed = True
def play_move_sound():
    if sound_allowed:
        # Plays a sound whenever called.
        mixer.music.load("assets/move.mp3")
        mixer.music.play(loops=0)

def play_jump_sound():
    if sound_allowed:
        # Plays a sound whenever the player returns to the start using 'q' or '/'
        mixer.music.load("assets/jump.mp3") 
        mixer.music.play(loops=0)

# NODES AND VERTICES ARE USED INTERCHANGEABLY (as they are the same in graph theory)

# Creates a graph object of size (n*n) where size = n.
class Graph:
    def __init__(self, size):
        global w, adj_mat
        # Width of each cell is the width of the canvas (600 pixels) divided by the size (number of rows/columns).
        w = 600 / size
        # Number of rows/columns.
        self.__size = size
        # Number of total nodes in the graph.
        self.__num_nodes = self.__size**2
        """
        The adjacency matrix for the graph.
        In this case, 0 means there is an edge between the two nodes and 1 means there isn't an edge between the two nodes.
        This may seem counterintuitive, but it means that 1 implies there is a wall between two cells.
        """
        adj_mat = [[0 for column in range(self.__num_nodes)]
                        for row in range(self.__num_nodes)] 
        
        # Removes the edges between all of the node (adding walls between nodes in a grid graph, ensuring that walls are added only within the boundaries of the grid and do not exceed them).
        for node in range(self.__num_nodes):
            # Ensures node is not at the end of a row.
            if (node+1)%self.__size != 0: 
                # Adds a wall between the current cell and the cell to the immediate right unless the cell is at the end of a row.
                self.add_wall(node, node+1)
            # Ensures node is not on the bottom row.
            if node+self.__size <= self.__size**2 - 1:
                # Adds a wall between the current cell and the cell immediately beneath it unless it is on the bottom row.
                self.add_wall(node, node+self.__size)
    
    # Function to remove edges between two nodes (add walls between two cells node1 and node2).
    def add_wall(self, node1, node2):
        adj_mat[node1][node2] = 1
        adj_mat[node2][node1] = 1

    # Function to add edges between two nodes (remove walls between two cells node1 and node2).
    def remove_wall(self, node1, node2):
        adj_mat[node1][node2] = 0
        adj_mat[node2][node1] = 0

    # Function to detect if there is a wall between two cells (detect the absence of an edge between two nodes).
    def detect_wall(self, node1, node2):
        if adj_mat[node1][node2] == 1:
            return True
        elif adj_mat[node1][node2] == 0:
            return False
    """
    Maze Generation Algorithms:
        - Depth First Search
        - Hunt and Kill
        - Sidewinder

    """
    def DFS(self):  # The Depth First Search maze generation algorithm.
        while True:
            try:
                node_visited = [0 for i in range(self.__num_nodes)]
                start_node = 0

                def unvisited_neighbours(cur_node):
                    lst = []  # List of neighbours
                    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]#rlbt
                    for dy, dx in directions:
                        try:
                            if self.detect_wall(cur_node, cur_node + dy * self.__size + dx) == True:
                                if node_visited[cur_node + dy * self.__size + dx] == 0:
                                    lst.append(cur_node + dy * self.__size + dx)
                        except IndexError:
                            pass
                    return lst if lst else [-1]
                
                def randDFS(cur_node):
                    node_visited[cur_node] = 1
                    node_list = unvisited_neighbours(cur_node)
                    next_node = random.choice(node_list)
                    while node_list[0] != -1:
                        next_node = random.choice(node_list)
                        self.remove_wall(cur_node, next_node)
                        randDFS(next_node)
                        node_list = unvisited_neighbours(cur_node)
            
                randDFS(start_node)

                break

            except RecursionError:
                print('Recursion error handled: regenerating maze')
                self.__init__(self.__size)
            
    def Hunt_and_Kill(self):
        node_visited = [0 for i in range(self.__num_nodes)]
        cur_node = random.randrange(self.__num_nodes)

        def walk(cur_node):
            node_visited[cur_node] = 1
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            random.shuffle(directions)
            node = -1
            for dy, dx in directions:
                try:
                    if self.detect_wall(cur_node, cur_node + dy * self.__size + dx) and node_visited[cur_node + dy * self.__size + dx] == 0:
                        node = cur_node + dy * self.__size + dx
                        self.remove_wall(cur_node, cur_node + dy * self.__size + dx)
                        break
                except IndexError:
                    pass
            return node
            
        def hunt():
            for cur_node in range(self.__num_nodes):
                if node_visited[cur_node] == 0:
                    neighbours = []
                    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
                    for dy, dx in directions:
                        try:
                            check_node = cur_node + dy * self.__size + dx
                            if node_visited[check_node] == 1 and self.detect_wall(cur_node, check_node):
                                neighbours.append((dy, dx))
                                pass
                        except IndexError:
                            pass
                    if neighbours:
                        dy, dx = random.choice(neighbours)
                        node_visited[cur_node] = 1
                        node = cur_node + dy * self.__size + dx
                        self.remove_wall(cur_node, node)
                        return cur_node
            return -1
                            
        while True:
            cur_node = walk(cur_node)
            if cur_node == -1:
                cur_node = hunt()
            if cur_node == -1:
                break
                
    def Sidewinder(self):  # The Sidewinder maze generation algorithm.
        for row in range(self.__size):
            run_start = 0
            for node in range(self.__size):
                if row > 0 and (node+1 == self.__size or random.randrange(2) == 0):
                    # Carve north.
                    rand_node = run_start+random.randrange(node-run_start+1)
                    self.remove_wall(self.__size*row+rand_node, self.__size*(row-1)+rand_node)
                    run_start = node+1
                elif node+1 < self.__size:
                    # Carve east.
                    self.remove_wall(self.__size*row+node, self.__size*row+node+1)

    # A function to randomly remove walls in an already generated maze (activated in the settings page under 'generate imperfact maze').
    def Imperfect(self):
        """
        For each cell in the maze, if the cell is not at the last column and there is a wall between the cell and its neighbours towards the right
        randomly decide if that wall should be removed, with the probability of removal being 1/(2*number of columns or rows)
            i.e. if the maze was 6x6, the probability will be 1/12
        
        If the cell is not at the last row and there is a wall between the cell and its neighbour below it
        randomly decide to remove wall between these two cells
        """
        for node in range(self.__num_nodes):
            if (node+1) % self.__size != 0:
                if self.detect_wall(node, node+1) and random.randrange(self.__size*2) == 1: 
                    self.remove_wall(node, node+1)
            if node < (self.__num_nodes-self.__size):
                if self.detect_wall(node, node+self.__size) and random.randrange(self.__size*2) == 1:
                    self.remove_wall(node, node+self.__size)

    @property
    def num_nodes(self):
        return self.__num_nodes

# Function to create the maze canvas and pass it to the main program
def create_canvas(frame, canvas_colour):
    global canvas_m
    canvas_m = ctk.CTkCanvas(frame, width=600, height=600, bg=canvas_colour, highlightthickness=0)
    canvas_m.pack(anchor=ctk.CENTER, expand=True)

# Function to clone the canvas after a game has been concluded in order for the solved maze to be visualised.
def clone_canvas(widget, frame, canvas_colour, line_colour):
    global cloned
    # get the config of the canvas
    cfg = {key: widget.cget(key) for key in widget.configure()}
    # create new canvas using the config
    cloned = ctk.CTkCanvas(frame, **cfg)
    cloned.configure(highlightthickness=3, bg=canvas_colour)
    draw_maze(cloned, line_colour)
    cloned.pack(anchor=ctk.CENTER, expand=True)

# Function to draw the maze on the canvas according to the information in the adjacency matrix from the graph object.
def draw_maze(canvas, line_colour):
    # Number of columns/rows.
    cols = int(600 / w)
    # Width of maze wall.
    linewidth = 2
    # Delete all the walls that were already in the canvas.
    canvas.delete(canvas.gettags("line"))
    # For each cell in the maze.
    for node in range(cols**2):
        directions = [(0, 1, 'R'), (1, 0, 'B')]
        # Consider the directions towards the right and bottom.
        for dy, dx, direction in directions:
            try:
                """
                For each direction, if the original cell and the cell in said direction are supposed to have a wall bewteen them:
                    If the wall is between two horizontally adjacent cells -
                    draw a line/wall between these two cells.
                
                    If the wall is between two vertically adjacent cells - 
                    draw a line/wall bewteen these two cells.
                """
                if adj_mat[node][node + dy * cols + dx] == 1:
                    r = node // cols # Row number of current cell.
                    c = node % cols # Column number of current cell.
                    if direction == 'R':
                        canvas.create_line((c+1)*w,
                                           r * w-(linewidth/2),
                                           (c+1)*w,
                                           (r+1)*w+(linewidth/2), width=linewidth, tags='line', fill=line_colour) 
                    elif direction == 'B':
                        canvas.create_line(c * w-(linewidth/2),
                                           (r + 1) * w,
                                           (c + 1) * w+(linewidth/2),
                                           (r + 1) * w, width=linewidth, tags='line', fill=line_colour)
            # Pass if we are looking for a cell that is outside the maze (either to the right or to the bottom).
            except IndexError:
                pass
    # If the canvas we are drawing the maze on is a canvas that will be played on.
    if canvas == canvas_m:
        # Draw a white x where the end is.
        canvas.create_text(int(w*(cols-0.5)), int(w*(cols-0.5)), font=('Upheaval TT (BRK)', int(300/cols)), 
                           text='X', fill='white')

# Function to draw the players onto the canvas/maze.
def draw_player(mode):
    global p1, p2, po
    # If in singleplayer, draw only player 1.
    if mode == 'single':
        p1 = canvas_m.create_rectangle(4, 4, w-4, w-4, fill='#a1d0d1', width=1, outline='white')
    # If in multiplayer, draw player 1, player 2, and po (which is a rectangle half the size of a player that will be placed on top of the players whenever they overlap).
    if mode == 'multi':
        p1 = canvas_m.create_rectangle(4, 4, w-4, w-4, fill='#c77373', width=0, outline='white')
        p2 = canvas_m.create_rectangle(4, 4, w-4, w-4, fill='#f4e59d', width=0, outline='white')
        po = canvas_m.create_rectangle(4, 4, w/2, w-4, fill='#c77373', width=0, outline='white')

# Heuristic function (manhattan distance).
def h(mode, node=None):
    # Cols is the number of rows/columns, in this case it is used to denote the goal.
    cols = int(600 / w)
    # For the singleplayer progress bar - calculates the manhattan distance between the player in the maze and the goal.
    if mode == 'single':
        coords = node_player(p1, 'manhattan')
        return cols-coords[0] + cols-coords[1]
    # For the multiplayer progress bars - calculates the manhattan distance between each player in the maze and the goal.
    if mode == 'multi':
        coord1 = node_player(p1, 'manhattan')
        coord2 = node_player(p2, 'manhattan')
        dist1 = cols-coord1[0] + cols-coord1[1]
        dist2 = cols-coord2[0] + cols-coord2[1]
        return [dist1, dist2]
    # For the a* search algorithm, calculates the manhattan distance between a node and the goal.
    if mode == 'a*':
        x = node % cols + 1
        y = node // cols + 1
        return (cols-x) + (cols-y)

# Function to convert hex to rgb values - purely for aesthetics
def hex_to_RGB(hex_str):
    return [int(hex_str[i:i+2], 16) for i in range(1,6,2)]

# Function to generate a gradient in the form of a list of n colours that vary slightly between two input colours - purely for aesthetics
def get_colour_gradient(c1, c2, n):
    assert n > 1
    c1_rgb = np.array(hex_to_RGB(c1))/255
    c2_rgb = np.array(hex_to_RGB(c2))/255
    mix_pcts = [x/(n-1) for x in range(n)]
    rgb_colours = [((1-mix)*c1_rgb + (mix*c2_rgb)) for mix in mix_pcts]
    return ["#" + "".join([format(int(round(val*255)), "02x") for val in item]) for item in rgb_colours]

# Returns the node the player is on given coordinates of top left corner of player on canvas.
def node_player(player, mode=None):
    # Number of columns in the maze.
    cols = int(600 / w)
    # Finds the coordinates of the player's bounding box (tkinter specific).
    coords = canvas_m.bbox(player)
    x = coords[0] - 2  # Adjusting coordinates.
    y = coords[1] - 2

    node_x = int(x/w)  # The x position of the node.
    node_y = int(y/w)  # The y position of the node.

    # Returns the x and y position for the progress bars (called by the heuristic function when calculating distance for progress bars).
    if mode == 'manhattan':
        return [node_x+1, node_y+1]
    else:
        # Returns the node the player is on.
        return node_y * cols + node_x

# Returns whether the future position of a move is viable (see move_p1 and move_p2 functions).
def future_pos(player, direction):
    coords = canvas_m.bbox(player)
    x = coords[0] - 2
    y = coords[1] - 2

    if direction == 'N':
        return y-w
    if direction == 'W':
        return x-w
    if direction == 'S':
        return y+w
    if direction == 'E':
        return x+w

# List to record which player finishes the fastest.
order_list = []

# Function to detect whether players have reached the goal node - is run every time the game updates to check.
def detect_win(mode): 
    # Variables to control whether you can move your player in multiplayer - if you have already reached the goal, you should not be able to move your player.
    global p1allowed, p2allowed

    cols = int(600 / w)
    # Bounding box of player 1 or the player in singleplayer.
    p1coords = canvas_m.bbox(p1)
    # If detecting from a singleplayer game - if the player is in the location of the goal return True.
    if mode == 'single':
        if p1coords[0] == p1coords[1] and (cols-1)*w + 2 <= p1coords[0] <= (cols-1)*w + 4:
            return True
    """
    If detecting from a multiplayer game:
        If player 1 finishes, append player 1's time to the order_list and disallow player 1 movement.
        If player 2 finishes, append player 2's time to the order_list and disallow player 2 movement.
        If the order_list is filled i.e. both players have finished, allow movement for potential next round, removes overlap and returns the order_list to the results page.
    """
    if mode == 'multi':
        p2coords = canvas_m.bbox(p2)  # Bounding box of player 2 in multiplayer.
        if p1coords[0] == p1coords[1] and (cols-1)*w + 2 <= p1coords[0] <= (cols-1)*w + 4 and p1allowed:
            order_list.append(['p1', time.time()])
            p1allowed = False
        if p2coords[0] == p2coords[1] and (cols-1)*w + 2 <= p2coords[0] <= (cols-1)*w + 4 and p2allowed:
            order_list.append(['p2', time.time()])
            p2allowed = False
        if len(order_list) == 2:
            p1allowed, p2allowed = True, True
            canvas_m.moveto(po, -100, -100)
            return order_list
        return [False]
    
# Function to get moves of players.
def get_moves(mode):
    if mode == 'single':
        return p1moves
    else:
        return [p1moves, p2moves]

# Function to check if the players in multiplayer are overlapping and if so moves the 'overlap' on top to represent overlapping.
def check_overlap():
    # If player 1 is on the same node as player 2.
    # Move the 'overlap' to that position and raise it to the top so it is visible else move it off the canvas if they are no longer overlapping.
    if node_player(p1) == node_player(p2):
        canvas_m.moveto(po, canvas_m.bbox(p1)[0], canvas_m.bbox(p1)[1])
        canvas_m.tag_raise(po)
    else:
        canvas_m.moveto(po, -100, -100)

p1allowed = True # Allows player 1 movement.
p2allowed = True # Allows player 2 movement.
pmode = '' # Variable that stores the mode of the current game i.e. whether it is singleplayer or multiplayer.

# Function to move player 1 - called after keypresses of W, A, S, or D.
def move_p1(event):
    global p1moves
    while p1allowed:
        try:
            cols = int(600 / w)
            node = node_player(p1)
            if event.keysym.lower() == 'w' and adj_mat[node][node-cols] == 0:  # If the keypress is W.
                pos = future_pos(p1, 'N')  # Check if the position after moving a certain direction is valid - in this case direction = north.
                if pos > 0:  # If it is valid.
                    play_move_sound()
                    canvas_m.move(p1, 0, -w)  # Move the player.
                    p1moves += 1  # Increment move counter.
            # Similar for rest of function.
            if event.keysym.lower() == 'a' and adj_mat[node][node-1] == 0:
                pos = future_pos(p1, 'W')
                if pos > 0:
                    play_move_sound()
                    canvas_m.move(p1, -w, 0)
                    p1moves += 1
            while True:
                try:
                    if event.keysym.lower() == 's' and adj_mat[node][node+cols] == 0:
                        pos = future_pos(p1, 'S')
                        if pos < 600:
                            play_move_sound()
                            canvas_m.move(p1, 0, w)
                            p1moves += 1
                    if event.keysym.lower() == 'd' and adj_mat[node][node+1] == 0:
                        pos = future_pos(p1, 'E')
                        if pos < 600:
                            play_move_sound()
                            canvas_m.move(p1, w, 0)
                            p1moves += 1
                    break
                except IndexError:  # Handles index errors where player is on the right or bottom edge and attempts to move off.
                    break
            # Overlap display.
            if p2 == None:
                pass
            if pmode == 'multi':
                check_overlap()
            break
        except NameError:  # If there is no player created yet, do nothing.
            break

# Function to move player 2 - called after keypresses of up, down, left, and right.
def move_p2(event): 
    global p2moves
    while p2allowed and pmode=='multi':
        try:
            cols = int(600 / w)
            node = node_player(p2)
            if event.keysym == 'Up' and adj_mat[node][node-cols] == 0:
                pos = future_pos(p2, 'N')
                if pos > 0:
                    play_move_sound()
                    canvas_m.move(p2, 0, -w)
                    p2moves += 1
            if event.keysym == 'Left' and adj_mat[node][node-1] == 0:
                pos = future_pos(p2, 'W')
                if pos > 0:
                    play_move_sound()
                    canvas_m.move(p2, -w, 0)
                    p2moves += 1
            while True:
                try:
                    if event.keysym == 'Down' and adj_mat[node][node+cols] == 0:
                        pos = future_pos(p2, 'S')
                        if pos < 600:
                            play_move_sound()
                            canvas_m.move(p2, 0, w)
                            p2moves += 1
                    if event.keysym == 'Right' and adj_mat[node][node+1] == 0:
                        pos = future_pos(p2, 'E')
                        if pos < 600:
                            play_move_sound()
                            canvas_m.move(p2, w, 0)
                            p2moves += 1
                    break
                except IndexError:
                    break
            # Overlap display.
            check_overlap()
            break
        except NameError:  # If there is no player created yet, do nothing.
            break

ret_start_allowed = False  # Activated in the settings page under 'allow return to start'.

# A function that allows players to return to node 0 by pressing a key - togglable.
def return_start(event):
    while ret_start_allowed:
        try:
            play_jump_sound()
            if event.keysym.lower() == 'q':
                canvas_m.moveto(p1, 3, 3)
                if pmode == 'multi':
                    canvas_m.moveto(po, -100, -100)
                    check_overlap()
            if event.keysym == 'slash':
                canvas_m.moveto(p2, 3, 3)
                canvas_m.moveto(po, -100, -100)
                check_overlap()
            break
        except NameError:
            break