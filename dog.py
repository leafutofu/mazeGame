import customtkinter as ctk
import algo

root = ctk.CTk()
root.geometry('900x900')

canvas = ctk.CTkCanvas(root, width=900, height=100)
canvas.place(relx=0.5, rely=0.5, anchor='center')

colours = ['#473d5a', '#463d5a', '#463d5a', '#453e5a', '#443e5a', '#433e5a', '#433e5a', '#423e5a', '#413e5a', '#413f5a', '#403f5a', '#3f3f5a', '#3e3f5a', '#3e3f5a', '#3d405a', '#3c405a', '#3c405a', '#3b405a', 
'#3a405a', '#39405a', '#39415a', '#38415a', '#37415a', '#37415a', '#36415a', '#35425a', '#34425a', '#34425a', '#33425a', '#32425a', '#31425a', '#31435a', '#30435a', '#2f435a', '#2f435a', '#2e435a', '#2d445a', '#2c445a', '#2c445a', '#2b445a', '#2a445a', '#2a445a', '#29455a', '#28455a', '#27455a', '#27455a', '#26455a', '#25465a', '#25465a', '#24465a', '#23465a', '#22465a', '#22465a', '#21475a', '#20475a', '#20475a', '#1f475a', '#1e475a', '#1d485a', '#1d485a', '#1c485a', '#1b485a', '#1b485a', '#1a485a', '#19495a', '#18495a', '#18495a', '#17495a', '#16495a', '#164a5a', '#154a5a', '#144a5a', '#134a5a', '#134a5a', '#124a5a', '#114b5a', '#104b5a', '#104b5a', '#0f4b5a', '#0e4b5a', '#0e4c5a', '#0d4c5a', '#0c4c5a', '#0b4c5a', '#0b4c5a', '#0a4c5a', '#094d5a', '#094d5a', '#084d5a', '#074d5a', '#064d5a', '#064e5a', '#054e5a', '#044e5a', '#044e5a', '#034e5a', '#024e5a', '#014f5a', '#014f5a', '#004f5a']
print(colours)
for index, colour in enumerate(colours):
    print(index, colour)
    canvas.create_rectangle(index*9, 0, (index+1)*9, 100, width=0, fill=colour)


root.mainloop()
