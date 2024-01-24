import customtkinter as ctk
import dog2

root = ctk.CTk()
root.configure(fg_color='green')
root.geometry("900x1000") #window size
root.title('Hedge') #window title
root.iconbitmap('assets/icon.ico') #window icon
#root.wm_resizable(False, False) #makes window a fixed size

canvas = dog2.draw_canvas(root)
dog2.make_rect()

frame = ctk.CTkFrame(root, fg_color='blue')
frame.pack()

def clone_widget(widget, master=None):
    """
    Create a cloned version o a widget

    Parameters
    ----------
    widget : tkinter widget
        tkinter widget that shall be cloned.
    master : tkinter widget, optional
        Master widget onto which cloned widget shall be placed. If None, same master of input widget will be used. The
        default is None.

    Returns
    -------
    cloned : tkinter widget
        Clone of input widget onto master widget.

    """
    # Get main info
    parent = master if master else widget.master
    cls = widget.__class__

    # Clone the widget configuration
    cfg = {key: widget.cget(key) for key in widget.configure()}
    cloned = cls(parent, **cfg)

    # Clone the widget's children
    for child in widget.winfo_children():
        child_cloned = clone_widget(child, master=cloned)
        if child.grid_info():
            grid_info = {k: v for k, v in child.grid_info().items() if k not in {'in'}}
            child_cloned.grid(**grid_info)
        elif child.place_info():
            place_info = {k: v for k, v in child.place_info().items() if k not in {'in'}}
            child_cloned.place(**place_info)
        else:
            pack_info = {k: v for k, v in child.pack_info().items() if k not in {'in'}}
            child_cloned.pack(**pack_info)

    return cloned

cloned_canvas = clone_widget(dog2.dog_canvas, frame)
cloned_canvas.pack()

dog2.dog_canvas.destroy()


root.mainloop()



