import neopixel
import digitalio
import time
import board as piBoard
from PIL import Image, ImageDraw, ImageFont
from adafruit_rgb_display.rgb import color565
import adafruit_rgb_display.st7789 as st7789

class C4Display:

    board = []

    DISPLAY = 0
    IMAGE = 0
    DRAW = 0

    NUM_PIXELS = 49
    PLAYER_1_COLOR = (0, 0, 255)
    PLAYER_2_COLOR = (255, 0, 0)
    BLANK_COLOR = (0, 0, 0)
    COLOR_SLEEP = .2
    FONT = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)

    buttonA = digitalio.DigitalInOut(piBoard.D23)
    buttonB = digitalio.DigitalInOut(piBoard.D24)
    buttonA.switch_to_input()
    buttonB.switch_to_input()

    def __init__(self):

        self.pixels = neopixel.NeoPixel(piBoard.D21, self.NUM_PIXELS, brightness=.03)

        # Configuration for CS and DC pins for Raspberry Pi
        cs_pin = digitalio.DigitalInOut(piBoard.CE0)
        dc_pin = digitalio.DigitalInOut(piBoard.D25)
        reset_pin = None
        BAUDRATE = 64000000  # The pi can be very fast!

        # Create the ST7789 display:
        self.DISPLAY = st7789.ST7789(
            piBoard.SPI(),
            cs=cs_pin,
            dc=dc_pin,
            rst=reset_pin,
            baudrate=BAUDRATE,
            width=135,
            height=240,
            x_offset=53,
            y_offset=40,
        )

        self.clearScreen()

    def clearColumnChooser(self):
        for x in range(7):
            self.pixels[x] = self.BLANK_COLOR

    def clearScreen(self):
        # Create blank image for drawing.
        # Make sure to create image with mode 'RGB' for full color.
        height = self.DISPLAY.width  # we swap height/width to rotate it to landscape!
        width = self.DISPLAY.height

        self.IMAGE = Image.new("RGB", (width, height))
        self.DRAW = ImageDraw.Draw(self.IMAGE)

        backlight = digitalio.DigitalInOut(piBoard.D22)
        backlight.switch_to_output()
        backlight.value = True

    def chooseColumn(self, playerNumber):

        column = 0

        while True:

            if playerNumber == 1:
                self.pixels[6 - column] = self.PLAYER_1_COLOR

            else:
                self.pixels[6 - column] = self.PLAYER_2_COLOR

            if self.buttonB.value and not self.buttonA.value:
                time.sleep(.2)
                column = column + 1

                if column > 6:
                    self.pixels[0] = self.BLANK_COLOR
                    column = 0
                elif column > 0:
                    self.pixels[6 - column + 1] = self.BLANK_COLOR

            elif self.buttonA.value and not self.buttonB.value:
                time.sleep(.2)
                break

            self.pixels.show()

        self.clearColumnChooser()
        return column

    def show(self, line_str, line_number):
        y = self.FONT.getsize("ABCDEFG")[1]
        self.DRAW.text((0, y*line_number), line_str, font=self.FONT, fill="#FFFFFF")

        self.DISPLAY.image(self.IMAGE, 90)

    def printPiBoard(self, winning_player, winning_play):

        toggle_flg = 0
        sleep = self.COLOR_SLEEP

        while True:

            for column in range(7):

                if (column + 1) % 2 == 0:
                    for row in range(6, 0, -1):

                        if [column, row - 1] in winning_play and toggle_flg == 0:
                            self.pixels[((column * 6) + (row - 1)) + 7] = self.BLANK_COLOR
                        elif self.board[column][row - 1] == 1:
                            self.pixels[((column * 6) + (row - 1)) + 7] = self.PLAYER_1_COLOR
                        elif self.board[column][row - 1] == 2:
                            self.pixels[((column * 6) + (row - 1)) + 7] = self.PLAYER_2_COLOR
                        else:
                            self.pixels[((column * 6) + (row - 1)) + 7] = self.BLANK_COLOR
                else:
                    for row in range(6):

                        if [column, row] in winning_play and toggle_flg == 0:
                            self.pixels[((column + 1) * 6 - row) + 7 - 1] = self.BLANK_COLOR
                        elif self.board[column][row] == 1:
                            self.pixels[((column + 1) * 6 - row) + 7 - 1] = self.PLAYER_1_COLOR
                        elif self.board[column][row] == 2:
                            self.pixels[((column + 1) * 6 - row) + 7 - 1] = self.PLAYER_2_COLOR
                        else:
                            self.pixels[((column + 1) * 6 - row) + 7 - 1] = self.BLANK_COLOR

            self.pixels.show()

            if winning_player == 0 or sleep < 0.03:
                break
            else:
                if toggle_flg == 0:
                    sleep = sleep -.015
                    toggle_flg = 1
                else:
                    toggle_flg = 0

                time.sleep(sleep)

    def getButtonInput(self):

        buttonA = digitalio.DigitalInOut(piBoard.D23)
        buttonB = digitalio.DigitalInOut(piBoard.D24)
        buttonA.switch_to_input()
        buttonB.switch_to_input()

        return buttonA, buttonB

    def setBoard(self, board):
        self.board = board