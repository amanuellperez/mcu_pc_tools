// Copyright (C) 2023 Manuel Perez 
//           mail: <manuel2perez@proton.me>
//           https://github.com/amanuellperez/mcu
//
// This file is part of the MCU++ Library.
//
// MCU++ Library is a free library: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// This library is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program.  If not, see <https://www.gnu.org/licenses/>.
/****************************************************************************
 *
 * DESCRIPCION
 *	Convierte el fichero de texto en imagen.
 *	El fichero de texto es uno generado por la camara OV7670
 *
 * HISTORIA
 *    Manuel Perez
 *    17/12/2023 Escrito
 *
 ****************************************************************************/
#include <iostream>
#include <exception>

#include <alp_getopts.h>

#include "rgb2img.h"


constexpr char USAGE[] =
"Crea una imagen a partir de un fichero en formato RGB444, RGB555 ó RGB565.\n"
"Forma de uso: rgb2img [--help] file\n"
"Argumentos:\n"
"    file       Nombre del fichero de entrada y nombre de la imagen generada.\n"
"Opciones:\n"
"    --help     Muestra esta ayuda.\n"
"    --rows rows Número de filas de la imagen.\n"
"    --cols cols Número de columnas que tiene la imagen.\n";


class Main_app{
public:
    void run(int argc, char* argv[]);

private:
    void parse_command_line(int argc, char* argv[]);
    void validate_command_line();
    void run();

// Data
    std::string app_name_;

// Args
    static constexpr int num_args = 0;
    std::string fin_;

// Options
    bool format_rgb444 = true;
    bool format_rgb555 = false;
    bool format_rgb565 = false;
    int cols = 0;
    int rows = 0;
};



void Main_app::parse_command_line(int argc, char* argv[])
{
    app_name_ = argv[0];

    bool help;
    cols = 0;
    rows = 0;

    alp::Getopts getopts{num_args, USAGE};

    getopts.add_option('h', help);
    getopts.add_option("help", help);
    getopts.add_option("rows", rows);
    getopts.add_option("cols", cols);

    getopts.add_option("rgb444", format_rgb444);
    getopts.add_option("rgb555", format_rgb555);
    getopts.add_option("rgb565", format_rgb565);

    auto files = getopts.parse(argc, argv);


    if (help){
	std::cerr << USAGE;
	exit(1);
    }

    if (rows == 0 or cols == 0){
	std::cerr << "Invalid number of rows or columns\n";
	exit(2);
    }

    if (files.size() != 1)
	throw std::runtime_error(USAGE);

    fin_ = files[0];
}

void Main_app::validate_command_line()
{
// ficheros de entrada existen?
// ficheros de salida no existen? si existen preguntar: lo reescribimos?
// opciones correctas?
}

void Main_app::run(int argc, char* argv[])
{
    parse_command_line(argc, argv);
    validate_command_line();
    run();
}

void Main_app::run()
{
    if (format_rgb555){
	std::cout << "RGB555 to image of " 
		  << rows << " rows and " << cols << " columns\n";
	rgb555_to_img(fin_, rows, cols);
    }

    else if (format_rgb565){
	std::cout << "RGB565 to image of " 
		  << rows << " rows and " << cols << " columns\n";
	rgb565_to_img(fin_, rows, cols);
    }

    else{ // default:
	std::cout << "RGB444 to image of " 
		  << rows << " rows and " << cols << " columns\n";
	rgb444_to_img(fin_, rows, cols);
    }
}



int main(int argc, char* argv[])
{
try{
    Main_app app;
    app.run(argc, argv);

}catch(std::exception& e){
    std::cerr << argv[0] << ": " << e.what() << '\n'; 
    return 1;
}

}
