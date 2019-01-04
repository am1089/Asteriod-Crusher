import pygame, random, sys
from pygame.locals import *

windowWidth = 600
windowHeight = 600
textColor = (0, 0, 255)
backgroundColor = (0, 0, 0)
FPS = 20
tonicSize = 40
tonicMinSpeed = 4
tonicMaxSpeed = 5
addTonicRate = 20
asteroidMinSize = 20
asteroidMaxSize = 40
asteroidMinSpeed = 2
asteroidMaxSpeed = 8
addNewAsteroidRate = 14
playerMoveRate = 5
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

def playerHasHitAsteroid(playerRect, asteroids):
    for a in asteroids:
        if playerRect.colliderect(a['rect']):
            asteroids.remove(a)
            return True
    return False

def playerHasHitTonic(playerRect, tonics):
    for t in tonics:
        if playerRect.colliderect(t['rect']):
            #print('Collide with Tonic')
            tonics.remove(t)
            return True
    return False

def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, textColor)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# Set up pygame, the window, and the mouse cursor.
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption('Asteroid')

# Set up the fonts.
font = pygame.font.SysFont(None, 48)

# Set up sounds.
gameOverSound = pygame.mixer.Sound('gameover.wav')
pygame.mixer.music.load('background.mid')

# Set up images.
playerImage = pygame.image.load('spaceship.jpg')
playerStrechedImage = pygame.transform.scale(playerImage, (40, 40))
playerRect = playerStrechedImage.get_rect()
asteroidImage = pygame.image.load('baddie.png')
tonicImage = pygame.image.load('goody-1.png')

# Show the "Start" screen.
windowSurface.fill(backgroundColor)
drawText('Asteroid', font, windowSurface, (windowWidth / 3),
       (windowHeight / 3))
drawText('Press a key to start.', font, windowSurface,
       (windowWidth / 3) - 30, (windowHeight / 3) + 50)
pygame.display.update()
#print('Start Game')
waitForPlayerToPressKey()

topScore = 0
while True:
    # Set up the start of the game.
    asteroids = []
    tonics = []
    score = 0
    life = 1
    playerRect.topleft = (windowWidth / 2, windowHeight - 50)
    moveLeft = moveRight = moveUp = moveDown = False
    reverseCheat = slowCheat = False
    tonicAddCounter = 0
    asteroidAddCounter = 0
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
        if not reverseCheat and not slowCheat:
            asteroidAddCounter += 1
        if asteroidAddCounter == addNewAsteroidRate:
            asteroidAddCounter = 0
            asteroidSize = random.randint(asteroidMinSize, asteroidMaxSize)
            newAsteroid = {'rect': pygame.Rect(windowWidth, random.randint(0, windowHeight - asteroidSize), asteroidSize, asteroidSize),
                         'speed': random.randint(asteroidMinSpeed, asteroidMaxSpeed),
                         'surface':pygame.transform.scale(asteroidImage, (asteroidSize, asteroidSize)),}

            asteroids.append(newAsteroid)
        
        # Add new tonics at the right of the screen
        if not reverseCheat and not slowCheat:
            tonicAddCounter += 1
        if tonicAddCounter == addTonicRate:
            tonicAddCounter = 0
            tonicSize = tonicSize
            newTonic = {'rect': pygame.Rect(windowWidth, random.randint(0, windowHeight - tonicSize), tonicSize, tonicSize),
                        'speed': random.randint(tonicMinSpeed, tonicMaxSpeed),
                        'surface':pygame.transform.scale(tonicImage, (tonicSize, tonicSize)),}
            
            tonics.append(newTonic)

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
        for a in asteroids:
            if not reverseCheat and not slowCheat:
                a['rect'].move_ip(-a['speed'], 0)
            elif reverseCheat:
                a['rect'].move_ip(5, 0)
            elif slowCheat:
                a['rect'].move_ip(-1, 0)
                
        # Move the tonics left
        for t in tonics:
            if not reverseCheat and not slowCheat:
                t['rect'].move_ip(-t['speed'], 0)
            elif reverseCheat:
                t['rect'].move_ip(5, 0)
            elif slowCheat:
                t['rect'].move_ip(-1, 0)
        
        # Delete asteroids that have fallen past the bottom.
        for a in asteroids[:]:
            if a['rect'].top > windowHeight:
                asteroids.remove(a)
        
        # Delete tonics that have fallen past the bottom
        for t in tonics[:]:
           # print("Checking...")
            if t['rect'].left < 0:
                tonics.remove(t)
               # print("Removed tonic")

        # Draw the game world on the window.
        windowSurface.fill(backgroundColor)

        # Draw the score and top score.
        drawText('Score: %s' % (score), font, windowSurface, 10, 0)
        drawText('Top Score: %s' % (topScore), font, windowSurface,
               10, 40)

        # Draw the player's rectangle.
        windowSurface.blit(playerStrechedImage, playerRect)

        # Draw each baddie.
        for a in asteroids:
            windowSurface.blit(a['surface'], a['rect'])

        pygame.display.update()
        
        # Draw each tonic
        for t in tonics:
            windowSurface.blit(t['surface'], t['rect'])
           
        pygame.display.update()

        # Check if any of the tonics have hit the player
        if playerHasHitTonic(playerRect, tonics):
            life += 1
            #tonics.remove(t)
           # print('Life = ' + str(life))

        # Check if any of the asteroids have hit the player.
        if playerHasHitAsteroid(playerRect, asteroids):
            life -= 1
            if life <= 0:
                if score > topScore:
                    topScore = score # Set new top score.
                break

        mainClock.tick(FPS)
        

    # Stop the game and show the "Game Over" screen.
    pygame.mixer.music.stop()
    gameOverSound.play()

    drawText('GAME OVER', font, windowSurface, (windowWidth / 3),
           (windowHeight / 3))
    drawText('Press a key to play again.', font, windowSurface,
           (windowWidth / 3) - 80, (windowHeight / 3) + 50)
    pygame.display.update()
    waitForPlayerToPressKey()

gameOverSound.stop()
