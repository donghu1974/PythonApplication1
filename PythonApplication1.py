import sys, os
from pygame.locals import *
import pygame

pygame.init()
window = pygame.display.set_mode((500, 500))
pygame.display.set_caption('Monkey Fever')
screen = pygame.display.get_surface()
BACKGROUND = (0,0,0)

monkey_head_file_name = os.path.join(r'C:\Users\dongh\anaconda3\lib\site-packages\pygame\examples', 'data', 'chimp.bmp')
monkey_surface = pygame.image.load(monkey_head_file_name)
rect = monkey_surface.get_rect()
x = 0
y = 0
clock = pygame.time.Clock()
screen.blit(monkey_surface, (x, y))
pygame.display.flip()

def input(events):
    global x, y
    for event in events:
        if event.type == QUIT:
            sys.exit(0)
        elif event.type == KEYDOWN:
            if event.unicode == 'l':
                x = x + 10
                y = y + 10
            else: 
                sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            x = pygame.mouse.get_pos()[0]
            y = pygame.mouse.get_pos()[1]           
        else:
            print(event)

while True:
    input(pygame.event.get())
    print(x, y)
    screen.fill(BACKGROUND)
    pygame.Rect.move_ip(rect, (x, y))
    screen.blit(monkey_surface, (x, y))
    pygame.display.flip()
    clock.tick(2)
    



