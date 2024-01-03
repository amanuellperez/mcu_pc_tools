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
#include <alp_termios_iostream.h>
#include "avr_termios.h"

#include <iostream>


/* Use this variable to remember original terminal attributes. */
static alp::Termios_cfg old_cin_cfg;

static void reset_input_mode ()
{
    old_cin_cfg.apply_cfg_now(STDIN_FILENO);
}


void cfg_cin()
{
    /* Make sure stdin is a terminal. */
    if (!::isatty (STDIN_FILENO))
	throw std::runtime_error{"cfg_cin"};

    /* Save the terminal attributes so we can restore them later. */
    old_cin_cfg.copy_cfg_from(STDIN_FILENO);
    ::atexit (reset_input_mode);

    /* Set the funny terminal modes. */
    alp::Termios_cfg cfg;
    cfg.copy_cfg_from(STDIN_FILENO);

    cfg.noncanonical_polling_read();
    if (cfg.apply_cfg_now(STDIN_FILENO) == -1)
	throw std::runtime_error("cfg_cin::apply_cfg_now");
}


void myterm()
{

    std::string usb_port = "/dev/ttyUSB0";
    alp::Termios_cfg usb_cfg;
    alp::cfg_avr_uart_polling_read(usb_cfg); 

    alp::Termios_iostream usb{usb_port, usb_cfg};
    cfg_cin();

    // Observar la forma de hacer el polling. No puedo usar los operadores >>
    // ya que bloquean. Necesitamos llamar a read directamente.
    while (1){
	char c;
	if (::read(usb.fd(), &c, 1))
	    std::cout << c << std::flush;

	if (::read(STDIN_FILENO, &c, 1)){
	    if (c == '\n')
		usb << '\r';
	    else
		usb << c;
	}

	if (!std::cin)
	    throw std::runtime_error{"stdin error!!!"};

	if (!usb)
	    throw std::runtime_error{"usb error!!!"};
    }

}






