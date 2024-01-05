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
#include <alp_termios_cfg.h>

struct Myterm_cfg{
    std::string serial_port = "/dev/ttyUSB0";
    int baud_rate        = 9600;

    // cfg -> usb_cfg
    static
    void to_termios_cfg(const Myterm_cfg& cfg, alp::Termios_cfg& usb_cfg);

};

void myterm(const Myterm_cfg& cfg);

std::ostream& operator<<(std::ostream& out, const Myterm_cfg&);

#endif



