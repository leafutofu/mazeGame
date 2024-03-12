import customtkinter as ctk
import numpy as np
import random
import time
import pygame

pygame.mixer.init() #initialises the pygame mixer to play sounds

def play_click_sound():
    pygame.mixer.music.load("assets/click.mp3") #plays a clicking sound whenever called
    pygame.mixer.music.play(loops=0)

sound_allowed = True #determines whether to play the move sound whenever a player moves
def play_move_sound():
    if sound_allowed:
        pygame.mixer.music.load("assets/move.mp3") #plays a sound whenever called
        pygame.mixer.music.play(loops=0)

# NODES AND VERTICES ARE USED INTERCHANGEABLY (as they are the same in graph theory)
class Graph: #creates a graph object of size (n*n) where size = n
    def __init__(self, size):
        global w, adj_mat
        w = 600 / size #width of each cell is the width of the canvas (600 pixels) divided by the size (number of rows/columns)
        self.size = size #number of rows/columns
        self.num_nodes = self.size**2 #number of total nodes in the graph
        adj_mat = [[0 for column in range(self.num_nodes)] #adjacency matrix for the graph
                        for row in range(self.num_nodes)] #in this case, 0 means there is an edge between the two nodes and 1 means there isn't an edge between the two nodes
                                                          #this could be seen as counterintuitive, but it means that 1 implies there is a wall between two cells.
        
        #Removes the edges between all of the node (adding walls between nodes in a grid graph, ensuring that walls are added only within the boundaries of the grid and do not exceed them.)
        for node in range(self.num_nodes):
            if (node+1)%self.size != 0: #ensures node is not at the end of a row
                self.add_wall(node, node+1) #adds a wall between the current cell and the cell to the immediate right unless the cell is at the end of a row
            if node+self.size <= self.size**2 - 1: #ensures node is not on the bottom row
                self.add_wall(node, node+self.size) #adds a wall between the current cell and the cell immediately beneath it unless it is on the bottom row
    
    #Function to remove edges between two nodes (add walls between two cells node1 and node2)
    def add_wall(self, node1, node2):
        adj_mat[node1][node2] = 1
        adj_mat[node2][node1] = 1

    #Function to add edges between two nodes (remove walls between two cells node1 and node2)
    def remove_wall(self, node1, node2):
        adj_mat[node1][node2] = 0
        adj_mat[node2][node1] = 0

    #Function to detect if there is a wall between two cells (detect the absence of an edge between two nodes)
    def detect_wall(self, node1, node2):
        if adj_mat[node1][node2] == 1:
            return True
        elif adj_mat[node1][node2] == 0:
            return False
    """
    Maze Generation Algorithms:
        Depth First Search
        Hunt and Kill
        Sidewinder
        
    Explained in depth in report>technical solution

    """
    def DFS(self): #The Depth First Search maze generation algorithm
        while True:
            try:
                node_visited = [0 for i in range(self.num_nodes)]
                start_node = 0
                def unvisited_neighbours(cur_node):
                    lst = [] #list of neighbours
                    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]#rlbt
                    for dy, dx in directions:
                        try:
                            if self.detect_wall(cur_node, cur_node + dy * self.size + dx) == True:
                                if node_visited[cur_node + dy * self.size + dx] == 0:
                                    lst.append(cur_node + dy * self.size + dx)
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
                print('recursion error')
                self.__init__(self.size)
            
    def Hunt_and_Kill(self): #The Hunt-and-Kill maze generation algorithm
        node_visited = [0 for i in range(self.num_nodes)]
        cur_node = random.randrange(self.num_nodes)

        def walk(cur_node):
            node_visited[cur_node] = 1
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            random.shuffle(directions)
            node = -1
            for dy, dx in directions:
                try:
                    if self.detect_wall(cur_node, cur_node + dy * self.size + dx) and node_visited[cur_node + dy * self.size + dx] == 0:
                        node = cur_node + dy * self.size + dx
                        self.remove_wall(cur_node, cur_node + dy * self.size + dx)
                        break
                except IndexError:
                    pass
            return node
            
        def hunt():
            for cur_node in range(self.num_nodes):
                if node_visited[cur_node] == 0:
                    neighbours = []
                    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
                    for dy, dx in directions:
                        try:
                            check_node = cur_node + dy * self.size + dx
                            if node_visited[check_node] == 1 and self.detect_wall(cur_node, check_node):
                                neighbours.append((dy, dx))
                                pass
                        except IndexError:
                            pass
                    if neighbours:
                        dy, dx = random.choice(neighbours)
                        node_visited[cur_node] = 1
                        node = cur_node + dy * self.size + dx
                        self.remove_wall(cur_node, node)
                        return cur_node
            return -1
                            
        while True:
            cur_node = walk(cur_node)
            if cur_node == -1:
                cur_node = hunt()
            if cur_node == -1:
                break
                
    def Sidewinder(self): #The Sidewinder maze generation algorithm
        for row in range(self.size):
            run_start = 0
            for node in range(self.size):
                if row > 0 and (node+1 == self.size or random.randrange(2)):
                    #carve north
                    rand_node = run_start+random.randrange(node-run_start+1)
                    self.remove_wall(self.size*row+rand_node, self.size*(row-1)+rand_node)
                    run_start = node+1
                elif node+1 < self.size:
                    #carve east
                    self.remove_wall(self.size*row+node, self.size*row+node+1)

    def Imperfect(self): #A function to randomly remove walls in an already generated maze (activated in the settings page under 'generate imperfact maze')
        for node in range(self.num_nodes): #for each cell in the maze
            if (node+1) % self.size != 0: #if the cell is not at the last column
                if self.detect_wall(node, node+1) and random.randrange(self.size*2) == 1: #if there is a wall between the cell and the next cell to the right
                    self.remove_wall(node, node+1) #randomly remove a wall between these two cells with the probability of removal being 1 in half of the size of the maze
                                                   #i.e. if the maze was 6x6, the probability will be 1/12
            if node < (self.num_nodes-self.size): #same but to remove horizontal walls instead
                if self.detect_wall(node, node+self.size) and random.randrange(self.size*2) == 1:
                    self.remove_wall(node, node+self.size)

def create_canvas(frame, canvas_colour): #function to create the maze canvas and pass to the main program
    global canvas_m
    canvas_m = ctk.CTkCanvas(frame, width=600, height=600, bg=canvas_colour, highlightthickness=0)
    canvas_m.pack(anchor=ctk.CENTER, expand=True)

def clone_canvas(widget, frame, canvas_colour, line_colour): #function to clone the canvas after a game has been concluded in order for the solved maze to be visualised
    global cloned
    # get the config of the canvas
    cfg = {key: widget.cget(key) for key in widget.configure()}
    # create new canvas using the config
    cloned = ctk.CTkCanvas(frame, **cfg)
    cloned.configure(highlightthickness=3, bg=canvas_colour)
    draw_maze(cloned, line_colour)
    cloned.pack(anchor=ctk.CENTER, expand=True)

def draw_maze(canvas, line_colour): #function to draw the maze on the canvas according to the information in the adjacency matrix from the graph object
    cols = int(600 / w) #number of columns/rows
    linewidth = 2 #width of maze wall
    canvas.delete(canvas.gettags("line")) #delete all the walls that were already in the canvas
    for node in range(cols**2): #for each cell in the maze
        directions = [(0, 1, 'R'), (1, 0, 'B')] #set the direction of right and bottom
        for dy, dx, direction in directions:
            try:
                if adj_mat[node][node + dy * cols + dx] == 1: #for each direction, if the original cell and the cell in said direction are supposed to have a wall bewteen them
                    r = node // cols #row number of current cell
                    c = node % cols #column number of current cell
                    if direction == 'R': #if the wall is between two horizontally adjacent cells
                        #create a line/wall between these two cells
                        canvas.create_line((c+1)*w,
                                           r * w-(linewidth/2),
                                           (c+1)*w,
                                           (r+1)*w+(linewidth/2), width=linewidth, tags='line', fill=line_colour) 
                    elif direction == 'B': #if the wall is between two vertically adjacent cells
                        #create a line/wall bewteen these two cells
                        canvas.create_line(c * w-(linewidth/2),
                                           (r + 1) * w,
                                           (c + 1) * w+(linewidth/2),
                                           (r + 1) * w, width=linewidth, tags='line', fill=line_colour)
            except IndexError: #if we are looking for a cell that is outside the maze (either to the right or to the bottom)
                pass #ignore and continue
    if canvas == canvas_m: #if the canvas we are drawing the maze on is a canvas that will be played on
        # draw a white x where the end is
        canvas.create_text(int(w*(cols-0.5)), int(w*(cols-0.5)), font=('Upheaval TT (BRK)', int(300/cols)), 
                           text='X', fill='white')

def draw_player(mode): #function to draw the players onto the canvas/maze
    global p1, p2, po
    if mode == 'single': #if in singleplayer, draw only player 1
        p1 = canvas_m.create_rectangle(4, 4, w-4, w-4, fill='#a1d0d1', width=1, outline='white')
    if mode == 'multi': #if in multiplayer, draw player 1, player 2, 
                        #and po (which is a rectangle half the size of a player that will be placed on top of the players whenever they overlap)
        p1 = canvas_m.create_rectangle(4, 4, w-4, w-4, fill='#c77373', width=0, outline='white')
        p2 = canvas_m.create_rectangle(4, 4, w-4, w-4, fill='#f4e59d', width=0, outline='white')
        po = canvas_m.create_rectangle(4, 4, w/2, w-4, fill='#c77373', width=0, outline='white')

def h(mode, node=None): #heuristic
    cols = int(600 / w) #cols is the number of rows/columns, in this case it is used to denote the goal
    if mode == 'single': #for the singleplayer progress bar - calculates the manhattan distance between the player in the maze and the goal
        coords = node_player(p1, 'manhattan')
        return cols-coords[0] + cols-coords[1]
    if mode == 'multi': #for the multiplayer progress bars - "
        coord1 = node_player(p1, 'manhattan')
        coord2 = node_player(p2, 'manhattan')
        dist1 = cols-coord1[0] + cols-coord1[1]
        dist2 = cols-coord2[0] + cols-coord2[1]
        return [dist1, dist2]
    if mode == 'a*': #for the a* search algorithm, calculates the manhattan distance between a node and the goal
        x = node % cols + 1
        y = node // cols + 1
        return (cols-x) + (cols-y)

def hex_to_RGB(hex_str): #function to convert hex to rgb values
    return [int(hex_str[i:i+2], 16) for i in range(1,6,2)]

def get_colour_gradient(c1, c2, n): #function to generate a gradient in the form of a list of n colours that vary slightly between two input colours
    assert n > 1
    c1_rgb = np.array(hex_to_RGB(c1))/255
    c2_rgb = np.array(hex_to_RGB(c2))/255
    mix_pcts = [x/(n-1) for x in range(n)]
    rgb_colours = [((1-mix)*c1_rgb + (mix*c2_rgb)) for mix in mix_pcts]
    return ["#" + "".join([format(int(round(val*255)), "02x") for val in item]) for item in rgb_colours]


def node_player(player, mode=None): #returns the node the player is on given coordinates of top left corner of player on canvas
    cols = int(600 / w) #number of columns in the maze
    coords = canvas_m.bbox(player) #finds the coordinates of the player's bounding box (tkinter specific)
    x = coords[0] - 2 #adjusting coords
    y = coords[1] - 2

    node_x = int(x/w) #the x position of the node
    node_y = int(y/w) #the y position of the node

    if mode == 'manhattan': #returns the x and y position for the progress bars
        return [node_x+1, node_y+1]
    else:
        return node_y * cols + node_x #returns the node the player is on

def future_pos(player, direction): #returns whether the future position of a move is viable (see move_p1 and move_p2 functions)
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

order_list = [] #list to record which player finishes the fastest

def detect_win(mode): #function to detect whether players have reached the goal node - is run every time the game updates to check
    global p1allowed, p2allowed #variables to control whether you can move your player in multiplayer - if you have already reached the goal, you should not be able to move your player
    cols = int(600 / w)
    p1coords = canvas_m.bbox(p1) #bounding box of player 1 or the player in singleplayer
    if mode == 'single': #if detecting from a singleplayer game
        if p1coords[0] == p1coords[1] and (cols-1)*w + 2 <= p1coords[0] <= (cols-1)*w + 4: #if the player is in the location of the goal
            return True
    elif mode == 'multi': #if detecting from a multiplayer game
        p2coords = canvas_m.bbox(p2) #bounding box of player 2 in multiplayer
        if p1coords[0] == p1coords[1] and (cols-1)*w + 2 <= p1coords[0] <= (cols-1)*w + 4 and p1allowed: #if player 1 finishes
            order_list.append(['p1', time.time()]) #appends player 1's time to the order_list
            p1allowed = False #disallows movement of the player until player 2 also reaches the goal
        if p2coords[0] == p2coords[1] and (cols-1)*w + 2 <= p2coords[0] <= (cols-1)*w + 4 and p2allowed: #if player 2 finishes
            order_list.append(['p2', time.time()]) #appeds player 2's time to the order_list
            p2allowed = False #disallows movement of the player until player 1 also reaches the goal
        if len(order_list) == 2: #if the order_list is filled i.e both players have finished
            p1allowed, p2allowed = True, True #allows movement for potential next round
            canvas_m.moveto(po, -100, -100) #moves the 'overlap' off the canvas
            return order_list #returns the order_list to the results page
        return [False]
    
def get_moves(mode): #function to get moves of players
    if mode == 'single':
        return p1moves
    else:
        return [p1moves, p2moves]

def check_overlap(): #function to check if the players in multiplayer are overlapping and if so moves the 'overlap' on top to represent overlapping
    if node_player(p1) == node_player(p2): #if player 1 is on the same node as player 2
        canvas_m.moveto(po, canvas_m.bbox(p1)[0], canvas_m.bbox(p1)[1]) #move the 'overlap' to that position
        canvas_m.tag_raise(po) #raise it to the top so it is visible
    else:
        canvas_m.moveto(po, -100, -100) #move it off the canvas if they are no longer overlapping

p1allowed = True #allows player 1 movement
p2allowed = True #allows player 2 movement
pmode = '' #variable that stores the mode of the current game i.e. whether it is singleplayer or multiplayer
def move_p1(event): #function to move player 1 - called after keypress of W, A, S, or D
    global p1moves
    while p1allowed:
        try:
            cols = int(600 / w)
            node = node_player(p1)
            if event.keysym.lower() == 'w' and adj_mat[node][node-cols] == 0: #if the keypress is W
                pos = future_pos(p1, 'N') #check if the position after moving a certain direction is valid - in this case direction = north
                if pos > 0: #if it is valid
                    play_move_sound()
                    canvas_m.move(p1, 0, -w) #move the player
                    p1moves += 1 #increment move counter
            #similar for rest of function
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
                except IndexError: #handles index errors where player is on the right or bottom edge and attempts to move off
                    break
            # overlap display
            if p2 == None:
                pass
            if pmode == 'multi':
                check_overlap()
            break
        except NameError: #if there is no player created yet, do nothing
            break

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
            # overlap display
            check_overlap()
            break
        except NameError: #if there is no player created yet, do nothing
            break

ret_start_allowed = False #activated in the settings page under 'allow return to start'
def return_start(event): #a function that allows players to return to node 0 by pressing a key - togglable
    while ret_start_allowed:
        try:
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