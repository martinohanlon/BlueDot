from argparse import ArgumentParser
from signal import pause
import pygame
from bluedot.btcomm import BluetoothAdapter, BluetoothClient

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GREY = (220, 220, 220)
SIZE = (240, 240)
BUFFER = 7
CLOSERECT = (220, 5, 15, 15)
TITLEPOS = (BUFFER, BUFFER)
FONT = "monospace"
FONTSIZE = 14
LINESPACE = 16

class BlueDotScreen():
    def __init__(self):
        self.draw_screen()
    
    def draw_screen(self):
        #set the screen background
        screen.fill(GREY)

        #draw close button
        self.close_rect = pygame.draw.rect(screen, BLUE, CLOSERECT, 2)
        pygame.draw.line(screen, BLUE,
                        (CLOSERECT[0], CLOSERECT[1]), (CLOSERECT[0] + CLOSERECT[2], CLOSERECT[1] + CLOSERECT[3]),
                        1)
        pygame.draw.line(screen, BLUE,
                        (CLOSERECT[0], CLOSERECT[1] + CLOSERECT[3]), (CLOSERECT[0] + CLOSERECT[2], CLOSERECT[1]),
                        1)

class DevicesScreen(BlueDotScreen):
    def __init__(self):
        self.bt_adapter = BluetoothAdapter()

        super(DevicesScreen, self).__init__()
        self.draw_screen()

    def draw_screen(self):
        self.device_rects = []

        super(DevicesScreen, self).draw_screen()

        #title 
        title = myfont.render("Connect", 1, BLUE)
        screen.blit(title, TITLEPOS)

        #show bluetooth adapters
        y = BUFFER + LINESPACE + BUFFER
        for d in self.bt_adapter.paired_devices:
            #draw a box
            device_rect = (BUFFER, y, 230, 20)
            pygame.draw.rect(screen, BLUE, device_rect, 2)

            #draw the name
            device_name = myfont.render(d[1], 1, BLUE)
            screen.blit(device_name, (device_rect[0] + BUFFER, device_rect[1], device_rect[2], device_rect[3]))
            self.device_rects.append(pygame.Rect(device_rect))

            y += LINESPACE + BUFFER

    def run(self):
        running = True
        while running:
            clock.tick(50)

            ev = pygame.event.get()

            for event in ev:

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    
                    #has a device been clicked?
                    for d in range(len(self.device_rects)):
                        if self.device_rects[d].collidepoint(pos):
                            print(self.bt_adapter.paired_devices[d])
                            # show the button
                            button_screen = ButtonScreen(self.bt_adapter.paired_devices[d][0])
                            button_screen.run()

                            #redraw the screen
                            self.draw_screen()

                    if self.close_rect.collidepoint(pos):
                        running = False
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

                if event.type == pygame.QUIT:
                    running = False
                    
            pygame.display.update()

class ButtonScreen(BlueDotScreen):
    def __init__(self, server):
        super(ButtonScreen, self).__init__()

        self.server = server

    def draw_screen(self):
        super(ButtonScreen, self).draw_screen()

        #draw the circle
        circle_centre = (int(SIZE[0] / 2), int(SIZE[1] / 2))
        circle_radius = (int(SIZE[0] / 2)) - (BUFFER * 2)
        circle_rect = pygame.draw.circle(screen, BLUE, circle_centre, circle_radius, 0)

    def run(self):
        running = True
        while running:
            clock.tick(50)

            ev = pygame.event.get()

            for event in ev:

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()

                    #has the dot been clicked

                    if self.close_rect.collidepoint(pos):
                        running = False
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

                if event.type == pygame.QUIT:
                    running = False
                    
            pygame.display.update()


#read command line options
parser = ArgumentParser(description="Blue Dot Python App")
parser.add_argument("--server", help="The name or mac address of the bluedot server")
parser.add_argument("--device", help="The name of the bluetooth device to use (default is hci0)")
parser.add_argument("--fullscreen", help="Fullscreen app", action="store_true")
args = parser.parse_args()

#init pygame
pygame.init()

#load font
myfont = pygame.font.SysFont(FONT, FONTSIZE)

#setup the screen
#set the screen caption
pygame.display.set_caption("Blue Dot App")

clock = pygame.time.Clock()

#create the screen
screenflags = 0
if args.fullscreen: screenflags = pygame.FULLSCREEN
screen = pygame.display.set_mode(SIZE, screenflags)

#start the devices screen
devices_screen = DevicesScreen()
devices_screen.run()

pygame.quit()
