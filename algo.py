import customtkinter as ctk
import random

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
                self.add_edge(node, node+1)
            if node-1 >= 0 and node%self.size != 0:
                self.add_edge(node, node-1)
            if node+self.size <= self.size**2 - 1:
                self.add_edge(node, node+self.size)
            if node-self.size >= 0:
                self.add_edge(node, node-self.size)
     
    def add_edge(self, node1, node2):
        adj_mat[node1][node2] = 1
        adj_mat[node2][node1] = 1

    def remove_edge(self, node1, node2):
        adj_mat[node1][node2] = 0
        adj_mat[node2][node1] = 0

    def detect_edge(self, node1, node2):
        if adj_mat[node1][node2] == 1:
            return True
        else:
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
                            if self.detect_edge(cur_node, cur_node + dy * self.size + dx) == True:
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
                        self.remove_edge(cur_node, next_node)
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
                    if self.detect_edge(cur_node, cur_node + dy * self.size + dx) and node_visited[cur_node + dy * self.size + dx] == 0:
                        node = cur_node + dy * self.size + dx
                        self.remove_edge(cur_node, cur_node + dy * self.size + dx)
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
                            if node_visited[check_node] == 1 and self.detect_edge(cur_node, check_node):
                                neighbours.append((dy, dx))
                                pass
                        except IndexError:
                            pass
                    if neighbours:
                        dy, dx = random.choice(neighbours)
                        node_visited[cur_node] = 1
                        node = cur_node + dy * self.size + dx
                        self.remove_edge(cur_node, node)
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
                    self.remove_edge(self.size*row+rand_node, self.size*(row-1)+rand_node)
                    run_start = node+1
                elif node+1 < self.size:
                    #carve east
                    self.remove_edge(self.size*row+node, self.size*row+node+1)

def create_canvas(frame):
    global canvas
    canvas = ctk.CTkCanvas(frame, width=600, height=600, bg='#FFFFFF')
    canvas.pack(anchor=ctk.CENTER, expand=True)

def draw_maze():
    cols = int(600 / w)
    linewidth = 3
    line_colour = '#44612d'
    canvas.delete("all")
    for node in range(cols**2):
        directions = [(0, 1, 'R'), (0, -1, 'L'), (1, 0, 'B'), (-1, 0, 'T')]
        for dy, dx, direction in directions:
            try:
                if adj_mat[node][node + dy * cols + dx] == 1:
                    r = node // cols #row number of current node
                    c = node % cols #column number of current node
                    if direction == 'R':
                        canvas.create_line((c+1)*w, (r)*w, (c+1)*w, (r+1)*w, width=linewidth, fill=line_colour)
                    elif direction == 'L':
                        canvas.create_line(c * w, r * w, c * w, (r + 1) * w, width=linewidth, fill=line_colour)
                    elif direction == 'B':
                        canvas.create_line(c * w, (r + 1) * w, (c + 1) * w, (r + 1) * w, width=linewidth, fill=line_colour)
                    elif direction == 'T':
                        canvas.create_line(c * w, r * w, (c + 1) * w, r * w, width=linewidth, fill=line_colour)
            except IndexError:
                pass
    canvas.create_rectangle((cols-1)*w+4, (cols-1)*w+4, cols*w-4, cols*w-4, fill='green')

def draw_player(mode):
    global p1, p2
    if mode == 'single':
        p1 = canvas.create_rectangle(4, 4, w-4, w-4, fill='red')
    if mode == 'multi':
        p1 = canvas.create_rectangle(4, 4, w-4, w-4, fill='red')
        p2 = canvas.create_rectangle(4, 4, w-4, w-4, fill='blue')

def node_player(player): #returns the node the player is on given coordinates of top left corner of player on canvas
    cols = int(600 / w)
    coords = canvas.bbox(player)
    x = coords[0] - 2
    y = coords[1] - 2

    node_x = int(x/w)
    node_y = int(y/w)

    return node_y * cols + node_x

def future_pos(player, direction):
    coords = canvas.bbox(player)
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
    cols = int(600 / w)
    p1coords = canvas.bbox(p1) #bounding box of players 
    print(p1coords)
    if mode == 'single':
        if p1coords[0] == p1coords[1] and (cols-1)*w + 2 <= p1coords[0] <= (cols-1)*w + 4:
            return True
    elif mode == 'multi':
        p2coords = canvas.bbox(p2)
        order_list = []
        if p1coords[0] == p1coords[1] and (cols-1)*w + 2 <= p1coords[0] <= (cols-1)*w + 4:
            order_list.append('p1')
        if p2coords[0] == p2coords[1] and (cols-1)*w + 2 <= p2coords[0] <= (cols-1)*w + 4:
            order_list.append('p2')
        if len(order_list) == 2:
            return order_list
        return False

def get_moves(mode):
    return p1moves if mode == 'single' else [p1moves, p2moves]

def move_p1(event):
    global p1moves
    while True:
        try:
            cols = int(600 / w)
            node = node_player(p1)
            if event.keysym == 'w' and adj_mat[node][node-cols] == 0:
                pos = future_pos(p1, 'N')
                if pos > 0:
                    canvas.move(p1, 0, -w)
                    p1moves += 1
            if event.keysym == 'a' and adj_mat[node][node-1] == 0:
                pos = future_pos(p1, 'W')
                if pos > 0:
                    canvas.move(p1, -w, 0)
                    p1moves += 1
            if event.keysym == 's' and adj_mat[node][node+cols] == 0:
                pos = future_pos(p1, 'S')
                if pos < 600:
                    canvas.move(p1, 0, w)
                    p1moves += 1
            if event.keysym == 'd' and adj_mat[node][node+1] == 0:
                pos = future_pos(p1, 'E')
                if pos < 600:
                    canvas.move(p1, w, 0)
                    p1moves += 1
            break
        except NameError:
            break

def move_p2(event): 
    global p2moves
    while True:
        try:
            cols = int(600 / w)
            node = node_player(p2)
            if event.keysym == 'Up' and adj_mat[node][node-cols] == 0:
                pos = future_pos(p2, 'N')
                if pos > 0:
                    canvas.move(p2, 0, -w)
                    p2moves += 1
            if event.keysym == 'Left' and adj_mat[node][node-1] == 0:
                pos = future_pos(p2, 'W')
                if pos > 0:
                    canvas.move(p2, -w, 0)
                    p2moves += 1
            if event.keysym == 'Down' and adj_mat[node][node+cols] == 0:
                pos = future_pos(p2, 'S')
                if pos < 600:
                    canvas.move(p2, 0, w)
                    p2moves += 1
            if event.keysym == 'Right' and adj_mat[node][node+1] == 0:
                pos = future_pos(p2, 'E')
                if pos < 600:
                    canvas.move(p2, w, 0)
                    p2moves += 1
            break
        except NameError:
            break