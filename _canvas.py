import customtkinter as ctk
from random import choice, random

root = ctk.CTk()
root.geometry('900x900')
root.title('Canvas Demo')

WIDTH, HEIGHT = 900, 900
cols = rows = 10
tile = WIDTH // cols

canvas = ctk.CTkCanvas(root, width=WIDTH+1, height=HEIGHT+1, bg='white')
canvas.pack(anchor=ctk.CENTER, expand=True)

class Graph:
    def __init__(self, num_nodes):
        self.m_graph = [[1 for column in range(num_nodes)]
                        for row in range(num_nodes)]
        for i in range(num_nodes):
            self.m_graph[i][i] = 0
    def remove_edge(self, node1, node2):
        self.m_graph[node1][node2] = 0
        self.m_graph[node2][node1] = 0

    def binary_tree(self):
        pass
    
graph1 = Graph(cols)




root.mainloop()
