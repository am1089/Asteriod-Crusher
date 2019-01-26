import pygame, random, sys
from pygame.locals import *

windowWidth = 700
windowHeight = 600
textColor = (0, 0, 255)
backgroundColor = (0, 0, 0)
FPS = 40
playerMoveRate = 5
MaxLife = 6
SuperMaxLife = 9

class variableSize(object):
    def __init__(self, minSize, maxSize, MinSpeed, MaxSpeed, addRate, image):
        self.minSize = minSize
        self.maxSize = maxSize
        self.MinSpeed = MinSpeed
        self.MaxSpeed = MaxSpeed
        self.addRate = addRate
        self.image = image
        self.counter = 0
        self.list = []

    def create_add(self):
        if not reverseCheat and not slowCheat:
            self.counter += 1
        if self.counter == self.addRate:
            self.counter = 0
            self.Size = random.randint(self.minSize, self.maxSize)
            newObject = {'rect': pygame.Rect(windowWidth, random.randint(0, windowHeight - self.Size), self.Size, self.Size),
                        'speed': random.randint(self.MinSpeed, self.MaxSpeed),
                        'surface':pygame.transform.scale(self.image, (self.Size, self.Size)),}
            
            self.list.append(newObject)


    def drawList(self):
        for o in self.list:
            windowSurface.blit(o['surface'], o['rect'])

    def moveList(self):
        for o in self.list[:]:
            if not reverseCheat and not slowCheat:
                o['rect'].move_ip(-o['speed'], 0)
            elif reverseCheat:
                o['rect'].move_ip(5, 0)
            elif slowCheat:
                o['rect'].move_ip(-1, 0)
        

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
player = pygame.Rect(300, 100, 35, 35)
playerImage = pygame.image.load('player-1.png')
playerStrechedImage = pygame.transform.scale(playerImage, (35, 35))
playerRect = playerStrechedImage.get_rect()
asteroidImage = pygame.image.load('asteroid.png')
tonicImage = pygame.image.load('Energy_Tank.png')
megaTankImage = pygame.image.load('mega_tank.png')
BigShroomImage = pygame.image.load('BigShroom.png')
SmallShroomImage = pygame.image.load('SmallShroom.png')
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
tank = constantSize(25, 8, 10, 500, megaTankImage)
tonic = constantSize(30, 4, 5, 25, tonicImage)
asteroid = variableSize(20, 40 , 2, 8, 8, asteroidImage)
bigShroom = constantSize(25, 3, 5, 60, BigShroomImage)
smallShroom = constantSize(25, 4, 5, 60, SmallShroomImage)
while True:
    # Set up the start of the game.
    asteroids = []
    tonics = []
    tanks = []
    bigShrooms = []
    smallShrooms = []
    score = 0
    life = 1
    playerRect.topleft = (windowWidth / 2, windowHeight/ 2)
    moveLeft = moveRight = moveUp = moveDown = False
    reverseCheat = slowCheat = False
    tonicAddCounter = 0
    asteroidAddCounter = 0
    tankAddCounter = 0
    bigShroomAddCounter = 0
    smallShroomAddCounter = 0
    pygame.mixer.music.play(-1, 0.0)

    while True: # The game loop runs while the game part is playing.
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

                if event.key == K_LEFT or event.key == K_a:
                    moveLeft = False
                if event.key == K_RIGHT or event.key == K_d:
                    moveRight = False
                if event.key == K_UP or event.key == K_w:
                    moveUp = False
                if event.key == K_DOWN or event.key == K_s:
                    moveDown = False

        # Add new asteroids at the right of the screen
        asteroid.create_add()
        
        # Add new tonics at the right of the screen
        tonic.create_add()

        # Add new mega tanks at the right of the screen
        tank.create_add()

        # Add new Bigshrooms at the right of the screen
        bigShroom.create_add()

        # Add new SmallShrooms at the right of the screen
        smallShroom.create_add()
            
        # Move the player around.
        if moveLeft and playerRect.left > 0:
            playerRect.move_ip(-1 * playerMoveRate, 0)
        if moveRight and playerRect.right < windowWidth:
            playerRect.move_ip(playerMoveRate, 0)
        if moveUp and playerRect.top > 0:
            playerRect.move_ip(0, -1 * playerMoveRate)
        if moveDown and playerRect.bottom < windowHeight:
            playerRect.move_ip(0, playerMoveRate)

        # Move the asteroids left
        asteroid.moveList()
        
        # Move the tonics left
        tonic.moveList()

        # Move the tanks left
        tank.moveList()
        
        # Move the Bigshrooms left
        bigShroom.moveList()

        # Move Smallshrooms left
        smallShroom.moveList()
      
        # Delete asteroids that have fallen past the left of the screen.
        asteroid.cullList()
        
        # Delete tonics that have fallen past the left of the screen
        tonic.cullList()

        # Delete tanks that have fallen past the left of the screen
        tank.cullList()

        # Delete BigShrooms that have fallen past the left of the screen
        bigShroom.cullList()

        # Delete Smallshrooms that have fallen past the left of the screen
        smallShroom.cullList()
        
        # Draw the game world on the window.
        windowSurface.blit(strechedBackgroundImage, (0, 0))

        # Draw the score and top score.
        drawText('Score: %s' % (score), font, windowSurface, 10, 0)
        drawText('Top Score: %s' % (topScore), font, windowSurface,
               10, 40)
        drawText('Life: %s' % (life), font, windowSurface, 10, 80)

        # Draw the player's rectangle.
        windowSurface.blit(playerStrechedImage, playerRect)

        # Draw each asteroid.
        asteroid.drawList()
        
        # Draw each tonic
        tonic.drawList()
        
        # Draw each mega tank
        tank.drawList()
            
        # Draw each Bigshroom
        bigShroom.drawList()
        
        # Draw each SmallShroom
        smallShroom.drawList()

        pygame.display.update()

        # Check if any of the tonics have hit the player
        if tonic.playerHit(playerRect):
            gotHitByTonicSound.play()
            score += 50
            if life < MaxLife:
                life += 1
                
        # Check if any of the asteroids have hit the player.
        if asteroid.playerHit(playerRect):
            score -= 10
            life -= 1
            gotHitByAsteroid.play()
            if life <= 0:
                tonic.list.clear()
                tank.list.clear()
                asteroid.list.clear()
                bigShroom.list.clear()
                smallShroom.list.clear()
                if score > topScore:
                    topScore = score # Set new top score.
                break

        # Check if player has hit a mega tank
        if tank.playerHit(playerRect):
            gotHitByMT.play()
            playerMoveRate = 5
            player.height = 35
            player.width = 35
            playerStrechedImage = pygame.transform.scale(playerImage, (player.height, player.width))
            score += 1000
            life += 3
            if life > SuperMaxLife:
                life = SuperMaxLife

        # Check if player has hit Bigshroom
        if bigShroom.playerHit(playerRect):
            gotHitByBigShroom.play()
            score += 20
            playerMoveRate -= 1
            player = pygame.Rect(player.left, player.top, player.width + 2, player.height + 2)
            playerStrechedImage = pygame.transform.scale(playerImage, (player.height, player.width))

        # Check if player has hit Smallshroom
        if smallShroom.playerHit(playerRect):
            gotHitBySmallShroom.play()
            score += 20
            playerMoveRate += 1
            player = pygame.Rect(player.left, player.top, player.width - 2, player.height - 2)
            playerStrechedImage = pygame.transform.scale(playerImage, (player.height, player.width))
            
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
