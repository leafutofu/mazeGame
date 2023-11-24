import customtkinter as ctk
from algo import *

root = ctk.CTk()
root.wm_geometry("900x700") #window size
root.wm_title('Hedge') #window title
root.wm_iconbitmap('assets/icon.ico') #window icon

frame1 = ctk.CTkFrame(root, width=600, height=600) 
frame1.pack()

create_canvas(frame1)
draw_maze(graph1)
graph1.remove_edge(0, 1)
draw_maze(graph1)
root.mainloop()

