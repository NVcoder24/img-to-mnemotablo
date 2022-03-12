import argparse
from PIL import Image

parser = argparse.ArgumentParser(description="Залупа")

parser.add_argument("--img", dest="img", required=True, help='Путь к картинке нахуй')
parser.add_argument("--side", dest="side", required=True, help='Сайд для враппа панели')
parser.add_argument("--fname", dest="fname", required=True, help='Имя функции')
parser.add_argument("--file", dest="file", required=True, help='Имя файла')
parser.add_argument("--size", dest="size", required=True, type=int, help='Размер (0, 1, 2, 3, 4, 5)')

ignore_color = (0, 0, 0)

args = parser.parse_args()

img_path = args.img
code_size = args.size
code_side = args.side
code_fname = args.fname
file = args.file

if code_size < 0 or code_size > 5:
    print("Э ты чо ахуел?\nСказано блять размеры от 0 до 5 сука")
    quit()

sizes = [
    2,
    4,
    8,
    16,
    32,
    128,
]

func_template = """{fname}_panel.setColorRGB({color_xy})"""

code_template = """
{fname}_panel = peripheral.wrap("{side}")
{fname}_panel.fill({ignore_color})
function {fname}_on()
    {fname}_panel.fill({ignore_color})
{stuff}
end
function {fname}_off()
    {fname}_panel.fill({ignore_color})
end
"""

img = Image.open(img_path)
img.convert('RGB')

img_size = (sizes[code_size], sizes[code_size])
img_res = img.resize(img_size, Image.ANTIALIAS)

def get_img_rgb_xy(img, ignore):
    w, h = img.size

    pixels = []
    for x in range(w):
        for y in range(h):
            pos = (x, y)
            color = img.getpixel(pos)
            if color != ignore:
                pixels.append(color + pos)
    
    return pixels

def render_funcs(colors_xy, fname):
    funcs = ""
    for color_xy in colors_xy:
        x = color_xy[3]
        y = color_xy[4]
        if len(color_xy) == 6:
            x = color_xy[4]
            y = color_xy[5]
        funcs += "    " + func_template.format(fname=fname, color_xy=f"{color_xy[0]}, {color_xy[1]}, {color_xy[2]}, {x}, {y}") + "\n"
    
    return funcs

def render(funcs, fname, ignore_color, side):
    return code_template.format(fname=fname, side=side, ignore_color=f"{ignore_color[0]}, {ignore_color[1]}, {ignore_color[2]}", stuff=funcs)

colors_xy = get_img_rgb_xy(img_res, ignore_color)
funcs = render_funcs(colors_xy, code_fname)
code = render(funcs, code_fname, ignore_color, code_side)

with open(file, "w") as file_save:
    file_save.writelines(code)

print("я сделал твою хуйню")