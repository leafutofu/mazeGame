import customtkinter as ctk
import numpy as np
import random
import time
import pygame

pygame.mixer.init()

def play_click_sound():
    pygame.mixer.music.load("assets/click.mp3")
    pygame.mixer.music.play(loops=0)

sound_allowed = True
def play_move_sound():
    if sound_allowed:
        pygame.mixer.music.load("assets/move.mp3")
        pygame.mixer.music.play(loops=0)


class Graph:
    def __init__(self, size):
        global w, adj_mat
        w = 600 / size
        self.size = size
        self.num_nodes = self.size**2
        adj_mat = [[0 for column in range(self.num_nodes)]
                        for row in range(self.num_nodes)]
        for node in range(self.num_nodes):
            if (node+1 <= (self.size**2) - 1) and ((node+1)%self.size != 0):
                self.add_wall(node, node+1)
            if node-1 >= 0 and node%self.size != 0:
                self.add_wall(node, node-1)
            if node+self.size <= self.size**2 - 1:
                self.add_wall(node, node+self.size)
            if node-self.size >= 0:
                self.add_wall(node, node-self.size)
    
    def add_wall(self, node1, node2):
        adj_mat[node1][node2] = 1
        adj_mat[node2][node1] = 1

    def remove_wall(self, node1, node2):
        adj_mat[node1][node2] = 0
        adj_mat[node2][node1] = 0

    def detect_wall(self, node1, node2):
        if adj_mat[node1][node2] == 1:
            return True
        elif adj_mat[node1][node2] == 0:
            return False
        
    def DFS(self):
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
            
    def Hunt_and_Kill(self):
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
                
    def Sidewinder(self):
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

    def Imperfect(self):
        print('gen imperfect')
        for node in range(self.num_nodes):
            if (node+1) % self.size != 0:
                if self.detect_wall(node, node+1) and random.randrange(self.size) == 1:
                    self.remove_wall(node, node+1)
            if node < (self.num_nodes-self.size):
                if self.detect_wall(node, node+self.size) and random.randrange(self.size//3) == 1:
                    self.remove_wall(node, node+self.size)

def create_canvas(frame, canvas_colour):
    global canvas_m
    canvas_m = ctk.CTkCanvas(frame, width=600, height=600, bg=canvas_colour, highlightthickness=0)
    canvas_m.pack(anchor=ctk.CENTER, expand=True)

def clone_canvas(widget, frame, canvas_colour, line_colour):
    global cloned
    # get the config of the canvas
    cfg = {key: widget.cget(key) for key in widget.configure()}
    # create new canvas using the config
    cloned = ctk.CTkCanvas(frame, **cfg)
    cloned.configure(highlightthickness=3, bg=canvas_colour)
    draw_maze(cloned, line_colour)
    cloned.pack(anchor=ctk.CENTER, expand=True)

def draw_maze(canvas, line_colour):
    cols = int(600 / w)
    linewidth = 2
    canvas.delete(canvas.gettags("line"))
    for node in range(cols**2):
        directions = [(0, 1, 'R'), (1, 0, 'B')]
        for dy, dx, direction in directions:
            try:
                if adj_mat[node][node + dy * cols + dx] == 1:
                    r = node // cols #row number of current node
                    c = node % cols #column number of current node
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
            except IndexError:
                pass
    if canvas == canvas_m:
        canvas.create_text(int(w*(cols-0.5)), int(w*(cols-0.5)), font=('Upheaval TT (BRK)', int(300/cols)), text='X', fill='white')

def draw_player(mode):
    global p1, p2, po
    if mode == 'single':
        p1 = canvas_m.create_rectangle(4, 4, w-4, w-4, fill='#a1d0d1', width=1, outline='white')
        #6f3e4a purple
        #4a6f3e green
        #a1d0d1 light blue  
    if mode == 'multi':
        p1 = canvas_m.create_rectangle(4, 4, w-4, w-4, fill='#c77373', width=0, outline='white')
        p2 = canvas_m.create_rectangle(4, 4, w-4, w-4, fill='#f4e59d', width=0, outline='white')
        po = canvas_m.create_rectangle(4, 4, w/2, w-4, fill='#c77373', width=0, outline='white')

def h(node=None): #heuristic
    cols = int(600 / w)
    x = node % cols + 1
    y = node // cols + 1
    return (cols-x) + (cols-y)

def hex_to_RGB(hex_str):
    return [int(hex_str[i:i+2], 16) for i in range(1,6,2)]

def get_colour_gradient(c1, c2, n):
    assert n > 1
    c1_rgb = np.array(hex_to_RGB(c1))/255
    c2_rgb = np.array(hex_to_RGB(c2))/255
    mix_pcts = [x/(n-1) for x in range(n)]
    rgb_colours = [((1-mix)*c1_rgb + (mix*c2_rgb)) for mix in mix_pcts]
    return ["#" + "".join([format(int(round(val*255)), "02x") for val in item]) for item in rgb_colours]


def node_player(player): #returns the node the player is on given coordinates of top left corner of player on canvas
    cols = int(600 / w)
    coords = canvas_m.bbox(player)
    x = coords[0] - 2
    y = coords[1] - 2

    node_x = int(x/w)
    node_y = int(y/w)
    print(f'node_player returning: {node_y * cols + node_x}')
    return node_y * cols + node_x

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

order_list = []

def detect_win(mode):
    global p1allowed, p2allowed
    cols = int(600 / w)
    p1coords = canvas_m.bbox(p1) #bounding box of players 
    if mode == 'single':
        if p1coords[0] == p1coords[1] and (cols-1)*w + 2 <= p1coords[0] <= (cols-1)*w + 4:
            return True
    elif mode == 'multi':
        p2coords = canvas_m.bbox(p2)
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
    
def get_moves(mode):
    return p1moves if mode == 'single' else [p1moves, p2moves]

def check_overlap():
    if node_player(p1) == node_player(p2):
        canvas_m.moveto(po, canvas_m.bbox(p1)[0], canvas_m.bbox(p1)[1])
        canvas_m.tag_raise(po)
    else:
        canvas_m.moveto(po, -100, -100)

p1allowed = True
p2allowed = True
pmode = ''
def move_p1(event):
    global p1moves
    while p1allowed:
        try:
            cols = int(600 / w)
            node = node_player(p1)
            if event.keysym.lower() == 'w' and adj_mat[node][node-cols] == 0:
                pos = future_pos(p1, 'N')
                if pos > 0:
                    play_move_sound()
                    canvas_m.move(p1, 0, -w)
                    p1moves += 1
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
                except IndexError:
                    break
            # overlap display
            if p2 == None:
                pass
            if pmode == 'multi':
                check_overlap()
            break
        except NameError:
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
        except NameError:
            break

ret_start_allowed = False
def return_start(event):
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