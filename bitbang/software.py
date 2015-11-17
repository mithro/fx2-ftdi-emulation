"""
Tools for generating efficient software based bit banging functions.
"""

from enum import Enum

import pins
import cycles


class BitBang(object):
	"""
	Base interface for a bit banging bit.
	"""

	def get_undefined(self, fname):
		def undefined(self):
			raise IOError('Operation %s not valid on %s (%s pin)' % (fname, self.pin.name, self.direction))
		return undefined.__get__(self, self.__class__)

	def __init__(self, name, pin, direction):
		self.name = name
		assert isinstance(pin, pins.Pin), pin
		self.pin = pin

		self.direction = direction
		if self.direction is pins.PinDirection.output:
			self.bit_to_carry = self.get_undefined("bit_to_carry")
			self.get = self.get_undefined("get")
		elif self.direction is pins.PinDirection.input:
			self.carry_to_bit = self.get_undefined("carry_to_bit")
			self.get = self.get_undefined("set")
		elif self.direction is pins.PinDirection.bidirectional:
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
		if self.direction == pins.PinDirection.bidirectional:
			if not direction:
				return ""
		else:
			if direction:
				assert direction == self.direction
				return ""
			direction = self.direction

		if direction == pins.PinDirection.input:
			return self._setup_input()
		elif direction == pins.PinDirection.output:
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
	def __init__(self, name, pin, direction):
		"""
		ByteAccessInC("clock", "A", 0)
		"""
		BitBang.__init__(self, name, pin, direction)

		self.def_port = name.upper() + "_PORT"
		self.def_oe = name.upper() + "_PORT_OE"
		self.def_mask = name.upper() + "_MASK"
		self.def_nask = name.upper() + "_NASK"

	def defines(self):
		d = {
			'port_name': sef.pin.port_name,
			'port_oe': self.pin.output_name,
			'mask': self.pin.mask,
			'nask': self.pin.nask,
		}
		d.update(self.__dict__)
		return """\
#define %(def_port)s %(port_name)s
#define %(def_oe)s %(port_oe)s
#define %(def_mask)s %(mask)#04X
#define %(def_nask)s %(nask)#04X
""" % d

	# Simple bit operations
	def set(self):
		return """\
%(def_port)s |= %(def_mask)s; /* Set %(name)s */""" % self.__dict__

	def get(self):
		return """\
(%(def_port)s & %(def_mask)s) /* Get %(name)s */""" % self.__dict__

	def clear(self):
		return """\
%(def_port)s &= %(def_nask)s; /* Clear %(name)s */""" % self.__dict__

	def toggle(self):
		return """\
%(def_port)s ^= %(def_mask)s; /* Toggle %(name)s */""" % self.__dict__

	# Direction set up
	def _setup_input(self):
		return """\
%(def_oe)s &= %(def_nask)s; /* Set %(name)s as input */""" % self.__dict__

	def _setup_output(self):
		return """\
%(def_oe)s |= %(def_mask)s; /* Set %(name)s as output */""" % self.__dict__

	# To/From the carry bit
	def carry_to_bit(self):
		raise NotImplementedError
		return """\
__asm__ ("");
"""
	def bit_to_carry(self):
		raise NotImplementedError
		return """\
__asm__ ("");
"""

	# Other
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



class BitAccessInC(BitBang):
	"""Access bits (in bit addressable space) via bit operations. Implemented in C."""

	def __init__(self, name, direction, pin):
		"""
		ByteAccessInC("clock", "A", 0)
		"""
		assert self.pin.bit_accessible, "%r not bit accessible!" % pin
		BitBang.__init__(self, name, direction, pin)

		self.def_bit = name.upper() + "_BIT"
		self.def_oe = name.upper() + "_BIT_OE"
		self.def_mask = name.upper() + "_MASK"
		self.def_nask = name.upper() + "_NASK"

	def defines(self):
		d = {
			'bit_name': sef.pin.bit_name,
			'bit_oe': self.pin.output_name,
			'mask': self.pin.mask,
			'nask': self.pin.nask,
		}
		d.update(self.__dict__)
		return """\
#define %(def_bit)s %(bit_name)s
""" % self.__dict__

	# Simple bit operations
	def set(self):
		return """\
%(def_bit)s = 1; /* Set %(name)s */""" % self.__dict__

	def get(self):
		return """\
%(def_bit)s /* Get %(name)s */""" % self.__dict__

	def clear(self):
		return """\
%(def_bit)s = 0; /* Clear %(name)s */""" % self.__dict__

	def toggle(self):
		return """\
%(def_bit)s ^= 1; /* Toggle %(name)s */""" % self.__dict__

	# Direction set up
	def _setup_input(self):
		raise """\
%(def_oe)s &= %(def_nask)s; /* Set %(name)s as input */""" % self.__dict__

	def _setup_output(self):
		raise """\
%(def_oe)s |= %(def_mask)s; /* Set %(name)s as output */""" % self.__dict__

	# To/From the carry bit
	def bit_to_carry(self):
		return """\
__asm__ ("mov c,%(def_bit)s"); /* %(name)s->carry */""" % self.__dict__

	def carry_to_bit(self):
		return """\
__asm__ ("mov %(def_bit)s,c"); /* carry->%(name)s */""" % self.__dict__

	# Other
	def setto(self, value_name):
		d = {}
		d.update(self.__dict__)
		d['value_name'] = value_name
		return """\
%(def_bit)s = %(value_name)s; /* Set %(name)s */""" % d

class ByteAccessInASM(BitBang):
	"""
	// Using proxy byte
	// =================================================
	// "proxy byte" in bit addressable space == direct space

	// No ops touch register A

	// Toggle clock - 5 cycles
	// (2cy) CPL proxy_pin_clk
	// (3cy) MOV pins, proxy

	// Write data out - 5 cycles
	// (2cy) MOV proxy_pin_data_out, C
	// (3cy) MOV pins, proxy

	// Read data in - 5 cycles
	// (3cy) MOV proxy, pins
	// (2cy) MOV C, proxy_pin_data_in

	// if READ and WRITE on same edge
	// -----------------------------------
	// b6  (2cy) CPL proxy_pin_clk
	// a1^ (3cy) MOV pins, proxy
	// a2  -- (2cy) MOV proxy_pin_data_out, C
	// a3  -- (3cy) MOV pins, proxy
	// a4  -- (3cy) MOV proxy, pins
	// a5  -- (2cy) MOV C, proxy_pin_data_in
	// a6  (2cy) CPL proxy_pin_clk
	// b1^ (3cy) MOV pins, proxy
	// b2  -- (2cy) ROTATE + NOP
	// b3  -- (3cy) NOP + NOP + NOP
	// b4  -- (3cy) NOP + NOP + NOP
	// b5  -- (2cy) NOP + NOP
	// == 15 cycles between CLK edges
	//
	// Better version?
	// b4  (2cy) MOV proxy_pin_data_out, C
	// b5  (2cy) CPL proxy_pin_clk
	// a1^ (3cy) MOV pins, proxy
	// a2  (3cy) MOV proxy, pins
	// a3  (2cy) MOV C, proxy_pin_data_in
	//
	// a4  (2cy) CPL proxy_pin_clk
	// a5  (2cy) ROTATE + NOP
	// b1^ (3cy) MOV pins, proxy
	// b2  (3cy) NOP + NOP + NOP
	// b3  (2cy) NOP + NOP
	// == 12 cycles between CLK edges
	//
	// if READ and WRITE on opposite edges
	// -----------------------------------
	// b5  (2cy) CPL R2_pin_clk
	// a1^ (3cy) MOV pins, proxy
	// a2  -- (2cy) MOV proxy_pin_data_out, C
	// a3  -- (3cy) MOV pins, proxy
	// a4  -- (1cy) NOP
	//
	// a5  (2cy) CPL R2_pin_clk
	// b1^ (3cy)*MOV pins, proxy
	// b2  -- (3cy) MOV proxy, pins
	// b3  -- (2cy) MOV C, proxy_pin_data_in
	// b4  -- (1cy) ROTATE
	// == 11 cycles between CLK edges
	//
	// Better version?
	// b4  (2cy) MOV proxy_pin_data_out, C
	// b5  (2cy) CPL proxy_pin_clk
	// a1^ (3cy)*MOV pins, R2
	// a2  (2cy) NOP + NOP
	// a3  (1cy) NOP
	// a4  (2cy) NOP + NOP
	//
	// a5  (2cy) CPL proxy_pin_clk
	// b1^ (3cy)*MOV pins, proxy
	// b2  (2cy) MOV proxy, pins
	// b3  (1cy) ROTATE 
	// == 9 cycles between CLK edges
	// -----------------------------------


	// Using proxy byte + @R0
	// =================================================
	// MOV direct, @Ri    == 2 cycles
	// MOV @Ri, direct    == 2 cycles
	// compared too....
	// MOV direct, direct == 3 cycles

	// No ops touch register A
	// R0 == proxy

	// Toggle clock - 4 cycles
	// (2cy) CPL proxy_pin_clk
	// (2cy) MOV pins, @R0

	// Write data out - 4 cycles
	// (2cy) MOV proxy_pin_data_out, C
	// (2cy) MOV pins, @R0

	// Read data in - 4 cycles
	// (2cy) MOV @R0, pins
	// (2cy) MOV C, proxy_pin_data_in


	// if READ and WRITE on same edge
	// -----------------------------------
	// a1^ (2cy) CPL proxy_pin_clk
	// a2  (2cy) MOV pins, @R0
	// a3  -- (2cy) MOV proxy_data_out, C
	// a4  -- (2cy) MOV pins, @R0
	// a5  -- (2cy) MOV @R0, pins
	// a6  -- (2cy) MOV C, proxy_data_in
	// b1^ (2cy) CPL pin_clk_out
	// b2  (2cy) MOV pins, @R0
	// b3  -- (2cy) ROTATE + NOP
	// b4  -- (2cy) NOP, NOP
	// b5  -- (2cy) NOP, NOP
	// b6  -- (2cy) NOP, NOP
	// == 12 cycles between clock edges
	//
	// Better version?
	// b4  (2cy) MOV proxy_pin_data_out, C
	// b5  (2cy) CPL proxy_pin_clk
	// a1^ (2cy) MOV pins, @R0
	// a2  (2cy) MOV @R0, pins
	// a3  (2cy) MOV C, proxy_pin_data_in
	//
	// a4  (2cy) CPL proxy_pin_clk
	// a5  (2cy) ROTATE + NOP
	// b1^ (2cy) MOV pins, @R0
	// b2  (2cy) NOP + NOP
	// b3  (2cy) NOP + NOP
	// == 10 cycles between CLK edges
	// 
	// if READ and WRITE on opposite edges
	// -----------------------------------
	// a1^ (2cy) CPL proxy_clk_out
	// a2  (2cy) MOV pins, @R0
	// a4  -- (2cy) MOV proxy_data_out, C
	// a5  -- (2cy) MOV pins, @R0
	// a6  -- (1cy) NOP
	// b1^ (2cy) CPL proxy_clk_out
	// b2  (2cy) MOV pins, @R0
	// b3  -- (2cy) MOV @R0, pins
	// b4  -- (2cy) MOV C, proxy_data_in
	// b6  -- (1cy) ROTATE
	// == 9 cycles between clock edges

	// 12MHz / 12 cycles per CLK == 1.0Mbit/s
	// 12MHz / 10 cycles per CLK == 1.2Mbit/s
	// 12MHz /  9 cycles per CLK == 1.3Mbit/s

	// Using lots of registers
	// =================================================

	//       MOV dest, src
	// (2cy) MOV direct, Rn - Move direct byte to register
	// (2cy) MOV Rn, direct - Move register to direct byte
	// (3cy) MOV direct, direct - Move direct to direct
	// (1cy) XCH A, Rn     - Exchange A and register
	// (2cy) XCH A, direct - Exchange A and direct

	// Rx_clk_out_mask
	// Rx_data_out_mask
	// Rx_data_out_store
	// Rx_data_in_mask
	// Rx_data_in_store

	// Toggle clock, preserving A - 4 cycles
	// (1cy) XCH A, Rx_clk_out_mask
	// (2cy) XRL pins, A
	// (1cy) XCH A, Rx_clk_out_mask

	// Toggle clock, clobbering A - 3 cycles
	// (1cy) MOV A, Rx_clk_out_mask
	// (2cy) XRL pins, A

	// Write data out - 6 cycles
	// -- (1cy) MOV A, Rx_data_out
	// -- (1cy) ROTATE
	// -- (1cy) MOV Rx_data_out, A
	// -- (1cy) ORL A, Rx_data_out_mask
	// -- (2cy) ORL pins, A

	// Read data in - 6 cycles
	// -- (1cy) MOV A, Rx_data_in_mask
	// -- (2cy) ANL A, pins
	// -- (1cy) ORL A, Rx_data_in
	// -- (1cy) ROTATE
	// -- (1cy) MOV Rx_data_in, A

	// =============================================
	"""


class BitAccessInASM(BitBang):
	"""Access bits (in bit addressable space) via bit operations. Implemented in assembly."""

	def __init__(self, name, pin, direction):
		"""
		ByteAccessInC("clock", "A", 0)
		"""
		assert pin.bit_accessible, "%r not bit accessible!" % self.pin
		BitBang.__init__(self, name, pin, direction)

		self.bit_name = self.pin.bit_name
		self.oe_name = self.pin.output_name
		self.mask = self.pin.mask
		self.nask = self.pin.nask

	def defines(self):
		return """\
""" % self.__dict__

	# Simple bit operations
	def set(self):
		return """\
__asm__ ("setb	_%(bit_name)s");		/* Set %(name)s */""" % self.__dict__

	def get(self):
		raise NotImplementedError

	def clear(self):
		return """\
__asm__ ("clr	_%(bit_name)s");		/* Clear %(name)s */""" % self.__dict__

	def toggle(self):
		return """\
__asm__ ("cpl	_%(bit_name)s");		/* Toggle %(name)s */""" % self.__dict__

	# Direction set up
	def _setup_input(self):
		return """\
__asm__ ("anl	_%(oe_name)s,#%(nask)#04x;");	/* Set %(name)s as input */""" % self.__dict__

	def _setup_output(self):
		return """\
__asm__ ("orl	_%(oe_name)s,#%(mask)#04x;");	/* Set %(name)s as output */""" % self.__dict__

	# To/From the carry bit
	def bit_to_carry(self):
		return """\
__asm__ ("mov	c,_%(bit_name)s");	/* %(name)s->carry */""" % self.__dict__

	def carry_to_bit(self):
		return """\
__asm__ ("mov	_%(bit_name)s,c");	/* carry->%(name)s */""" % self.__dict__

	# Other
	def setto(self, value_name):
		raise NotImplementedError


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
		assert self.clk_pin.direction == pins.PinDirection.output, (self.clk_pin.direction, pins.PinDirection.output)

		if din_pin == dout_pin:
			assert din_pin.direction == pins.PinDirection.bidirectional
			self.din_pin = dout_pin
			self.dout_pin = din_pin
		else:
			assert din_pin.direction == pins.PinDirection.input
			self.din_pin = din_pin
			assert dout_pin.direction == pins.PinDirection.output
			self.dout_pin = dout_pin

	"""
	@property
	def data_direction(self):
		assert self.data_pin
		if self.din_pin:
			return pins.PinDirection.input
		elif self.dout_pin:
			return pins.PinDirection.output
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

		if direction == pins.PinDirection.output:
			assert self.dout_pin is None
			self.dout_pin = self.data_pin
			self.din_pin = None
			return "FIXME: Switching instructions here."
		elif direction == pins.PinDirection.input:
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

		read_ops = self.din_pin.bit_to_carry().splitlines()
		write_ops = self.dout_pin.carry_to_bit().splitlines()

		# Do we need to change directions between read/write?
		if self.din_pin == self.dout_pin:
			if write_on != ShiftOp.ClockMode.none and read_on != ShiftOp.ClockMode.none:
				read_ops = self.din_pin.setup(pins.PinDirection.input).splitlines() + read_ops
				write_ops = self.dout_pin.setup(pins.PinDirection.output).splitlines() + write_ops

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
		# FIXME: This won't work for the C versions...
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

