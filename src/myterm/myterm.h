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

#pragma once

#ifndef __MYTERM_H__
#define __MYTERM_H__

#include <string>
#include <fstream>

#include <alp_termios_cfg.h>
#include <alp_termios_iostream.h>

struct Myterm_cfg{
// Conexión
    std::string serial_port = "/dev/ttyUSB0";
    int baud_rate        = 9600;

// Cfg
    std::string output_file;	// si !empty() guardamos la salida ahí también

// Helpers
    // cfg -> usb_cfg
    static
    void to_termios_cfg(const Myterm_cfg& cfg, alp::Termios_cfg& usb_cfg);

};

std::ostream& operator<<(std::ostream& out, const Myterm_cfg&);


class Myterm{
public:
    void open(const Myterm_cfg& cfg);
    
private:
// Data
    alp::Termios_iostream usb_;	// name??? tty_? term_? ...?
    
// Cfg
    std::ofstream fout_;    

// Functions
    void init(const Myterm_cfg& cfg);
	void usb_init(const Myterm_cfg& cfg);
	void cin_init();
	void file_init(const std::string& fname);

    void run();

// Static interface
    static void hello(std::ostream& out, const Myterm_cfg& cfg);

    static void print(std::ostream& screen, std::ofstream& file, char c);
    static void screen_print(std::ostream& out, char c);
    static void file_print(std::ofstream& out, char c);

    static bool isprint(char c);
    
};



#endif



