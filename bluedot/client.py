from argparse import ArgumentParser
import pygame
import sys
from .btcomm import BluetoothAdapter, BluetoothClient

BLUE = (0, 0, 255)
DARKBLUE = (0, 0, 200)
GREY = (220, 220, 220)
RED = (255, 0, 0)
SIZE = (240, 240)
BUFFER = 7
CLOSERECT = (220, 5, 15, 15)
TITLEPOS = (BUFFER, BUFFER)
FONT = "monospace"
FONTSIZE = 14
LINESPACE = 16
CHARSPERLINE = 26

class BlueDotClient():
    def __init__(self, device, server, fullscreen):
        self.device = device
        if self.device == None: self.device = "hci0"
        
        self.server = server

        #init pygame
        pygame.init()

        #load font
        font = pygame.font.SysFont(FONT, FONTSIZE)

        #setup the screen
        #set the screen caption
        pygame.display.set_caption("Blue Dot")

        #create the screen
        screenflags = 0
        if fullscreen: screenflags = pygame.FULLSCREEN
        screen = pygame.display.set_mode(SIZE, screenflags)

        #has a server been specified?  If so connected directly
        if server:
            button_screen = ButtonScreen(screen, font, device, server)
            button_screen.run()
        else:
            #start the devices screen
            devices_screen = DevicesScreen(screen, font, device)
            devices_screen.run()

        pygame.quit()


class BlueDotScreen(object):
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.draw_screen()
    
    def draw_screen(self):
        #set the screen background
        self.screen.fill(GREY)

        #draw close button
        self.close_rect = pygame.draw.rect(self.screen, BLUE, CLOSERECT, 2)
        pygame.draw.line(self.screen, BLUE,
                        (CLOSERECT[0], CLOSERECT[1]), (CLOSERECT[0] + CLOSERECT[2], CLOSERECT[1] + CLOSERECT[3]),
                        1)
        pygame.draw.line(self.screen, BLUE,
                        (CLOSERECT[0], CLOSERECT[1] + CLOSERECT[3]), (CLOSERECT[0] + CLOSERECT[2], CLOSERECT[1]),
                        1)

    def draw_error(self, e):
        text = "Error:\n{}".format(e)
        print(text)
        self.draw_text(text)

    def draw_text(self, text):
        self.draw_screen()
        current_pos = [BUFFER, BUFFER]
        lines = text.split("\n")
        for line in lines:
            #will this line fit on the screen? if not split it
            for l in [line[i:i+CHARSPERLINE] for i in range(0, len(line), CHARSPERLINE)]:
                l_render = self.font.render(l, 1, RED)
                self.screen.blit(l_render, current_pos)
                current_pos[1] += LINESPACE + BUFFER
                


class DevicesScreen(BlueDotScreen):
    def __init__(self, screen, font, device):
        self.bt_adapter = BluetoothAdapter(device = device)

        super(DevicesScreen, self).__init__(screen, font)
        self.draw_screen()

    def draw_screen(self):
        self.device_rects = []

        super(DevicesScreen, self).draw_screen()

        #title 
        title = self.font.render("Connect", 1, BLUE)
        self.screen.blit(title, TITLEPOS)

        #show bluetooth adapters
        y = BUFFER + LINESPACE + BUFFER
        for d in self.bt_adapter.paired_devices:
            #draw a box
            device_rect = (BUFFER, y, 230, 20)
            pygame.draw.rect(self.screen, BLUE, device_rect, 2)

            #draw the name
            device_name = self.font.render(d[1], 1, BLUE)
            self.screen.blit(device_name, (device_rect[0] + BUFFER, device_rect[1], device_rect[2], device_rect[3]))
            self.device_rects.append(pygame.Rect(device_rect))

            y += LINESPACE + BUFFER

    def run(self):
        clock = pygame.time.Clock()
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
                            # show the button
                            button_screen = ButtonScreen(self.screen, self.font, self.bt_adapter.device, self.bt_adapter.paired_devices[d][0])
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
    def __init__(self, screen, font, device, server):
        super(ButtonScreen, self).__init__(screen, font)

        self.device = device
        self.server = server

    def draw_screen(self):
        super(ButtonScreen, self).draw_screen()

        self._draw_circle(BLUE)

    def _draw_circle(self, colour):
        #draw the circle
        self.circle_centre = (int(SIZE[0] / 2), int(SIZE[1] / 2))
        self.circle_radius = (int(SIZE[0] / 2)) - (BUFFER * 2)
        self.circle_rect = pygame.draw.circle(self.screen, colour, self.circle_centre, self.circle_radius, 0)

    def _send_message(self, op, pos):
        if self.bt_client.connected:
            x = (pos[0] - self.circle_centre[0]) / self.circle_radius
            y = ((pos[1] - self.circle_centre[1]) / self.circle_radius) * -1
            message = "{},{},{}\n".format(op, x, y)
            try:
                self.bt_client.send(message)
            except:
                e = str(sys.exc_info()[1])
                self.draw_error(e)
        else:
            self.draw_error("Blue Dot not connected")
            
    def run(self):
        
        self.bt_client = BluetoothClient(self.server, None, device = self.device, auto_connect = False)
        try:
            self.bt_client.connect()
        except:
            e = str(sys.exc_info()[1])
            self.draw_error(e)
    
        clock = pygame.time.Clock()
        pygame.event.clear()
        
        mouse_pressed = False
        running = True
        while running:
            clock.tick(50)

            ev = pygame.event.get()

            for event in ev:
                
                # handle mouse
                if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP or (event.type == pygame.MOUSEMOTION and mouse_pressed):
                    pos = pygame.mouse.get_pos()

                    #circle clicked?
                    if self.circle_rect.collidepoint(pos):

                        if event.type == pygame.MOUSEBUTTONDOWN:
                            mouse_pressed = True
                            self._draw_circle(DARKBLUE)
                            self._send_message(1, pos)
                            
                        elif event.type == pygame.MOUSEBUTTONUP:
                            mouse_pressed = False
                            self._draw_circle(BLUE)
                            self._send_message(0, pos)
                        
                        elif event.type == pygame.MOUSEMOTION:
                            self._send_message(2, pos)
                
                    #close clicked?
                    if self.close_rect.collidepoint(pos):
                        running = False
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

                if event.type == pygame.QUIT:
                    running = False
                    
            pygame.display.update()
            
        self.bt_client.disconnect()

if __name__ == "__main__":
    #read command line options
    parser = ArgumentParser(description="Blue Dot Python Client")
    parser.add_argument("--device", help="The name of the bluetooth device to use (default is hci0)")
    parser.add_argument("--server", help="The name or mac address of the bluedot server")
    parser.add_argument("--fullscreen", help="Fullscreen app", action="store_true")
    args = parser.parse_args()

    #start the blue dot client
    blue_dot_client = BlueDotClient(args.device, args.server, args.fullscreen)


