
from enum import Enum

import cycles

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


class BitAccessInASM(BitBang):
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
""" % self.__dict__

	def set(self):
		return """\
__asm__ ("setb	_%(bitname)s");		/* Set %(name)s */""" % self.__dict__

	def bit_to_carry(self):
		return """\
__asm__ ("mov	c,_%(bitname)s");	/* %(name)s->carry */""" % self.__dict__

	def carry_to_bit(self):
		return """\
__asm__ ("mov	_%(bitname)s,c");	/* carry->%(name)s */""" % self.__dict__

	def clear(self):
		return """\
__asm__ ("clr	_%(bitname)s");		/* Clear %(name)s */""" % self.__dict__

	def toggle(self):
		return """\
__asm__ ("cpl	_%(bitname)s");		/* Toggle %(name)s */""" % self.__dict__


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


class ShiftOp(object):
	class FirstBit(Enum):
		"""
		MSB == Most Significant bit first
		LSB == Least Significant bit first
		"""
		MSB = 'rlc'
		LSB = 'rrc'

	class ClockMode(Enum):
		none = 0
		positive = 1
		negative = 2

	def __init__(self, clk_pin, din_pin, dout_pin):
		self.clk = clk_pin
		self.din = din_pin
		self.dout = dout_pin

	def generate(self):
		raise NotImplementedError()

def asm_comment(s):
	return '__asm__ ("	; %s");' % s.replace('\\', '\\\\')

class ShiftByte(ShiftOp):

	def generate(self, direction, read_on, write_on, pad=True):
		assert isinstance(direction, ShiftOp.FirstBit)
		assert isinstance(read_on, ShiftOp.ClockMode)
		assert isinstance(write_on, ShiftOp.ClockMode)

		read_ops = self.din.bit_to_carry().splitlines()
		write_ops = self.dout.carry_to_bit().splitlines()

		# Collect instructions on negative edge
		neg_edge = []
		neg_edge.append(self.clk.clear())
		if write_on == ShiftOp.ClockMode.negative:
			neg_edge += write_ops
		if read_on == ShiftOp.ClockMode.negative:
			neg_edge += read_ops

		# Collect instructions on positive edge
		pos_edge = []
		pos_edge.append(self.clk.set())
		if write_on == ShiftOp.ClockMode.positive:
			pos_edge += write_ops
		if read_on == ShiftOp.ClockMode.positive:
			pos_edge += read_ops

		# Figure out how the rotate will work
		rotate_tmpl = '__asm__ ("%s	a"); 		/* %%s */' % direction.value
		rotate_op = ""
		if write_on != ShiftOp.ClockMode.none and read_on != ShiftOp.ClockMode.none:
			rotate_op = rotate_tmpl % "data->carry->data"
		elif write_on != ShiftOp.ClockMode.none:
			rotate_op = rotate_tmpl % "data->carry"
		elif read_on != ShiftOp.ClockMode.none:
			rotate_op = rotate_tmpl % "carry->data"

		# Find were we want to put the rotate operation
		if rotate_op:
			if len(neg_edge) > len(pos_edge):
				pos_edge.append(rotate_op)
			elif len(neg_edge) < len(pos_edge):
				neg_edge.append(rotate_op)
			else:
				neg_edge.append(rotate_op)

		# Pad the edges out to be symmetrical in cycle length
		neg_edge_instructions = cycles.parse("\n".join(neg_edge))
		neg_edge_len = sum(i[0].cycles for i in neg_edge_instructions if i)

		pos_edge_instructions = cycles.parse("\n".join(pos_edge))
		pos_edge_len = sum(i[0].cycles for i in pos_edge_instructions if i)

		longest = max(neg_edge_len, pos_edge_len)

		if pad:
			for i in range(0, longest - pos_edge_len):
				pos_edge.append('__asm__ ("nop");')
			for i in range(0, longest - neg_edge_len):
				neg_edge.append('__asm__ ("nop");')

			neg_edge_instructions = cycles.parse("\n".join(neg_edge))
			pos_edge_instructions = cycles.parse("\n".join(pos_edge))

		cmds = []
		if write_on == ShiftOp.ClockMode.negative:
			cmds.append(asm_comment("Before"))
			cmds.append(rotate_tmpl % "data->carry")

		for i in range(0, 8):
			cmds.append(asm_comment("Bit %i" % i))
			cmds.append("/* \_ (%s cycles) */" % neg_edge_len)
			cmds += neg_edge
			cmds.append("/* _/ (%s cycles) */" % pos_edge_len)
			cmds += pos_edge

		if read_on == ShiftOp.ClockMode.positive:
			cmds.append(asm_comment("After)"))
			cmds.append(rotate_tmpl % "carry->data")

		return cmds

