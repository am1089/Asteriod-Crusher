import pygame, random, sys
from pygame.locals import *

windowWidth = 600
windowHeight = 600
textColor = (0, 0, 255)
backgroundColor = (0, 0, 0)
FPS = 40
tonicSize = 20
tonicMinSpeed = 4
tonicMaxSpeed = 5
addTonicRate = 18
asteriodMinSize = 20
asteriodMaxSize = 40
asteriodMinSpeed = 2
asteriodMaxSpeed = 8
addNewAsteriodRate = 14
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

def playerHasHitAsteriod(playerRect, asteriods):
    for a in asteriods:
        if playerRect.colliderect(a['rect']):
            return True
    return False

def playerHasHitTonic(playerRect, tonics):
    for t in tonics:
        if playerrect.colliderect(t['rect']):
            retrun True
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
pygame.display.set_caption('Asteriod')

# Set up the fonts.
font = pygame.font.SysFont(None, 48)

# Set up sounds.
gameOverSound = pygame.mixer.Sound('gameover.wav')
pygame.mixer.music.load('background.mid')

# Set up images.
playerImage = pygame.image.load('spaceship.png')
playerStrechedImage = pygame.transform.scale(playerImage, (40, 40))
playerRect = playerStrechedImage.get_rect()
asteriodImage = pygame.image.load('baddie.png')
tonicImage = pygame.image.load('goody1.png')

# Show the "Start" screen.
windowSurface.fill(backgroundColor)
drawText('Asteriod', font, windowSurface, (windowWidth / 3),
       (windowHeight / 3))
drawText('Press a key to start.', font, windowSurface,
       (windowWidth / 3) - 30, (windowHeight / 3) + 50)
pygame.display.update()
waitForPlayerToPressKey()

topScore = 0
while True:
    # Set up the start of the game.
    asteriods = []
    tonics = []
    score = 0
    playerRect.topleft = (windowWidth / 2, windowHeight - 50)
    moveLeft = moveRight = moveUp = moveDown = False
    reverseCheat = slowCheat = False
    tonicAddCounter = 0
    asteriodAddCounter = 0
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

        # Add new asteriods at the right of the screen
        if not reverseCheat and not slowCheat:
            asteriodAddCounter += 1
        if asteriodAddCounter == addNewAsteriodRate:
            asteriodAddCounter = 0
            asteriodSize = random.randint(asteriodMinSize, asteriodMaxSize)
            newAsteriod = {'rect': pygame.Rect(windowWidth, random.randint(0, windowHeight - asteriodSize), asteriodSize, asteriodSize),
                         'speed': random.randint(asteriodMinSpeed, asteriodMaxSpeed),
                         'surface':pygame.transform.scale(asteriodImage, (asteriodSize, asteriodSize)),}

            asteriods.append(newAsteriod)
        
        # Add new asteriods at the right of the screen
        if not reverseCheat and not slowCheat:
            tonicAddCounter += 1
        if tonicAddCounter == addNewTonicRate:
            tonicAddCounter = 0
            tonicSize = tonicSize
            newTonic = {'rect': pygame.Rect(windowWidth, random.randint(0, windowHeight - tonicSize), tonicSize, tonicSize),
                        'speed': random.randint(tonicMinSize, tonicMaxSize),
                        'surface':pygame.transform.scale(tonicImage, (tonicSize, tonicSize)),}
            
            asteriods.append(newTonic)

        # Move the player around.
        if moveLeft and playerRect.left > 0:
            playerRect.move_ip(-1 * playerMoveRate, 0)
        if moveRight and playerRect.right < windowWidth:
            playerRect.move_ip(playerMoveRate, 0)
        if moveUp and playerRect.top > 0:
            playerRect.move_ip(0, -1 * playerMoveRate)
        if moveDown and playerRect.bottom < windowHeight:
            playerRect.move_ip(0, playerMoveRate)

        # Move the asteriods left
        for a in asteriods:
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
        
        # Delete asteriods that have fallen past the bottom.
        for a in asteriods[:]:
            if a['rect'].top > windowHeight:
                asteriods.remove(a)
        
        # Delete tonics that have fallen past the bottom
        for t in tonics[:]:
            if t['rect'].top > windowHeight:
                tonics.remove(t)

        # Draw the game world on the window.
        windowSurface.fill(backgroundColor)

        # Draw the score and top score.
        drawText('Score: %s' % (score), font, windowSurface, 10, 0)
        drawText('Top Score: %s' % (topScore), font, windowSurface,
               10, 40)

        # Draw the player's rectangle.
        windowSurface.blit(playerStrechedImage, playerRect)

        # Draw each baddie.
        for a in asteriods:
            windowSurface.blit(a['surface'], a['rect'])

        pygame.display.update()
        
        # Draw each tonic
        for t in tonics:
            windowSurface.blit(t['surface'], t['rect'])
           
        pygame.display.update()

        # Check if any of the asteriods have hit the player.
        if playerHasHitAsteriod(playerRect, asteriods):
            if score > topScore:
                topScore = score # Set new top score.
            break

        mainClock.tick(FPS)
        
        # Check if any of the tonics have hit the player
        if playerHasHitTonic(playerRect, tonics):
            score += 10
            if score > topScore:
                topScore = score
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

