import pygame, requests, os, ctypes, webbrowser, pygame.gfxdraw

#SETUP ---------------------------------------------------------------

def setup():

    global cbuttons
    cbuttons = []

    pygame.init()

    global icons
    icons = [pygame.image.load("assets/hammer.png"), pygame.image.load("assets/hammer64.png")]

    pygame.display.set_icon(icons[0])
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("clarence112.mps")

    open('downloads/officialpacks.txt', 'wb').write(requests.get('http://clarencecraft.ddns.net:8000/officialpacks.txt', allow_redirects=True).content)

    global font
    font = [pygame.font.Font("assets/rubik.ttf", 24), pygame.font.Font("assets/rubik.ttf", 24), pygame.font.Font("assets/Anton-Regular.ttf", 8), pygame.font.Font("assets/BowlbyOneSC-Regular.ttf", 80), pygame.font.Font("assets/rubik.ttf", 16)]
    font[1].set_bold(True)

    global clock
    clock = pygame.time.Clock()

    global stage
    stage = 0

    global packurl
    packurl = ""

    if(not(os.path.exists("downloads"))):
        os.mkdir("downloads")

    if(os.path.exists("C:/Program Files (x86)/Minecraft/runtime")):
        global screen
        size = width, height = 850, 500
        screen = pygame.display.set_mode(size)
        pygame.display.set_caption("MDP")
    else:
        ctypes.windll.user32.MessageBoxW(0, "Uh oh, you don't have Minecraft installed!", "Error", 0)
        stage = "close"

#BUTTON --------------------------------------------------------------

def makeBttn(action, textinput, x = 0, y = 0, bgcolor = [0, 0, 0], key = 1, textcolor = [255, 255, 255], fonttype = 0, aa = True, fancy = True):
    textsize = list(pygame.font.Font.size(font[fonttype], textinput))  # lint:ok
    if fancy:
        pygame.gfxdraw.aacircle(screen, x, y + int(textsize[1] / 2), int(textsize[1] / 2), bgcolor)
        pygame.gfxdraw.filled_circle(screen, x, y + int(textsize[1] / 2), int(textsize[1] / 2), bgcolor)
        pygame.gfxdraw.aacircle(screen, x + textsize[0] + 10, y + int(textsize[1] / 2), int(textsize[1] / 2), bgcolor)
        pygame.gfxdraw.filled_circle(screen, x + textsize[0] + 10, y + int(textsize[1] / 2), int(textsize[1] / 2), bgcolor)
    pygame.draw.rect(screen, bgcolor, pygame.Rect((x, y), (textsize[0] + 10, int(textsize[1] / 2) * 2 + 1)))
    textrend(textinput, x + 5, y, textcolor, fonttype, aa)
    global cbuttons
    cbuttons.append([action, x, y, x + textsize[0] + 10, y + textsize[1], key])

#CLICKABLE AREA ------------------------------------------------------

def makeRegion(action, x = 0, y = 0, w = 10, h = 10, key = 1):
    global cbuttons
    cbuttons.append([action, x, y, x + w, y + h, key])

#DRAW TEXT -----------------------------------------------------------

def textrend(textinput, x = 0, y = 0, textcolor = [255, 255, 255], fonttype = 0, aa = True):
    textSuface = font[fonttype].render(textinput, aa, textcolor)  # lint:ok
    screen.blit(textSuface,(x, y))

#CHECK BUTTONS -------------------------------------------------------

def bttnChk(x, y, key):
    global cbuttons
    for button in cbuttons:
        if (button[1] <= x <= button[3]) and (button[2] <= y <= button[4]) and (key == button[5]):
            exec(button[0])

#DRAW THE TOP BAR ----------------------------------------------------

def drawTopBar():
    pygame.draw.rect(screen, 0x333333, pygame.Rect((0, 0), (850, 70)))
    textrend("MDP", 80, 20, fonttype = 1)
    screen.blit(icons[1], (13,3))
    textsize = pygame.font.Font.size(font[1], "MDP")
    makeRegion("webbrowser.open_new_tab('http://clarencecraft.ddns.net:8000/modpackDistroPlatform/')", 13, 3, textsize[0] + 80, 70)

#DRAW FOOTER ---------------------------------------------------------

def drawFooter():
    pygame.draw.rect(screen, 0x333333, pygame.Rect((0, 482), (850, 70)))
    makeBttn("webbrowser.open_new_tab('https://github.com/clarence112/ModpackDistributionPlatform')", "MDP was made by clarence112", 3, 485, [51, 51, 51], fonttype = 2)

#DRAW STAGE 0 --------------------------------------------------------

def drawWelcomeScreen():
    pass

#DRAW ERRORS ---------------------------------------------------------

def drawError(problem = "Something went wrong!", soulution = "Whatever it was, there isn't a specific error message for it so it's probs really bad...", title = "Error!", crash = "and burn"):
    textrend(title, 6, 50, [255, 255, 255], fonttype = 3)
    textrend(problem, 6, 150)
    textrend(soulution, 6, 180, fonttype = 4)
    if crash == "and burn":
        makeBttn("global stage; stage = 'close'", "Quit MDP", 450, 445, [255, 51, 102], fonttype = 1)
        makeBttn("global stage; stage = 'close'; webbrowser.open_new_tab('https://github.com/clarence112/ModpackDistributionPlatform/issues')", "File Bug Report", 616, 445, [255, 51, 102], fonttype = 1)
    if crash == "no":
        makeBttn("global stage; stage = 0", "Retry", 745, 445, [255, 51, 102], fonttype = 1)

#COMMON CODE FOR ALL STAGES ------------------------------------------

def commonstart():
    screen.fill(0x363C3D)
    global cbuttons
    cbuttons = []
    clock.tick(10)

def commonend():
    drawTopBar()
    drawFooter()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            global stage
            stage = "close"
        if event.type == pygame.MOUSEBUTTONUP:
            bttnChk(event.pos[0], event.pos[1], event.button)

    pygame.display.flip()


#MAIN CODE SECTION ---------------------------------------------------

setup()

stage = "error0"

while(not(stage == "close")):

    commonstart()

    if stage == 0:
        drawWelcomeScreen()

    if stage == "error0":
        drawError("The URL source or .modpack file is corrupted!", "Please check the file or URL and try again.", crash = "no")

    commonend()