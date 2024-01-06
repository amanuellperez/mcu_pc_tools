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

#include <atd_ascii.h>

#include <alp_termios_cfg.h>
#include <alp_termios_iostream.h>

struct Myterm_cfg{
// Conexión
    std::string serial_port = "/dev/ttyUSB0";
    int baud_rate        = 9600;

// Cfg
    std::string output_file; // si !empty() guardamos la salida ahí también
    static constexpr const char output_file_default_name[] = "myterm_file.dat";
    bool no_print_cout = false; // sacamos por pantalla la salida?

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
// static cfg
    static constexpr char char_ctrl = atd::ASCII::Ctrl::A;

// Data
    alp::Termios_iostream usb_;	// name??? tty_? term_? ...?
    std::ofstream fout_;    
    std::string output_file_name_ = Myterm_cfg::output_file_default_name; 
    
// Cfg
    bool print_cout_ = true;

// Functions
    void init(const Myterm_cfg& cfg);
	void usb_init(const Myterm_cfg& cfg);
	void cin_init();
	void file_init(const std::string& fname);

    void open_fout(const std::string& fname);

    void run();
    void control_command();
	void change_save_file();
	void change_cout_log() {print_cout_ = !print_cout_;}

    void print(std::ostream& out, std::ofstream& file, char c);

// Static interface
    static void hello(std::ostream& out, const Myterm_cfg& cfg);

    static void cout_print(std::ostream& out, char c);
    static void file_print(std::ofstream& out, char c);

    static bool isprint(char c);
    
};



#endif



