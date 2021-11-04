import pygame
WIDTH = 400
HEIGHT = 300
BACKGROUND = (0,0,0)

class Sprite(pygame.sprite.Sprite):
  def __init__(self, image, startx, starty):
    super().__init__()
    self.image = pygame.image.load(image)
    self.rect = self.image.get_rect()
    self.rect.center = [startx, starty]

  def update(self):
    pass

  def draw(self, screen):
    screen.blit(self.image, self.rect)

class Player(Sprite):
  def __init__(self, startx, starty):
    super().__init__('p1_front.png', startx, starty)
    self.stand_image = self.image
    self.walk_cycle = [pygame.image.load(f"p1_walk{i:0>2}.png") for i in range(1,12)]
    self.animation_index = 0
    self.facing_left = False
    self.speed = 4
    self.jumpspeed = 20
    self.vsp = 0
    self.gravity = 1

  def move(self, x, y):
    self.rect.move_ip([x, y])

  def walk_animation(self):
    self.image = self.walk_cycle[self.animation_index]
    if self.facing_left:
      self.image = pygame.transform.flip(self.image, True, False)

    if self.animation_index < len(self.walk_cycle) - 1:
      self.animation_index += 1
    else:
      self.animation_index = 0
    

  def update(self, boxes):
    hsp = 0
    onground = pygame.sprite.spritecollideany(self, boxes)

    key = pygame.key.get_pressed()

    if key[pygame.K_LEFT]:
      self.facing_left = True
      self.walk_animation()
      hsp = -self.speed
    elif key[pygame.K_RIGHT]:
      self.facing_left = False
      self.walk_animation()
      hsp = self.speed
    else:
      self.image =self.stand_image

    if key[pygame.K_UP] and onground:
      self.vsp = -self.jumpspeed
      print('onground: %s' % onground)

    if self.vsp < 10 and (onground == None):
      self.vsp += self.gravity

    if self.vsp > 0 and onground:
      self.vsp = 0

    self.move(hsp, self.vsp)

class Box(Sprite):
  def __init__(self, startx, starty):
    super().__init__('boxAlt.png', startx, starty)

    
def main():
  pygame.init()
  screen = pygame.display.set_mode((WIDTH, HEIGHT))
  clock = pygame.time.Clock()

  player = Player(100, 220)
  boxes = pygame.sprite.Group()
  for bx in range(0, 400, 70):
    boxes.add(Box(bx, 300))

  while True:
    pygame.event.pump()
    player.update(boxes)

    screen.fill(BACKGROUND)
    player.draw(screen)
    boxes.draw(screen)
    pygame.display.flip()
    clock.tick(60)

if __name__ == "__main__":
  main()

