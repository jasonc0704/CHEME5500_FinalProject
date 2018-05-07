import pygame as pg
import random
import math

WIDTH = 1000
HEIGHT = 600
FPS = 60

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)


# initialize pygame and create window
pg.init()
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Spaceship")
clock = pg.time.Clock()


font_type = pg.font.match_font('arial')
def DrawText(surf, text, size, x, y):
	font = pg.font.Font(font_type, size)
	text_surface = font.render(text, True, WHITE)
	text_rect = text_surface.get_rect()
	text_rect.midtop = (x, y)
	surf.blit(text_surface, text_rect)



def out_of_bounds(position):
	x, y = position  # You can unpack a list or tuple like so.
	return x < 0 or x > WIDTH or y < 0 or y > HEIGHT



class Player(pg.sprite.Sprite):
	def __init__(self):
		pg.sprite.Sprite.__init__(self)
		super(Player, self).__init__()
		self.image = pg.Surface((25, 15), pg.SRCALPHA)
		pg.draw.polygon(self.image, YELLOW, ((0, 0), (25, 7.5), (0, 15)))
		self.rect = self.image.get_rect()
		self.rect.x = 400
		self.rect.y = 250
		self.position = (self.rect.x, self.rect.y)
		self.speedx = 0
		self.speedy = 0

		# Rotate the player
		mousePosition = pg.mouse.get_pos()
		sinnn = mousePosition[1] - self.rect.centery
		cosss = mousePosition[0] - self.rect.centerx
		angle = math.atan2(sinnn, cosss)
		self.rotate = pg.transform.rotate(self.image, -math.degrees(angle))
		self.rotate_rect = self.rotate.get_rect(center=self.rect.center)


	def update(self):
		keystate = pg.key.get_pressed()
		self.speedx = 0
		self.speedy = 0
		if keystate[pg.K_LEFT]:
			self.speedx = -5
		if keystate[pg.K_RIGHT]:
			self.speedx = 5
		if keystate[pg.K_UP]:
			self.speedy = -5
		if keystate[pg.K_DOWN]:
			self.speedy = 5

		# Update positions
		self.rect.x += self.speedx
		self.rect.y += self.speedy

		# Constrain the player inside the screen
		if self.rect.centerx > WIDTH:
			self.rect.centerx = WIDTH
		if self.rect.centerx < 0:
			self.rect.centerx = 0
		if self.rect.centery > HEIGHT:
			self.rect.centery = HEIGHT
		if self.rect.centery < 0:
			self.rect.centery = 0


		# Rotate the player
		mousePosition = pg.mouse.get_pos()
		sinnn = mousePosition[1] - self.rect.centery
		cosss = mousePosition[0] - self.rect.centerx
		angle = math.atan2(sinnn, cosss)
		self.rotate = pg.transform.rotate(self.image, -math.degrees(angle))
		self.rotate_rect = self.rotate.get_rect(center=self.rect.center)


p = Player()


class Bullet(pg.sprite.Sprite):
	def __init__(self):
		pg.sprite.Sprite.__init__(self)
		self.image = pg.Surface((12,12))

		self.rect = self.image.get_rect()
		pg.draw.circle(self.image, GREEN, (self.rect.centerx, self.rect.centery), 6)

		mousePosition = pg.mouse.get_pos()
		sinnn = mousePosition[1] - p.rect.centery
		cosss = mousePosition[0] - p.rect.centerx
		angle = math.atan2(sinnn, cosss)

		# bullets generate at player's position 
		self.rect.x = p.rect.centerx
		self.rect.y = p.rect.centery
		
		# bullet flies toward the mouse 
		self.speedx = math.cos(angle) * 10
		self.speedy = math.sin(angle) * 10


	def update(self):

		self.rect.x += self.speedx
		self.rect.y += self.speedy

		self.position = (self.rect.x, self.rect.y)

		if out_of_bounds(self.position):
			self.kill()




class Mob(pg.sprite.Sprite):
	def __init__(self):
		pg.sprite.Sprite.__init__(self)
		self.image = pg.Surface((15,15))
		self.image.fill(RED)
		self.rect = self.image.get_rect()

		self.rect.x = random.randrange(WIDTH)
		self.rect.y = random.randrange(HEIGHT)

		#if self.rect.x > p.rect.x+d and self.rect.x < p.rect.x-d and self.rect.y > p.rect.y+d and self.rect.y < p.rect.y-d:
			#pass

		ang_ram = math.radians(random.randrange(360))
		self.speedx = 3 * math.cos(ang_ram)
		self.speedy = 3 * math.sin(ang_ram)


	def update(self):
		self.rect.x += self.speedx
		self.rect.y += self.speedy
		self.position = (self.rect.x, self.rect.y)

		# If a mob flies out of the screen, spawn a new mob
		if out_of_bounds(self.position):
			self.rect = self.image.get_rect()
			self.rect.x = random.randrange(800)
			self.rect.y = random.randrange(500)
			self.position = (self.rect.x, self.rect.y)
			ang_ram = math.radians(random.randrange(360))
			self.speedx = 5*math.cos(ang_ram)
			self.speedy = 5*math.sin(ang_ram)


score = 0
# make game over screen
def show_gameover_screen():
	screen.blit(background, background_rect)
	DrawText(screen, "Spaceship", 64, WIDTH/2, HEIGHT/5)
	DrawText(screen, "Your score is: %d" % score, 28, WIDTH/2, HEIGHT*2/5)
	DrawText(screen, "Arrow keys to move, mouse to rotate and fire", 24, WIDTH/2, HEIGHT*3/5)
	DrawText(screen, "Press any key to begin", 20, WIDTH/2, HEIGHT*4/5)
	pg.display.update()

	# stay at game over screen
	waiting = True
	while waiting:
		clock.tick(FPS)
		for event in pg.event.get():
			if event.type == pg.QUIT:
				pg.quit()

			# quit game over screen if press any key
			if event.type == pg.KEYUP:
				waiting = False



# load bacground image
background = pg.image.load("space.png")
background_rect = background.get_rect()

# generate "all_sprites" to hold all the species
all_sprites = pg.sprite.Group()

mobs = pg.sprite.Group()
bullets = pg.sprite.Group()
for i in range(10):
	m = Mob()
	all_sprites.add(m)
	mobs.add(m)

# add score
score = 0
# This is game loop
game_over = True
running = True
while running:

	# Display a game over screen before each game
	if game_over:
		show_gameover_screen()
		game_over = False
		all_sprites = pg.sprite.Group()
		mobs = pg.sprite.Group()
		bullets = pg.sprite.Group()
		p = Player()
		for i in range(10):
			m = Mob()
			all_sprites.add(m)
			mobs.add(m)
		score = 0

	# keep loop running at the right speed
	clock.tick(FPS)

	p.update()

	# Process input (events)
	for event in pg.event.get():

		# check for closing window
		if event.type == pg.QUIT:
			running = False

		elif event.type == pg.MOUSEBUTTONDOWN:
			b = Bullet()
			all_sprites.add(b)
			bullets.add(b)

	
	for b in bullets:
		b.update()


	for m in mobs:
		m.update()

	# Whenever a bullet hits a mob, delete both bullet and mob
	hits = pg.sprite.groupcollide(mobs, bullets, True, True)
	# Spawn a mob after hit one
	for hit in hits:
		score += 1
		m = Mob()
		all_sprites.add(m)
		mobs.add(m)

	#Gameover after player being hit by a mob
	hits = pg.sprite.spritecollide(p, mobs, False)
	if hits:
		game_over = True


	# Display a game over screen before each game
	if game_over:
		show_gameover_screen()
		game_over = False
		all_sprites = pg.sprite.Group()
		mobs = pg.sprite.Group()
		bullets = pg.sprite.Group()
		p = Player()
		for i in range(10):
			m = Mob()
			all_sprites.add(m)
			mobs.add(m)
		score = 0


	# Draw / render everything
	screen.fill(BLACK)
	screen.blit(background, background_rect)
	all_sprites.draw(screen)
	DrawText(screen, str(score), 28, WIDTH/2, 20)
	screen.blit(p.rotate, p.rotate_rect)
	for b in bullets:
		screen.blit(b.image, b.rect)

	# after drawing everything, update the display
	pg.display.update()


pg.quit()