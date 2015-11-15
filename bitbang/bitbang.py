

class BitBang(object):
	def __init__(self, name):
		self.name = name

	def set(self):
		raise NotImplementedError

	def setto(self, value_name):
		raise NotImplementedError

	def bit_to_carry(self):
		raise NotImplementedError

	def carry_to_bit(self):
		raise NotImplementedError

	def get(self):
		raise NotImplementedError
		
	def clear(self):
		raise NotImplementedError

	def toggle(self):
		raise NotImplementedError
	
	def shift_in(self):
		raise NotImplementedError
		
	def shift_out(self):
		raise NotImplementedError

def indent(s):
	return ("\n	".join(s.split("\n")))


class ByteAccessInC(BitBang):
	def __init__(self, name, port, bit):
		"""
		ByteAccessInC("clock", "A", 0)
		"""
		BitBang.__init__(self, name)

		self.portname = "IO%s" % port
		self.bit = bit

		self.mask = (1 << self.bit)
		self.nask = ~(1 << self.bit) & 0xff

		self.name_port_def = name.upper() + "_PORT"
		self.name_mask_def = name.upper() + "_MASK"
		self.name_nask_def = name.upper() + "_NASK"

	def defines(self):
		return """\
#define %(name_port_def)s %(portname)s
#define %(name_mask_def)s %(mask)#04X
#define %(name_nask_def)s %(nask)#04X
""" % self.__dict__

	def set(self):
		return """\
%(name_port_def)s |= %(name_mask_def)s; /* Set %(name)s */""" % self.__dict__
	
	def get(self):
		return """\
(%(name_port_def)s & %(name_mask_def)s) /* Get %(name)s */""" % self.__dict__

	def setto(self, value_name):
		return """\
if (%(value_name)s) {
	%(set)s
} else {
 	%(clear)s
}""" % {
	'value_name': value_name,
	'set': self.set(),
	'clear': self.clear(),
	}

	def carry_to_bit(self):
		return """\
__asm__ ("");
"""
	def bit_to_carry(self):
		return """\
__asm__ ("");
"""

	def clear(self):
		return """\
%(name_port_def)s &= %(name_nask_def)s; /* Clear %(name)s */""" % self.__dict__

	def toggle(self):
		return """\
%(name_port_def)s ^= %(name_mask_def)s; /* Toggle %(name)s */""" % self.__dict__


class BitAccessInC(BitBang):
	def __init__(self, name, port, bit):
		"""
		ByteAccessInC("clock", "A", 0)
		"""
		BitBang.__init__(self, name)

		self.bitname = "P%s%s" % (port, bit)

		self.port = port
		self.bit = bit

		self.mask = (1 << self.bit)

		self.name_portbit_def = name.upper() + "_BIT"

	def defines(self):
		return """\
#define %(name_portbit_def)s %(bitname)s
""" % self.__dict__

	def set(self):
		return """\
%(name_portbit_def)s = 1; /* Set %(name)s */""" % self.__dict__

	def setto(self, value_name):
		d = {}
		d.update(self.__dict__)
		d['value_name'] = value_name
		return """\
%(name_portbit_def)s = %(value_name)s; /* Set %(name)s */""" % d

	def get(self):
		return """\
%(name_portbit_def)s /* Get %(name)s */""" % self.__dict__

	def bit_to_carry(self):
		return """\
__asm__ ("mov c,%(name_portbit_def)s"); /* %(name)s->carry */""" % self.__dict__

	def carry_to_bit(self):
		return """\
__asm__ ("mov %(name_portbit_def)s,c"); /* carry->%(name)s */""" % self.__dict__

	def clear(self):
		return """\
%(name_portbit_def)s = 0; /* Clear %(name)s */""" % self.__dict__

	def toggle(self):
		return """\
%(name_portbit_def)s ^= 1; /* Toggle %(name)s */""" % self.__dict__


def GenerateFunctions(bitbang):
	return """
// Generated functions for %(name)s from %(class)s
// -----------------------------------------------------------------------

%(defines)s

inline void %(name)s_set() {
	%(set)s;
}

inline void %(name)s_setto(_Bool value) {
	%(setto)s
}

inline _Bool %(name)s_get() {
	return %(get)s;
}

inline void %(name)s_clear() {
	%(clear)s;
}

inline void %(name)s_toggle() {
	%(toggle)s;
}
// -----------------------------------------------------------------------

""" % {
	'class': bitbang.__class__,
	'name': bitbang.name,
	'defines': bitbang.defines(),
	'set': indent(bitbang.set()),
	'setto': indent(bitbang.setto("value")),
	'get': bitbang.get(),
	'clear': indent(bitbang.clear()),
	'toggle': indent(bitbang.toggle()),
	}



print("""

#include "fx2regs.h"

#define ROTATE_LEFT(i, n) \
        i = ((i >> (8-n)) | (i << n))

#define ROTATE_RIGHT(i, n) \
        i = ((i >> n) | (i << (8-n)))


""")

porta_byte = ByteAccessInC("a1", "A", 0)
porta_bit = BitAccessInC("a2", "A", 0)

print(GenerateFunctions(porta_byte))
print(GenerateFunctions(porta_bit))
print("""

int main() {
	BYTE b1 = 0;
	BYTE b2 = 0;

	a1_set();
	a1_clear();
	a1_toggle();

	a2_set();
	a2_clear();
	a2_toggle();

	b1 |= a1_get();
	ROTATE_LEFT(b1, 1);
	b1 |= a1_get();
	ROTATE_LEFT(b1, 1);

	b2 |= a2_get();
	ROTATE_LEFT(b2, 1);
	b2 |= a2_get();
	ROTATE_LEFT(b2, 1);

	return b1 + b2;
}

""")


from enum import Enum

class ClockMode(Enum):
	none = 0
	positive = 1
	negative = 2

def ShiftByte(clock, data_out, data_in, read_on, write_on):
	"""
	ShiftByte(ClockMode.positive, ClockMode.negative)
	"""

	cmds = []

	if write_on == ClockMode.negative:
		cmds.append("rotate carry /* data->carry %i */" % 0)

	for i in range(0, 8):
		cmds.append("/* Bit %i */" % i)

		# Negative edge
		cmds.append("\_")

		if write_on == ClockMode.negative:
			cmds.append("write")
		elif write_on == ClockMode.positive:
			cmds.append("rotate carry /* data->carry %i */" % i)

		if read_on == ClockMode.negative:
			cmds.append("read")
		elif read_on == ClockMode.positive:
			cmds.append("rotate carry /* carry->data %i */" % i)

		# Positive edge
		cmds.append("_/")

		if write_on == ClockMode.positive:
			cmds.append("write")
		elif write_on == ClockMode.negative:
			cmds.append("rotate carry /* data->data %i */" % i)

		if read_on == ClockMode.positive:
			cmds.append("read")
		elif read_on == ClockMode.negative:
			cmds.append("rotate carry /* carry->data %i */" % i)


	cmds.append("/* After */")
	if read_on == ClockMode.positive:
		cmds.append("rotate carry /* carry->data %i */" % i)

	print(cmds)


#	rotate carry /* carry->data */
#	rotate carry /* data->carry */
# --
#	rotate carry /* carry->data->carry */

#(a)
#	rotate carry /* carry->data */
#	(....)
#	rotate carry /* data->carry */
# --
#	rotate carry /* carry->data->carry */
#	\1

#(b)
#	rotate carry /* carry->data */
#	(....)
#	rotate carry /* data->carry */
# --
#	\1
#	rotate carry /* carry->data->carry */

	i = 0
	while i < len(cmds)-1:
		if cmds[i].startswith("rotate carry") and cmds[i+1].startswith("rotate carry"):
			cmds.pop(i)
			cmds.pop(i)
			cmds.insert(i, "rotate carry /* carry->data->carry */")
		i += 1
	
	print(cmds)

	output = []
	for cmd in cmds:
		if cmd == "\_":
			output.append(clock.clear())
		elif cmd == "_/":
			output.append(clock.set())
		elif cmd == "read":
			output.append(data_in.bit_to_carry())
		elif cmd == "write":
			output.append(data_out.carry_to_bit())
		elif cmd == "nops":
			output.append("DELAY;")
		elif cmd.startswith("rotate carry"):
			output.append("""\
__asm__ ("rlc"); %s""" % cmd[13:])
		elif cmd.startswith("/*"):
			output.append(cmd)

	defs = ''
	args = ''
	if read_on != ClockMode.none:
		if write_on != ClockMode.none:
			args = 'BYTE data'
		else:
			defs = 'BYTE data = 0;'

		rettype = 'BYTE'
		ret = 'return data;'
	else:
		rettype = 'void'
		ret = 'return;'

	print("""\
/* ---------------------------- */
%(rettype)s shift_byte(%(args)s) {
	%(defs)s""" % locals())
	print("	"+"\n	".join(output))
	print("""\
	%(ret)s
}
/* ---------------------------- */""" % locals())

clock = BitAccessInC("clk", "E", 5)
data_out = BitAccessInC("dout", "E", 2)
data_in = BitAccessInC("din", "E", 3)

print("// read:none, write:none")
ShiftByte(clock, data_out, data_in, read_on=ClockMode.none, write_on=ClockMode.none)
print("// ---------\n")
print("// read: +ve, write:none")
ShiftByte(clock, data_out, data_in, read_on=ClockMode.positive, write_on=ClockMode.none)
print("// ---------\n")
print("// read: -ve, write:none")
ShiftByte(clock, data_out, data_in, read_on=ClockMode.negative, write_on=ClockMode.none)
print("// ---------\n")
print("// read: +ve, write: +ve")
ShiftByte(clock, data_out, data_in, read_on=ClockMode.positive, write_on=ClockMode.positive)
print("// ---------\n")
print("// read: +ve, write: -ve")
ShiftByte(clock, data_out, data_in, read_on=ClockMode.positive, write_on=ClockMode.negative)
print("// ---------\n")
print("// read: -ve, write: +ve")
ShiftByte(clock, data_out, data_in, read_on=ClockMode.negative, write_on=ClockMode.positive)
print("// ---------\n")


def ShiftByte(bitbang):
	return """
inline BYTE %(name)s_shift(BYTE input) {
	_Bool carry = 0;
	BYTE output = 0;

	carry = input & 0x1;
	ROTATE_RIGHT(input, 1);
	%(name)s_setto(carry);
	output &= %(name)s_get();
	ROTATE_LEFT(output, 1);
}
"""
