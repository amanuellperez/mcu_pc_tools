#!/usr/bin/python3
#
# Copyright (C) 2024 Manuel Perez 
# mail: <manuel2perez@proton.me> 
# https://github.com/amanuellperez/mcu_pc_tools
# 
# This file is part of the ALP Library. 
# 
# MCU++ Library is a free library: you can redistribute it and/or modify 
# it under the terms of the GNU General Public License as published by 
# the Free Software Foundation, either version 3 of the License, or 
# (at your option) any later version. 
# 
# This library is distributed in the hope that it will be useful, 
# but WITHOUT ANY WARRANTY; without even the implied warranty of 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the 
# GNU General Public License for more details. 
# 
# You should have received a copy of the GNU General Public License 
# along with this program. If not, see <https://www.gnu.org/licenses/>. 
#
#****************************************************************************
#
#  DESCRIPCION
#       Para poder escribir en un display texto necesito los bitmaps
#       correspondienes. 
#       El problema todas los tipos de letras gratuitas de internet
#       estan en formato .ttf y yo las quiero en formato txt.
#
#       Este script se encarga de convertir el fichero .ttf en .txt
#
#  IDEA
#       Uso Pillow para convertir .ttf en .txt y luego el .txt lo convierto en
#       el formato binario.
#
#       ve.0: (ve = version experimental)
#       Al principio intenté generar un fichero .txt por cada letra, pero
#       pillow generaba las letras de diferente altura. 
#
#       ve.1:
#       Para evitar eso escribo todas las letras una detras de otra, 
#       de tal manera que cada cual se coloca en la posición adecuada. 
#       Para poder distinguir entre unas letras y otras uso un marcador '|' 
#       que dibujo  en otro color que las letras para asi luego poder 
#       separar las letras facilmente.
#
#  TODO
#   + Probarlo con letras otf
#   + No funciona con italic letters que tienen el símbolo ! oblícuo (al
#     usarlo como marcador genera una línea inclinada de separación entre
#     caracteres)
#
#  HISTORIA
#    Manuel Perez
#    13/08/2024 Primer intento
#
#****************************************************************************/
import os, sys, argparse
import string

from PIL import Image, ImageFont, ImageDraw

# **************************************************************************
#                               FUNCTIONS
# **************************************************************************
# Si lo dibujo en blanco los colores los dibuja en gris
def mark_color():
    #return (255, 0, 0)
    return (255, 255, 255)

def is_gray_but_not_black(r, g, b):
    if ((r + g + b) < 100):
        return False    # black

    return (abs(r - g) < 50 and abs (r - b) < 50)

# TODO: dar opción a pasar como parametro la resolucion con la que mirar los
# colores
# El color del marcador es rojo, deberia de ser
# r == 255 and g == 0 and b == 0 pero las imagenes no siempre
# guardan los colores pedidos, sino que hace un gradiente 
def is_mark_color(r, g, b):
    #return (r > 127 and g < 128 and b < 128)
    return is_gray_but_not_black(r, g, b)

def X_color():
    return (0, 255, 0)

# black: r = 0, g = 0, b = 0
def is_X_color(r, g, b):
    return (r < 128 and g > 127 and b < 128)

# Creamos una imagen con todas los caracteres ASCII en una línea
# Los caracteres en posiciones pares los escribimos en rojo (es el marcador
# |), los de posiciones impares en blanco
def image_with_text(font_file, font_size, str_txt, out_file):
    font = ImageFont.truetype(font_file, font_size)

    img = Image.new("RGB", (100,100))
    draw = ImageDraw.Draw(img)

    # TODO: ¿cómo calcular la altura de la imagen? 
    w =int( draw.textlength(str_txt, font) + 1)
    img2 = img.resize((w, 100), Image.NEAREST)
    draw = ImageDraw.Draw(img2)

#    draw.text((0,0), ascii_char, font=font, fill=(0, 255,0,0))
    i = 0
    x = 0
    for c in str_txt:
        i += 1
        if i % 2 == 0:
            color = X_color()
        else:
            color = mark_color()

        draw.text((x,0), c, font = font, fill=color)
        x += font.getlength(c)


    img2.save(out_file)


# Convierte una imagen en txt
# Los marcadores entre letras los identifico con !
def image2txt(fin, fout):
    img = Image.open(fin)
    out = open(fout, "w")

    for j in range(img.height):
        for i in range(img.width):
            r, g, b = img.getpixel((i, j))
            if (is_mark_color(r, g, b)):
                out.write("! ")

            else:
                if (is_X_color(r, g, b)):
                    out.write("X ")
                else:
                    out.write(". ")

        out.write("\n")


# Devuelve True si la linea tiene alguna caracter c
def line_has_char(line, c):

    for i in range(len(line)):
        if (line[i] == c):
            return True

    return False


# Devuelve True si la columna j de la matriz x tiene el caracter c
def column_has_char(x, j, c):

    for i in range(len(x)):
        if (x[i][j] == c):
            return True

    return False


# line: array de strings
def skip_blank_lines(line):
    for i in range(len(line)):
        if (line_has_char(line[i], "X")):
            return i

    return len(line)



# filas (TODO: esta función sobra cuando se calcule correctamente la altura)
def remove_blank_lines(txt_in, txt_out):
    fout = open(txt_out, "w")

    with open(txt_in, "r") as fin:
        line = fin.read().splitlines()
    
    i0 = skip_blank_lines(line)


    for i in range(i0, len(line)):

        if (not line_has_char(line[i], "X")):
            return

        fout.write(line[i] + "\n")
# Borra la columna j de la matriz x
def matrix_remove_column(x, j):
    for i in range(len(x)):
        x[i].pop(j)



# **************************************************************************
#                               MAIN
# **************************************************************************
# args
# ----
parser = argparse.ArgumentParser(
                    description="Convert ttf file in txt file")

parser.add_argument("font_file", help="TTF file")
parser.add_argument("-s", "--font_size", type=int, default=16)
parser.add_argument("-c", "--characters", default="",
                        help="Generated the sequence after -c option")
parser.add_argument("-n", "--number", action="store_true", default=False,
                        help="Generated only number char")
parser.add_argument("-d", "--debug", action="store_true", default=False)
args = parser.parse_args()

font_file   = args.font_file
font_size   = args.font_size
debug       = args.debug
characters  = args.characters
only_digits = args.number


# Fase validación
# ---------------
if (os.path.isfile(font_file) == False):
    print("Can't find file " + font_file)
    exit(1)


output =os.path.splitext(font_file)[0]
output_bmp  = output + ".bmp"
tmp_file    = output + "1.txt"

output_txt  = output
if (only_digits):
    output_txt += "_number"

output_txt += "_s" + str(font_size) + ".txt"


# main
# ----
#ascii_char0 ="| |!|\"|#|$|%|&|'|(|)|*|+|,|-|.|/|0|1|2|3|4|5|6|7|8|9|:|;|<|=|>|?|@|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|[|\\|]|^|_|`|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|{|||}|"
#if (only_digits):
#    ascii_char0 ="|0|1|2|3|4|5|6|7|8|9|"

ascii_char0 =" !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}"
if (only_digits):
    ascii_char0 ="0123456789"

if (len(characters) > 0):
    ascii_char0 = characters

ascii_char = "|"
for i in range(len(ascii_char0)):
    ascii_char += ascii_char0[i] + "|"


# output_bmp: fichero bmp con todas las letras "ascii_char"
image_with_text(font_file, font_size, ascii_char, output_bmp)

# output_txt: fichero txt con todas las letras "ascii_char"
image2txt(output_bmp, tmp_file)
remove_blank_lines(tmp_file, output_txt)



# Clean
if (debug == False):
    os.remove(output_bmp)
    os.remove(tmp_file)


