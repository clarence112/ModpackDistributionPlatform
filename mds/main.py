from tkinter import *
import pygame, requests, os, ctypes, webbrowser, pygame.gfxdraw, pygame_textinput, tkinter, tkinter.constants, tkinter.filedialog

#SETUP ---------------------------------------------------------------

def setup():

    global ranStageInit
    ranStageInit = "nope"

    global events
    events = []

    global cbuttons
    cbuttons = []

    pygame.init()

    global icons
    icons = [pygame.image.load("assets/hammer.png"), pygame.image.load("assets/hammer64.png")]

    pygame.display.set_icon(icons[0])
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("clarence112.mps")

    try:
        open('downloads/officialpacks.txt', 'wb').write(requests.get('http://clarencecraft.ddns.net:8000/officialpacks.txt', allow_redirects=True).content)
    except:
         print("Pack list server down.")

    try:
        global officialPackList
        with open("downloads/officialpacks.txt") as f:
                officialPackList = f.read().splitlines()
    except:
        print("Pack list missing.")
        officialPackList = ["No packs", "No packs"]

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
    screen.blit(icons[1], (9,3))
    textsize = pygame.font.Font.size(font[1], "MDP")
    makeRegion("webbrowser.open_new_tab('http://clarencecraft.ddns.net:8000/modpackDistroPlatform/')", 13, 3, textsize[0] + 80, 70)

#DRAW FOOTER ---------------------------------------------------------

def drawFooter():
    pygame.draw.rect(screen, 0x333333, pygame.Rect((0, 482), (850, 70)))
    makeBttn("webbrowser.open_new_tab('https://github.com/clarence112/ModpackDistributionPlatform')", "MDP was made by clarence112", 3, 485, [51, 51, 51], fonttype = 2, fancy = False)

#GET TEXT WIDTH ------------------------------------------------------

def twidth(tinput, fonttype):
    return(pygame.font.Font.size(font[fonttype], tinput)[0])

#DRAW STAGE 0 --------------------------------------------------------

def drawWelcomeScreen():

    #URL bar
    if textinput.update(events):
         global stage;
         stage = 1
         global packurl
         packurl = textinput.get_text()
    pygame.draw.rect(screen, 0xffffff, pygame.Rect((0, 100), (850, 21)))

    if(twidth(textinput.get_text(), 4) > 680):
        screen.blit(textinput.get_surface(), (10 - (twidth(textinput.get_text(), 4) - 680), 100))
    else:
        screen.blit(textinput.get_surface(), (10, 100))

    if(textinput.get_text() == ""):
        textrend("Paste or type mopack URL here!", 12, 101, [150, 150, 150], 4)
    makeBttn("global stage; stage = 1; global packurl; packurl = textinput.get_text()", "Install Modpack", 710, 100, [255, 51, 102], fonttype = 4)

    #Featured box
    textrend("Featured modpacks:", 10, 130)

    for i in list(range(14)):
        if (i % 2) == 0:
            pygame.draw.rect(screen, 0xffffff, pygame.Rect((10, 21 * i + 170), (410, 21)))
        else:
            pygame.draw.rect(screen, 0xeeeeee, pygame.Rect((10, 21 * i + 170), (410, 21)))

    if(len(officialPackList) > 28):

        for i in list(range(14)):
            bfunc = "global textinput; textinput = pygame_textinput.TextInput(font_family = 'assets/rubik.ttf', font_size = 16, initial_string = '" + officialPackList[(i + scroll) * 2 + 1] + "')"
            if (i % 2) == 0:
                makeBttn(bfunc, officialPackList[(i + scroll) * 2], 10, 21 * i + 170, [255, 255, 255], textcolor = [0, 0, 0], fonttype = 4, fancy = 0)
            else:
                makeBttn(bfunc, officialPackList[(i + scroll) * 2], 10, 21 * i + 170, [238, 238, 238], textcolor = [0, 0, 0], fonttype = 4, fancy = 0)
    else:
        for i in list(range(int(len(officialPackList) / 2))):
            bfunc = "global textinput; textinput = pygame_textinput.TextInput(font_family = 'assets/rubik.ttf', font_size = 16, initial_string = '" + officialPackList[i * 2 + 1] + "')"
            if (i % 2) == 0:
                makeBttn(bfunc, officialPackList[i * 2], 10, 21 * i + 170, [255, 255, 255], textcolor = [0, 0, 0], fonttype = 4, fancy = 0)
            else:
                makeBttn(bfunc, officialPackList[i * 2], 10, 21 * i + 170, [238, 238, 238], textcolor = [0, 0, 0], fonttype = 4, fancy = 0)

    pygame.draw.rect(screen, 0xaaaaaa, pygame.Rect((378, 170), (42, 42)))
    pygame.draw.rect(screen, 0xaaaaaa, pygame.Rect((378, 422), (42, 42)))

    if(len(officialPackList) > 28):
        if(scroll > 0):
            makeRegion("global scroll; scroll = scroll - 1", 378, 170, 42, 42)
            pygame.draw.polygon(screen, 0x333333, [[399, 170], [378, 212], [420, 212]])

        if(((len(officialPackList) / 2) - scroll) > 14):
            makeRegion("global scroll; scroll = scroll + 1", 378, 422, 42, 42)
            pygame.draw.polygon(screen, 0x333333, [[378, 422], [399, 464], [420, 422]])

#DRAW ERRORS ---------------------------------------------------------

def drawError(problem = "Something went wrong!", soulution = "Whatever it was, there isn't a specific error message for it so it's probs really bad...", title = "Error!", crash = "and burn"):
    textrend(title, 6, 50, [255, 255, 255], fonttype = 3)
    textrend(problem, 6, 150)
    textrend(soulution, 6, 180, fonttype = 4)
    if crash == "and burn":
        makeBttn("global stage; stage = 'close'", "Quit MDP", 450, 445, [255, 51, 102], fonttype = 1)
        makeBttn("global textinput; stage = 'close'; webbrowser.open_new_tab('https://github.com/clarence112/ModpackDistributionPlatform/issues')", "File Bug Report", 616, 445, [255, 51, 102], fonttype = 1)
    if crash == "no":
        makeBttn("global stage; stage = 0", "Retry", 745, 445, [255, 51, 102], fonttype = 1)

#COMMON CODE FOR ALL STAGES ------------------------------------------

def folderselect():
    root = Tk()
    root.withdraw()
    return(tkinter.filedialog.askdirectory())


def commonstart():
    screen.fill(0x363C3D)
    global cbuttons
    cbuttons = []
    clock.tick(10)

def commonend():
    drawTopBar()
    drawFooter()

    global events
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            global stage
            stage = "close"
        if event.type == pygame.MOUSEBUTTONUP:
            bttnChk(event.pos[0], event.pos[1], event.button)

    pygame.display.flip()


#MAIN CODE SECTION ---------------------------------------------------

setup()

scroll = 0

#stage = "error0"

global stage
while(not(stage == "close")):

    commonstart()

    if stage == 0:

        if(not(ranStageInit == 0)):
            ranStageInit = 0
            global textinput
            textinput = pygame_textinput.TextInput(font_family = "assets/rubik.ttf", font_size = 16)

        drawWelcomeScreen()

    if stage == 1:
        if(not(ranStageInit == 1)):
            ranStageInit = 1
            if(not(packurl == "")):
                global httpcode
                try:
                    modpfile = requests.get(packurl, allow_redirects=False)
                    httpcode = modpfile.status_code
                except requests.exceptions.InvalidSchema:
                    httpcode = "INVALID_URL"
                except requests.exceptions.ConnectionError:
                    httpcode = "CONNECTION_TIMEOUT"

                if httpcode == 200:
                    open("downloads/pack.modpack", "wb").write(modpfile.content)
                    stage = "verif"
                else:
                    stage = "errorhttp"
            else:
                stage = 0

        drawError("MDP is downloading the source list... ", "", "Please wait.", "nope")

    if stage == "verif":
        if(not(ranStageInit == "verif")):
            ranStageInit = "verif"
            with open("downloads/pack.modpack") as f:
                packToInstall = f.read().splitlines()

            if("MCVERSION:" in packToInstall) and ("MODPACKNAME:" in packToInstall) and ("FORGEVERSION:" in packToInstall) and ("MODSOURCES:" in packToInstall):
                pass
            else:
                stage = "error0"

    if stage == "error0":
        #drawError()
        drawError("The URL source or .modpack file is corrupted!", "Please check the file or URL and try again.", crash = "no")

    if stage == "errorhttp":
        drawError("There's somthing wrong with the pack URL", "Got error " + str(httpcode) + ", please check your URL and try again.", crash = "no")

    commonend()