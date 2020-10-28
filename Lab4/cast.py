import pygame
from math import *

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BACKGROUND = (0, 255, 255)

colors = {
  "1": (255, 0, 0),
  "2": (0, 255, 0),
  "3": (0, 0, 255)
}

wall1 = pygame.image.load('./wall1.png')
wall2 = pygame.image.load('./wall2.png')
wall3 = pygame.image.load('./wall3.png')
wall4 = pygame.image.load('./wall4.png')
wall5 = pygame.image.load('./wall5.png')

textures = {
  "1": wall1,
  "2": wall2,
  "3": wall3,
  "4": wall4,
  "5": wall5,
}

enemy1 = pygame.image.load('./sprite1.png')
enemy2 = pygame.image.load('./sprite2.png')
enemy3 = pygame.image.load('./sprite3.png')
enemy4 = pygame.image.load('./sprite4.png')

hand = pygame.image.load('./player.png')

enemies = [
  {
    "x": 100,
    "y": 200,
    "texture": enemy4
  }
]


class Raycaster(object):
  def __init__(self, screen):
    _, _, self.width, self.height = screen.get_rect()
    self.screen = screen
    self.blocksize = 50
    self.map = []
    self.player = {
      "x": self.blocksize + 25,
      "y": self.blocksize + 25,
      "a": 0,
      "fov": pi/3,
    }
    self.zbuffer = [-float("inf") for z in range(0, 500)]

  def point(self, x, y, c):
    screen.set_at((x, y), c)

  def draw_rectangle(self, x, y, texture):
    for cx in range(x, x + 50):
      for cy in range(y, y + 50):
        tx = int((cx - x) * 128/50)
        ty = int((cy - y) * 128/50)
        c = texture.get_at((tx, ty))
        self.point(cx, cy, c)

  def load_map(self, filename):
    with open(filename) as f:
      for line in f.readlines():
        self.map.append(list(line))

  def cast_ray(self, a):
    d = 0
    while True:
      x = self.player["x"] + (d * cos(a))
      y = self.player["y"] + (d * sin(a))

      i = int(x / self.blocksize)
      j = int(y / self.blocksize)

      if self.map[j][i] != ' ':
        hitx = x - j*50
        hity = y - j*50

        # maxhit = hity
        hitx = x - int(x+0.5)
        hity = y - int(y+0.5)

        if abs(hity) > abs(hitx):
          tx = hity * 128
        else:
          tx = hitx * 128

        print("tx1", tx)
        # if tx < 0:
        #   tx += 128
        # elif tx >= 128:
        #   tx -= 128
        tx = int(tx % 128)
        
        # if 10 < hitx < 40:
          
        #   maxhit = hitx
        # else:
        #   maxhit = hity

        # tx = int(maxhit * 128/50)
        print("tx", tx)
        # print("y", y)
        return d, self.map[j][i], tx

      self.point(int(x), int(y), (255, 255, 255))
      d += 1

  def draw_stake(self, x, h, tx, texture):
    start = int(250 - h/2)
    end = int(250 + h/2)
    for y in range(start, end):
      ty = int((y - start) * (128 / (end - start)))
      c = texture.get_at((tx, ty))
      self.point(x, y, c)

  def draw_sprite(self, sprite):
    sprite_a = atan2((sprite["y"] - self.player["y"]), (sprite["x"] - self.player["x"]))
    sprite_d = ((self.player["x"] - sprite["x"])**2 + (self.player["y"] - sprite["y"])**2) ** 0.5
	  
    sprite_size = int(500/sprite_d * 50)
    
    sprite_x = int(500 + (sprite_a - self.player["a"]) * 500/self.player["fov"] + 250 - sprite_size/2)

    sprite_y = int(250 - sprite_size/2)

    for x in range(sprite_x, sprite_x + sprite_size):
      for y in range(sprite_y, sprite_y + sprite_size):
        i = x - 500
        if 500 < x < 1000 and self.zbuffer[i] <= sprite_d:
          tx = int((x - sprite_x) * 128/sprite_size)
          ty = int((y - sprite_y) * 128/sprite_size)
          c = sprite["texture"].get_at((tx, ty))
          if c != (152, 0, 136, 255):
            self.point(x, y, c)
            self.zbuffer[i] = sprite_d

  def draw_player(self, xi, yi, w = 150, h = 150):
	    for x in range(xi, xi + w):
	      for y in range(yi, yi + h):
	        tx = int((x - xi) * 32/w)
	        ty = int((y - yi) * 32/h)
	        c = hand.get_at((tx, ty))
	        if c != (152, 0, 136, 255):
	          self.point(x, y, c)

  def render(self):
    for x in range(0, 500, self.blocksize):
      for y in range(0, 500, self.blocksize):
        i = int(x / self.blocksize)
        j = int(y / self.blocksize)
        if self.map[j][i] != ' ':
          self.draw_rectangle(x, y, textures[self.map[j][i]])

    self.point(self.player["x"], self.player["y"], (255, 255, 255))

    for i in range(0, 500):
      self.point(500, i, (0, 0, 0))
      self.point(501, i, (0, 0, 0))
      self.point(499, i, (0, 0, 0))

    for i in range(0, 500):
      a =  self.player["a"] - self.player["fov"]/2 + (i * self.player["fov"] / 500)
      d, m, tx = self.cast_ray(a)

      x = 500 + i
      h = (500 / (d * cos(a - self.player["a"]))) * 50

      self.draw_stake(x, h, tx, textures[m])

    for i in range(0, 500):
      self.point(499, i, (0, 0, 0))
      self.point(500, i, (0, 0, 0))
      self.point(501, i, (0, 0, 0))

    for enemy in enemies:
      self.point(enemy["x"], enemy["y"], (0, 0, 0))
      self.draw_sprite(enemy)

    self.draw_player(1000 - 256 - 128, 500 - 256)


pygame.init()
screen = pygame.display.set_mode((1000, 500))
r = Raycaster(screen)
r.load_map('./map.txt')


while True:
  screen.fill((0, 0, 0))

  for e in pygame.event.get():
    if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
      exit(0)
    if e.type == pygame.KEYDOWN:
      if e.key == pygame.K_a:
        r.player["a"] -= pi/10
      elif e.key == pygame.K_d:
        r.player["a"] += pi/10

      elif e.key == pygame.K_RIGHT:
        r.player["y"] += 10
      elif e.key == pygame.K_LEFT:
        r.player["y"] -= 10
      elif e.key == pygame.K_UP:
        r.player["x"] += 10
      elif e.key == pygame.K_DOWN:
        r.player["x"] -= 10

      if e.key == pygame.K_f:
        if screen.get_flags() and pygame.FULLSCREEN:
            pygame.display.set_mode((1000, 500))
        else:
            pygame.display.set_mode((1000, 500),  pygame.DOUBLEBUF|pygame.HWACCEL|pygame.FULLSCREEN)

  r.render()
  pygame.display.flip()




