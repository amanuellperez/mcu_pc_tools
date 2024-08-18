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
#       Este script se encarga de convertir la salida de ttf2txt.py en .cpp
#
#       En lugar de generar el .cpp directamente a partir del ttf lo
#       genero el .txt para poder editarlo a mano y modificar las letras a
#       gusto del personal.
#
#  HISTORIA
#    Manuel Perez
#    17/08/2024 Primer intento
#
#****************************************************************************/
import os, sys, argparse
import string, datetime


# **************************************************************************
#                               FUNCTIONS
# **************************************************************************
# Borra la columna j de la matriz x
def matrix_remove_column(x, j):
    for i in range(len(x)):
        x[i].pop(j)



# Devuelve True si la columna j de la matriz x tiene el caracter c
def column_has_char(x, j, c):

    for i in range(len(x)):
        if (x[i][j] == c):
            return True

    return False



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


def print_zeros_to_complete_bytes(n):
    if (n <= 8):
        print ('0' * (8 - n), end = '')
        return

    if (n <= 16):
        print ('0' * (16 - n), end = '')
        return

    if (n <= 32):
        print ('0' * (32 - n), end = '')
        return

    if (n <= 64):
        print ('0' * (64 - n), end = '')
        return

    print ("ERROR: too many zeros")
    exit(1)

def print_matrix(matrix):
    n = len(matrix)
    m = len(matrix[0])

    for i in range(n):
        print ("0b", end = '')
        print_zeros_to_complete_bytes(n)
        for j in range(m):
            print (matrix[i][j], end = '')

        if (j != n-1):
            print (", ", end = '')

def print_matrix_transpose(matrix):
    n = len(matrix)
    m = len(matrix[0])

    for j in range(m):
        print ("0b", end = '')
        print_zeros_to_complete_bytes(n)
        for i in range(n):
            print (matrix[i][j], end = '')

        if (j != m-1):
            print (", ", end = '')


def print_matrix_reverse_transpose(matrix):
    n = len(matrix)
    m = len(matrix[0])

    for j in range(m):
        print ("0b", end = '')
        print_zeros_to_complete_bytes(n)
        for i in range(n - 1, -1, -1):
            print (matrix[i][j], end = '')

        if (j != m - 1):
            print (", ", end = '')





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

# Añade k columnas a la matriz x
def add_zero_columns_to(x, k):
    if (k == 0):
        return

    n = len(x)
    m = len(x[0])

    for i in range(n):
        for s in range(k):
            x[i].append('0')



# Hacemos todos los chars del mismo ancho
def resize_all_chars_same_size(char):
    col = 0

    for k in range(len(char)):
        c = len(char[k][0])
        if (c > col):
            col = c

    for k in range(len(char)):
        c = len(char[k][0])
        add_zero_columns_to(char[k], col - c)



# char: array de matrices de caracteres
# Devuelve el indice j1 de las columnas que hay que borrar (las columnas [0,
# j1] de todas las matrices del array char están en blanco)
# Devuelve -1 en caso de que no haya que borrar ninguna columna
def j_index_of_left_column_to_delete(char):
    
    jblank = -1     # columna a borrar

    for k in range(len(char)):
        j = -1  # uso -1 para saber si la columna 0 tiene '1'
        while(column_has_char(char[k], j + 1, '1') == False):
            j += 1
            if (j + 1 == len(char[k][0])):  # El space son todo blancos
                break

        if (k == 0): 
            jblank = j

        else:
            if (jblank > j):
                jblank = j

    return jblank

# char: array de matrices de caracteres
# Devuelve el indice j1 de las columnas que hay que borrar (las columnas [j1,
# end) de todas las matrices del array char están en blanco)
# Devuelve -1 en caso de que no haya que borrar ninguna columna
def j_index_of_right_column_to_delete(char):
    
    jblank = -1     # columna a borrar
    for k in range(len(char)):
        j = 0   # la primera columna es -1
        while(column_has_char(char[k], -(j + 1), '1') == False):
            j += 1
            if (j + 1 == len(char[k][0])):  # El space son todo blancos
                break

        if (k == 0): 
            jblank = j

        else:
            if (jblank > j):
                jblank = j

    return jblank


# char: array de matrices con los caracteres
def remove_lateral_blank_columns(char):

    # Quitamos columnas blancas del lado izdo
    j1 = j_index_of_left_column_to_delete(char)
    if (j1 != -1):
        for k in range(len(char)):
            for j in range(j1 + 1):
                matrix_remove_column(char[k], 0)

    # Quitamos columnas blancas del lado dcho
    j1 = j_index_of_right_column_to_delete(char)
    if (j1 != 0):
        for k in range(len(char)):
            for j in range(j1):
                matrix_remove_column(char[k], -1)


# DUDA: ¿Quién debe ser el autor que aparece en la licencia?
#       A fin de cuentas está generado automáticamente. Mejor
#       `ttf_txt2bin.py`?
def print_gpl_license():
    print ("// Copyright (C) ", end ='')
    print (datetime.datetime.today().year, end = '')
    print (" Manuel Perez ")
    print ("//           mail: <manuel2perez@proton.me>")
    print ("//           https://github.com/amanuellperez/mcu")
    print ("//")
    print ("// This file is part of the MCU++ Library.")
    print ("//")
    print ("// MCU++ Library is a free library: you can redistribute it and/or modify")
    print ("// it under the terms of the GNU General Public License as published by")
    print ("// the Free Software Foundation, either version 3 of the License, or")
    print ("// (at your option) any later version.")
    print ("//")
    print ("// This library is distributed in the hope that it will be useful,")
    print ("// but WITHOUT ANY WARRANTY; without even the implied warranty of")
    print ("// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the")
    print ("// GNU General Public License for more details.")
    print ("//")
    print ("// You should have received a copy of the GNU General Public License")
    print ("// along with this program.  If not, see <https://www.gnu.org/licenses/>.")
    print ("\n")
    print ("// This file has been generated automatically by `ttf_txt2bin.py`")
    print ("\n")

def print_header(font_name, only_digits, nrows, ncols, nchars):
    print ("#pragma once")
    tag = "__ROM_FONT_" + font_name;
    if (only_digits):
        tag += "_NUMBER"

    tag += "_" + str(nrows) + "x" + str(ncols) + "_H__"
    print ("#ifndef " + tag.upper())
    print ("#define " + tag.upper())

    print ("\n#include <atd_rom.h>")
    print ("// #include <avr_memory.h> <-- hay que incluirlo antes de este archivo")
    print ("\nnamespace rom{")
    print ("namespace font_" + font_name.lower() + "_" + str(nrows) + "x" +
           str(ncols) + "{")

    print ("\nusing ROM_read = MCU::ROM_read;\n")

    if (only_digits == False):
        print ("constexpr uint8_t font_index0 = 32;");

    print ("constexpr uint8_t font_rows   = " + str(nrows) + "; // número de filas que tiene cada font")
    print ("constexpr uint8_t font_cols   = " + str(ncols) + "; // número de columnas que tiene cada font")
    print ("constexpr uint8_t font_nchars = " + str(nchars) + "; // número de caracteres")

    print ("\nconstexpr")
    print ("atd::ROM_biarray<", end = '')
    # TODO: puede ser de uint16_t !!!
    print ("uint8_t", end = '')
    print (", font_nchars, font_cols, ROM_read> font")
    print ("\tPROGMEM = {")

    
def print_tail():
    print ("};")
    print ("\n\n} // namespace font")
    print ("} // namespace rom")
    print ("\n#endif")
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
                    description="Convert ouput of ttf2txt.py in txt file")

parser.add_argument("txt_file", help="output of ttf2txt.py file")
parser.add_argument("-p", "--print_type",
                    default=PRINT_MATRIX_REVERSE_TRANSPOSE,
                        type=int,
                        help="0 = print matrix; 1 = print matrix transpose; 2 = print matrix reverse transpose")
#parser.add_argument("-d", "--debug", action="store_true", default=False)
args = parser.parse_args()

txt_file   = args.txt_file
#debug       = args.debug
print_type = args.print_type


# Fase validación
# ---------------
if (os.path.isfile(txt_file) == False):
    print("Can't find file " + txt_file)
    exit(1)


output = os.path.splitext(txt_file)[0]
output_spl = output.split("_")
font_name = output_spl[0]
if (output_spl[1] == "number"):
    only_digits = True
else:
    only_digits = False



# main
# ----
ascii_char =" !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}"
if (only_digits):
    ascii_char ="0123456789"


# Convertimos el fichero en matriz
y = read_file_as_matrix(txt_file, True)

# Lo descomponemos en un array de matrices, cada matriz con el caracter
# correspondiente
char = split_as_array(y)

# Parece ser que al generar el txt a partir del ttf no todos los caracteres
# son del mismo ancho
resize_all_chars_same_size(char)

remove_lateral_blank_columns(char)

nchars = len(char)         # número de caracteres
nrows  = len(char[0])      # núm. de filas que tiene un caracter
ncols  = len(char[0][0])   # núm. de columnas que tiene un caracter

print_gpl_license()
print_header(font_name, only_digits, nrows, ncols, nchars)

for i in range(nchars):
    if (print_type == PRINT_MATRIX):
        print_matrix(char[i])

    elif (print_type == PRINT_MATRIX_TRANSPOSE):
        print_matrix_transpose(char[i])

    elif (print_type == PRINT_MATRIX_REVERSE_TRANSPOSE):
        print_matrix_reverse_transpose(char[i])

    if (i != nchars - 1):
        print (", ", end = '')

    print ("// ", end = '')

    if (ascii_char[i] != '\\'):  # el \ es problemático
        print (ascii_char[i], end ='')

    print ("", end='\n')

    

print_tail()

