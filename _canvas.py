import customtkinter as ctk

root = ctk.CTk()
root.geometry('900x700')
root.title('Canvas Demo')

canvas = ctk.CTkCanvas(root, width=600, height=600, bg='white')
canvas.pack(anchor=ctk.CENTER, expand=True)
canvas.create_line(100 ,200 ,100 ,0 ,fill="green" , width=2)

root.mainloop()

