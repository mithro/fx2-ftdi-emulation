# This repo is a **WIP**

This repository is a **WIP** and currently does **not** work. I would love
contributions to make it work.

This repository aims to contains firmware for the [Cypress FX2]() which enables 
it to emulate much of the behaviour of the [FTDI serial converter chips]().

The primary purpose of this firmware is to enable the usage of the FX2 as a USB
[JTAG programmer]() with many popular existing tools.

The emulation has been created based on how two primary boards operate, both
which have the FTDI FT2232H chip on them.

 * [Pipistrello](http://pipistrello.saanlima.com/index.php?title=Welcome_to_Pipistrello)
 * [TIAO USB Multi-Protocol Adapter (JTAG, SPI, I2C, Serial)](http://www.diygadget.com/tiao-usb-multi-protocol-adapter-jtag-spi-i2c-serial.html)

The secondary purpose is to allow easy interfacing to many common FPGA systems.

The firmware also aims to provide a common interface to both FX2 hardware and
optimised bit banging routines.

The boards supported are;

 * Digilent Atlys
 * Numato Opsis

 * TODO: More? Should be able to support everything in ixo-usb-jtag.
 * TODO: Xilinx Platform Cable

The tools which have currently been tested are;

 * TODO: xc3sprogs
 * TODO: urjtag
 * TODO: OpenOCD

 * TODO: More? Should be able supported by everything that also supports the
   [TIAO USB Multi-Protocol Adapter (JTAG, SPI, I2C, Serial)](http://www.tiaowiki.com/w/JTAG_Tutorials)


# Third Party

 * `libftdi.h` comes from http://www.intra2net.com/en/developer/libftdi/
 * `ftdi_sio.h` and `ftdi_sio_ids.h` comes from Linux Kernel

