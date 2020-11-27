import pygame
import time
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
wall5 = pygame.image.load('./garden.png')

textures = {
  "1": wall1,
  "2": wall2,
  "3": wall3,
  "4": wall4,
  "5": wall5,
}

friend1 = pygame.image.load('./poke1.png')
friend2 = pygame.image.load('./poke2.png')
friend3 = pygame.image.load('./poke3.png')
friend4 = pygame.image.load('./poke4.png')
friend5 = pygame.image.load('./poke5.png')

hand = pygame.image.load('./player.png')

friends = [
  {
    "x": 155,
    "y": 265,
    "texture": friend1
  },
  {
    "x": 155,
    "y": 355,
    "texture": friend2
  },
  {
    "x": 425,
    "y": 385,
    "texture": friend3
  },
  {
    "x": 375,
    "y": 280,
    "texture": friend4
  },
  {
    "x": 425,
    "y": 195,
    "texture": friend5
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
        hitx = x - i*50
        hity = y - j*50

        if 1 < hitx < 49:
          tx = hitx
        else:
          tx = hity

        tx = int(tx * 128 / 50)
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
	  
    sprite_size = int(250/sprite_d * 70)
    
    sprite_x = int(500 + (sprite_a - self.player["a"]) * 500/self.player["fov"] + 250 - sprite_size/2)

    sprite_y = int(250 - sprite_size/2)

    for x in range(sprite_x, sprite_x + sprite_size):
      for y in range(sprite_y, sprite_y + sprite_size):
        i = x - 500
        if 500 < x < 1000 and self.zbuffer[i] >= sprite_d:
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
      self.zbuffer[i] = d

    for i in range(0, 500):
      self.point(499, i, (0, 0, 0))
      self.point(500, i, (0, 0, 0))
      self.point(501, i, (0, 0, 0))

    for friend in friends:
      self.point(friend["x"], friend["y"], (0, 0, 0))
      self.draw_sprite(friend)

    self.draw_player(1000 - 256 - 128, 500 - 200)

# de acuerdo al tutorial de Python Programming Tutorials

pygame.init()
screen = pygame.display.set_mode((1000, 500))
r = Raycaster(screen)
r.load_map('./map.txt')
clock = pygame.time.Clock()

def text_objects(text, font):
  textSurface = font.render(text, True, BLACK)
  return textSurface, textSurface.get_rect()

def button(msg,x,y,w,h,ic,ac,action=None):
  mouse = pygame.mouse.get_pos()
  click = pygame.mouse.get_pressed()
  if x+w > mouse[0] > x and y+h > mouse[1] > y:
    pygame.draw.rect(screen, ac,(x,y,w,h))

    if click[0] == 1 and action != None:
      if action == "Jugar":
        jugar()
      elif action == "Exit":
        exit(0)
  else:
    pygame.draw.rect(screen, ic,(x,y,w,h))

  smallText = pygame.font.SysFont("comicsansms",20)
  textSurf, textRect = text_objects(msg, smallText)
  textRect.center = ( (x+(w/2)), (y+(h/2)) )
  screen.blit(textSurf, textRect)

  smallText = pygame.font.SysFont("comicsansms",20)
  textSurf, textRect = text_objects(msg, smallText)
  textRect.center = ( (x+(w/2)), (y+(h/2)) )
  screen.blit(textSurf, textRect)


def game_intro():
  intro = True
  while intro:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        quit()
            
    screen.fill(WHITE)
    largeText = pygame.font.Font('freesansbold.ttf',90)
    TextSurf, TextRect = text_objects("Busqueda Pokemon!", largeText)
    TextRect.center = ((500),(100))
    screen.blit(TextSurf, TextRect)

    largeText = pygame.font.Font('freesansbold.ttf',30)
    TextSurf, TextRect = text_objects("Los pokemones te guiaran al jardin para terminar", largeText)
    TextRect.center = ((500),(275))
    screen.blit(TextSurf, TextRect)

    button('Jugar', 450, 400, 100, 50, (0, 255, 0), (0, 200, 0), "Jugar")

    pygame.display.update()

def game_congrat():
  intro = True
  while intro:
    for e in pygame.event.get():
      if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
        exit(0)    
    screen.fill(WHITE)
    largeText = pygame.font.Font('freesansbold.ttf',100)
    TextSurf, TextRect = text_objects("Ganaste!", largeText)
    TextRect.center = ((500),(250))
    screen.blit(TextSurf, TextRect)

    button('Salir', 450, 400, 100, 50, (0, 255, 0), (0, 200, 0), "Exit")

    pygame.display.update()

def fps_counter(count):
  font = pygame.font.SysFont(None, 25)
  text = font.render("FPS: "+str(count), True, BLACK)
  screen.blit(text,(0,0))

def jugar():
  # pygame.mixer.music.load('./music.mp3')
  # pygame.mixer.music.set_volume(0.1)
  # pygame.mixer.music.play(-1)
  while True:
    screen.fill((0, 0, 0))
    r.render()
    for e in pygame.event.get():
      if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
        exit(0)
      if e.type == pygame.KEYDOWN:
        if e.key == pygame.K_d:
          r.player["y"] += 10
        elif e.key == pygame.K_a:
          r.player["y"] -= 10
        elif e.key == pygame.K_w:
          r.player["x"] += 10
        elif e.key == pygame.K_s:
          r.player["x"] -= 10

        elif e.key == pygame.K_RIGHT:
          r.player["y"] += 10
        elif e.key == pygame.K_LEFT:
          r.player["y"] -= 10
        elif e.key == pygame.K_UP:
          r.player["x"] += 10
        elif e.key == pygame.K_DOWN:
          r.player["x"] -= 10

        print(r.player["x"], r.player["y"])
        

        if r.player["x"] > 65 and r.player["x"] < 125 and r.player["y"] > 255 and r.player["y"] < 285:
          pygame.mixer.Channel(0).play(pygame.mixer.Sound('./pokemongo.mp3'))
          pygame.mixer.Channel(0).set_volume(0.3)

        if r.player["x"] > 65 and r.player["x"] < 125 and r.player["y"] > 345 and r.player["y"] < 375:
          pygame.mixer.Channel(0).play(pygame.mixer.Sound('./pokemongo.mp3'))
          pygame.mixer.Channel(0).set_volume(0.3)

        if r.player["x"] > 315 and r.player["x"] < 375 and r.player["y"] > 375 and r.player["y"] < 405:
          pygame.mixer.Channel(0).play(pygame.mixer.Sound('./pokemongo.mp3'))
          pygame.mixer.Channel(0).set_volume(0.3)
        
        if r.player["x"] > 265 and r.player["x"] < 355 and r.player["y"] > 275 and r.player["y"] < 305:
          pygame.mixer.Channel(0).play(pygame.mixer.Sound('./pokemongo.mp3'))
          pygame.mixer.Channel(0).set_volume(0.3)

        if r.player["x"] > 335 and r.player["x"] < 395 and r.player["y"] > 185 and r.player["y"] < 205:
          pygame.mixer.Channel(0).play(pygame.mixer.Sound('./pokemongo.mp3'))
          pygame.mixer.Channel(0).set_volume(0.3)
        
        if r.player["x"] > 345 and r.player["x"] < 395 and r.player["y"] > 65 and r.player["y"] < 165:
          game_congrat()

        if e.key == pygame.K_f:
          if screen.get_flags() and pygame.FULLSCREEN:
            pygame.display.set_mode((1000, 500))
          else:
            pygame.display.set_mode((1000, 500),  pygame.DOUBLEBUF|pygame.HWACCEL|pygame.FULLSCREEN)
      

    fps_counter(clock.tick(30))
    pygame.display.flip()

game_intro()