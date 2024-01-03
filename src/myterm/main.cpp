// Copyright (C) 2024 Manuel Perez 
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
 *	"My terminal"
 *	Pues eso: un terminal más.
 *
 * HISTORIA
 *    Manuel Perez
 *    03/01/2024 Escrito. Basado en el ejemplo de `alp`.
 *
 ****************************************************************************/
#include <iostream>
#include <exception>

#include <alp_getopts.h>

#include "myterm.h"


constexpr char USAGE[] =
"Terminal\n"
"Forma de uso: myterm [--help] TODO \n"
"Argumentos:\n"
"    TODO\n"
"Opciones:\n"
"    --help     Muestra esta ayuda.\n";


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

// Options
};



void Main_app::parse_command_line(int argc, char* argv[])
{
    app_name_ = argv[0];

    bool help;

    alp::Getopts getopts{num_args, USAGE};

    getopts.add_option('h', help);
    getopts.add_option("help", help);


    auto files = getopts.parse(argc, argv);


    if (help){
	std::cerr << USAGE;
	exit(1);
    }
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
    myterm();
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
