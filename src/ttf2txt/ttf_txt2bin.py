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
import string


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
parser.add_argument("-p", "--print_type", default=PRINT_MATRIX_TRANSPOSE,
                        type=int,
                        help="0 = print matrix; 1 = print matrix transpose; 2 = print matrix reverse transpose")
parser.add_argument("-n", "--number", action="store_true", default=False,
                        help="Generated only number char")
#parser.add_argument("-d", "--debug", action="store_true", default=False)
args = parser.parse_args()

txt_file   = args.txt_file
#debug       = args.debug
only_digits = args.number
print_type = args.print_type


# Fase validación
# ---------------
if (os.path.isfile(txt_file) == False):
    print("Can't find file " + txt_file)
    exit(1)


#output =os.path.splitext(txt_file)[0]


# main
# ----
ascii_char ="| |!|\"|#|$|%|&|'|(|)|*|+|,|-|.|/|0|1|2|3|4|5|6|7|8|9|:|;|<|=|>|?|@|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|[|\\|]|^|_|`|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|{|||}|"
if (only_digits):
    ascii_char="|0|1|2|3|4|5|6|7|8|9|"

# Convertimos el fichero en matriz
y = read_file_as_matrix(txt_file, True)

# Lo descomponemos en un array de matrices, cada matriz con el caracter
# correspondiente
char = split_as_array(y)

# Parece ser que al generar el txt a partir del ttf no todos los caracteres
# son del mismo ancho
resize_all_chars_same_size(char)

remove_lateral_blank_columns(char)

for i in range(len(char)):
    print ("// " + ascii_char[2*i + 1])
    
    if (print_type == PRINT_MATRIX):
        print_matrix(char[i])

    elif (print_type == PRINT_MATRIX_TRANSPOSE):
        print_matrix_transpose(char[i])

    elif (print_type == PRINT_MATRIX_REVERSE_TRANSPOSE):
        print_matrix_reverse_transpose(char[i])
    



