import customtkinter as ctk
import random
can_width, can_height = 600, 600
cols = 30
w = can_width / cols
counter = 0
class Graph:
    def __init__(self, size):
        self.size = size
        self.num_nodes = self.size**2
        self.adj_mat = [[0 for column in range(self.num_nodes)]
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
        #for i in range(self.num_nodes):
        #    print(self.adj_mat[i])        
    def add_edge(self, node1, node2):
        self.adj_mat[node1][node2] = 1
        self.adj_mat[node2][node1] = 1
    def remove_edge(self, node1, node2):
        self.adj_mat[node1][node2] = 0
        self.adj_mat[node2][node1] = 0
    def detect_edge(self, node1, node2):
        if self.adj_mat[node1][node2] == 1:
            return True
        else:
            return False
        
    def DFS(self):
        while True:
            try:
                node_visited = [0 for i in range(self.num_nodes)]
                start_node = 0
                def rand_unvisited_neighbour(cur_node):
                    lst = []
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
                    node_list = rand_unvisited_neighbour(cur_node)
                    next_node = random.choice(node_list)
                    while node_list[0] != -1:
                        next_node = random.choice(node_list)
                        self.remove_edge(cur_node, next_node)
                        randDFS(next_node)
                        node_list = rand_unvisited_neighbour(cur_node)
                randDFS(start_node)
                break
            except RecursionError:
                global counter
                counter += 1
                print('recursion error: retrying')
                self.__init__(cols)

    def Hunt_and_Kill(self):
        pass
    def Sidewinder(self):
        pass

def create_canvas(frame):
    global canvas
    canvas = ctk.CTkCanvas(frame, width=can_width, height=can_height, bg='white')
    canvas.pack(anchor=ctk.CENTER, expand=True)

def draw_maze(graph):
    canvas.delete("all")
    for node in range(cols**2):
        directions = [(0, 1, 'R'), (0, -1, 'L'), (1, 0, 'B'), (-1, 0, 'T')]
        for dy, dx, direction in directions:
            try:
                if graph.adj_mat[node][node + dy * cols + dx] == 1:
                    r = node // cols #row number of current node
                    c = node % cols #column number of current node
                    if direction == 'R':
                        canvas.create_line((c+1)*w, (r)*w, (c+1)*w, (r+1)*w)
                    elif direction == 'L':
                        canvas.create_line(c * w, r * w, c * w, (r + 1) * w)
                    elif direction == 'B':
                        canvas.create_line(c * w, (r + 1) * w, (c + 1) * w, (r + 1) * w)
                    elif direction == 'T':
                        canvas.create_line(c * w, r * w, (c + 1) * w, r * w)
            except IndexError:
                pass
            


graph1 = Graph(cols)
graph1.DFS()
print(f'generated after {counter+1} attempt(s)')
