import board
import displayio
import usb_cdc

ser = usb_cdc.data

display = board.DISPLAY

bitmap = displayio.Bitmap(display.width, display.height, 8)
palette = displayio.Palette(8)
palette[0] = 0x000000
palette[1] = 0xFFFFFF
palette[2] = 0xFF0000
palette[3] = 0x00FF00
palette[4] = 0x0000FF
palette[5] = 0xFFFF00
palette[6] = 0xFF00FF
palette[7] = 0x00FFFF
BRUSH_COLOR = 0

canvas = displayio.TileGrid(bitmap, pixel_shader=palette)

splash = displayio.Group()
splash.append(canvas)
display.show(splash)

def error(msg):
    ser.write(msg.encode())

def set_color(args):
    try:
        c = int(args)
    except:
        error("set_color 1")
    global BRUSH_COLOR
    BRUSH_COLOR = c

def draw_point(args):
    print("POINT", args)
    try:
        x, sep, y = args.partition(" ")
        x = int(x)
        y = int(y)
    except:
        return error("draw_point 1")
    if sep != " ":
        return error("draw_point 2")
    x = x if x > 0 else 0
    x = x if x < display.width else display.width - 1
    y = y if y > 0 else 0
    y = y if y < display.height else display.height - 1
    bitmap[x, y] = BRUSH_COLOR

def draw_line(args):
    print("LINE", args)

while True:
    user_input = ser.readline().decode().strip().upper()
    print(user_input)
    cmd, sep, args = user_input.partition(" ")
    if cmd=="CLEAR":
        bitmap.fill(BRUSH_COLOR)
    elif cmd=="COLOR":
        set_color(args)
    elif cmd=="POINT":
        draw_point(args)
    elif cmd=="LINE":
        draw_line(args)
    else:
        print("Unknown command:", cmd)
