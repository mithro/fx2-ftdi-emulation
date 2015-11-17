
"""
Generate the shift functions needed by the MPSSE module.

Bytes || Bits
(MSB || LSB) First
Out on (+ve || -ve)
 In on (+ve || -ve)

"""

import software as sw

# Create the shift byte commands
clock = sw.BitAccessInASM("clk", sw.BitDirection.output, "A", 5)
data_in = sw.BitAccessInASM("din", sw.BitDirection.input, "A", 3)
data_out = sw.BitAccessInASM("dout", sw.BitDirection.output, "A", 2)

byte_shifter = sw.ShiftByte(clock, data_in, data_out)

combos = []
for d in sw.ShiftOp.FirstBit:
	for read_on in sw.ShiftOp.ClockMode:
		for write_on in sw.ShiftOp.ClockMode:
			if read_on == sw.ShiftOp.ClockMode.none and write_on == sw.ShiftOp.ClockMode.none:
				continue
			combos.append((d, read_on, write_on))

print("""\
/* Generated file from mpsse.py */

#include "fx2regs.h"
#include "fx2types.h"

""")
print(clock.defines())
print(data_in.defines())
print(data_out.defines())
print("""

""")

for d, read_on, write_on in combos:
	name = ["ShiftByte"]
	if d == sw.ShiftOp.FirstBit.MSB:
		name.append("MSBFirst")
	elif d == sw.ShiftOp.FirstBit.LSB:
		name.append("LSBFirst")

	if read_on == sw.ShiftOp.ClockMode.positive:
		name.append("inOnPos")
	elif read_on == sw.ShiftOp.ClockMode.negative:
		name.append("inOnNeg")
	if write_on == sw.ShiftOp.ClockMode.positive:
		name.append("outOnPos")
	elif write_on == sw.ShiftOp.ClockMode.negative:
		name.append("outOnNeg")
	name = "_".join(name)

	defs = ''
	args = ''
	if read_on != sw.ShiftOp.ClockMode.none:
		if write_on != sw.ShiftOp.ClockMode.none:
			args = 'BYTE data'
			defs = """
	(data);
	__asm__("mov	a,dpl");	/* Move data->a */
"""
		else:
			defs = """
	__asm__("clr	a");		/* Get accumulator ready */
"""

		rettype = 'BYTE'
		ret = """
	__asm__("mov	dpl,a");		/* Move a->retvalue */
	return;					/* return */
"""
	else:
		rettype = 'void'
		ret = 'return;'

	output = "\n	".join(byte_shifter.generate(d, read_on, write_on))

	print("""\
/* ---------------------------- */
%(rettype)s %(name)s(%(args)s) {
	%(defs)s
	%(output)s
	%(ret)s
}
/* ---------------------------- */
""" % locals())


print("""\
BYTE main() {
	BYTE data = 0xaa;

	data = ShiftByte_MSBFirst_inOnPos_outOnPos(data);
	data = ShiftByte_MSBFirst_inOnPos_outOnPos(data);
	data = ShiftByte_MSBFirst_inOnPos_outOnPos(data);
	return data;
}
""")
