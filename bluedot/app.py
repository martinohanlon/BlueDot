import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

from argparse import ArgumentParser
import pygame
import sys
from .btcomm import BluetoothAdapter, BluetoothClient
from .constants import PROTOCOL_VERSION
from .colors import BLUE, GRAY43, GRAY86, RED, parse_color

DEFAULTSIZE = (320, 240)
BORDER = 7
FONT = "monospace"
FONTSIZE = 18
FONTPAD = 3

CLIENT_NAME = "Blue Dot Python app"
BORDER_THICKNESS = 0.025

class BlueDotClient:
    def __init__(self, device, server, port, fullscreen, width, height):

        self._device = device
        self._server = server
        self._port = 1 if port is None else port
        self._fullscreen = fullscreen
        
        #init pygame
        pygame.init()

        #load font
        self._font = pygame.font.SysFont(FONT, FONTSIZE)

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

        self._screen = pygame.display.set_mode((width, height), screenflags)

        self._width = width
        self._height = height

        self._run()

        pygame.quit()

    def _run(self):
        # has a server been specified?  If so connected directly
        if self._server:
            button_screen = ButtonScreen(self._screen, self._font, self._device, self._server, self._port, self._width, self._height)
            button_screen.run()
        else:
            # start the devices screen
            devices_screen = DevicesScreen(self._screen, self._font, self._device, self._port, self._width, self._height)
            devices_screen.run()


class BlueDotScreen:
    def __init__(self, screen, font, width, height):
        self.screen = screen
        self.font = font
        self.width = width
        self.height = height

        # setup screen attributes
        self.frame_rect = pygame.Rect(BORDER, BORDER, self.width - (BORDER * 2) - FONTSIZE - FONTPAD, self.height - (BORDER * 2))
        self.close_rect = pygame.Rect(self.width - FONTSIZE - FONTPAD - BORDER, BORDER, FONTSIZE + FONTPAD, FONTSIZE + FONTPAD)

        self.draw_screen()

    def draw_screen(self):
        # set the screen background
        self.screen.fill(GRAY86.rgb)

        self.draw_close_button()

    def draw_close_button(self):
        # draw close button
        pygame.draw.rect(self.screen, BLUE.rgb, self.close_rect, 2)
        pygame.draw.line(self.screen, BLUE.rgb,
                        (self.close_rect[0], self.close_rect[1]),
                        (self.close_rect[0] + self.close_rect[2], self.close_rect[1] + self.close_rect[3]),
                        1)
        pygame.draw.line(self.screen, BLUE.rgb,
                        (self.close_rect[0], self.close_rect[1] + self.close_rect[3]),
                        (self.close_rect[0] + self.close_rect[2], self.close_rect[1]),
                        1)

    def draw_error(self, e):
        message = "Error: {}".format(e)
        print(message)
        self.draw_status_message(message, colour = RED.rgb)

    def draw_status_message(self, message, colour = BLUE.rgb):
        self.screen.fill(GRAY86.rgb, self.frame_rect)
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
    def __init__(self, screen, font, device, port, width, height):
        self.bt_adapter = BluetoothAdapter(device = device)
        self.port = port

        super(DevicesScreen, self).__init__(screen, font, width, height)
        # self.draw_screen()

    def draw_screen(self):
        self.device_rects = []

        super(DevicesScreen, self).draw_screen()

        #title
        title_rect = self.draw_text("Connect", RED.rgb, 0)

        y = title_rect.bottom
        for d in self.bt_adapter.paired_devices:
            device_rect = self.draw_text("{} ({})".format(d[1], d[0]), BLUE.rgb, y, border = True, border_pad = FONTPAD)

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
                            button_screen = ButtonScreen(self.screen, self.font, self.bt_adapter.device, self.bt_adapter.paired_devices[d][0], self.port, self.width, self.height)
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
    def __init__(self, screen, font, device, server, port, width, height):        
        self.device = device
        self.server = server
        self.port = port
        self._data_buffer = ""

        self.last_x = 0
        self.last_y = 0

        self._colour = BLUE
        self._border = False
        self._square = False
        self._visible = True
        self._pressed = False

        super(ButtonScreen, self).__init__(screen, font, width, height)

    def draw_screen(self):
        super(ButtonScreen, self).draw_screen()

        # work out dot position
        self.dot_centre = (int(self.frame_rect.top + (self.frame_rect.width / 2)), int(self.frame_rect.left + (self.frame_rect.height / 2)))
        
        if self.frame_rect.width > self.frame_rect.height:
            self.dot_rect = pygame.Rect(self.frame_rect.left + int((self.frame_rect.width - self.frame_rect.height) / 2), self.frame_rect.top, self.frame_rect.height, self.frame_rect.height)
            self.dot_radius = int(self.dot_rect.height / 2)
        else:
            self.dot_rect = pygame.Rect(self.frame_rect.left, self.frame_rect.top + int((self.frame_rect.height - self.frame_rect.width) / 2), self.frame_rect.width, self.frame_rect.width)
            self.dot_radius = int(self.dot_rect.width / 2)

        self.border_width = max(int(self.dot_rect.width * BORDER_THICKNESS), 1)
        self.border_height = max(int(self.dot_rect.height * BORDER_THICKNESS), 1)

        self._draw_dot()

    def _draw_dot(self):

        # clear the dot

        pygame.draw.rect(
            self.screen,
            GRAY86.rgb, 
            (
                self.dot_rect.left - self.border_width, 
                self.dot_rect.top - self.border_height, 
                self.dot_rect.width + (self.border_width * 2), 
                self.dot_rect.height + (self.border_height * 2), 
            )
        )
        colour = self._colour if not self._pressed else self._colour.get_adjusted_color(0.85)

        # draw the dot
        if self._square:
            if self._visible:
                pygame.draw.rect(self.screen, colour.rgb, self.dot_rect)
            if self._border:
                pygame.draw.rect(self.screen, GRAY43.rgb, self.dot_rect, max(int(self.dot_radius * BORDER_THICKNESS), 1))
        else:
            if self._visible:
                pygame.draw.ellipse(self.screen, colour.rgb, self.dot_rect)
            if self._border:
                pygame.draw.ellipse(self.screen, GRAY43.rgb, self.dot_rect, max(int(self.dot_radius * BORDER_THICKNESS), 1))

    def _process(self, op, pos):
        if self.bt_client.connected:
            x = (pos[0] - self.dot_centre[0]) / float(self.dot_radius)
            x = round(x, 4)
            y = ((pos[1] - self.dot_centre[1]) / float(self.dot_radius)) * -1
            y = round(y, 4)
            message = "{},0,0,{},{}\n".format(op, x, y)
            if op == 2:
                if x != self.last_x or y != self.last_y:
                    self._send_message(message)
            else:
                self._send_message(message)
            self.last_x = x
            self.last_y = y
        else:
            self.draw_error("Blue Dot not connected")

    def _send_protocol_version(self):
        if self.bt_client.connected:
            self._send_message("3,{},{}\n".format(PROTOCOL_VERSION, CLIENT_NAME))
            
    def _send_message(self, message):
        try:
            self.bt_client.send(message)
        except:
            e = str(sys.exc_info()[1])
            self.draw_error(e)

    def _data_received(self, data):
        # add the data received to the buffer
        self._data_buffer += data

        # get any full commands ended by \n
        last_command = self._data_buffer.rfind("\n")
        if last_command != -1:
            commands = self._data_buffer[:last_command].split("\n")
            # remove the processed commands from the buffer
            self._data_buffer = self._data_buffer[last_command + 1:]
            self._process_commands(commands)

    def _process_commands(self, commands):
        for command in commands:
            params = command.split(",")

            invalid_command = False
            if len(params) == 7:

                if params[0] == "4":
                    # currently the python blue dot client only supports 1 button
                    if params[5] != "1" or params[6] != "1":
                        print("Error - The BlueDot python client only supports a single button.")

                    self._colour = parse_color(params[1])
                    self._square = True if params[2] == "1" else False
                    self._border = True if params[3] == "1" else False
                    self._visible = True if params[4] == "1" else False

                    self._draw_dot()

                elif params[0] == "5":
                    if params[5] == "0" and params[6] == "0":
                        
                        self._colour = parse_color(params[1])
                        self._square = True if params[2] == "1" else False
                        self._border = True if params[3] == "1" else False
                        self._visible = True if params[4] == "1" else False                    
                    
                        self._draw_dot()

            else:
                invalid_command = True

            if invalid_command:
                print("Error - Invalid message received '{}'".format(command))
                
    def run(self):

        self._connect()
        self._send_protocol_version()
    
        clock = pygame.time.Clock()
        pygame.event.clear()

        self._pressed = False
        running = True

        while running:
            clock.tick(50)

            ev = pygame.event.get()

            for event in ev:

                # handle mouse
                if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP or (event.type == pygame.MOUSEMOTION and self._pressed):
                    pos = pygame.mouse.get_pos()

                    #circle clicked?
                    if self.dot_rect.collidepoint(pos):

                        if event.type == pygame.MOUSEBUTTONDOWN:
                            self._pressed = True
                            self._draw_dot()
                            self._process(1, pos)

                        elif event.type == pygame.MOUSEBUTTONUP:
                            self._pressed = False
                            self._draw_dot()
                            self._process(0, pos)

                        elif event.type == pygame.MOUSEMOTION:
                            self._process(2, pos)

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

    def _connect(self):
        self.bt_client = BluetoothClient(self.server, self._data_received, port = self.port, device = self.device, auto_connect = False)
        try:
            self.bt_client.connect()
        except:
            e = str(sys.exc_info()[1])
            self.draw_error(e)
        
def main():
    #read command line options
    parser = ArgumentParser(description="Blue Dot Python App")
    parser.add_argument("--device", help="The name of the bluetooth device to use (default is hci0)")
    parser.add_argument("--server", help="The name or mac address of the bluedot server")
    parser.add_argument("--port", help="The port number to use when connecting (default is 1)", type=int)
    parser.add_argument("--fullscreen", help="Fullscreen app", action="store_true")
    parser.add_argument("--width", type=int, help="A custom screen width (default is {})".format(DEFAULTSIZE[0]))
    parser.add_argument("--height", type=int, help="A customer screen height (default is {})".format(DEFAULTSIZE[1]))
    args = parser.parse_args()

    #start the blue dot client
    blue_dot_client = BlueDotClient(args.device, args.server, args.port, args.fullscreen, args.width, args.height)

if __name__ == "__main__":
    main()