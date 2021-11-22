import pygame
from pygame.locals import *
import random
from pygame.sprite import collide_mask

# ball_1.py: has a moving ball and a player.
# ball_2.py: 
#       has collision feature.Multiple balls.
# ball_3.py:
#       has text info
# ball_4.py
#       bricks, and bounced by bricks
screen_width = 640
screen_height = 720

COLLISION_TOLERANCE = 2
BRICK_AREA = pygame.Rect(40, 100, screen_width - 2 * 40, 300)
BALL_GENERATING_AREA = pygame.Rect(BRICK_AREA.left, BRICK_AREA.bottom + 10, BRICK_AREA.width, 10) 


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (154, 205, 50)
BLUE = (34,0,204)
ORANGE = (255,128,0)
PINK = (217,25,255)
COLOR = [WHITE, RED, GREEN, BLUE, ORANGE, PINK]


class Ball(pygame.sprite.Sprite):
    def __init__(self, surf, radius, color, xspeed, yspeed, id):
        pygame.sprite.Sprite.__init__(self)
        self.xspeed = xspeed
        self.yspeed = yspeed
        self.x = random.randrange(BALL_GENERATING_AREA.left, BALL_GENERATING_AREA.left + BALL_GENERATING_AREA.width)
        self.y = random.randrange(BALL_GENERATING_AREA.top, BALL_GENERATING_AREA.top + BALL_GENERATING_AREA.height)
        self.radius = radius
        self.color = color
        self.surface = surf
        self.rect = self.draw_ball()
        self.id = id
        self.pause = True

    def __eq__(self, other):
        return self.id == other.id

    def draw_ball(self):
        rect = pygame.draw.circle(self.surface, self.color, (self.x, self.y), self.radius)
        self.rect = rect
        return rect

    def bounce_left_right(self):
        self.xspeed *= -1

    def bounce_up_down(self):
        self.yspeed *= -1

    def pause_resume(self):
        self.pause = not(self.pause)
    
    def update(self, player_rect):
        in_game = True
        collision = False 
        if self.pause:
            self.draw_ball()
            return in_game, collision

        newx = self.x + self.xspeed
        newy = self.y + self.yspeed

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
        if pygame.Rect.colliderect(self.rect, player_rect):
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

    def pause_resume(self):
        for ball in self.balls:
            ball.pause_resume()

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
      
class Brick():
    def __init__(self, surface, left, top, width, height, id, color = None):
        self.x = left
        self.y = top
        self.width = width
        self.height = height
        self.surface = surface
        self.id = id
        if color == None:
            self.color = random.choice(COLOR)
        else:
            self.color = color
        self.rect = self.draw_brick()

    def draw_brick(self):
        rect = pygame.draw.rect(self.surface, self.color, (self.x, self.y, self.width, self.height))
        self.rect = rect
        return rect

    def __eq__(self, other):
        return self.id == other.id

    def update(self, balls):
        collision = False
        if self.collide(balls):
            collision = True
        else:
            self.draw_brick()
        return collision

    def collide(self, balls):
        left_rect = pygame.Rect(self.x, self.y, COLLISION_TOLERANCE, self.height)
        right_rect = pygame.Rect(self.x + self.width - COLLISION_TOLERANCE, self.y, COLLISION_TOLERANCE, self.height)
        top_rect = pygame.Rect(self.x, self.y, self.width, COLLISION_TOLERANCE)
        bottom_rect = pygame.Rect(self.x, self.y + self.height - COLLISION_TOLERANCE, self.width, COLLISION_TOLERANCE)

        for ball in balls:
            if pygame.Rect.colliderect(left_rect, ball.rect) or pygame.Rect.colliderect(right_rect, ball.rect):
                ball.bounce_left_right()
                return True
            elif pygame.Rect.colliderect(top_rect, ball.rect) or pygame.Rect.colliderect(bottom_rect, ball.rect):
                ball.bounce_up_down()
                return True
            else:
                return False
      
    def collide_with_rect(self, rect):
        if pygame.Rect.colliderect(self.rect, rect):
            return True
        else:
            return False

class Brick_wall():
    def __init__(self, surface, brick_area_rect, row, col):
        self.surface = surface
        self.bricks = []

        brick_w = int((brick_area_rect.width) * 1.0 / col)
        brick_h = int((brick_area_rect.height) * 1.0 / row)
        id = 0
        for i in range(row):
            for j in range(col):
                id = id + 1
                brick_x = brick_area_rect.left + j * brick_w
                brick_y = brick_area_rect.top + i * brick_h
                brick = Brick(surface, brick_x, brick_y, brick_w, brick_h, id)
                self.bricks.append(brick)

    def remove_brick(self, brick_to_be_removed):
        for brick in self.bricks:
            if brick.id == brick_to_be_removed.id:
                self.bricks.remove(brick)

    def update(self, balls):
        pts = 0
        for brick in self.bricks:
            if brick.update(balls.balls):
                self.remove_brick(brick)
                pts += 1
        return pts


def main():
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill(BLACK)
    clock = pygame.time.Clock()

    going = True
    points = 0

    player = Player(screen, WHITE, 200, 700, 145, 3, 8)
    ball_list = Balls(screen, 1, 8)
 
    game_over = Text(screen, 'Courier New', 55, True)
    game_over.set_text('Game Over', RED, (BALL_GENERATING_AREA.left + 100, BALL_GENERATING_AREA.bottom + 50))
    num_balls = Text(screen, 'Courier New', 15, True)
    num_balls.set_text('Balls: ' + str(ball_list.number_balls()), RED, ((20, 20)))
    score_text = Text(screen, 'Courier New', 15, True)
    score_text.set_text('Points: ' + str(points), RED, (screen_width - 120, 20))

    bricks = Brick_wall(screen, BRICK_AREA, 10, 10)

    while going:
        clock.tick(40)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                going = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                going = False

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_LEFT]:
            player.move_left()
        elif pressed[pygame.K_RIGHT]:
            player.move_right()
        elif pressed[pygame.K_SPACE]:
            ball_list.pause_resume()
        elif pressed[pygame.K_r]:
            points = 0
            ball_list = Balls(screen, 1, 8)
            bricks = Brick_wall(screen, BRICK_AREA, 10, 10)
        
        screen.blit(background, (0,0))
        newpoint = ball_list.update(player.rect)
        points = points + newpoint
        player.update()
        newpoint = bricks.update(ball_list)
        points = points + newpoint
        num_balls.change_text('Balls: ' + str(ball_list.number_balls()))
        num_balls.update()
        score_text.change_text('Points: ' + str(points))
        score_text.update()
        if ball_list.has_ball() == False:
            game_over.update()  

        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()
