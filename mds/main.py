import pygame, requests, os, ctypes
pygame.init()

pygame.display.set_icon(pygame.image.load("assets/hammer.png"))
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("clarence112.mps")

open('downloads/officialpacks.txt', 'wb').write(requests.get('http://clarencecraft.ddns.net:8000/officialpacks.txt', allow_redirects=True).content)

font = pygame.font.Font("assets/rubik.ttf", 24)

stage = 0
packurl = ""

def textrend(textinput, x = 0, y = 0, textcolor = [255, 255, 255], aa = True):
    textSuface = font.render(textinput, aa, textcolor)  # lint:ok
    screen.blit(textSuface,(x, y))

def drawWelcomeScreen():
    if stage == 0:
        textrend("test")

if(os.path.exists("C:/Program Files (x86)/Minecraft/runtime")):
    size = width, height = 850, 500
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("MDP")
    test = 1

    while test == 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                test = 0
        screen.fill(0x333333)
        drawWelcomeScreen()
        pygame.display.flip()
else:
    ctypes.windll.user32.MessageBoxW(0, "Uh oh, you don't have Minecraft installed!", "Error", 0)
