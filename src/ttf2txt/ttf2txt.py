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
def mark_color():
    return (255, 0, 0)

# TODO: dar opción a pasar como parametro la resolucion con la que mirar los
# colores
# El color del marcador es rojo, deberia de ser
# r == 255 and g == 0 and b == 0 pero las imagenes no siempre
# guardan los colores pedidos, sino que hace un gradiente 
def is_mark_color(r, g, b):
    return (r > 127 and g < 128 and b < 128)

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
    w =int( draw.textlength(ascii_char, font) + 1)
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


# Devuelve False si la linea tiene alguna X
def is_blank(line):

    for i in range(len(line)):
        if (line[i] == "X"):
            return False

    return True



def skip_blank_lines(fin):

    for line in fin:
        if (not is_blank(line)):
            return


# Como no se calcular la altura de las letras estoy creando una imagen
# demasiado alta, con muchas filas blancas. Esta función borra todas esas
# filas (TODO: esta función sobra cuando se calcule correctamente la altura)
def remove_blank_lines(txt_in, txt_out):
    fout = open(txt_out, "w")

    with open(txt_in, "r") as fin:
        skip_blank_lines(fin)
        
        for line in fin:
            if (is_blank(line)):
                return

            fout.write(line)


# uso use_binary para poder depurar. 
# Los caracteres se ven mejor con . y X, que con 0 y 1
def read_file_as_matrix(fname, use_binary):
    with open(fname, "r") as f:
        r = f.read()
    
    if (use_binary == True):
        r = r.replace('.', '0')
        r = r.replace('X', '1')

    line = r.splitlines()

    y = []
    for i in range(len(line)):
        y += [line[i].split(' ')]

    return y



def print_matrix(matrix):
    n = len(matrix)
    m = len(matrix[0])

    for i in range(n):
        print ("0b", end = '')
        for j in range(m):
            print (matrix[i][j], end = '')

        print(' ')


def print_matrix_transpose(matrix):
    n = len(matrix)
    m = len(matrix[0])

    for j in range(m):
        print ("0b", end = '')
        for i in range(n):
            print (matrix[i][j], end = '')

        print(' ')


def print_matrix_reverse_transpose(matrix):
    n = len(matrix)
    m = len(matrix[0])

    for j in range(m):
        print ("0b", end = '')
        for i in range(n - 1, -1, -1):
            print (matrix[i][j], end = '')

        print(' ')





# Se nota que soy programador de C++? @_@
def find_first(c, x, i0, ie):
    return x.index('!', i0, ie)

def skip(c, x, i0, ie):
    if (i0 >= ie):
        return ie
    # while (i0 < ie and x[i0] == c): dont work
    while (x[i0] == c):
        i0 += 1
        if (i0 >= ie):
            return ie

    i0 += 1
    return i0



# buscamos la siguiente columna que tenga !
def find_mark_column(y, j0):
    n = len(y)
    m = len(y[0])

    for j in range(j0, m):
        for i in range(n):
            if (y[i][j] == '!'):
                return j

    return m


# Buscamos la primera columna que no tenga mark
def skip_mark_column(y, j0):
    n = len(y)
    m = len(y[0])


    for j in range(j0, m):
        is_mark_column = False
        for i in range(n):
            if (y[i][j] == '!'):
                is_mark_column = True

        if (is_mark_column == False):
            return j

    return m


def split_as_array(y):
    j0 = find_mark_column(y, 0)
    j0 += 1
    j0 = skip_mark_column(y, j0)

    je = find_mark_column(y, j0)

    n = len(y)
    m = len(y[0])

    char = []
    while (je != m):
        c = []
        for i in range(n):
            c += [y[i][j0:je]]
        
        char += [c]

        j0 = skip_mark_column(y, je)
        je = find_mark_column(y, j0)

    return char



        







# **************************************************************************
#                               MAIN
# **************************************************************************
# args
# ----
# Formato de salida
PRINT_MATRIX                   = 0
PRINT_MATRIX_TRANSPOSE         = 1
PRINT_MATRIX_REVERSE_TRANSPOSE = 2

parser = argparse.ArgumentParser(
                    description="Convert ttf file in txt file")

parser.add_argument("font_file", help="TTF file")
parser.add_argument("-p", "--print_type", default=PRINT_MATRIX_TRANSPOSE,
                        type=int,
                        help="0 = print matrix; 1 = print matrix transpose; 2 = print matrix reverse transpose")
parser.add_argument("-s", "--font_size", default=16)
parser.add_argument("-n", "--number", action="store_true", default=False,
                        help="Generated only number char")
parser.add_argument("-d", "--debug", action="store_true", default=False)
args = parser.parse_args()

font_file   = args.font_file
font_size   = args.font_size
debug       = args.debug
only_digits = args.number
print_type = args.print_type


# Fase validación
# ---------------
if (os.path.isfile(font_file) == False):
    print("Can't find file " + font_file)
    exit(1)


output =os.path.splitext(font_file)[0]
output_bmp  = output + ".bmp"
tmp_file    = output + "1.txt"
output_txt  = output + ".txt"


# main
# ----
ascii_char ="| |!|\"|#|$|%|&|'|(|)|*|+|,|-|.|/|0|1|2|3|4|5|6|7|8|9|:|;|<|=|>|?|@|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|[|\\|]|^|_|`|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|{|||}|"
if (only_digits):
    ascii_char="|0|1|2|3|4|5|6|7|8|9|"


# output_bmp: fichero bmp con todas las letras "ascii_char"
image_with_text(font_file, font_size, ascii_char, output_bmp)

# output_txt: fichero txt con todas las letras "ascii_char"
image2txt(output_bmp, tmp_file)
remove_blank_lines(tmp_file, output_txt)


# Convertimos el fichero en matriz
y = read_file_as_matrix(output_txt, True)

# Lo descomponemos en un array de matrices, cada matriz con el caracter
# correspondiente
char = split_as_array(y)

for i in range(len(char)):
    print ("// " + ascii_char[2*i + 1])
    
    if (print_type == PRINT_MATRIX):
        print_matrix(char[i])

    elif (print_type == PRINT_MATRIX_TRANSPOSE):
        print_matrix_transpose(char[i])

    elif (print_type == PRINT_MATRIX_REVERSE_TRANSPOSE):
        print_matrix_reverse_transpose(char[i])
    


# Clean
if (debug == False):
    os.remove(output_bmp)
    os.remove(tmp_file)


