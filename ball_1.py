import pygame
from pygame.locals import *

# has a moving ball and a player.
screen_width = 640
screen_height = 480

class Ball(pygame.sprite.Sprite):
    def __init__(self, surf, radius, color, xspeed, yspeed):
        pygame.sprite.Sprite.__init__(self)
        self.xspeed = xspeed
        self.yspeed = yspeed
        self.x = radius * 2
        self.y = radius * 2
        self.radius = radius
        self.color = color
        self.surface = surf
        self.rect = self.draw_ball()


    def draw_ball(self):
        rect = pygame.draw.circle(self.surface, self.color, (self.x, self.y), self.radius)
        self.rect = rect
        return rect

    def update(self):
        newx = self.x + self.xspeed
        newy = self.y + self.yspeed
        if newx > screen_width:
            self.xspeed *= -1
            self.x = screen_width - self.radius
        elif newx < 0:
            self.xspeed *= -1
            self.x = self.radius
        else:
            self.x = newx

        if newy > screen_height:
            self.yspeed *= -1
            self.y = screen_height - self.radius
        elif newy < 0:
            self.y = self.radius
            self.yspeed *= -1
        else:
            self.y = newy

        self.draw_ball()

    def set_speed(self, xs, ys):
        self.xspeed = xs
        self.yspeed = ys

    def collide(self, player_rect):
        '''decide if the ball collides with the player. return True if yes, otherwise return False.'''
        ball_southend_y = self.y + self.radius
        if (self.x > player_rect.topleft_x and self.x < player_rect.topleft_x + player_rect.width and ball_southend_y >= player_rect.topleft_y):
            return True
        else:
            return False

class Player(pygame.sprite.Sprite):
    def __init__(self, surface, color, x, y, width, height, xspeed):
        pygame.sprite.Sprite.__init__(self)
        self.color = color
        self.height = height
        self.width = width
        self.xspeed = xspeed
        self.surface = surface
        self.topleft_x = x
        self.topleft_y = y
        self.draw_player()

    def draw_player(self): 
        rect = pygame.draw.rect(self.surface, self.color, (self.topleft_x, self.topleft_y, self.width, self.height))
        self.rect = rect
        return rect

    def update(self):
        if self.topleft_x < 0:
             self.topleft_x = 0
        elif self.topleft_x >= screen_width - self.width:
             self.topleft_x = screen_width - self.width

        self.rect = self.draw_player()

    def set_speed(self, xs):
        self.xspeed += xs

    def move_left(self):
        self.topleft_x -= self.xspeed

    def move_right(self):
        self.topleft_x += self.xspeed


        

def main():
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0,0,0))
    clock = pygame.time.Clock()

    going = True
    ball = Ball(screen, 8, (255,255,255), 3, 4)
    player = Player(screen, (255, 255, 255), 200, 450, 45, 3, 4)
    #allsprites = pygame.sprite.RenderPlain((ball))
    while going:
        clock.tick(40)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                going = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                going = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                player.move_left()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                player.move_right()

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_LEFT]:
            player.move_left()
        elif pressed[pygame.K_RIGHT]:
            player.move_right()
        screen.blit(background, (0,0))
        ball.update()
        player.update()
        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()
