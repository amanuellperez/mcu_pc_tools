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
#                               CONSTANTES
# **************************************************************************
# Formato de salida
PRINT_MATRIX_BY_ROWS_LOOKING_FROM_THE_FRONT = 0
PRINT_MATRIX_BY_ROWS_LOOKING_FROM_THE_BACK  = 1
PRINT_MATRIX_COLUMNS_LEFT                   = 2
PRINT_MATRIX_COLUMNS_RIGHT                  = 3

# **************************************************************************
#                           MATRIX FUNCTIONS
# **************************************************************************

def matrix_empty(rows, cols):
    return [[None for i in range(cols)] for j in range(rows)]
#    return [[None]*cols]*rows <-- esto crea una shallow list!

def matrix_rotate_to_the_right(matrix):
    m = len(matrix) # numero de filas
    n = len(matrix[0]) # numero de columnas

    res = matrix_empty(n, m)

    for i in range(m):
        for j in range(n):
            I = j
            J = m - 1 - i
            res[I][J] = matrix[i][j]

    return res
 
def matrix_rotate_to_the_left(matrix):
    m = len(matrix) # numero de filas
    n = len(matrix[0]) # numero de columnas

    res = matrix_empty(n, m)

    for i in range(m):
        for j in range(n):
            I = n - 1 - j
            J = i
            res[I][J] = matrix[i][j]

    return res
            

def matrix_look_from_the_back(matrix):
    m = len(matrix) # numero de filas
    n = len(matrix[0]) # numero de columnas

    res = matrix_empty(m, n)

    for i in range(m):
        for j in range(n):
            I = i
            J = n - 1 - j
            res[I][J] = matrix[i][j]

    return res

# imprimimos la matriz como uint8_t
def print_matrix(matrix):
    m = len(matrix)     # número de filas del caracter
    n = len(matrix[0])  # número de columnas del caracter

    nbytes = int(n / 8)
    if ((n % 8) != 0):
        nbytes += 1

    for i in range(m):
        for b in range(nbytes):
            
            print ("0b", end = '')
            
            for k in range(8):
                j = 8*b + k
                if (j < n):
                    print (matrix[i][j], end = '')
                else:
                    print ('0', end = '')   # padding con 0 el último byte

            if (b != nbytes - 1 or i != m - 1):
                print (", ", end = '')



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


# **************************************************************************
#                               FUNCTIONS
# **************************************************************************
def print_matrix_by_rows_looking_from_the_front(matrix):
    print_matrix(matrix)


def print_matrix_by_rows_looking_from_the_back(matrix):
    res = matrix_look_from_the_back(matrix)
    print_matrix(res)


def print_matrix_by_columns_turn_left(matrix):
    res = matrix_rotate_to_the_left(matrix)
    print_matrix(res)


# En los displays como el SDD1306 se escribe por 'pages', esto es, se escribe
# a la vez los 8 bits en una columna, escribiendo de los bits menos
# significativos a los mas (fila[0] = bit[0], fila[1] = bit[1] ...)
# (ver fig. 8-14 de la datasheet).
# Cuando queremos escribir glyphs de más de 1 byte de altura, tenemos que
# escribir los bytes respetando ese orden (doy por supuesto que escribimos en
# modo vertical)
# Ejemplo:
#   Supongamos que queremos escribir el siguiente '2' que tiene 2 bits de
#   altura
#
#   . . X X X X . . .
#   . . X X X X . . . 
#   X X . . . . X X . 
#   X X . . . . X X . 
#   . . . . X X . . .  
#   . . . . X X . . . 
#   . . X X . . . . . 
#   . . X X . . . . . 
#   X X . . . . . . . 
#   X X . . . . . . . 
#   X X X X X X X X . 
#   X X X X X X X X . 
#   . . . . . . . . . 
#   . . . . . . . . . 
#   . . . . . . . . . 
#   . . . . . . . . . 
#
#  Si nos fijamos en la primera columna:
#
#   . 0 <-- este es el bit menos significativo para el SDD1306
#   . 0
#   X 1
#   X 1  <-- 1er byte a escribir
#   . 0
#   . 0
#   . 0
#   . 0
# -------
#   X 1 <-- este es el bit menos significativo para el SDD1306
#   X 1
#   X 1
#   X 1  <-- 2º byte a escribir
#   . 0
#   . 0
#   . 0
#   . 0
# Para escribir esta columna (usando el modo vertical) en el SDD1306 tenemos
# que usar los bytes:
#       0b00001100, 0b00001111
# Lo que hacemos es descomponer la columna en bytes y cada byte "girarlo hacia
# la derecha" (en el sentido de las agujas del reloj)
def print_matrix_by_columns_turn_right(matrix):
    res = matrix_rotate_to_the_right(matrix)
    print_matrix(res)




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

def is_by_rows(print_type):
    if (print_type == PRINT_MATRIX_BY_ROWS_LOOKING_FROM_THE_FRONT
        or 
        print_type == PRINT_MATRIX_BY_ROWS_LOOKING_FROM_THE_BACK):
        return True

    else:
        return False

def print_type_trait(print_type):
    if (print_type == PRINT_MATRIX_BY_ROWS_LOOKING_FROM_THE_FRONT):
        print ("static constexpr bool is_looking_from_the_front{};")

    elif(print_type == PRINT_MATRIX_BY_ROWS_LOOKING_FROM_THE_BACK):
        print ("static constexpr bool is_looking_from_the_back{};")

    elif(print_type == PRINT_MATRIX_COLUMNS_RIGHT):
        print ("static constexpr bool is_turned_to_the_right{};")

    elif(print_type == PRINT_MATRIX_COLUMNS_LEFT):
        print ("static constexpr bool is_turned_to_the_left{};")

def print_row_or_cols_in_bytes(nrows, ncols, print_type):
    if (print_type == PRINT_MATRIX_BY_ROWS_LOOKING_FROM_THE_FRONT
        or 
        print_type == PRINT_MATRIX_BY_ROWS_LOOKING_FROM_THE_BACK):
        bytes_in_a_row = int(ncols/ 8) 

        if (ncols % 8):
            bytes_in_a_row += 1

        print ("static constexpr uint8_t bytes_in_a_row   = " 
                    + str(bytes_in_a_row) + "; // número de bytes que tiene cada fila")

        print ("static constexpr uint8_t rows_in_bytes = " + str(nrows) + ";")
        print ("static constexpr uint8_t cols_in_bytes = " +
                                                    str(bytes_in_a_row) + ";")

        return True

    else:
        # CUIDADO: el número de bytes que tiene una columna se calcula a
        # partir del número de filas!!
        bytes_in_a_column = int(nrows/ 8) 

        if (nrows % 8):
            bytes_in_a_column += 1

        print ("static constexpr uint8_t bytes_in_a_column= " 
                    + str(bytes_in_a_column) + "; // número de bytes que tiene cada columna")
        print ("static constexpr uint8_t rows_in_bytes = " +
                    str(bytes_in_a_column) + ";")
        print ("static constexpr uint8_t cols_in_bytes = " +
                                                    str(ncols) + ";")

        return False

def print_header(font_name, only_digits, print_type,
                  nrows, ncols, nchars):

    by_rows = is_by_rows(print_type)

    print ("#pragma once")
    tag = "__ROM_FONT_" + font_name + "_H__"

    print ("#ifndef " + tag.upper())
    print ("#define " + tag.upper())

    print ("\n#include <atd_rom.h>")
    print ("// #include <avr_memory.h> <-- hay que incluirlo antes de este archivo")
    print ("\nnamespace rom{")
    print ("namespace font_" + font_name + "{")

    print ("\nusing ROM_read = MCU::ROM_read;\n")

    print ("struct Font{")

    print ("// Traits requirements")

    if (by_rows):
        print ("static constexpr bool is_by_rows{};")
    else:
        print ("static constexpr bool is_by_columns{};")

    print_type_trait(print_type)

    print ("static constexpr bool is_ASCII_font{};")


    print ("\n// Número de caracteres")
    print ("static constexpr uint8_t nchars = " + str(nchars) + ";")

    # TODO: mas que `only_digits` realmente el parámetro es `is_ascii_font`
    if (only_digits == False):
        print ("\n// Los códigos ASCII empiezan en 32")
        print ("static constexpr uint8_t index(char c) {return c - 32;}")
    else:
        print ("static constexpr uint8_t index(char c) {return c;}")


    print ("\n// Dimensions")
    print ("static constexpr uint8_t rows = " 
                + str(nrows) + "; // número de filas que tiene cada font")
    print ("static constexpr uint8_t cols = " 
                + str(ncols) + "; // número de columnas que tiene cada font")

    print ("\n// Tamaño en bytes")
    print_row_or_cols_in_bytes(nrows, ncols, print_type)


    print ("inline static constexpr uint8_t char_byte_size() ", end='')
    if (by_rows == True):
        print ("{return rows * bytes_in_a_row;}")
    else:
        print ("{return cols * bytes_in_a_column;}")

    print ("\nstatic constexpr")
    print ("atd::ROM_biarray<", end = '')
    print ("uint8_t", end = '')

    if (by_rows == True):
        print (", nchars, rows*bytes_in_a_row, ROM_read> glyph")
    else:
        print (", nchars, cols*bytes_in_a_column, ROM_read> glyph")

    print ("\tPROGMEM = {")

    
def print_tail():
    print ("}; // glyphs")

    print ("}; // struct Font")
    print ("\n\n} // namespace font")
    print ("} // namespace rom")
    print ("\n#endif")


def output_name(iname, only_digits, print_type, char):
    nrows  = len(char[0])      # núm. de filas que tiene un caracter
    ncols  = len(char[0][0])   # núm. de columnas que tiene un caracter

    oname = iname;
    if (only_digits):
        oname += "_number"

    oname += "_" + str(ncols) + "x" + str(nrows)

    if (print_type == PRINT_MATRIX_BY_ROWS_LOOKING_FROM_THE_FRONT):
        oname += "_rf"

    elif (print_type == PRINT_MATRIX_BY_ROWS_LOOKING_FROM_THE_BACK):
        oname += "_rb"

    elif (print_type == PRINT_MATRIX_COLUMNS_LEFT):
        oname += "_cl"

    elif (print_type == PRINT_MATRIX_COLUMNS_RIGHT):
        oname += "_cr"

    return oname

def print_output(char, only_digits, print_type, ascii_char):
    nchars = len(char)         # número de caracteres
    nrows  = len(char[0])      # núm. de filas que tiene un caracter
    ncols  = len(char[0][0])   # núm. de columnas que tiene un caracter

    print_gpl_license()
    print_header(oname, only_digits, print_type, nrows, ncols, nchars)

    for i in range(nchars):
        if (print_type == PRINT_MATRIX_BY_ROWS_LOOKING_FROM_THE_FRONT):
            print_matrix_by_rows_looking_from_the_front(char[i])

        elif (print_type == PRINT_MATRIX_BY_ROWS_LOOKING_FROM_THE_BACK):
            print_matrix_by_rows_looking_from_the_back(char[i])

        elif (print_type == PRINT_MATRIX_COLUMNS_LEFT):
            print_matrix_by_columns_turn_left(char[i])

        elif (print_type == PRINT_MATRIX_COLUMNS_RIGHT):
            print_matrix_by_columns_turn_right(char[i])

        if (i != nchars - 1):
            print (", ", end = '')

        print ("// ", end = '')

        if (ascii_char[i] != '\\'):  # el \ es problemático
            print (ascii_char[i], end ='')

        print ("", end='\n')

    print_tail()



# **************************************************************************
#                               MAIN
# **************************************************************************
# args
# ----

parser = argparse.ArgumentParser(
                    description="Convert ouput of ttf2txt.py in txt file",
                    formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument("txt_file", help="output of ttf2txt.py file")
parser.add_argument("-p", "--print_type",
                    default=PRINT_MATRIX_COLUMNS_RIGHT,
                        type=int,
help='''0 = print matrix by rows, looking from the front
1 = print matrix by rows, looking from the back
2 = print matrix by columns, turning to the left the characters
3 = print matrix by columns, turning to the right the characters''')
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


iname = os.path.splitext(txt_file)[0]
iname_spl = iname.split("_")
font_name = iname_spl[0]

if (iname_spl[1] == "number"):
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



# ---------------
# print_output():
# ---------------

oname = output_name(font_name, only_digits, print_type, char)
cpp_name = "rom_font_" + oname+ ".h"    # es un .h!!!

# print_file(oname):
sys.stdout = open(cpp_name, "w")
print_output(char, only_digits, print_type, ascii_char)

