// Copyright (C) 2024 Manuel Perez <manuel2perez@proton.me>
//
// This file is part of the ALP Library.
//
// ALP Library is a free library: you can redistribute it and/or modify
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

// Programa básico equivalente a screen. Probarlo con el test de uart.
#include "myterm.h"

#include <alp_termios_iostream.h>
#include "avr_termios.h"

#include <iostream>
#include <cctype>   // isprint
		    
#include <atd_ostream.h>


// Myterm_cfg
// ----------
// cfg -> usb_cfg
void Myterm_cfg::to_termios_cfg(const Myterm_cfg& cfg, alp::Termios_cfg& usb_cfg)
{
    usb_cfg.baud_rate(cfg.baud_rate);

    cfg_avr_uart_polling_read(usb_cfg); 
//    usb_cfg.print(std::cout);
}

std::ostream& operator<<(std::ostream& out, const Myterm_cfg& cfg)
{
    out << "Myterm_cfg\n";
    out << "\tserial_port = " << cfg.serial_port << '\n';
    out << "\tbaud_rate   = " << cfg.baud_rate << '\n';

    return out;
}




/* Use this variable to remember original terminal attributes. */
static alp::Termios_cfg old_cin_cfg;

static void reset_input_mode ()
{
    old_cin_cfg.apply_cfg_now(STDIN_FILENO);
}


void cin_init()
{
    /* Make sure stdin is a terminal. */
    if (!::isatty (STDIN_FILENO))
	throw std::runtime_error{"cin_init"};

    /* Save the terminal attributes so we can restore them later. */
    old_cin_cfg.copy_cfg_from(STDIN_FILENO);
    ::atexit (reset_input_mode);

    /* Set the funny terminal modes. */
    alp::Termios_cfg cfg;
    cfg.copy_cfg_from(STDIN_FILENO);

    cfg.noncanonical_polling_read();
    if (cfg.apply_cfg_now(STDIN_FILENO) == -1)
	throw std::runtime_error("cin_init::apply_cfg_now");
}

// std::isprint no considera printable: \n, \r
static inline bool isprint(char c)
{
    return std::isprint(c) or 
	    (c == '\n')	or
	    (c == '\r');
}

static void myterm_print(std::ostream& out, char c)
{
    if (isprint(c))
	out << c;

    else
	atd::print_int_as_hex(out, static_cast<uint8_t>(c), '\\');

    out.flush();
}

static void myterm_run(alp::Termios_iostream& usb)
{
    // Observar la forma de hacer el polling. No puedo usar los operadores >>
    // ya que bloquean. Necesitamos llamar a read directamente.
    while (1){
	char c;
	if (alp::read(usb, c))
	    myterm_print(std::cout, c);

	if (alp::cin_read(c))
	    usb << c;

	if (!std::cin)
	    throw std::runtime_error{"stdin error!!!"};

	if (!usb)
	    throw std::runtime_error{"usb error!!!"};
    }
}


static void myterm_hello(std::ostream& out, const Myterm_cfg& cfg)
{
    out << cfg << '\n';
}


void myterm(const Myterm_cfg& cfg)
{
// usb_init:
    alp::Termios_cfg usb_cfg;
    Myterm_cfg::to_termios_cfg(cfg, usb_cfg);

    alp::Termios_iostream usb{cfg.serial_port, usb_cfg};

    cin_init();

    myterm_hello(std::cout, cfg);
    myterm_run(usb);

}






