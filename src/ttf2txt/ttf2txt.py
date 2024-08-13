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
#  USAGE
#       > ttf2txt.py font.ttf
#       Genera el fichero font.txt con las letras ascii
#
#  HISTORIA
#    Manuel Perez
#    13/08/2024 Primer intento
#
#****************************************************************************/
# Depende de: img2txt (proyecto app)
#   "img2txt -m image" genera un fichero de texto a partir
#   de la imagen 'image' con valores 0/255 (monocroma)
import os, sys, string

from PIL import Image, ImageFont

# args
# ----
if (len(sys.argv) < 2):
    print ("Usage: ttf2txt file.ttf [point_size]")
    sys.exit(1)


font_file=sys.argv[1]
if (len(sys.argv) >= 3):
    point_size = sys.argv[2]
else:
    point_size = 16


output_file=os.path.splitext(font_file)[0] + ".txt"

# main
# ----
# Genero un fichero a.m, b.m, ... por cada letra (la extensión .m
# la decide el programa img2txt -m)
font = ImageFont.truetype(font_file, point_size)

ascii_char ="!\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~"

i = 0   # no puedo usar el nombre de la letra para el fichero
        # ya que hay simbolos no validos como nombres
for c in ascii_char:
    i += 1
    print (c + " ... ", end='')
    imgfile = str(i) + ".bmp"

    img = Image.Image()._new(font.getmask(c))
    img.save(imgfile)

    res = os.system("img2txt -m " + imgfile)
    if res == 0:
        print ("OK")
    else:
        print ("FAIL")

    os.remove(imgfile);


# Concateno todos los ficheros en uno solo
# aprovechando para sustituir 0 y 255 por . y X
out = open(output_file, "w")

i = 0
for c in ascii_char:
    i += 1
    fname = str(i) + ".m"
    with open(fname, 'r') as f:
        letter = f.read()

    out.write("CHAR: " + c + "\n");
    out.write(letter.replace('0', '.')
                    .replace('255', 'X'))

    out.write("\n");
    os.remove(fname);
     




