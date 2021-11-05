import pygame
from pygame.locals import *
import random

from pygame.sprite import collide_mask

# ball_1.py: has a moving ball and a player.
# ball_2.py: 
#       has collision feature.Multiple balls.
# ball_3.py:
#       has text info
screen_width = 640
screen_height = 480

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (255, 0, 0)
BLUE = (0,0,255)
COLOR = [WHITE, BLACK, RED, GREEN, BLUE]

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
        collision = False

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
        else: 
            collision = True
        self.draw_ball()
        return in_game, collision

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

class Balls():
    '''holds a number of balls.'''
    def __init__(self, surf, num_of_balls, radius, color = None, xspeed = 0, yspeed = 0):
        self.balls = []
        for i in range(num_of_balls):
            if color == None:
                value = random.choice(COLOR)
            else:
                value = color

            if xspeed == 0 and yspeed == 0:
                xs = random.randint(2,8)
                ys = random.randint(2,8)
            else:
                xs = xspeed
                ys = yspeed

            new_ball = Ball(surf, radius, value, xs, ys, i+1)
            self.balls.append(new_ball)
            self.max_id = i + 1

    def addBall(self, ball):
        self.balls.append(ball)

    def removeBall(self, ball_to_be_removed):
        for ball in self.balls:
            if ball == ball_to_be_removed:
                self.balls.remove(ball)

    def update(self, player_rect):
        points = 0
        for ball in self.balls:
            in_game, collision = ball.update(player_rect)
            if collision:
                points += 1
            if in_game == False:
                self.removeBall(ball)
        return points

    def number_balls(self):
        return len(self.balls)

    def has_ball(self):
        if len(self.balls) > 0:
            return True
        else:
            return False

class Text():
    def __init__(self, surface, fontname, fontsize, bold):
        self.fontname = fontname
        self.size = fontsize
        self.font = pygame.font.SysFont(fontname, fontsize, bold)
        self.surface = surface
        self.text = ''
        self.color = None
        self.left_top = None

    def set_text(self, text, color, left_top):
        fontsurf = self.font.render(text, False, color)
        self.text = text
        self.color = color
        self.left_top = left_top
 
    def change_text(self, new_text):
        self.text = new_text

    def update(self):
        fontsurf = self.font.render(self.text, False, self.color)
        self.surface.blit(fontsurf, self.left_top)
      
        
def main():
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill(BLACK)
    clock = pygame.time.Clock()

    going = True
    points = 0

    player = Player(screen, WHITE, 200, 450, 145, 3, 8)
    ball_list = Balls(screen, 8, 8)
 
    game_over = Text(screen, 'Courier New', 55, True)
    game_over.set_text('Game Over', RED, (200, 200))
    num_balls = Text(screen, 'Courier New', 15, True)
    num_balls.set_text('Balls: ' + str(ball_list.number_balls()), RED, ((20, 20)))
    score_text = Text(screen, 'Courier New', 15, True)
    score_text.set_text('Points: ' + str(points), RED, (screen_width - 120, 20))

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
        points = points + ball_list.update(player.rect)
        num_balls.change_text('Balls: ' + str(ball_list.number_balls()))
        num_balls.update()
        score_text.change_text('Points: ' + str(points))
        score_text.update()
        player.update()
        if ball_list.has_ball() == False:
            game_over.update()
        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()
