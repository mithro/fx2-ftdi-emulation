"""
Efficient i2c operation in bitbanging software.
"""

import pins
import software as sw
import calling

# Create the shift byte commands
clock = sw.BitAccessInASM("i2c_clk", pins.Pin("A", 5), pins.PinDirection.output)
data = sw.BitAccessInASM("i2c_dat", pins.Pin("A", 3), pins.PinDirection.bidirectional)

byte_shifter = sw.ShiftByte(clock, data, data)

print("""\
/* Generated file from mpsse.py */

#include "fx2regs.h"
#include "fx2types.h"

""")
print(clock.defines())
print(data.defines())
print("""

""")

# i2c, you write on negative edge, read on the positive edge
# sda ▔▔▔▔\___XXXX--b0--XXXX--b1-- ...
# clk ▔▔▔▔▔▔▔\____/▔▔▔▔\____/▔▔▔▔\ ... 
#read_on=sw.ShiftOp.ClockMode.positive,
read_on = sw.ShiftOp.ClockMode.none
write_on = sw.ShiftOp.ClockMode.negative

body = []

body += ["/* Start bit */"]
body += data.setup(pins.PinDirection.output).splitlines()
body += data.clear().splitlines()

body += ["/* Byte shift */"]
body += byte_shifter.generate(
	direction=sw.ShiftOp.FirstBit.MSB,
	read_on=read_on,
	write_on=write_on,
	pad=True)

body += ["/* Ack / Stop Bit */"]
body += clock.clear().splitlines()
body += data.setup(pins.PinDirection.input).splitlines()
body += clock.set().splitlines()
# If carry is 1, then the bit was nacked
body += data.bit_to_carry().splitlines()
body += ["/* JC nacked */"]
# Loop here while bit is 0, clock stretching
body += data.bit_to_carry().splitlines()
body += ["/* JNC rel - */"]
# Success!
body += ["/* Success */"]
# Failure
body += ["/* Nacked response... */"]

print(calling.generate(
	name="i2cTest",
	read_on=read_on,
	write_on=write_on,
	body=body))

print("""\
BYTE main() {
	BYTE data = 0xaa;
	i2cTest(data);
	return 1;
}
""")
