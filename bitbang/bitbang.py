

class BitBang(object):
	def __init__(self, name):
		self.name = name

	def set(self):
		raise NotImplementedError

	def setto(self, value_name):
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
		print(bin(self.nask))
		return """\
#define %(name_port_def)s %(portname)s
#define %(name_mask_def)s %(mask)#04X
#define %(name_nask_def)s %(nask)#04X
""" % self.__dict__

	def set(self):
		return """\
%(name_port_def)s |= %(name_mask_def)s; /* Set %(name)s */""" % self.__dict__

	def setto(self, value_name):
		d = {}
		d.update(self.__dict__)
		d['value_name'] = value_name
		return """\
%(name_port_def)s |= (%(name_mask_def)s & %(value_name)s); /* Set %(name)s */""" % d

	def get(self):
		return """\
(%(name_port_def)s & %(name_mask_def)s) /* Get %(name)s */""" % self.__dict__

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

inline void %(name)s_setto(bool value) {
	%(setto)s;
}

inline bool %(name)s_get() {
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
	'set': bitbang.set(),
	'setto': bitbang.setto("value"),
	'get': bitbang.get(),
	'clear': bitbang.clear(),
	'toggle': bitbang.toggle(),
	}


porta_byte = ByteAccessInC("a1", "A", 0)
porta_bit = BitAccessInC("a1", "A", 0)

print(GenerateFunctions(porta_byte))
print(GenerateFunctions(porta_bit))

def ShiftByte(bitbang):
	return """


inline BYTE %(name)s_shift(BYTE input) {
	BYTE output = 0;

	output = %(name)s_get();
	
}


"""
