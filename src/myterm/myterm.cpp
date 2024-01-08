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

constexpr char MYTERM_CONTROL_HELP[] =
"\n\nCtrl+A\n"
"       +h    Muestra esta ayuda.\n"
"       +s    [save] Graba (o deja de grabar) en el fichero de salida.\n"
"       +n    Escribe (o deja de escribir) la salida en std::cout\n"
"             (aunque de momento sigue haciendo `echo` del teclado).\n";

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



// Myterm
// ------
/* Use this variable to remember original terminal attributes. */
static alp::Termios_cfg old_cin_cfg;

static void reset_input_mode ()
{
    old_cin_cfg.apply_cfg_now(STDIN_FILENO);
}


void Myterm::cin_init()
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

   // cfg.noncanonical_polling_read();
    cfg.noncanonical_polling_read();
    if (cfg.apply_cfg_now(STDIN_FILENO) == -1)
	throw std::runtime_error("cin_init::apply_cfg_now");
}

// std::isprint no considera printable: \n, \r
inline bool Myterm::isprint(char c)
{
    return std::isprint(c) or 
	    (c == '\n')	or
	    (c == '\r');
}

void Myterm::cout_print(std::ostream& screen, char c)
{
    if (isprint(c))
	screen << c;

    else
	atd::print_int_as_hex(screen, static_cast<uint8_t>(c), '\\');

    screen.flush();
}



inline 
void Myterm::file_print(std::ofstream& out, char c)
{
    out << c << std::flush;
}

void Myterm::print(std::ostream& screen, std::ofstream& file, char c)
{
    if (print_cout_)
	cout_print(screen, c);

    if (file.is_open())
	file_print(file, c);
}

inline int cin_read(char& c, bool wait = false)
{
    if (wait == false)
	return alp::cin_read(c);

// else
    int n = 0;
    while (n == 0){
	n = alp::cin_read(c);
    }
    return n;
}

void Myterm::open_fout(const std::string& fname)
{
    fout_.open(fname);

// TODO: comprobar que el nombre sea de un fichero no existente

    if (!fout_){
	std::cerr << "Error: can't open file " << fname << '\n';
	return;
    }
}

void Myterm::change_save_file()
{
    if (fout_.is_open()){
	fout_.close();
	std::cerr << "\nClosing file " << output_file_name_ << '\n';
    }

    else {
	open_fout(output_file_name_);
	std::cerr << "\nSaving output in file " << output_file_name_ << '\n';
    }
}


void Myterm::control_command()
{
    char c;
    if (cin_read(c, true) <= 0)
	return;

    switch (c){
	break; case 's': change_save_file();
	break; case 'n': change_cout_log();
	break; case 'h': std::cerr << MYTERM_CONTROL_HELP;
		
    }
}

// wait for file descriptor event
void Myterm::wait_for_fd_event()
{
// std::cerr << '.'; // para mostrar el flujo
    if (poll(pfds_.data(), pfds_.size(), -1) == -1){
	perror("poll");
	throw std::runtime_error{"poll error"};
    }
}

// Observar la forma de hacer el polling. No puedo usar los operadores >>
// ya que bloquean. Necesitamos llamar a read directamente.
// TODO: nombre? no me gusta write_fd_event!!!
void Myterm::write_fd_event()
{
    char c;

    while(alp::read(usb_, c) > 0) // TODO: ahora puedo leer bloques de bytes
	print(std::cout, fout_, c);

    if (alp::cin_read(c)){
	if (c == char_ctrl)
	    control_command();

	else
	    usb_ << c;
    }

    if (!std::cin)
	throw std::runtime_error{"stdin error!!!"};

    if (!usb_)
	throw std::runtime_error{"usb error!!!"};
}

void Myterm::run()
{
    while (1){
	wait_for_fd_event();
	write_fd_event();
    }
}


void Myterm::hello(std::ostream& out, const Myterm_cfg& cfg)
{
    out << cfg << '\n';
}

void Myterm::usb_init(const Myterm_cfg& cfg)
{
    alp::Termios_cfg usb_cfg;
    Myterm_cfg::to_termios_cfg(cfg, usb_cfg);

    usb_.open(cfg.serial_port, usb_cfg);
}

void Myterm::file_init(const std::string& fname)
{
    if (fname.empty())
	return;

    output_file_name_ = fname;

    open_fout(fname);

}

void Myterm::poll_init()
{
    pfds_[0].fd	    = STDIN_FILENO;
    pfds_[0].events = POLLIN;

    pfds_[1].fd	    = usb_.fd();
    pfds_[1].events = POLLIN;
}

void Myterm::init(const Myterm_cfg& cfg)
{
    usb_init(cfg);
    cin_init();
    file_init(cfg.output_file);
    poll_init();

    print_cout_ = !cfg.no_print_cout;
}

void Myterm::open(const Myterm_cfg& cfg)
{
    init(cfg);
    hello(std::cout, cfg);
    run();
}






