from argparse import ArgumentParser
import pygame
import sys
from .btcomm import BluetoothAdapter, BluetoothClient

#colours
BLUE = (0, 0, 255)
DARKBLUE = (0, 0, 200)
GREY = (220, 220, 220)
RED = (255, 0, 0)

DEFAULTSIZE = (320, 240)
BORDER = 7
FONT = "monospace"
FONTSIZE = 18
FONTPAD = 3

class BlueDotClient():
    def __init__(self, device, server, fullscreen, width, height):

        #init pygame
        pygame.init()

        #load font
        font = pygame.font.SysFont(FONT, FONTSIZE)

        #setup the screen
        #set the screen caption
        pygame.display.set_caption("Blue Dot")

        #create the screen
        screenflags = 0
        
        if fullscreen:
            screenflags = pygame.FULLSCREEN
            if width == None and height == None:
                display_info = pygame.display.Info()
                width = display_info.current_w
                height = display_info.current_h

        if width == None: width = DEFAULTSIZE[0]
        if height == None: height = DEFAULTSIZE[1]
        
        screen = pygame.display.set_mode((width, height), screenflags)

        #has a server been specified?  If so connected directly
        if server:
            button_screen = ButtonScreen(screen, font, device, server, width, height)
            button_screen.run()
        else:
            #start the devices screen
            devices_screen = DevicesScreen(screen, font, device, width, height)
            devices_screen.run()

        pygame.quit()

class BlueDotScreen(object):
    def __init__(self, screen, font, width, height):
        self.screen = screen
        self.font = font
        self.width = width
        self.height = height

        #setup screen attributes
        self.frame_rect = pygame.Rect(BORDER, BORDER, self.width - (BORDER * 2), self.height - (BORDER * 2))
        self.close_rect = pygame.Rect(self.width - FONTSIZE - FONTPAD - BORDER, BORDER, FONTSIZE + FONTPAD, FONTSIZE + FONTPAD)

        self.draw_screen()
    
    def draw_screen(self):
        #set the screen background
        self.screen.fill(GREY)

        self.draw_close_button()
        
    def draw_close_button(self):
        #draw close button
        pygame.draw.rect(self.screen, BLUE, self.close_rect, 2)
        pygame.draw.line(self.screen, BLUE,
                        (self.close_rect[0], self.close_rect[1]),
                        (self.close_rect[0] + self.close_rect[2], self.close_rect[1] + self.close_rect[3]),
                        1)
        pygame.draw.line(self.screen, BLUE,
                        (self.close_rect[0], self.close_rect[1] + self.close_rect[3]),
                        (self.close_rect[0] + self.close_rect[2], self.close_rect[1]),
                        1)
        
    def draw_error(self, e):
        message = "Error: {}".format(e)
        print(message)
        self.draw_status_message(message, colour = RED)

    def draw_status_message(self, message, colour = BLUE):
        self.screen.fill(GREY, self.frame_rect)
        self.draw_close_button()
        self.draw_text(message, colour, self.frame_rect.height / 2, border = True, border_pad = FONTPAD)
        pygame.display.update()

    def draw_text(self, text, colour, start_y, antiaalias=False, background=None, border=False, border_width=1, border_pad=0):
        rect = pygame.Rect(self.frame_rect)
        y = rect.top + start_y + border_pad
        lineSpacing = -2

        # get the height of the font
        fontHeight = self.font.size("Tg")[1]

        while text:
            i = 1

            # determine if the row of text will be outside our area
            if y + fontHeight > rect.bottom:
                break

            # determine maximum width of line
            while self.font.size(text[:i])[0] < (rect.width - (border_pad * 2)) and i < len(text):
                i += 1

            # if we've wrapped the text, then adjust the wrap to the last word      
            if i < len(text): 
                i = text.rfind(" ", 0, i) + 1

            # render the line and blit it to the surface
            if background:
                image = self.font.render(text[:i], 1, colour, background)
                image.set_colorkey(background)
            else:
                image = self.font.render(text[:i], antiaalias, colour)

            self.screen.blit(image, (rect.left + border_pad, y))
            y += fontHeight + lineSpacing + border_pad

            # remove the text we just blitted
            text = text[i:]

        #return the rect the text was drawn in
        rect.top = rect.top + start_y
        rect.height = y - start_y
    
        if border:
            pygame.draw.rect(self.screen, colour, rect, border_width)

        return rect

class DevicesScreen(BlueDotScreen):
    def __init__(self, screen, font, device, width, height):
        self.bt_adapter = BluetoothAdapter(device = device)

        super(DevicesScreen, self).__init__(screen, font, width, height)
        #self.draw_screen()

    def draw_screen(self):
        self.device_rects = []

        super(DevicesScreen, self).draw_screen()

        #title
        title_rect = self.draw_text("Connect", RED, 0)

        y = title_rect.bottom
        for d in self.bt_adapter.paired_devices:
            device_rect = self.draw_text("{} ({})".format(d[1], d[0]), BLUE, y, border = True, border_pad = FONTPAD)
    
            self.device_rects.append(pygame.Rect(device_rect))

            y = device_rect.bottom

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
                            self.draw_status_message("Connecting")
                            button_screen = ButtonScreen(self.screen, self.font, self.bt_adapter.device, self.bt_adapter.paired_devices[d][0], self.width, self.height)
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
    def __init__(self, screen, font, device, server, width, height):
        super(ButtonScreen, self).__init__(screen, font, width, height)

        self.device = device
        self.server = server

    def draw_screen(self):
        super(ButtonScreen, self).draw_screen()

        self._draw_circle(BLUE)

    def _draw_circle(self, colour):
        #draw the circle
        self.circle_centre = (int(self.frame_rect.top + (self.frame_rect.width / 2)), int(self.frame_rect.left + (self.frame_rect.height / 2)))
        if self.frame_rect.width > self.frame_rect.height:
            self.circle_radius = int(self.frame_rect.height / 2)
        else:
            self.circle_radius = int(self.frame_rect.width / 2)
        
        self.circle_rect = pygame.draw.circle(self.screen, colour, self.circle_centre, self.circle_radius, 0)

    def _send_message(self, op, pos):
        if self.bt_client.connected:
            x = (pos[0] - self.circle_centre[0]) / float(self.circle_radius)
            y = ((pos[1] - self.circle_centre[1]) / float(self.circle_radius)) * -1
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
    parser = ArgumentParser(description="Blue Dot Python App")
    parser.add_argument("--device", help="The name of the bluetooth device to use (default is hci0)")
    parser.add_argument("--server", help="The name or mac address of the bluedot server")
    parser.add_argument("--fullscreen", help="Fullscreen app", action="store_true")
    parser.add_argument("--width", type=int, help="A custom screen width (default is {})".format(DEFAULTSIZE[0]))
    parser.add_argument("--height", type=int, help="A customer screen height (default is {})".format(DEFAULTSIZE[1]))
    args = parser.parse_args()

    #start the blue dot client
    blue_dot_client = BlueDotClient(args.device, args.server, args.fullscreen, args.width, args.height)


