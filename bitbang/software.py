"""
Tools for generating efficient software based bit banging functions.
"""

from enum import Enum

import cycles

class BitDirection(Enum):
	bidirectional = 'bidir'
	output = 'out'
	input = 'in'
	high_impedance = input


class BitBang(object):
	"""
	Base interface for a bit banging bit.
	"""

	def get_undefined(self, fname):
		def undefined(self):
			raise IOError('Operation %s not valid on %s (%s pin)' % (fname, self.name, self.direction))
		return undefined.__get__(self, self.__class__)

	def __init__(self, name, direction):
		self.name = name

		self.direction = direction
		if self.direction is BitDirection.output:
			self.bit_to_carry = self.get_undefined("bit_to_carry")
			self.get = self.get_undefined("get")
		elif self.direction is BitDirection.input:
			self.carry_to_bit = self.get_undefined("carry_to_bit")
			self.get = self.get_undefined("set")
		elif self.direction is BitDirection.bidirectional:
			pass
		else:
			raise ValueError("Unknown direction %r" % direction)

	# Simple bit operations
	def get(self):
		"""Get the bit value."""
		raise NotImplementedError

	def set(self):
		"""Set the bit value to 1."""
		raise NotImplementedError

	def toggle(self):
		"""Invert the current value of the bit. IE 1 -> 0 and 0 -> 1."""
		raise NotImplementedError

	def clear(self):
		"""Set the bit value to 0."""
		raise NotImplementedError

	# Direction set up
	def setup(self, direction=None):
		if self.direction == BitDirection.bidirectional:
			if not direction:
				return ""
		else:
			if direction:
				assert direction == self.direction
				return ""
			direction = self.direction

		if direction == BitDirection.input:
			return self._setup_input()
		elif direction == BitDirection.output:
			return self._setup_output()
		else:
			raise ValueError("Invalid direction %r for setup." % direction)

	def _setup_input(self):
		raise NotImplementedError

	def _setup_output(self):
		raise NotImplementedError

	# To/From the carry bit
	def bit_to_carry(self):
		"""Move the bit contents into the carry bit."""
		raise NotImplementedError

	def carry_to_bit(self):
		"""Move the carry bit into the contents."""
		raise NotImplementedError

	# FIXME: Is this needed?
	def setto(self, value_name):
		raise NotImplementedError

def indent(s):
	return ("\n	".join(s.split("\n")))


class ByteAccessInC(BitBang):
	"""Access bits via byte operations. Implemented in C."""
	def __init__(self, name, direction, port, bit):
		"""
		ByteAccessInC("clock", "A", 0)
		"""
		BitBang.__init__(self, name, direction)

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
	"""Access bits (in bit addressable space) via bit operations. Implemented in C."""

	def __init__(self, name, direction, port, bit):
		"""
		ByteAccessInC("clock", "A", 0)
		"""
		BitBang.__init__(self, name, direction)

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
	"""Access bits (in bit addressable space) via bit operations. Implemented in assembly."""

	def __init__(self, name, direction, port, bit):
		"""
		ByteAccessInC("clock", "A", 0)
		"""
		BitBang.__init__(self, name, direction)

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
		self.clk_pin = clk_pin
		assert self.clk_pin.direction == BitDirection.output, (self.clk_pin.direction, BitDirection.output)

		if din_pin == dout_pin:
			assert din_pin.direction == BitDirection.bidirectional
			self.din_pin = dout_pin
			self.dout_pin = din_pin
		else:
			assert din_pin.direction == BitDirection.input
			self.din_pin = din_pin
			assert dout_pin.direction == BitDirection.output
			self.dout_pin = dout_pin

	"""
	@property
	def data_direction(self):
		assert self.data_pin
		if self.din_pin:
			return BitDirection.input
		elif self.dout_pin:
			return BitDirection.output
		else:
			raise ValueError("Data direction currently undefined!")

	def data_direction(self, direction):
		if not self.data_pin:
			return ""
		try:
			if direction == self.data_direction:
				# No direction change needed, as already that
				# direction.
				return ""
		except ValueError:
			pass

		if direction == BitDirection.output:
			assert self.dout_pin is None
			self.dout_pin = self.data_pin
			self.din_pin = None
			return "FIXME: Switching instructions here."
		elif direction == BitDirection.input:
			self.dout_pin = None
			assert self.din_pin is None
			self.din_pin = self.data_pin
			return "FIXME: Switching instructions here."
		else:
			raise ValueError("Invalid data direction %r" % direction)
"""

	def generate(self):
		raise NotImplementedError()

def asm_comment(s):
	return '__asm__ ("	; %s");' % s.replace('\\', '\\\\')

class ShiftByte(ShiftOp):
	"""
	The shift byte functions are built around the "rotate accumulator
	through carry" operation and data is moved into / out of the carry bit.

	      +---+---+---+---+---+---+---+---+      +---+
	 /--> | 7 | 6 | 5 | 4 | 3 | 2 | 1 | 0 | <--> | c | <--\
	 |    +---+---+---+---+---+---+---+---+      +---+    |
	 |                                                    |
	 \----------------------------------------------------/

	(1cy) RLC A - Rotate A left through carry
	(1cy) RRC A - Rotate A right through carry
	"""

	def generate(self, direction, read_on, write_on, pad=True):
		assert isinstance(direction, ShiftOp.FirstBit)
		assert isinstance(read_on, ShiftOp.ClockMode)
		assert isinstance(write_on, ShiftOp.ClockMode)

		read_ops = self.din_pin.setup(BitDirection.input).splitlines() + self.din_pin.bit_to_carry().splitlines()
		write_ops = self.dout_pin.setup(BitDirection.output).splitlines() + self.dout_pin.carry_to_bit().splitlines()

		# Collect instructions on negative edge
		neg_edge = []
		neg_edge.append(self.clk_pin.clear())
		if write_on == ShiftOp.ClockMode.negative:
			neg_edge += write_ops
		if read_on == ShiftOp.ClockMode.negative:
			neg_edge += read_ops

		# Collect instructions on positive edge
		pos_edge = []
		pos_edge.append(self.clk_pin.set())
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

