import customtkinter as ctk

def draw_canvas(frame):
    global dog_canvas
    dog_canvas = ctk.CTkCanvas(frame, width=500, height=500)
    dog_canvas.pack()

def make_rect():
    dog_canvas.create_rectangle(0,0,100,100,fill='red')