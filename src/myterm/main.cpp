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
"Forma de uso: myterm [--help] [--baud baud_rate] [--port serial_port]\n"
"                     [--save fname] [--no_cout]\n"
"Opciones:\n"
"   --help                 Muestra esta ayuda.\n"
"   --baud baud_rate       Pasamos el baud rate de la conexión.\n"
"   --no_cout              No muestra en pantalla lo que envia la conexión.\n"
"   --port serial_port     Cadena con el nombre del puerto donde conectarse.\n"
"   --save fname           Guarda la salida en el fichero `fname`.\n"
"\n\n"
"Terminal básico para poder conectar el atmega32 al PC vía el cable de FTDI.\n"
"La configuración se puede hacer por línea de comando, con las opciones\n"
"anteriores, o pulsando la combinación de teclas Ctrl+A+<tecla_comando>.\n\n";


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
    Myterm_cfg cfg;

// Options
};



void Main_app::parse_command_line(int argc, char* argv[])
{
    app_name_ = argv[0];

    bool help;

    alp::Getopts getopts{num_args, USAGE};

    getopts.add_option('h', help);
    getopts.add_option("help", help);

    getopts.add_option("baud", cfg.baud_rate);
    getopts.add_option("port", cfg.serial_port);
    getopts.add_option("save", cfg.output_file);
    getopts.add_option("no_cout", cfg.no_print_cout);


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
    Myterm term;
    term.open(cfg);
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
