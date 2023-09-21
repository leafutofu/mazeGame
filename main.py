import pygame, settings
pygame.init()

window_width = settings.WIDTH #define window width
window_height = settings.HEIGHT #define window height
bg_colour = settings.BGCOLOUR #define background colour
window = pygame.display.set_mode((window_width, window_height)) #create window

game_state = 'start_menu' #set default state on launch to start menu

def draw_start_menu(): #function to draw start menu
    window.fill(bg_colour) #fill with default colour
    font = pygame.font.SysFont('arial', 40) #define font
    title = font.render('HEDGE', True, (255, 255, 255)) #render text
    window.blit(title, (window_width/2 - title.get_width()/2, window_height/2 - title.get_height()/2)) #positioning text
    pygame.display.update() #update display

run = True 
while run: #game loop

    #quit
    for event in pygame.event.get(): 
       if event.type == pygame.QUIT:
           pygame.quit()
           quit()
    
    #draw the start menu
    if game_state == 'start_menu':
        draw_start_menu()