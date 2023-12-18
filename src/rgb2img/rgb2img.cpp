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


#include "rgb2img.h"
#include "main.h"

#include <string>

#include <fstream>


static 
inline img::ColorRGB rgb444_to_color(uint8_t x, uint8_t y)
{ return img::ColorRGB{x & 0x0F, (y & 0xF0) >> 4, y & 0x0F}; }


static
img::Image rgb444_to_img(std::istream& in, int rows, int cols)
{
    img::Image img0{rows, cols};

    for (int i = 0; i < img0.rows() and in; ++i){
	for (int j = 0; j < img0.cols() and in; ++j){
	    uint8_t b0, b1;
	    in >> b0 >> b1;

	    img0(i, j) = rgb444_to_color(b0, b1);
	}
    }

    return img0;

}

void rgb444_to_img(const std::string& fname, int rows, int cols)
{
    std::ifstream in(fname);
    if (!in)
	throw std::runtime_error(alp::as_str() << "Can't open file " << fname);

    auto img0 = rgb444_to_img(in, rows, cols);

    img::write(img0, fname_img(fname));
}


static 
inline img::ColorRGB rgb555_to_color(uint8_t x, uint8_t y)
{ return img::ColorRGB{(x & 0x7C) >> 2, 
		       ((x & 0x03) << 3) | (y & 0xE0) >> 5, y & 0x1F}; }

static
img::Image rgb555_to_img(std::istream& in, int rows, int cols)
{
    img::Image img0{rows, cols};

    for (int i = 0; i < img0.rows() and in; ++i){
	for (int j = 0; j < img0.cols() and in; ++j){
	    uint8_t b0, b1;
	    in >> b0 >> b1;

	    img0(i, j) = rgb555_to_color(b0, b1);
	}
    }

    return img0;

}

void rgb555_to_img(const std::string& fname, int rows, int cols)
{
    std::ifstream in(fname);
    if (!in)
	throw std::runtime_error(alp::as_str() << "Can't open file " << fname);

    auto img0 = rgb555_to_img(in, rows, cols);

    img::write(img0, fname_img(fname));
}

static 
inline img::ColorRGB rgb565_to_color(uint8_t x, uint8_t y)
{ return img::ColorRGB{(x & 0xF8) >> 3, 
		       ((x & 0x07) << 3) | (y & 0xE0) >> 5,
		       y & 0x1F}; }

static
img::Image rgb565_to_img(std::istream& in, int rows, int cols)
{
    img::Image img0{rows, cols};

    for (int i = 0; i < img0.rows() and in; ++i){
	for (int j = 0; j < img0.cols() and in; ++j){
	    uint8_t b0, b1;
	    in >> b0 >> b1;

	    img0(i, j) = rgb565_to_color(b0, b1);
	}
    }

    return img0;

}

void rgb565_to_img(const std::string& fname, int rows, int cols)
{
    std::ifstream in(fname);
    if (!in)
	throw std::runtime_error(alp::as_str() << "Can't open file " << fname);

    auto img0 = rgb565_to_img(in, rows, cols);

    img::write(img0, fname_img(fname));
}


