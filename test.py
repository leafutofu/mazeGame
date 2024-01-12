import customtkinter as ctk
if __name__ == "__main__":
    #initialises the tkinter window
    root = ctk.CTk()
    root.configure(fg_color='green')
    root.geometry("900x1000") #window size
    root.title('Hedge') #window title
    root.iconbitmap('assets/icon.ico') #window icon
    #root.wm_resizable(False, False) #makes window a fixed size
    
    root.mainloop()
