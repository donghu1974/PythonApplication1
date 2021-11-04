import pygame
from pygame.locals import *
import random

# ball_1.py: has a moving ball and a player.
# ball_2.py: 
#       has collision feature.Multiple balls.
screen_width = 640
screen_height = 480
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class Ball(pygame.sprite.Sprite):
    def __init__(self, surf, radius, color, xspeed, yspeed, id):
        pygame.sprite.Sprite.__init__(self)
        self.xspeed = xspeed
        self.yspeed = yspeed
        self.x = random.randrange(20, 620)
        self.y = random.randrange(10, 200)
        self.radius = radius
        self.color = color
        self.surface = surf
        self.rect = self.draw_ball()
        self.id = id

    def __eq__(self, other):
        return self.id == other.id

    def draw_ball(self):
        rect = pygame.draw.circle(self.surface, self.color, (self.x, self.y), self.radius)
        self.rect = rect
        return rect

    def update(self, player_rect):
        newx = self.x + self.xspeed
        newy = self.y + self.yspeed
        in_game = True

        # always inbound on x axis
        if newx > screen_width:
            self.xspeed *= -1
            self.x = screen_width - self.radius
        elif newx < 0:
            self.xspeed *= -1
            self.x = self.radius
        else:
            self.x = newx

        if self.collide(player_rect) == False:
            if newy - self.radius > screen_height: ## player fails to kick the ball. this ball is gone.
                in_game = False
            elif newy < 0:
                self.y = self.radius
                self.yspeed *= -1
            else:
                self.y = newy
        self.draw_ball()
        return in_game

    def set_speed(self, xs, ys):
        self.xspeed = xs
        self.yspeed = ys

    def collide(self, player_rect):
        '''decide if the ball collides with the player. return True if yes, otherwise return False.'''
        ball_southend_y = self.y + self.radius
        if (self.x > player_rect.left and self.x < player_rect.left + player_rect.width and ball_southend_y >= player_rect.top):
            self.yspeed *= -1
            self.y = player_rect.top - self.radius + self.yspeed
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

class balls():
    '''holds a number of balls.'''
    def __init__(self):
        self.balls = []

    def addBall(self, ball):
        self.balls.append(ball)

    def removeBall(self, ball_to_be_removed):
        for ball in self.balls:
            if ball == ball_to_be_removed:
                self.balls.remove(ball)

    def update(self, player_rect):
        for ball in self.balls:
            in_game = ball.update(player_rect)
            if in_game == False:
                self.removeBall(ball)

    def has_ball(self):
        if len(self.balls) > 0:
            return True
        else:
            return False

def main():
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill(BLACK)
    clock = pygame.time.Clock()

    going = True
    ball1 = Ball(screen, 8, RED, 3, 4, 1)
    ball2 = Ball(screen, 8, WHITE, 2, 2.5, 2)

    player = Player(screen, WHITE, 200, 450, 145, 3, 8)
    ball_list = balls()
    ball_list.addBall(ball1)
    ball_list.addBall(ball2)

    #game_over_font = pygame.font.SysFont('Courier New', 55)

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
        ball_list.update(player.rect)
        player.update()
        #if ball_list.has_ball() == False:
            #game_over_surf = game_over_font.render('Game Over', False, BLUE)
            #screen.blit(game_over_surf, (200, 100))
        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()
