# color codes obtained from https://www.webucator.com/blog/2015/03/python-color-constants-module/

class Color:
    """
    Represents a color within bluedot. Used to change the color of the dot.

    Color objects are immutable.

    :param int red:
        The red value of the color `0 - 255`. Default is `255`.

    :param int green:
        The green value of the color `0 - 255`. Default is `255`.

    :param int green:
        The blue value of the color `0 - 255`. Default is `255`.

    :param int green:
        The alpha value of the color `0 - 255`. `0` is transparent. Default 
        is `255`.
    """
    def __init__(self, red = 255, green = 255, blue = 255, alpha = 255):
        self._red = red
        self._green = green
        self._blue = blue
        self._alpha = alpha

    @property
    def red(self):
        """
        Returns the red value of the color.
        """
        return self._red

    @property
    def green(self):
        """
        Returns the green value of the color.
        """
        return self._green

    @property
    def blue(self):
        """
        Returns the blue value of the color.
        """
        return self._blue

    @property
    def alpha(self):
        """
        Returns the alpha value of the color.
        """
        return self._alpha

    @property
    def rgb(self):
        """
        Returns a tuple of `(red, green, blue)` values.
        """
        return (self._red, self._green, self._blue)

    @property
    def rgba(self):
        """
        Returns a tuple of `(red, green, blue, alpha)` values.
        """
        return (self._red, self._green, self._blue, self._alpha)

    @property
    def str_rgb(self):
        """
        Returns a string of red, green, blue hex values in the format
        `#rrggbb`.
        """
        return '#%02x%02x%02x' % (self._red, self._green, self._blue)

    @property
    def str_rgba(self):
        """
        Returns a string of red, green, blue, alpha hex values in the format
        `#rrggbbaa`.
        """
        return '#%02x%02x%02x%02x' % (self._red, self._green, self._blue, self._alpha)

    @property
    def str_argb(self):
        """
        Returns a string of alpha, red, green, blue hex values in the format
        `#aarrggbb`.
        """
        return '#%02x%02x%02x%02x' % (self._alpha, self._red, self._green, self._blue)

    def get_adjusted_color(self, factor):
        """
        Returns a new Color object based on this Color adjusted by a factor

        :param float factor:
            The value to adjust this color by. 
        """
        return Color(self.red * factor, self.green * factor, self.blue * factor)

    def __eq__(self, other):
        other = parse_color(other)
        return self._red == other._red and self._green == other._green and self._blue == other._blue and self._alpha == other._alpha

    def __str__(self):
        return self.str_rgba

ALICEBLUE = Color(240, 248, 255)
ANTIQUEWHITE = Color(250, 235, 215)
ANTIQUEWHITE1 = Color(255, 239, 219)
ANTIQUEWHITE2 = Color(238, 223, 204)
ANTIQUEWHITE3 = Color(205, 192, 176)
ANTIQUEWHITE4 = Color(139, 131, 120)
AQUA = Color(0, 255, 255)
AQUAMARINE1 = Color(127, 255, 212)
AQUAMARINE2 = Color(118, 238, 198)
AQUAMARINE3 = Color(102, 205, 170)
AQUAMARINE4 = Color(69, 139, 116)
AZURE1 = Color(240, 255, 255)
AZURE2 = Color(224, 238, 238)
AZURE3 = Color(193, 205, 205)
AZURE4 = Color(131, 139, 139)
BANANA = Color(227, 207, 87)
BEIGE = Color(245, 245, 220)
BISQUE1 = Color(255, 228, 196)
BISQUE2 = Color(238, 213, 183)
BISQUE3 = Color(205, 183, 158)
BISQUE4 = Color(139, 125, 107)
BLACK = Color(0, 0, 0)
BLANCHEDALMOND = Color(255, 235, 205)
BLUE = Color(0, 0, 255)
BLUE2 = Color(0, 0, 238)
BLUE3 = Color(0, 0, 205)
BLUE4 = Color(0, 0, 139)
BLUEVIOLET = Color(138, 43, 226)
BRICK = Color(156, 102, 31)
BROWN = Color(165, 42, 42)
BROWN1 = Color(255, 64, 64)
BROWN2 = Color(238, 59, 59)
BROWN3 = Color(205, 51, 51)
BROWN4 = Color(139, 35, 35)
BURLYWOOD = Color(222, 184, 135)
BURLYWOOD1 = Color(255, 211, 155)
BURLYWOOD2 = Color(238, 197, 145)
BURLYWOOD3 = Color(205, 170, 125)
BURLYWOOD4 = Color(139, 115, 85)
BURNTSIENNA = Color(138, 54, 15)
BURNTUMBER = Color(138, 51, 36)
CADETBLUE = Color(95, 158, 160)
CADETBLUE1 = Color(152, 245, 255)
CADETBLUE2 = Color(142, 229, 238)
CADETBLUE3 = Color(122, 197, 205)
CADETBLUE4 = Color(83, 134, 139)
CADMIUMORANGE = Color(255, 97, 3)
CADMIUMYELLOW = Color(255, 153, 18)
CARROT = Color(237, 145, 33)
CHARTREUSE1 = Color(127, 255, 0)
CHARTREUSE2 = Color(118, 238, 0)
CHARTREUSE3 = Color(102, 205, 0)
CHARTREUSE4 = Color(69, 139, 0)
CHOCOLATE = Color(210, 105, 30)
CHOCOLATE1 = Color(255, 127, 36)
CHOCOLATE2 = Color(238, 118, 33)
CHOCOLATE3 = Color(205, 102, 29)
CHOCOLATE4 = Color(139, 69, 19)
COBALT = Color(61, 89, 171)
COBALTGREEN = Color(61, 145, 64)
COLDGREY = Color(128, 138, 135)
CORAL = Color(255, 127, 80)
CORAL1 = Color(255, 114, 86)
CORAL2 = Color(238, 106, 80)
CORAL3 = Color(205, 91, 69)
CORAL4 = Color(139, 62, 47)
CORNFLOWERBLUE = Color(100, 149, 237)
CORNSILK1 = Color(255, 248, 220)
CORNSILK2 = Color(238, 232, 205)
CORNSILK3 = Color(205, 200, 177)
CORNSILK4 = Color(139, 136, 120)
CRIMSON = Color(220, 20, 60)
CYAN1 = Color(0, 238, 238)
CYAN2 = Color(0, 205, 205)
CYAN3 = Color(0, 139, 139)
DARKGOLDENROD = Color(184, 134, 11)
DARKGOLDENROD1 = Color(255, 185, 15)
DARKGOLDENROD2 = Color(238, 173, 14)
DARKGOLDENROD3 = Color(205, 149, 12)
DARKGOLDENROD4 = Color(139, 101, 8)
DARKGRAY = Color(169, 169, 169)
DARKGREEN = Color(0, 100, 0)
DARKKHAKI = Color(189, 183, 107)
DARKOLIVEGREEN = Color(85, 107, 47)
DARKOLIVEGREEN1 = Color(202, 255, 112)
DARKOLIVEGREEN2 = Color(188, 238, 104)
DARKOLIVEGREEN3 = Color(162, 205, 90)
DARKOLIVEGREEN4 = Color(110, 139, 61)
DARKORANGE = Color(255, 140, 0)
DARKORANGE1 = Color(255, 127, 0)
DARKORANGE2 = Color(238, 118, 0)
DARKORANGE3 = Color(205, 102, 0)
DARKORANGE4 = Color(139, 69, 0)
DARKORCHID = Color(153, 50, 204)
DARKORCHID1 = Color(191, 62, 255)
DARKORCHID2 = Color(178, 58, 238)
DARKORCHID3 = Color(154, 50, 205)
DARKORCHID4 = Color(104, 34, 139)
DARKSALMON = Color(233, 150, 122)
DARKSEAGREEN = Color(143, 188, 143)
DARKSEAGREEN1 = Color(193, 255, 193)
DARKSEAGREEN2 = Color(180, 238, 180)
DARKSEAGREEN3 = Color(155, 205, 155)
DARKSEAGREEN4 = Color(105, 139, 105)
DARKSLATEBLUE = Color(72, 61, 139)
DARKSLATEGRAY = Color(47, 79, 79)
DARKSLATEGRAY1 = Color(151, 255, 255)
DARKSLATEGRAY2 = Color(141, 238, 238)
DARKSLATEGRAY3 = Color(121, 205, 205)
DARKSLATEGRAY4 = Color(82, 139, 139)
DARKTURQUOISE = Color(0, 206, 209)
DARKVIOLET = Color(148, 0, 211)
DEEPPINK1 = Color(255, 20, 147)
DEEPPINK2 = Color(238, 18, 137)
DEEPPINK3 = Color(205, 16, 118)
DEEPPINK4 = Color(139, 10, 80)
DEEPSKYBLUE1 = Color(0, 191, 255)
DEEPSKYBLUE2 = Color(0, 178, 238)
DEEPSKYBLUE3 = Color(0, 154, 205)
DEEPSKYBLUE4 = Color(0, 104, 139)
DIMGRAY = Color(105, 105, 105)
DODGERBLUE1 = Color(30, 144, 255)
DODGERBLUE2 = Color(28, 134, 238)
DODGERBLUE3 = Color(24, 116, 205)
DODGERBLUE4 = Color(16, 78, 139)
EGGSHELL = Color(252, 230, 201)
EMERALDGREEN = Color(0, 201, 87)
FIREBRICK = Color(178, 34, 34)
FIREBRICK1 = Color(255, 48, 48)
FIREBRICK2 = Color(238, 44, 44)
FIREBRICK3 = Color(205, 38, 38)
FIREBRICK4 = Color(139, 26, 26)
FLESH = Color(255, 125, 64)
FLORALWHITE = Color(255, 250, 240)
FORESTGREEN = Color(34, 139, 34)
GAINSBORO = Color(220, 220, 220)
GHOSTWHITE = Color(248, 248, 255)
GOLD1 = Color(255, 215, 0)
GOLD2 = Color(238, 201, 0)
GOLD3 = Color(205, 173, 0)
GOLD4 = Color(139, 117, 0)
GOLDENROD = Color(218, 165, 32)
GOLDENROD1 = Color(255, 193, 37)
GOLDENROD2 = Color(238, 180, 34)
GOLDENROD3 = Color(205, 155, 29)
GOLDENROD4 = Color(139, 105, 20)
GRAY = Color(128, 128, 128)
GRAY1 = Color(3, 3, 3)
GRAY10 = Color(26, 26, 26)
GRAY11 = Color(28, 28, 28)
GRAY12 = Color(31, 31, 31)
GRAY13 = Color(33, 33, 33)
GRAY14 = Color(36, 36, 36)
GRAY15 = Color(38, 38, 38)
GRAY16 = Color(41, 41, 41)
GRAY17 = Color(43, 43, 43)
GRAY18 = Color(46, 46, 46)
GRAY19 = Color(48, 48, 48)
GRAY2 = Color(5, 5, 5)
GRAY20 = Color(51, 51, 51)
GRAY21 = Color(54, 54, 54)
GRAY22 = Color(56, 56, 56)
GRAY23 = Color(59, 59, 59)
GRAY24 = Color(61, 61, 61)
GRAY25 = Color(64, 64, 64)
GRAY26 = Color(66, 66, 66)
GRAY27 = Color(69, 69, 69)
GRAY28 = Color(71, 71, 71)
GRAY29 = Color(74, 74, 74)
GRAY3 = Color(8, 8, 8)
GRAY30 = Color(77, 77, 77)
GRAY31 = Color(79, 79, 79)
GRAY32 = Color(82, 82, 82)
GRAY33 = Color(84, 84, 84)
GRAY34 = Color(87, 87, 87)
GRAY35 = Color(89, 89, 89)
GRAY36 = Color(92, 92, 92)
GRAY37 = Color(94, 94, 94)
GRAY38 = Color(97, 97, 97)
GRAY39 = Color(99, 99, 99)
GRAY4 = Color(10, 10, 10)
GRAY40 = Color(102, 102, 102)
GRAY42 = Color(107, 107, 107)
GRAY43 = Color(110, 110, 110)
GRAY44 = Color(112, 112, 112)
GRAY45 = Color(115, 115, 115)
GRAY46 = Color(117, 117, 117)
GRAY47 = Color(120, 120, 120)
GRAY48 = Color(122, 122, 122)
GRAY49 = Color(125, 125, 125)
GRAY5 = Color(13, 13, 13)
GRAY50 = Color(127, 127, 127)
GRAY51 = Color(130, 130, 130)
GRAY52 = Color(133, 133, 133)
GRAY53 = Color(135, 135, 135)
GRAY54 = Color(138, 138, 138)
GRAY55 = Color(140, 140, 140)
GRAY56 = Color(143, 143, 143)
GRAY57 = Color(145, 145, 145)
GRAY58 = Color(148, 148, 148)
GRAY59 = Color(150, 150, 150)
GRAY6 = Color(15, 15, 15)
GRAY60 = Color(153, 153, 153)
GRAY61 = Color(156, 156, 156)
GRAY62 = Color(158, 158, 158)
GRAY63 = Color(161, 161, 161)
GRAY64 = Color(163, 163, 163)
GRAY65 = Color(166, 166, 166)
GRAY66 = Color(168, 168, 168)
GRAY67 = Color(171, 171, 171)
GRAY68 = Color(173, 173, 173)
GRAY69 = Color(176, 176, 176)
GRAY7 = Color(18, 18, 18)
GRAY70 = Color(179, 179, 179)
GRAY71 = Color(181, 181, 181)
GRAY72 = Color(184, 184, 184)
GRAY73 = Color(186, 186, 186)
GRAY74 = Color(189, 189, 189)
GRAY75 = Color(191, 191, 191)
GRAY76 = Color(194, 194, 194)
GRAY77 = Color(196, 196, 196)
GRAY78 = Color(199, 199, 199)
GRAY79 = Color(201, 201, 201)
GRAY8 = Color(20, 20, 20)
GRAY80 = Color(204, 204, 204)
GRAY81 = Color(207, 207, 207)
GRAY82 = Color(209, 209, 209)
GRAY83 = Color(212, 212, 212)
GRAY84 = Color(214, 214, 214)
GRAY85 = Color(217, 217, 217)
GRAY86 = Color(219, 219, 219)
GRAY87 = Color(222, 222, 222)
GRAY88 = Color(224, 224, 224)
GRAY89 = Color(227, 227, 227)
GRAY9 = Color(23, 23, 23)
GRAY90 = Color(229, 229, 229)
GRAY91 = Color(232, 232, 232)
GRAY92 = Color(235, 235, 235)
GRAY93 = Color(237, 237, 237)
GRAY94 = Color(240, 240, 240)
GRAY95 = Color(242, 242, 242)
GRAY97 = Color(247, 247, 247)
GRAY98 = Color(250, 250, 250)
GRAY99 = Color(252, 252, 252)
GREEN = Color(0, 128, 0)
GREEN1 = Color(0, 255, 0)
GREEN2 = Color(0, 238, 0)
GREEN3 = Color(0, 205, 0)
GREEN4 = Color(0, 139, 0)
GREENYELLOW = Color(173, 255, 47)
HONEYDEW1 = Color(240, 255, 240)
HONEYDEW2 = Color(224, 238, 224)
HONEYDEW3 = Color(193, 205, 193)
HONEYDEW4 = Color(131, 139, 131)
HOTPINK = Color(255, 105, 180)
HOTPINK1 = Color(255, 110, 180)
HOTPINK2 = Color(238, 106, 167)
HOTPINK3 = Color(205, 96, 144)
HOTPINK4 = Color(139, 58, 98)
INDIANRED = Color(176, 23, 31)
INDIANRED = Color(205, 92, 92)
INDIANRED1 = Color(255, 106, 106)
INDIANRED2 = Color(238, 99, 99)
INDIANRED3 = Color(205, 85, 85)
INDIANRED4 = Color(139, 58, 58)
INDIGO = Color(75, 0, 130)
IVORY1 = Color(255, 255, 240)
IVORY2 = Color(238, 238, 224)
IVORY3 = Color(205, 205, 193)
IVORY4 = Color(139, 139, 131)
IVORYBLACK = Color(41, 36, 33)
KHAKI = Color(240, 230, 140)
KHAKI1 = Color(255, 246, 143)
KHAKI2 = Color(238, 230, 133)
KHAKI3 = Color(205, 198, 115)
KHAKI4 = Color(139, 134, 78)
LAVENDER = Color(230, 230, 250)
LAVENDERBLUSH1 = Color(255, 240, 245)
LAVENDERBLUSH2 = Color(238, 224, 229)
LAVENDERBLUSH3 = Color(205, 193, 197)
LAVENDERBLUSH4 = Color(139, 131, 134)
LAWNGREEN = Color(124, 252, 0)
LEMONCHIFFON1 = Color(255, 250, 205)
LEMONCHIFFON2 = Color(238, 233, 191)
LEMONCHIFFON3 = Color(205, 201, 165)
LEMONCHIFFON4 = Color(139, 137, 112)
LIGHTBLUE = Color(173, 216, 230)
LIGHTBLUE1 = Color(191, 239, 255)
LIGHTBLUE2 = Color(178, 223, 238)
LIGHTBLUE3 = Color(154, 192, 205)
LIGHTBLUE4 = Color(104, 131, 139)
LIGHTCORAL = Color(240, 128, 128)
LIGHTCYAN1 = Color(224, 255, 255)
LIGHTCYAN2 = Color(209, 238, 238)
LIGHTCYAN3 = Color(180, 205, 205)
LIGHTCYAN4 = Color(122, 139, 139)
LIGHTGOLDENROD1 = Color(255, 236, 139)
LIGHTGOLDENROD2 = Color(238, 220, 130)
LIGHTGOLDENROD3 = Color(205, 190, 112)
LIGHTGOLDENROD4 = Color(139, 129, 76)
LIGHTGOLDENRODYELLOW = Color(250, 250, 210)
LIGHTGREY = Color(211, 211, 211)
LIGHTPINK = Color(255, 182, 193)
LIGHTPINK1 = Color(255, 174, 185)
LIGHTPINK2 = Color(238, 162, 173)
LIGHTPINK3 = Color(205, 140, 149)
LIGHTPINK4 = Color(139, 95, 101)
LIGHTSALMON1 = Color(255, 160, 122)
LIGHTSALMON2 = Color(238, 149, 114)
LIGHTSALMON3 = Color(205, 129, 98)
LIGHTSALMON4 = Color(139, 87, 66)
LIGHTSEAGREEN = Color(32, 178, 170)
LIGHTSKYBLUE = Color(135, 206, 250)
LIGHTSKYBLUE1 = Color(176, 226, 255)
LIGHTSKYBLUE2 = Color(164, 211, 238)
LIGHTSKYBLUE3 = Color(141, 182, 205)
LIGHTSKYBLUE4 = Color(96, 123, 139)
LIGHTSLATEBLUE = Color(132, 112, 255)
LIGHTSLATEGRAY = Color(119, 136, 153)
LIGHTSTEELBLUE = Color(176, 196, 222)
LIGHTSTEELBLUE1 = Color(202, 225, 255)
LIGHTSTEELBLUE2 = Color(188, 210, 238)
LIGHTSTEELBLUE3 = Color(162, 181, 205)
LIGHTSTEELBLUE4 = Color(110, 123, 139)
LIGHTYELLOW1 = Color(255, 255, 224)
LIGHTYELLOW2 = Color(238, 238, 209)
LIGHTYELLOW3 = Color(205, 205, 180)
LIGHTYELLOW4 = Color(139, 139, 122)
LIMEGREEN = Color(50, 205, 50)
LINEN = Color(250, 240, 230)
MAGENTA = Color(255, 0, 255)
MAGENTA2 = Color(238, 0, 238)
MAGENTA3 = Color(205, 0, 205)
MAGENTA4 = Color(139, 0, 139)
MANGANESEBLUE = Color(3, 168, 158)
MAROON = Color(128, 0, 0)
MAROON1 = Color(255, 52, 179)
MAROON2 = Color(238, 48, 167)
MAROON3 = Color(205, 41, 144)
MAROON4 = Color(139, 28, 98)
MEDIUMORCHID = Color(186, 85, 211)
MEDIUMORCHID1 = Color(224, 102, 255)
MEDIUMORCHID2 = Color(209, 95, 238)
MEDIUMORCHID3 = Color(180, 82, 205)
MEDIUMORCHID4 = Color(122, 55, 139)
MEDIUMPURPLE = Color(147, 112, 219)
MEDIUMPURPLE1 = Color(171, 130, 255)
MEDIUMPURPLE2 = Color(159, 121, 238)
MEDIUMPURPLE3 = Color(137, 104, 205)
MEDIUMPURPLE4 = Color(93, 71, 139)
MEDIUMSEAGREEN = Color(60, 179, 113)
MEDIUMSLATEBLUE = Color(123, 104, 238)
MEDIUMSPRINGGREEN = Color(0, 250, 154)
MEDIUMTURQUOISE = Color(72, 209, 204)
MEDIUMVIOLETRED = Color(199, 21, 133)
MELON = Color(227, 168, 105)
MIDNIGHTBLUE = Color(25, 25, 112)
MINT = Color(189, 252, 201)
MINTCREAM = Color(245, 255, 250)
MISTYROSE1 = Color(255, 228, 225)
MISTYROSE2 = Color(238, 213, 210)
MISTYROSE3 = Color(205, 183, 181)
MISTYROSE4 = Color(139, 125, 123)
MOCCASIN = Color(255, 228, 181)
NAVAJOWHITE1 = Color(255, 222, 173)
NAVAJOWHITE2 = Color(238, 207, 161)
NAVAJOWHITE3 = Color(205, 179, 139)
NAVAJOWHITE4 = Color(139, 121, 94)
NAVY = Color(0, 0, 128)
OLDLACE = Color(253, 245, 230)
OLIVE = Color(128, 128, 0)
OLIVEDRAB = Color(107, 142, 35)
OLIVEDRAB1 = Color(192, 255, 62)
OLIVEDRAB2 = Color(179, 238, 58)
OLIVEDRAB3 = Color(154, 205, 50)
OLIVEDRAB4 = Color(105, 139, 34)
ORANGE = Color(255, 128, 0)
ORANGE1 = Color(255, 165, 0)
ORANGE2 = Color(238, 154, 0)
ORANGE3 = Color(205, 133, 0)
ORANGE4 = Color(139, 90, 0)
ORANGERED1 = Color(255, 69, 0)
ORANGERED2 = Color(238, 64, 0)
ORANGERED3 = Color(205, 55, 0)
ORANGERED4 = Color(139, 37, 0)
ORCHID = Color(218, 112, 214)
ORCHID1 = Color(255, 131, 250)
ORCHID2 = Color(238, 122, 233)
ORCHID3 = Color(205, 105, 201)
ORCHID4 = Color(139, 71, 137)
PALEGOLDENROD = Color(238, 232, 170)
PALEGREEN = Color(152, 251, 152)
PALEGREEN1 = Color(154, 255, 154)
PALEGREEN2 = Color(144, 238, 144)
PALEGREEN3 = Color(124, 205, 124)
PALEGREEN4 = Color(84, 139, 84)
PALETURQUOISE1 = Color(187, 255, 255)
PALETURQUOISE2 = Color(174, 238, 238)
PALETURQUOISE3 = Color(150, 205, 205)
PALETURQUOISE4 = Color(102, 139, 139)
PALEVIOLETRED = Color(219, 112, 147)
PALEVIOLETRED1 = Color(255, 130, 171)
PALEVIOLETRED2 = Color(238, 121, 159)
PALEVIOLETRED3 = Color(205, 104, 137)
PALEVIOLETRED4 = Color(139, 71, 93)
PAPAYAWHIP = Color(255, 239, 213)
PEACHPUFF1 = Color(255, 218, 185)
PEACHPUFF2 = Color(238, 203, 173)
PEACHPUFF3 = Color(205, 175, 149)
PEACHPUFF4 = Color(139, 119, 101)
PEACOCK = Color(51, 161, 201)
PINK = Color(255, 192, 203)
PINK1 = Color(255, 181, 197)
PINK2 = Color(238, 169, 184)
PINK3 = Color(205, 145, 158)
PINK4 = Color(139, 99, 108)
PLUM = Color(221, 160, 221)
PLUM1 = Color(255, 187, 255)
PLUM2 = Color(238, 174, 238)
PLUM3 = Color(205, 150, 205)
PLUM4 = Color(139, 102, 139)
POWDERBLUE = Color(176, 224, 230)
PURPLE = Color(128, 0, 128)
PURPLE1 = Color(155, 48, 255)
PURPLE2 = Color(145, 44, 238)
PURPLE3 = Color(125, 38, 205)
PURPLE4 = Color(85, 26, 139)
RASPBERRY = Color(135, 38, 87)
RAWSIENNA = Color(199, 97, 20)
RED = Color(255, 0, 0)
RED1 = Color(238, 0, 0)
RED2 = Color(205, 0, 0)
RED3 = Color(139, 0, 0)
RED4 = Color(125, 0, 0)
ROSYBROWN = Color(188, 143, 143)
ROSYBROWN1 = Color(255, 193, 193)
ROSYBROWN2 = Color(238, 180, 180)
ROSYBROWN3 = Color(205, 155, 155)
ROSYBROWN4 = Color(139, 105, 105)
ROYALBLUE = Color(65, 105, 225)
ROYALBLUE1 = Color(72, 118, 255)
ROYALBLUE2 = Color(67, 110, 238)
ROYALBLUE3 = Color(58, 95, 205)
ROYALBLUE4 = Color(39, 64, 139)
SALMON = Color(250, 128, 114)
SALMON1 = Color(255, 140, 105)
SALMON2 = Color(238, 130, 98)
SALMON3 = Color(205, 112, 84)
SALMON4 = Color(139, 76, 57)
SANDYBROWN = Color(244, 164, 96)
SAPGREEN = Color(48, 128, 20)
SEAGREEN1 = Color(84, 255, 159)
SEAGREEN2 = Color(78, 238, 148)
SEAGREEN3 = Color(67, 205, 128)
SEAGREEN4 = Color(46, 139, 87)
SEASHELL1 = Color(255, 245, 238)
SEASHELL2 = Color(238, 229, 222)
SEASHELL3 = Color(205, 197, 191)
SEASHELL4 = Color(139, 134, 130)
SEPIA = Color(94, 38, 18)
SGIBEET = Color(142, 56, 142)
SGIBRIGHTGRAY = Color(197, 193, 170)
SGICHARTREUSE = Color(113, 198, 113)
SGIDARKGRAY = Color(85, 85, 85)
SGIGRAY12 = Color(30, 30, 30)
SGIGRAY16 = Color(40, 40, 40)
SGIGRAY32 = Color(81, 81, 81)
SGIGRAY36 = Color(91, 91, 91)
SGIGRAY52 = Color(132, 132, 132)
SGIGRAY56 = Color(142, 142, 142)
SGIGRAY72 = Color(183, 183, 183)
SGIGRAY76 = Color(193, 193, 193)
SGIGRAY92 = Color(234, 234, 234)
SGIGRAY96 = Color(244, 244, 244)
SGILIGHTBLUE = Color(125, 158, 192)
SGILIGHTGRAY = Color(170, 170, 170)
SGIOLIVEDRAB = Color(142, 142, 56)
SGISALMON = Color(198, 113, 113)
SGISLATEBLUE = Color(113, 113, 198)
SGITEAL = Color(56, 142, 142)
SIENNA = Color(160, 82, 45)
SIENNA1 = Color(255, 130, 71)
SIENNA2 = Color(238, 121, 66)
SIENNA3 = Color(205, 104, 57)
SIENNA4 = Color(139, 71, 38)
SILVER = Color(192, 192, 192)
SKYBLUE = Color(135, 206, 235)
SKYBLUE1 = Color(135, 206, 255)
SKYBLUE2 = Color(126, 192, 238)
SKYBLUE3 = Color(108, 166, 205)
SKYBLUE4 = Color(74, 112, 139)
SLATEBLUE = Color(106, 90, 205)
SLATEBLUE1 = Color(131, 111, 255)
SLATEBLUE2 = Color(122, 103, 238)
SLATEBLUE3 = Color(105, 89, 205)
SLATEBLUE4 = Color(71, 60, 139)
SLATEGRAY = Color(112, 128, 144)
SLATEGRAY1 = Color(198, 226, 255)
SLATEGRAY2 = Color(185, 211, 238)
SLATEGRAY3 = Color(159, 182, 205)
SLATEGRAY4 = Color(108, 123, 139)
SNOW1 = Color(255, 250, 250)
SNOW2 = Color(238, 233, 233)
SNOW3 = Color(205, 201, 201)
SNOW4 = Color(139, 137, 137)
SPRINGGREEN = Color(0, 255, 127)
SPRINGGREEN1 = Color(0, 238, 118)
SPRINGGREEN2 = Color(0, 205, 102)
SPRINGGREEN3 = Color(0, 139, 69)
STEELBLUE = Color(70, 130, 180)
STEELBLUE1 = Color(99, 184, 255)
STEELBLUE2 = Color(92, 172, 238)
STEELBLUE3 = Color(79, 148, 205)
STEELBLUE4 = Color(54, 100, 139)
TAN = Color(210, 180, 140)
TAN1 = Color(255, 165, 79)
TAN2 = Color(238, 154, 73)
TAN3 = Color(205, 133, 63)
TAN4 = Color(139, 90, 43)
TEAL = Color(0, 128, 128)
THISTLE = Color(216, 191, 216)
THISTLE1 = Color(255, 225, 255)
THISTLE2 = Color(238, 210, 238)
THISTLE3 = Color(205, 181, 205)
THISTLE4 = Color(139, 123, 139)
TOMATO1 = Color(255, 99, 71)
TOMATO2 = Color(238, 92, 66)
TOMATO3 = Color(205, 79, 57)
TOMATO4 = Color(139, 54, 38)
TURQUOISE = Color(64, 224, 208)
TURQUOISE1 = Color(0, 245, 255)
TURQUOISE2 = Color(0, 229, 238)
TURQUOISE3 = Color(0, 197, 205)
TURQUOISE4 = Color(0, 134, 139)
TURQUOISEBLUE = Color(0, 199, 140)
VIOLET = Color(238, 130, 238)
VIOLETRED = Color(208, 32, 144)
VIOLETRED1 = Color(255, 62, 150)
VIOLETRED2 = Color(238, 58, 140)
VIOLETRED3 = Color(205, 50, 120)
VIOLETRED4 = Color(139, 34, 82)
WARMGREY = Color(128, 128, 105)
WHEAT = Color(245, 222, 179)
WHEAT1 = Color(255, 231, 186)
WHEAT2 = Color(238, 216, 174)
WHEAT3 = Color(205, 186, 150)
WHEAT4 = Color(139, 126, 102)
WHITE = Color(255, 255, 255)
WHITESMOKE = Color(245, 245, 245)
WHITESMOKE = Color(245, 245, 245)
YELLOW = Color(255, 255, 0)
YELLOW1 = Color(255, 255, 0)
YELLOW2 = Color(238, 238, 0)
YELLOW3 = Color(205, 205, 0)
YELLOW4 = Color(139, 139, 0)

COLORS = {}

# Add colors to colors dictionary
COLORS["aliceblue"] = ALICEBLUE
COLORS["antiquewhite"] = ANTIQUEWHITE
COLORS["antiquewhite1"] = ANTIQUEWHITE1
COLORS["antiquewhite2"] = ANTIQUEWHITE2
COLORS["antiquewhite3"] = ANTIQUEWHITE3
COLORS["antiquewhite4"] = ANTIQUEWHITE4
COLORS["aqua"] = AQUA
COLORS["aquamarine"] = AQUAMARINE1
COLORS["aquamarine1"] = AQUAMARINE1
COLORS["aquamarine2"] = AQUAMARINE2
COLORS["aquamarine3"] = AQUAMARINE3
COLORS["aquamarine4"] = AQUAMARINE4
COLORS["azure"] = AZURE1
COLORS["azure1"] = AZURE1
COLORS["azure2"] = AZURE2
COLORS["azure3"] = AZURE3
COLORS["azure4"] = AZURE4
COLORS["banana"] = BANANA
COLORS["beige"] = BEIGE
COLORS["bisque"] = BISQUE1
COLORS["bisque1"] = BISQUE1
COLORS["bisque2"] = BISQUE2
COLORS["bisque3"] = BISQUE3
COLORS["bisque4"] = BISQUE4
COLORS["black"] = BLACK
COLORS["blanchedalmond"] = BLANCHEDALMOND
COLORS["blue"] = BLUE
COLORS["blue1"] = BLUE
COLORS["blue2"] = BLUE2
COLORS["blue3"] = BLUE3
COLORS["blue4"] = BLUE4
COLORS["blueviolet"] = BLUEVIOLET
COLORS["brick"] = BRICK
COLORS["brown"] = BROWN
COLORS["brown1"] = BROWN1
COLORS["brown2"] = BROWN2
COLORS["brown3"] = BROWN3
COLORS["brown4"] = BROWN4
COLORS["burlywood"] = BURLYWOOD
COLORS["burlywood1"] = BURLYWOOD1
COLORS["burlywood2"] = BURLYWOOD2
COLORS["burlywood3"] = BURLYWOOD3
COLORS["burlywood4"] = BURLYWOOD4
COLORS["burntsienna"] = BURNTSIENNA
COLORS["burntumber"] = BURNTUMBER
COLORS["cadetblue"] = CADETBLUE
COLORS["cadetblue1"] = CADETBLUE1
COLORS["cadetblue2"] = CADETBLUE2
COLORS["cadetblue3"] = CADETBLUE3
COLORS["cadetblue4"] = CADETBLUE4
COLORS["cadmiumorange"] = CADMIUMORANGE
COLORS["cadmiumyellow"] = CADMIUMYELLOW
COLORS["carrot"] = CARROT
COLORS["chartreuse"] = CHARTREUSE1
COLORS["chartreuse1"] = CHARTREUSE1
COLORS["chartreuse2"] = CHARTREUSE2
COLORS["chartreuse3"] = CHARTREUSE3
COLORS["chartreuse4"] = CHARTREUSE4
COLORS["chocolate"] = CHOCOLATE
COLORS["chocolate1"] = CHOCOLATE1
COLORS["chocolate2"] = CHOCOLATE2
COLORS["chocolate3"] = CHOCOLATE3
COLORS["chocolate4"] = CHOCOLATE4
COLORS["cobalt"] = COBALT
COLORS["cobaltgreen"] = COBALTGREEN
COLORS["coldgrey"] = COLDGREY
COLORS["coral"] = CORAL
COLORS["coral1"] = CORAL1
COLORS["coral2"] = CORAL2
COLORS["coral3"] = CORAL3
COLORS["coral4"] = CORAL4
COLORS["cornflowerblue"] = CORNFLOWERBLUE
COLORS["cornsilk"] = CORNSILK1
COLORS["cornsilk1"] = CORNSILK1
COLORS["cornsilk2"] = CORNSILK2
COLORS["cornsilk3"] = CORNSILK3
COLORS["cornsilk4"] = CORNSILK4
COLORS["crimson"] = CRIMSON
COLORS["cyan"] = CYAN1
COLORS["cyan1"] = CYAN1
COLORS["cyan2"] = CYAN2
COLORS["cyan3"] = CYAN3
COLORS["darkgoldenrod"] = DARKGOLDENROD
COLORS["darkgoldenrod1"] = DARKGOLDENROD1
COLORS["darkgoldenrod2"] = DARKGOLDENROD2
COLORS["darkgoldenrod3"] = DARKGOLDENROD3
COLORS["darkgoldenrod4"] = DARKGOLDENROD4
COLORS["darkgray"] = DARKGRAY
COLORS["darkgreen"] = DARKGREEN
COLORS["darkkhaki"] = DARKKHAKI
COLORS["darkolivegreen"] = DARKOLIVEGREEN
COLORS["darkolivegreen1"] = DARKOLIVEGREEN1
COLORS["darkolivegreen2"] = DARKOLIVEGREEN2
COLORS["darkolivegreen3"] = DARKOLIVEGREEN3
COLORS["darkolivegreen4"] = DARKOLIVEGREEN4
COLORS["darkorange"] = DARKORANGE
COLORS["darkorange1"] = DARKORANGE1
COLORS["darkorange2"] = DARKORANGE2
COLORS["darkorange3"] = DARKORANGE3
COLORS["darkorange4"] = DARKORANGE4
COLORS["darkorchid"] = DARKORCHID
COLORS["darkorchid1"] = DARKORCHID1
COLORS["darkorchid2"] = DARKORCHID2
COLORS["darkorchid3"] = DARKORCHID3
COLORS["darkorchid4"] = DARKORCHID4
COLORS["darksalmon"] = DARKSALMON
COLORS["darkseagreen"] = DARKSEAGREEN
COLORS["darkseagreen1"] = DARKSEAGREEN1
COLORS["darkseagreen2"] = DARKSEAGREEN2
COLORS["darkseagreen3"] = DARKSEAGREEN3
COLORS["darkseagreen4"] = DARKSEAGREEN4
COLORS["darkslateblue"] = DARKSLATEBLUE
COLORS["darkslategray"] = DARKSLATEGRAY
COLORS["darkslategray1"] = DARKSLATEGRAY1
COLORS["darkslategray2"] = DARKSLATEGRAY2
COLORS["darkslategray3"] = DARKSLATEGRAY3
COLORS["darkslategray4"] = DARKSLATEGRAY4
COLORS["darkturquoise"] = DARKTURQUOISE
COLORS["darkviolet"] = DARKVIOLET
COLORS["deeppink"] = DEEPPINK1
COLORS["deeppink1"] = DEEPPINK1
COLORS["deeppink2"] = DEEPPINK2
COLORS["deeppink3"] = DEEPPINK3
COLORS["deeppink4"] = DEEPPINK4
COLORS["deepskyblue"] = DEEPSKYBLUE1
COLORS["deepskyblue1"] = DEEPSKYBLUE1
COLORS["deepskyblue2"] = DEEPSKYBLUE2
COLORS["deepskyblue3"] = DEEPSKYBLUE3
COLORS["deepskyblue4"] = DEEPSKYBLUE4
COLORS["dimgray"] = DIMGRAY
COLORS["dodgerblue"] = DODGERBLUE1
COLORS["dodgerblue1"] = DODGERBLUE1
COLORS["dodgerblue2"] = DODGERBLUE2
COLORS["dodgerblue3"] = DODGERBLUE3
COLORS["dodgerblue4"] = DODGERBLUE4
COLORS["eggshell"] = EGGSHELL
COLORS["emeraldgreen"] = EMERALDGREEN
COLORS["firebrick"] = FIREBRICK
COLORS["firebrick1"] = FIREBRICK1
COLORS["firebrick2"] = FIREBRICK2
COLORS["firebrick3"] = FIREBRICK3
COLORS["firebrick4"] = FIREBRICK4
COLORS["flesh"] = FLESH
COLORS["floralwhite"] = FLORALWHITE
COLORS["forestgreen"] = FORESTGREEN
COLORS["gainsboro"] = GAINSBORO
COLORS["ghostwhite"] = GHOSTWHITE
COLORS["gold"] = GOLD1
COLORS["gold1"] = GOLD1
COLORS["gold2"] = GOLD2
COLORS["gold3"] = GOLD3
COLORS["gold4"] = GOLD4
COLORS["goldenrod"] = GOLDENROD
COLORS["goldenrod1"] = GOLDENROD1
COLORS["goldenrod2"] = GOLDENROD2
COLORS["goldenrod3"] = GOLDENROD3
COLORS["goldenrod4"] = GOLDENROD4
COLORS["gray"] = GRAY
COLORS["gray1"] = GRAY1
COLORS["gray10"] = GRAY10
COLORS["gray11"] = GRAY11
COLORS["gray12"] = GRAY12
COLORS["gray13"] = GRAY13
COLORS["gray14"] = GRAY14
COLORS["gray15"] = GRAY15
COLORS["gray16"] = GRAY16
COLORS["gray17"] = GRAY17
COLORS["gray18"] = GRAY18
COLORS["gray19"] = GRAY19
COLORS["gray2"] = GRAY2
COLORS["gray20"] = GRAY20
COLORS["gray21"] = GRAY21
COLORS["gray22"] = GRAY22
COLORS["gray23"] = GRAY23
COLORS["gray24"] = GRAY24
COLORS["gray25"] = GRAY25
COLORS["gray26"] = GRAY26
COLORS["gray27"] = GRAY27
COLORS["gray28"] = GRAY28
COLORS["gray29"] = GRAY29
COLORS["gray3"] = GRAY3
COLORS["gray30"] = GRAY30
COLORS["gray31"] = GRAY31
COLORS["gray32"] = GRAY32
COLORS["gray33"] = GRAY33
COLORS["gray34"] = GRAY34
COLORS["gray35"] = GRAY35
COLORS["gray36"] = GRAY36
COLORS["gray37"] = GRAY37
COLORS["gray38"] = GRAY38
COLORS["gray39"] = GRAY39
COLORS["gray4"] = GRAY4
COLORS["gray40"] = GRAY40
COLORS["gray42"] = GRAY42
COLORS["gray43"] = GRAY43
COLORS["gray44"] = GRAY44
COLORS["gray45"] = GRAY45
COLORS["gray46"] = GRAY46
COLORS["gray47"] = GRAY47
COLORS["gray48"] = GRAY48
COLORS["gray49"] = GRAY49
COLORS["gray5"] = GRAY5
COLORS["gray50"] = GRAY50
COLORS["gray51"] = GRAY51
COLORS["gray52"] = GRAY52
COLORS["gray53"] = GRAY53
COLORS["gray54"] = GRAY54
COLORS["gray55"] = GRAY55
COLORS["gray56"] = GRAY56
COLORS["gray57"] = GRAY57
COLORS["gray58"] = GRAY58
COLORS["gray59"] = GRAY59
COLORS["gray6"] = GRAY6
COLORS["gray60"] = GRAY60
COLORS["gray61"] = GRAY61
COLORS["gray62"] = GRAY62
COLORS["gray63"] = GRAY63
COLORS["gray64"] = GRAY64
COLORS["gray65"] = GRAY65
COLORS["gray66"] = GRAY66
COLORS["gray67"] = GRAY67
COLORS["gray68"] = GRAY68
COLORS["gray69"] = GRAY69
COLORS["gray7"] = GRAY7
COLORS["gray70"] = GRAY70
COLORS["gray71"] = GRAY71
COLORS["gray72"] = GRAY72
COLORS["gray73"] = GRAY73
COLORS["gray74"] = GRAY74
COLORS["gray75"] = GRAY75
COLORS["gray76"] = GRAY76
COLORS["gray77"] = GRAY77
COLORS["gray78"] = GRAY78
COLORS["gray79"] = GRAY79
COLORS["gray8"] = GRAY8
COLORS["gray80"] = GRAY80
COLORS["gray81"] = GRAY81
COLORS["gray82"] = GRAY82
COLORS["gray83"] = GRAY83
COLORS["gray84"] = GRAY84
COLORS["gray85"] = GRAY85
COLORS["gray86"] = GRAY86
COLORS["gray87"] = GRAY87
COLORS["gray88"] = GRAY88
COLORS["gray89"] = GRAY89
COLORS["gray9"] = GRAY9
COLORS["gray90"] = GRAY90
COLORS["gray91"] = GRAY91
COLORS["gray92"] = GRAY92
COLORS["gray93"] = GRAY93
COLORS["gray94"] = GRAY94
COLORS["gray95"] = GRAY95
COLORS["gray97"] = GRAY97
COLORS["gray98"] = GRAY98
COLORS["gray99"] = GRAY99
COLORS["green"] = GREEN
COLORS["green1"] = GREEN1
COLORS["green2"] = GREEN2
COLORS["green3"] = GREEN3
COLORS["green4"] = GREEN4
COLORS["greenyellow"] = GREENYELLOW
COLORS["honeydew"] = HONEYDEW1
COLORS["honeydew1"] = HONEYDEW1
COLORS["honeydew2"] = HONEYDEW2
COLORS["honeydew3"] = HONEYDEW3
COLORS["honeydew4"] = HONEYDEW4
COLORS["hotpink"] = HOTPINK
COLORS["hotpink1"] = HOTPINK1
COLORS["hotpink2"] = HOTPINK2
COLORS["hotpink3"] = HOTPINK3
COLORS["hotpink4"] = HOTPINK4
COLORS["indianred"] = INDIANRED
COLORS["indianred"] = INDIANRED
COLORS["indianred1"] = INDIANRED1
COLORS["indianred2"] = INDIANRED2
COLORS["indianred3"] = INDIANRED3
COLORS["indianred4"] = INDIANRED4
COLORS["indigo"] = INDIGO
COLORS["ivory"] = IVORY1
COLORS["ivory1"] = IVORY1
COLORS["ivory2"] = IVORY2
COLORS["ivory3"] = IVORY3
COLORS["ivory4"] = IVORY4
COLORS["ivoryblack"] = IVORYBLACK
COLORS["khaki"] = KHAKI
COLORS["khaki1"] = KHAKI1
COLORS["khaki2"] = KHAKI2
COLORS["khaki3"] = KHAKI3
COLORS["khaki4"] = KHAKI4
COLORS["lavender"] = LAVENDER
COLORS["lavenderblush"] = LAVENDERBLUSH1
COLORS["lavenderblush1"] = LAVENDERBLUSH1
COLORS["lavenderblush2"] = LAVENDERBLUSH2
COLORS["lavenderblush3"] = LAVENDERBLUSH3
COLORS["lavenderblush4"] = LAVENDERBLUSH4
COLORS["lawngreen"] = LAWNGREEN
COLORS["lemonchiffon"] = LEMONCHIFFON1
COLORS["lemonchiffon1"] = LEMONCHIFFON1
COLORS["lemonchiffon2"] = LEMONCHIFFON2
COLORS["lemonchiffon3"] = LEMONCHIFFON3
COLORS["lemonchiffon4"] = LEMONCHIFFON4
COLORS["lightblue"] = LIGHTBLUE
COLORS["lightblue1"] = LIGHTBLUE1
COLORS["lightblue2"] = LIGHTBLUE2
COLORS["lightblue3"] = LIGHTBLUE3
COLORS["lightblue4"] = LIGHTBLUE4
COLORS["lightcoral"] = LIGHTCORAL
COLORS["lightcyan"] = LIGHTCYAN1
COLORS["lightcyan1"] = LIGHTCYAN1
COLORS["lightcyan2"] = LIGHTCYAN2
COLORS["lightcyan3"] = LIGHTCYAN3
COLORS["lightcyan4"] = LIGHTCYAN4
COLORS["lightgoldenrod"] = LIGHTGOLDENROD1
COLORS["lightgoldenrod1"] = LIGHTGOLDENROD1
COLORS["lightgoldenrod2"] = LIGHTGOLDENROD2
COLORS["lightgoldenrod3"] = LIGHTGOLDENROD3
COLORS["lightgoldenrod4"] = LIGHTGOLDENROD4
COLORS["lightgoldenrodyellow"] = LIGHTGOLDENRODYELLOW
COLORS["lightgrey"] = LIGHTGREY
COLORS["lightpink"] = LIGHTPINK
COLORS["lightpink1"] = LIGHTPINK1
COLORS["lightpink2"] = LIGHTPINK2
COLORS["lightpink3"] = LIGHTPINK3
COLORS["lightpink4"] = LIGHTPINK4
COLORS["lightsalmon"] = LIGHTSALMON1
COLORS["lightsalmon1"] = LIGHTSALMON1
COLORS["lightsalmon2"] = LIGHTSALMON2
COLORS["lightsalmon3"] = LIGHTSALMON3
COLORS["lightsalmon4"] = LIGHTSALMON4
COLORS["lightseagreen"] = LIGHTSEAGREEN
COLORS["lightskyblue"] = LIGHTSKYBLUE
COLORS["lightskyblue1"] = LIGHTSKYBLUE1
COLORS["lightskyblue2"] = LIGHTSKYBLUE2
COLORS["lightskyblue3"] = LIGHTSKYBLUE3
COLORS["lightskyblue4"] = LIGHTSKYBLUE4
COLORS["lightslateblue"] = LIGHTSLATEBLUE
COLORS["lightslategray"] = LIGHTSLATEGRAY
COLORS["lightsteelblue"] = LIGHTSTEELBLUE
COLORS["lightsteelblue1"] = LIGHTSTEELBLUE1
COLORS["lightsteelblue2"] = LIGHTSTEELBLUE2
COLORS["lightsteelblue3"] = LIGHTSTEELBLUE3
COLORS["lightsteelblue4"] = LIGHTSTEELBLUE4
COLORS["lightyellow"] = LIGHTYELLOW1
COLORS["lightyellow1"] = LIGHTYELLOW1
COLORS["lightyellow2"] = LIGHTYELLOW2
COLORS["lightyellow3"] = LIGHTYELLOW3
COLORS["lightyellow4"] = LIGHTYELLOW4
COLORS["limegreen"] = LIMEGREEN
COLORS["linen"] = LINEN
COLORS["magenta"] = MAGENTA
COLORS["magenta1"] = MAGENTA2
COLORS["magenta2"] = MAGENTA2
COLORS["magenta3"] = MAGENTA3
COLORS["magenta4"] = MAGENTA4
COLORS["manganeseblue"] = MANGANESEBLUE
COLORS["maroon"] = MAROON
COLORS["maroon1"] = MAROON1
COLORS["maroon2"] = MAROON2
COLORS["maroon3"] = MAROON3
COLORS["maroon4"] = MAROON4
COLORS["mediumorchid"] = MEDIUMORCHID
COLORS["mediumorchid1"] = MEDIUMORCHID1
COLORS["mediumorchid2"] = MEDIUMORCHID2
COLORS["mediumorchid3"] = MEDIUMORCHID3
COLORS["mediumorchid4"] = MEDIUMORCHID4
COLORS["mediumpurple"] = MEDIUMPURPLE
COLORS["mediumpurple1"] = MEDIUMPURPLE1
COLORS["mediumpurple2"] = MEDIUMPURPLE2
COLORS["mediumpurple3"] = MEDIUMPURPLE3
COLORS["mediumpurple4"] = MEDIUMPURPLE4
COLORS["mediumseagreen"] = MEDIUMSEAGREEN
COLORS["mediumslateblue"] = MEDIUMSLATEBLUE
COLORS["mediumspringgreen"] = MEDIUMSPRINGGREEN
COLORS["mediumturquoise"] = MEDIUMTURQUOISE
COLORS["mediumvioletred"] = MEDIUMVIOLETRED
COLORS["melon"] = MELON
COLORS["midnightblue"] = MIDNIGHTBLUE
COLORS["mint"] = MINT
COLORS["mintcream"] = MINTCREAM
COLORS["mistyrose"] = MISTYROSE1
COLORS["mistyrose1"] = MISTYROSE1
COLORS["mistyrose2"] = MISTYROSE2
COLORS["mistyrose3"] = MISTYROSE3
COLORS["mistyrose4"] = MISTYROSE4
COLORS["moccasin"] = MOCCASIN
COLORS["navajowhite"] = NAVAJOWHITE1
COLORS["navajowhite1"] = NAVAJOWHITE1
COLORS["navajowhite2"] = NAVAJOWHITE2
COLORS["navajowhite3"] = NAVAJOWHITE3
COLORS["navajowhite4"] = NAVAJOWHITE4
COLORS["navy"] = NAVY
COLORS["oldlace"] = OLDLACE
COLORS["olive"] = OLIVE
COLORS["olivedrab"] = OLIVEDRAB
COLORS["olivedrab1"] = OLIVEDRAB1
COLORS["olivedrab2"] = OLIVEDRAB2
COLORS["olivedrab3"] = OLIVEDRAB3
COLORS["olivedrab4"] = OLIVEDRAB4
COLORS["orange"] = ORANGE
COLORS["orange1"] = ORANGE1
COLORS["orange2"] = ORANGE2
COLORS["orange3"] = ORANGE3
COLORS["orange4"] = ORANGE4
COLORS["orangered"] = ORANGERED1
COLORS["orangered1"] = ORANGERED1
COLORS["orangered2"] = ORANGERED2
COLORS["orangered3"] = ORANGERED3
COLORS["orangered4"] = ORANGERED4
COLORS["orchid"] = ORCHID
COLORS["orchid1"] = ORCHID1
COLORS["orchid2"] = ORCHID2
COLORS["orchid3"] = ORCHID3
COLORS["orchid4"] = ORCHID4
COLORS["palegoldenrod"] = PALEGOLDENROD
COLORS["palegreen"] = PALEGREEN
COLORS["palegreen1"] = PALEGREEN1
COLORS["palegreen2"] = PALEGREEN2
COLORS["palegreen3"] = PALEGREEN3
COLORS["palegreen4"] = PALEGREEN4
COLORS["paleturquoise1"] = PALETURQUOISE1
COLORS["paleturquoise2"] = PALETURQUOISE2
COLORS["paleturquoise3"] = PALETURQUOISE3
COLORS["paleturquoise4"] = PALETURQUOISE4
COLORS["palevioletred"] = PALEVIOLETRED
COLORS["palevioletred1"] = PALEVIOLETRED1
COLORS["palevioletred2"] = PALEVIOLETRED2
COLORS["palevioletred3"] = PALEVIOLETRED3
COLORS["palevioletred4"] = PALEVIOLETRED4
COLORS["papayawhip"] = PAPAYAWHIP
COLORS["peachpuff1"] = PEACHPUFF1
COLORS["peachpuff2"] = PEACHPUFF2
COLORS["peachpuff3"] = PEACHPUFF3
COLORS["peachpuff4"] = PEACHPUFF4
COLORS["peacock"] = PEACOCK
COLORS["pink"] = PINK
COLORS["pink1"] = PINK1
COLORS["pink2"] = PINK2
COLORS["pink3"] = PINK3
COLORS["pink4"] = PINK4
COLORS["plum"] = PLUM
COLORS["plum1"] = PLUM1
COLORS["plum2"] = PLUM2
COLORS["plum3"] = PLUM3
COLORS["plum4"] = PLUM4
COLORS["powderblue"] = POWDERBLUE
COLORS["purple"] = PURPLE
COLORS["purple1"] = PURPLE1
COLORS["purple2"] = PURPLE2
COLORS["purple3"] = PURPLE3
COLORS["purple4"] = PURPLE4
COLORS["raspberry"] = RASPBERRY
COLORS["rawsienna"] = RAWSIENNA
COLORS["red"] = RED
COLORS["red1"] = RED1
COLORS["red2"] = RED2
COLORS["red3"] = RED3
COLORS["red4"] = RED4
COLORS["rosybrown"] = ROSYBROWN
COLORS["rosybrown1"] = ROSYBROWN1
COLORS["rosybrown2"] = ROSYBROWN2
COLORS["rosybrown3"] = ROSYBROWN3
COLORS["rosybrown4"] = ROSYBROWN4
COLORS["royalblue"] = ROYALBLUE
COLORS["royalblue1"] = ROYALBLUE1
COLORS["royalblue2"] = ROYALBLUE2
COLORS["royalblue3"] = ROYALBLUE3
COLORS["royalblue4"] = ROYALBLUE4
COLORS["salmon"] = SALMON
COLORS["salmon1"] = SALMON1
COLORS["salmon2"] = SALMON2
COLORS["salmon3"] = SALMON3
COLORS["salmon4"] = SALMON4
COLORS["sandybrown"] = SANDYBROWN
COLORS["sapgreen"] = SAPGREEN
COLORS["seagreen1"] = SEAGREEN1
COLORS["seagreen2"] = SEAGREEN2
COLORS["seagreen3"] = SEAGREEN3
COLORS["seagreen4"] = SEAGREEN4
COLORS["seashell1"] = SEASHELL1
COLORS["seashell2"] = SEASHELL2
COLORS["seashell3"] = SEASHELL3
COLORS["seashell4"] = SEASHELL4
COLORS["sepia"] = SEPIA
COLORS["sgibeet"] = SGIBEET
COLORS["sgibrightgray"] = SGIBRIGHTGRAY
COLORS["sgichartreuse"] = SGICHARTREUSE
COLORS["sgidarkgray"] = SGIDARKGRAY
COLORS["sgigray12"] = SGIGRAY12
COLORS["sgigray16"] = SGIGRAY16
COLORS["sgigray32"] = SGIGRAY32
COLORS["sgigray36"] = SGIGRAY36
COLORS["sgigray52"] = SGIGRAY52
COLORS["sgigray56"] = SGIGRAY56
COLORS["sgigray72"] = SGIGRAY72
COLORS["sgigray76"] = SGIGRAY76
COLORS["sgigray92"] = SGIGRAY92
COLORS["sgigray96"] = SGIGRAY96
COLORS["sgilightblue"] = SGILIGHTBLUE
COLORS["sgilightgray"] = SGILIGHTGRAY
COLORS["sgiolivedrab"] = SGIOLIVEDRAB
COLORS["sgisalmon"] = SGISALMON
COLORS["sgislateblue"] = SGISLATEBLUE
COLORS["sgiteal"] = SGITEAL
COLORS["sienna"] = SIENNA
COLORS["sienna1"] = SIENNA1
COLORS["sienna2"] = SIENNA2
COLORS["sienna3"] = SIENNA3
COLORS["sienna4"] = SIENNA4
COLORS["silver"] = SILVER
COLORS["skyblue"] = SKYBLUE
COLORS["skyblue1"] = SKYBLUE1
COLORS["skyblue2"] = SKYBLUE2
COLORS["skyblue3"] = SKYBLUE3
COLORS["skyblue4"] = SKYBLUE4
COLORS["slateblue"] = SLATEBLUE
COLORS["slateblue1"] = SLATEBLUE1
COLORS["slateblue2"] = SLATEBLUE2
COLORS["slateblue3"] = SLATEBLUE3
COLORS["slateblue4"] = SLATEBLUE4
COLORS["slategray"] = SLATEGRAY
COLORS["slategray1"] = SLATEGRAY1
COLORS["slategray2"] = SLATEGRAY2
COLORS["slategray3"] = SLATEGRAY3
COLORS["slategray4"] = SLATEGRAY4
COLORS["snow"] = SNOW1
COLORS["snow1"] = SNOW1
COLORS["snow2"] = SNOW2
COLORS["snow3"] = SNOW3
COLORS["snow4"] = SNOW4
COLORS["springgreen"] = SPRINGGREEN
COLORS["springgreen1"] = SPRINGGREEN1
COLORS["springgreen2"] = SPRINGGREEN2
COLORS["springgreen3"] = SPRINGGREEN3
COLORS["steelblue"] = STEELBLUE
COLORS["steelblue1"] = STEELBLUE1
COLORS["steelblue2"] = STEELBLUE2
COLORS["steelblue3"] = STEELBLUE3
COLORS["steelblue4"] = STEELBLUE4
COLORS["tan"] = TAN
COLORS["tan1"] = TAN1
COLORS["tan2"] = TAN2
COLORS["tan3"] = TAN3
COLORS["tan4"] = TAN4
COLORS["teal"] = TEAL
COLORS["thistle"] = THISTLE
COLORS["thistle1"] = THISTLE1
COLORS["thistle2"] = THISTLE2
COLORS["thistle3"] = THISTLE3
COLORS["thistle4"] = THISTLE4
COLORS["tomato"] = TOMATO1
COLORS["tomato1"] = TOMATO1
COLORS["tomato2"] = TOMATO2
COLORS["tomato3"] = TOMATO3
COLORS["tomato4"] = TOMATO4
COLORS["turquoise"] = TURQUOISE
COLORS["turquoise1"] = TURQUOISE1
COLORS["turquoise2"] = TURQUOISE2
COLORS["turquoise3"] = TURQUOISE3
COLORS["turquoise4"] = TURQUOISE4
COLORS["turquoiseblue"] = TURQUOISEBLUE
COLORS["violet"] = VIOLET
COLORS["violetred"] = VIOLETRED
COLORS["violetred1"] = VIOLETRED1
COLORS["violetred2"] = VIOLETRED2
COLORS["violetred3"] = VIOLETRED3
COLORS["violetred4"] = VIOLETRED4
COLORS["warmgrey"] = WARMGREY
COLORS["wheat"] = WHEAT
COLORS["wheat1"] = WHEAT1
COLORS["wheat2"] = WHEAT2
COLORS["wheat3"] = WHEAT3
COLORS["wheat4"] = WHEAT4
COLORS["white"] = WHITE
COLORS["whitesmoke"] = WHITESMOKE
COLORS["whitesmoke"] = WHITESMOKE
COLORS["yellow"] = YELLOW
COLORS["yellow1"] = YELLOW1
COLORS["yellow2"] = YELLOW2
COLORS["yellow3"] = YELLOW3
COLORS["yellow4"] = YELLOW4

def parse_color(value):
    if value is not None:

        # is it a Color object?
        if isinstance(value, Color):
            return value

        # is the color a string
        elif isinstance(value, str):
            # strip the color of white space
            value = value.strip()

            # if it starts with a # check it is a valid color
            if value[0] == "#":

                # check its format
                if len(value) != 7 and len(value) != 9:
                    raise ValueError("{} is not a valid # color, it must be in the format #rrggbb or #rrggbbaa".format(value))
                else:
                    # add the alpha if required
                    if len(value) == 7:
                        value = value + "ff"

                    hex_values = (value[1:3], value[3:5], value[5:7], value[7:9])
                
                    # check hex values are between 00 and ff
                    int_values = []
                    for hex_color in hex_values:
                        try:
                            int_color = int(hex_color, 16)
                            int_values.append(int_color)
                        except: 
                            raise ValueError("{} is not a valid value, it must be hex 00 - ff".format(hex_color))

                        if not (0 <= int_color <= 255):
                            raise ValueError("{} is not a valid color value, it must be 00 - ff".format(hex_color))

                    return Color(red=int_values[0], green=int_values[1], blue=int_values[2], alpha=int_values[3])
            
            else:
                # does the color exist in the dictionary of colors
                if value.lower() in COLORS:
                    return COLORS[value.lower()]
                else:
                    raise ValueError("'{}' is not a valid color value.")

        # if the color is not a string or a Color object, maybe its a list or tuple - try and convert it
        else:
            # get the number of colors and check it is iterable
            try:
                no_of_colors = len(value)
            except:
                raise ValueError("A color must be a Color object, string or list of values (red, green, blue) or (alpha, red, green, blue)") 

            if not (3 <= no_of_colors <= 4):
                raise ValueError("A color must contain 3 or 4 values (red, green, blue) or (red, green, blue, alpha)")
            
            # check the color values are between 0 and 255
            for c in value:
                if not (0 <= c <= 255):
                    raise ValueError("{} is not a valid color value, it must be 0 - 255")
                    
            if no_of_colors == 3:
                return Color(red=value[0], green=value[1], blue=value[2])
            else:
                return Color(red=value[0], green=value[1], blue=value[2], alpha=value[3])

