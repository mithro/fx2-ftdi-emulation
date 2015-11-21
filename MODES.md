
## UART Modes

 * TXD
 * RXD

The following pins are optional;

 * RTS - Ready to Send (handshake output)
 * CTS - Clear to Send (handshake input)
 * DTR - Data Transmit Ready (modem signalling)
 * DSR - Data Carrier Detect (modem signalling)
 * RI  - Ring indicator (modem signalling)
 * TXDEN - Enable TX (RS485)
 * RXLED - Receive LED
 * TXLED - Transmit LED

If using a 100 pin FX2 or greater, the TXD/RXD can be mapped to the hardware
UART for increased performance. Otherwise the signals need to be bit banged.

The optional signals all need to be bit banged.

## FIFO Modes

 * Data[7..0]
 * FIFO Not Empty
 * FIFO Full
 * Read data
 * Write data
 * Wakeup
 * Output Enable
 * Address Bit (only for CPU FIFO)

If the mapping is correct, the FX2 can use the "Slave FIFO" or GPFIF mode which
dramatically increases performance.

Otherwise the FIFO mode is emulated by the CPU -- this is slow.

## MPSSE Modes - JTAG, SPI

 * Clock
 * Out
 * In
 * Extra

If using a 100 pin FX2 or greater, the Clock/Out/In can be mapped to the
hardware UART for increased performance. Otherwise the signals need to be bit
banged.


# Bit Banging Modes

There are two different bit banging modes;

 * Bit operations - These use the 8051 bit set / bit clear / bit test operations.
 * Byte operations - This is used when the pins are on Port E, which isn't compatible with the bit set operations.

