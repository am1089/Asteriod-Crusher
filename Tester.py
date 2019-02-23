import pygame, random, sys, math
from pygame.locals import *

windowWidth = 700
windowHeight = 600
textColor = (0, 0, 255)
backgroundColor = (0, 0, 0)
FPS = 30
playerMoveRate = 5
MaxLife = 6
SuperMaxLife = 9
noScreenUpdate = 0

class variableSize(object):
    def __init__(self, size, center_x, center_y, radius, revsPerSec, image):
        self.size = size
        self.center = (int(center_x), int(center_y))
        self.radius = radius
        self.revsPerSec = revsPerSec
        self.image = image
        self.theta = 90
        self.color = (255,0,0)
        self.list = []

    def create_add(self):
            newObject = {'rect': pygame.Rect(self.center[0],
                                             self.center[1],
                                             self.size, self.size),
                        'surface':pygame.transform.scale(self.image, (self.size, self.size)),
                         'theta': self.theta,}
            
            self.list.append(newObject)


    def drawList(self):
        #print("Color=",self.color,"center=",self.center,"radius=",self.radius)
        pygame.draw.circle(windowSurface, self.color, self.center, self.radius, 4);
        for o in self.list[:]:
            windowSurface.blit(o['surface'], o['rect'])

    def moveList(self):
        for o in self.list[:]:
            radians = math.radians(o['theta'])
            x = self.radius * math.cos(radians)
            y = self.radius * math.sin(radians)
            #print('x=', x, 'y=', y)
            theta = self.revsPerSec * 360 / FPS
            o['rect'].x = x + self.center[0] - self.size/2
            o['rect'].y = y + self.center[1] - self.size/2
            theta += o['theta']
            if (theta >= 360):
                theta -= 360
            o['theta'] = theta

    def cullList(self):
        for o in self.list[:]:
            if o['rect'].left < 0:
                self.list.remove(o)

    def playerHit(self, playerRect):
        for o in self.list[:]:
            if playerRect.colliderect(o['rect']):
                self.list.remove(o)
                return True
        return False
    
class constantSize(variableSize):
    def __init__(self, Size, MinSpeed, MaxSpeed, addRate, image):
        super().__init__(Size, Size, MinSpeed, MaxSpeed, addRate, image)
        self.Size = Size

    def create_add(self):
        if not reverseCheat and not slowCheat:
            self.counter += 1
        if self.counter == self.addRate:
            self.counter = 0
            newObject = {'rect': pygame.Rect(windowWidth, random.randint(0, windowHeight - self.Size), self.Size, self.Size),
                        'speed': random.randint(self.MinSpeed, self.MaxSpeed),
                        'surface':pygame.transform.scale(self.image, (self.Size, self.Size)),}
            
            self.list.append(newObject)

        
        
def terminate():
    pygame.quit()
    sys.exit()

def freeze():
    print("noScreenUpdate=", noScreenUpdate)
    if noScreenUpdate == 1:
        noScreenUpdate = 0
    else:
        noScreenUpdate = 1

def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: # Pressing ESC quits.
                    terminate()
                return

def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, textColor)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


# Set up pygame and the window
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption('Asteroid')

# Set up the fonts.
font = pygame.font.SysFont(None, 48)

# Set up sounds.
gameOverSound = pygame.mixer.Sound('gameover.wav')
pygame.mixer.music.load('background.mid')
gotHitByTonicSound = pygame.mixer.Sound('smw_1-up.wav')
gotHitByAsteroid = pygame.mixer.Sound('0477.wav')
gotHitByMT = pygame.mixer.Sound('cheering.wav')
gotHitByBigShroom = pygame.mixer.Sound('blip.wav')
gotHitBySmallShroom = pygame.mixer.Sound('blurp.wav')

# Set up images
asteroidImage = pygame.image.load('asteroid.png')
backgroundImage = pygame.image.load('8-bit_Space.jpg')
strechedBackgroundImage = pygame.transform.scale(backgroundImage, (windowWidth, windowHeight))

# Show the "Start" screen.
windowSurface.blit(strechedBackgroundImage, (0, 0))
drawText('Asteroid', font, windowSurface, (windowWidth / 3),
       (windowHeight / 3))
drawText('Press a key to start.', font, windowSurface,
       (windowWidth / 3) - 30, (windowHeight / 3) + 50)
pygame.display.update()
waitForPlayerToPressKey()

topScore = 0
asteroid = variableSize(40, windowWidth/2, windowHeight/2, 100, 0.25, asteroidImage)
while True:
    # Set up the start of the game.
    asteroids = []
    score = 0
    life = 1
    moveLeft = moveRight = moveUp = moveDown = False
    reverseCheat = slowCheat = False
    pygame.mixer.music.play(-1, 0.0)
    # Add new asteroids at the right of the screen
    asteroid.create_add()

    while True: # The game loop runs while the game part is playing.
        if noScreenUpdate == 1:
            continue

        score += 1 # Increase score.

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:
                if event.key == K_z:
                    reverseCheat = True
                if event.key == K_x:
                    slowCheat = True
                if event.key == K_LEFT or event.key == K_a:
                    moveRight = False
                    moveLeft = True
                if event.key == K_RIGHT or event.key == K_d:
                    moveLeft = False
                    moveRight = True
                if event.key == K_UP or event.key == K_w:
                    moveDown = False
                    moveUp = True
                if event.key == K_DOWN or event.key == K_s:
                    moveUp = False
                    moveDown = True

            if event.type == KEYUP:
                if event.key == K_z:
                    reverseCheat = False
                    score = 0
                if event.key == K_x:
                    slowCheat = False
                    score = 0
                if event.key == K_ESCAPE:
                    terminate()
                if event.key == K_SPACE:
                    freeze()

                if event.key == K_LEFT or event.key == K_a:
                    moveLeft = False
                if event.key == K_RIGHT or event.key == K_d:
                    moveRight = False
                if event.key == K_UP or event.key == K_w:
                    moveUp = False
                if event.key == K_DOWN or event.key == K_s:
                    moveDown = False

        # Move the asteroids left
        asteroid.moveList()
        
        # Draw the game world on the window.
        windowSurface.blit(strechedBackgroundImage, (0, 0))

        # Draw each asteroid.
        asteroid.drawList()
        
        pygame.display.update()

        mainClock.tick(FPS)
        

    # Stop the game and show the "Game Over" screen.
    pygame.mixer.music.stop()
    gameOverSound.play()

    drawText('GAME OVER', font, windowSurface, (windowWidth / 3),
           (windowHeight / 3))
    drawText('Press a key to play again.', font, windowSurface,
           (windowWidth / 3) - 80, (windowHeight / 3) + 50)
    player.width = 35
    player.height = 35
    playerMoveRate = 5
    playerStrechedImage = pygame.transform.scale(playerImage, (player.height, player.width))
    pygame.display.update()
    waitForPlayerToPressKey()

gameOverSound.stop()
