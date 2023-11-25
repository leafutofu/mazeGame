import customtkinter as ctk
from algo import *
    
root = ctk.CTk()
root.wm_geometry("600x600") #window size
root.wm_title('Hedge') #window title
root.wm_iconbitmap('assets/icon.ico') #window icon

frame1 = ctk.CTkFrame(root, width=600, height=600) 
frame1.pack()

create_canvas(frame1)
draw_maze(graph)
draw_player('multi')

root.bind('<w>', move_p1)
root.bind('<a>', move_p1)
root.bind('<s>', move_p1)
root.bind('<d>', move_p1)

root.bind('<Up>', move_p2)
root.bind('<Left>', move_p2)
root.bind('<Down>', move_p2)
root.bind('<Right>', move_p2)

root.mainloop()

