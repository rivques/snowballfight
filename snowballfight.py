#import
import pygame, sys, numpy, random
#create fps clock
clock = pygame.time.Clock()
#
MAPHEIGHT = 80
MAPWIDTH = 80
TILESIZE =  40
TILESONSCREENW = 13
TILESONSCREENH = 13
#set screen size
SCREENH = TILESONSCREENH*TILESIZE
SCREENW = TILESONSCREENW*TILESIZE
#create character vars
circleRad = 20
circleSpeed = 4
#create circle pos vars
circleX = 250
circleY = 250
#create keyboard button vars
rightP = False
leftP = False
upP = False
downP = False
#
playerOnTileS = pygame.Surface((MAPWIDTH*TILESIZE, MAPHEIGHT*TILESIZE))

#constants for the tilemap
GRASS = pygame.image.load("grass.png")
TREE = pygame.image.load("tree.png")

#convert grass

#tilemap
tilemap = [[GRASS for i in range(MAPHEIGHT)] for j in range(MAPWIDTH)]
numTrees = random.randint(1000,2000)
print(len(tilemap[1]))
treeRects = []
for k in range(numTrees):
	treeX = random.randint(1,MAPWIDTH-1)
	treeY = random.randint(1,MAPHEIGHT-1)
	print((treeX,treeY))
	treeRects.append(pygame.Rect(treeX*TILESIZE,treeY*TILESIZE,TILESIZE,TILESIZE))
	tilemap[treeX][treeY] = TREE
for row in range(len(tilemap)):
    for column in range(len(tilemap[row])):
        playerOnTileS.blit(tilemap[row][column],(column*TILESIZE,row*TILESIZE))
#create window
DISPLAYSURF = pygame.display.set_mode((SCREENW, SCREENH))
#set window name
pygame.display.set_caption("Snowball Fight!")

class Projectile:
	currentX = 0
	currentY = 0
	def __init__(self, startX, startY, direction, speed, size):
		self.startX = startX
		self.startY = startY
		self.speed = speed
		self.direction = direction
		self.numcollisions = 0
		self.size = size
		self.projSurface = pygame.Surface((size, size))
		pygame.draw.rect(self.projSurface, (255,200,15), (0,0,size, size))
		self.currentX = self.startX
		self.currentY = self.startY
	def move(self,speed):
		newX = self.currentX + speed
		newY = round(numpy.interp(newX,[self.startX, MAPWIDTH*TILESIZE],[self.startY, MAPHEIGHT*TILESIZE]))
		self.currentX = newX
		self.currentY = newY
	def update(self):
		if self.currentX >= MAPWIDTH*TILESIZE and self.currentY >= MAPHEIGHT*TILESIZE:
			return True
		else:
			DISPLAYSURF.blit(self.projSurface, (self.currentX, self.currentY))
class Player:
	def __init__(self, playX, playY, size):
		self.playerX = playX
		self.playerY = playY
		self.numcollisions = 0
		self.size = size
		self.playerSurface = pygame.Surface((size, size))
		self.rect = pygame.Rect(playX,playY,size,size)
		pygame.draw.rect(self.playerSurface, (19,135,67), (0,0,size, size))
	def resize(self, newsize):
		self.size = newsize
		self.playerSurface = pygame.Surface((newsize, newsize))
		pygame.draw.rect(self.playerSurface, (19,135,67), (0,0,newsize, newsize))
	def getPos(self):
		return((self.playerX, self.playerY))
	def getAll(self):
		return((self.playerX, self.playerY, self.size))
	def move(self, newX, newY):
		self.playerX += newX
		self.playerY += newY
		self.rect.left = self.playerX
		self.rect.top = self.playerY
		for tree in treeRects:
			if self.rect.colliderect(tree):
				self.numcollisions += 1
				print("collision!"+str(self.numcollisions))
				if newX > 0: # Moving right; Hit the left side of the wall
					self.rect.right = tree.left
				if newX < 0: # Moving left; Hit the right side of the wall
					self.rect.left = tree.right
				if newY > 0: # Moving down; Hit the top side of the wall
					self.rect.bottom = tree.top
				if newY < 0: # Moving up; Hit the bottom side of the wall
					self.rect.top = tree.bottom
		self.playerX = self.rect.left
		self.playerY = self.rect.top

	def update(self):
		DISPLAYSURF.blit(self.playerSurface, (SCREENW/2-self.size ,SCREENH/2-self.size))
#game loop
myPlayer = Player(SCREENW/2+circleRad,SCREENH/2+circleRad,circleRad)
projectiles = []
while True:
	DISPLAYSURF.fill((0,0,0))
	oldPos = myPlayer.getPos()
	for event in pygame.event.get():
		#if the user closed the window
		if event.type == pygame.QUIT:
			#close pygame
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_a:
				leftP = True
			if event.key == pygame.K_d:
				rightP = True
			if event.key == pygame.K_w:
				upP = True
			if event.key == pygame.K_s:
				downP = True
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_a:
				leftP = False
			if event.key == pygame.K_d:
				rightP = False
			if event.key == pygame.K_w:
				upP = False
			if event.key == pygame.K_s:
				downP = False
	for projectile in projectiles:
		projectile.move(3)
		if projectile.update():
			projectiles.remove(projectile)
	if leftP:
		if myPlayer.getPos()[0]>SCREENH/2+myPlayer.getAll()[2]:
			myPlayer.move(-circleSpeed,0)
	if rightP:
		myPlayer.move(circleSpeed,0)
	if downP:
		myPlayer.move(0,circleSpeed)
	if upP:
		if myPlayer.getPos()[1]>SCREENH/2+myPlayer.getAll()[2]:
			myPlayer.move(0,-circleSpeed)
	DISPLAYSURF.blit(playerOnTileS, (SCREENW-myPlayer.getPos()[0],SCREENH-myPlayer.getPos()[1]))
	myPlayer.update()
	pygame.display.update()
	clock.tick(30)