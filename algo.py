import customtkinter as ctk
import random
import time

path = {}
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
                print('recursion error: retrying')
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


def create_canvas(frame):
    global canvas_m
    canvas_m = ctk.CTkCanvas(frame, width=600, height=600, bg='#0c1f13', highlightthickness=2)
    canvas_m.pack(anchor=ctk.CENTER, expand=True)

def clone_canvas(widget, frame):
    global cloned
    # get the config of the canvas
    cfg = {key: widget.cget(key) for key in widget.configure()}
    # create new canvas using the config
    cloned = ctk.CTkCanvas(frame, **cfg)
    #cloned.configure(highlightthickness=0)
    draw_maze(cloned)
    cloned.pack(anchor=ctk.CENTER, expand=True)

def draw_maze(canvas):
    cols = int(600 / w)
    linewidth = 2
    line_colour = '#afbf8b'
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

def h(mode, node=None): #heuristic
    cols = int(600 / w)
    if mode == 'single':
        coords = node_player(p1, 'manhattan')
        return cols-coords[0] + cols-coords[1]
    if mode == 'multi':
        coord1 = node_player(p1, 'manhattan')
        coord2 = node_player(p2, 'manhattan')
        dist1 = cols-coord1[0] + cols-coord1[1]
        dist2 = cols-coord2[0] + cols-coord2[1]
        return [dist1, dist2]
    if mode == 'a*':
        x = node % cols + 1
        y = node // cols + 1
        return (cols-x) + (cols-y)

def node_player(player, mode): #returns the node the player is on given coordinates of top left corner of player on canvas
    cols = int(600 / w)
    coords = canvas_m.bbox(player)
    x = coords[0] - 2
    y = coords[1] - 2

    node_x = int(x/w)
    node_y = int(y/w)

    if mode == 'manhattan':
        return [node_x+1, node_y+1]
    else:
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

def detect_win(mode):
    global p1allowed, p2allowed
    cols = int(600 / w)
    p1coords = canvas_m.bbox(p1) #bounding box of players 
    if mode == 'single':
        if p1coords[0] == p1coords[1] and (cols-1)*w + 2 <= p1coords[0] <= (cols-1)*w + 4:
            return True
    elif mode == 'multi':
        p2coords = canvas_m.bbox(p2)
        order_list = []
        if p1coords[0] == p1coords[1] and (cols-1)*w + 2 <= p1coords[0] <= (cols-1)*w + 4:
            order_list.append('p1')
            p1_time_end = time.time()
            p1allowed = False
        if p2coords[0] == p2coords[1] and (cols-1)*w + 2 <= p2coords[0] <= (cols-1)*w + 4:
            order_list.append('p2')
            p2_time_end = time.time()
            p2allowed = False
        if len(order_list) == 2:
            p1allowed, p2allowed = True, True
            return [order_list, p1_time_end, p2_time_end]
        return [False]
    
def draw_solution():
    pass

def get_moves(mode):
    return p1moves if mode == 'single' else [p1moves, p2moves]

p1allowed = True
p2allowed = True
def move_p1(event):
    global p1moves
    while p1allowed == True:
        try:
            cols = int(600 / w)
            node = node_player(p1, -1)
            if event.keysym.lower() == 'w' and adj_mat[node][node-cols] == 0:
                pos = future_pos(p1, 'N')
                if pos > 0:
                    canvas_m.move(p1, 0, -w)
                    p1moves += 1
            if event.keysym.lower() == 'a' and adj_mat[node][node-1] == 0:
                pos = future_pos(p1, 'W')
                if pos > 0:
                    canvas_m.move(p1, -w, 0)
                    p1moves += 1
            while True:
                try:
                    if event.keysym.lower() == 's' and adj_mat[node][node+cols] == 0:
                        pos = future_pos(p1, 'S')
                        if pos < 600:
                            canvas_m.move(p1, 0, w)
                            p1moves += 1
                    if event.keysym.lower() == 'd' and adj_mat[node][node+1] == 0:
                        pos = future_pos(p1, 'E')
                        if pos < 600:
                            canvas_m.move(p1, w, 0)
                            p1moves += 1
                    break
                except IndexError:
                    break
            #squashie
            if p2 == None:
                pass
            elif node_player(p1, -1) == node_player(p2, -1):
                canvas_m.moveto(po, canvas_m.bbox(p1)[0], canvas_m.bbox(p1)[1])
                canvas_m.tag_raise(po)
            else:
                canvas_m.moveto(po, -100, -100)
            break
        except NameError:
            break

def move_p2(event): 
    global p2moves
    while p2allowed == True:
        try:
            cols = int(600 / w)
            node = node_player(p2, -1)
            if event.keysym == 'Up' and adj_mat[node][node-cols] == 0:
                pos = future_pos(p2, 'N')
                if pos > 0:
                    canvas_m.move(p2, 0, -w)
                    p2moves += 1
            if event.keysym == 'Left' and adj_mat[node][node-1] == 0:
                pos = future_pos(p2, 'W')
                if pos > 0:
                    canvas_m.move(p2, -w, 0)
                    p2moves += 1
            while True:
                try:
                    if event.keysym == 'Down' and adj_mat[node][node+cols] == 0:
                        pos = future_pos(p2, 'S')
                        if pos < 600:
                            canvas_m.move(p2, 0, w)
                            p2moves += 1
                    if event.keysym == 'Right' and adj_mat[node][node+1] == 0:
                        pos = future_pos(p2, 'E')
                        if pos < 600:
                            canvas_m.move(p2, w, 0)
                            p2moves += 1
                    break
                except IndexError:
                    break
            # squashie
            if node_player(p1, -1) == node_player(p2, -1):
                canvas_m.moveto(po, canvas_m.bbox(p1)[0], canvas_m.bbox(p1)[1])
                canvas_m.tag_raise(po)
            else:
                canvas_m.moveto(po, -100, -100)
            break
        except NameError:
            break