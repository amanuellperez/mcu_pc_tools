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


#pragma once

#ifndef __MAIN_H__
#define __MAIN_H__


#include <filesystem>


// Devuelve el nombre del fichero sin extensión
inline std::string fname_without_extension(const std::string& name)
{ return std::filesystem::path{name}.replace_extension(); }

inline std::string fname_img(const std::string& fname)
{
    std::string fout = fname_without_extension(fname);
    fout += ".jpg";
    return fout;
}


#endif


