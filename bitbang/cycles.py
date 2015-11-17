"""
Tools for calculating the cycles ASM instructions need.

Reads the information from the cycles.md file.
"""

import re
from collections import namedtuple
from collections import OrderedDict
from enum import Enum

class ArgType(Enum):
	accumulator = 'A'
	b = 'B'
	register = 'Rn'
	carry = 'C'
	direct_byte = 'direct'
	indirect_byte = '@Ri'
	relative = 'rel'
	direct_bit = 'bit'
	inverse_direct_bit = '/bit'
	immediate_byte = '#data'
	immediate_word = '#data16'
	address_full = 'addr16'
	address_small = 'addr11'
	program_counter = 'PC'
	data_pointer = 'DPTR'
	indirect_data_pointer = '@DPTR'

	@classmethod
	def convert(cls, s):
		if '+' in s:
			arg0, arg1 = s.split('+')
			assert arg0[0] == '@'
			arg0 = ArgType.convert(arg0[1:])
			arg1 = ArgType.convert(arg1)
			return arg0, arg1

		for e in cls:
			if e.value == s:
				return e
		raise ValueError('%s not found in %s' % (s, cls))

	def regex(self):
		a = "\s,\"'"
		not_reg = '(?:[^{0}][^{0}][^{0}]+)|(?:[^{0}Rr][^{0}])|(?:[Rr][^0-7])|(?:[^{0}AaCcBb])'.format(a)
		if self == ArgType.accumulator:
			return '[Aa]'
		elif self == ArgType.b:
			return '[Bb]'
		elif self == ArgType.register:
			return '[Rr][0-7]'
		elif self == ArgType.carry:
			return '[Cc]'
		elif self == ArgType.direct_byte:
			return not_reg
		elif self == ArgType.indirect_byte:
			return '@[Rr][01]'
		elif self == ArgType.relative:
			return not_reg
		elif self == ArgType.direct_bit:
			return not_reg
		elif self == ArgType.inverse_direct_bit:
			return '/'+not_reg
		elif self == ArgType.immediate_byte:
			return '#[^\s,]+'
		elif self == ArgType.immediate_word:
			return '#[^\s,]+'
		elif self == ArgType.address_full:
			return ''
		elif self == ArgType.address_small:
			return ''
		elif self == ArgType.program_counter:
			return 'PC'
		elif self == ArgType.data_pointer:
			return 'DPTR'
		elif self == ArgType.indirect_data_pointer:
			return '@DPTR'
	
# ----------------------

ArgsNone = namedtuple('ArgsNone', [])
class ArgsNone(ArgsNone):
	def __repr__(self):
		return ""

	def regex(self):
		return ""

ArgsSingle = namedtuple('ArgsSingle', ['arg'])
class ArgsSingle(ArgsSingle):
	def __repr__(self):
		if isinstance(self.arg, tuple):
			return "+".join(x.value for x in self.arg)
		else:
			return self.arg.value

	def regex(self):
		return "(?P<arg0>%s)" % self.arg.regex()

ArgsSimple = namedtuple('ArgsSimple', ['dst', 'src'])
class ArgsSimple(ArgsSimple):
	def __repr__(self):
		if isinstance(self.src, tuple):
			src = "+".join(x.value for x in self.src)
		else:
			src = self.src.value
		return "%s<-%s" % (self.dst.value, src)

	def regex(self):
		return r"(?P<arg0>%s)\s*,\s*(?P<arg1>%s)" % (self[0].regex(), self[1].regex())

ArgsCompare = namedtuple('ArgsCompare', ['a', 'b', 'jump'])
class ArgsCompare(ArgsCompare):
	def __repr__(self):
		return "%s!=%s %s->PC" % (self.a.value, self.b.value, self.jump.value)

	def regex(self):
		return r"(?P<arg0>%s)\s*,\s*(?P<arg1>%s)\s*,\s*(?P<arg2>%s)" % (self[0].regex(), self[1].regex(), self[2].regex())

ArgsMul = namedtuple('ArgsMul', ['a', 'b'])
class ArgsMul(ArgsMul):
	def __repr__(self):
		return "AB"

# ----------------------

Instruction = namedtuple('Instruction', ['mneomic', 'args', 'description', 'size', 'cycles', 'flags']) #, 'opcodes'])
class Instruction(Instruction):
	def __repr__(self):
		flags = " ".join(self.flags)
		if flags:
			flags = "(%s)" % flags
		return "(%i) %s %s" % (self.cycles, self.mneomic, self.args)

	@property
	def effects_carry(self):
		for f in self.flags:
			if 'CY' in f:
				return True
		return False

	@property
	def effects_accumulator(self):
		if isinstance(self.args, (ArgsSimple, ArgsSingle)):
			return self.args[0] == ArgType.accumulator
		return False

	def regex(self):
		return r"(?:[\s'\"]|^)(%s|%s)\s*%s(?:[\s'\"]|$)" % (self.mneomic.upper(), self.mneomic.lower(), self.args.regex())

instructions = {}
for line in open('cycles.md').readlines():
	if not line.strip():
		continue

	_, mnemoic, desc, size, cycles, flags, opcode, _ = (x.strip() for x in line.split('|'))
	if mnemoic.lower() == "mnemoic" or mnemoic.startswith("-"):
		continue

	if ' ' in mnemoic:
		mnemoic_code, args = (x.strip() for x in mnemoic.split(' ', 1))
		if args == 'AB':
			args = ArgsMul(ArgType.accumulator, ArgType.b)
		elif ',' in args:
			arg0, arg1 = args.split(', ', 1)
			arg0 = ArgType.convert(arg0)
			if ',' in arg1:
				arg1, arg2 = arg1.split(', ', 1)
				arg1 = ArgType.convert(arg1)
				arg2 = ArgType.convert(arg2)
				args = ArgsCompare(arg0, arg1, arg2)
			else:
				arg1 = ArgType.convert(arg1)
				args = ArgsSimple(arg0, arg1)
		else:
			args = ArgsSingle(ArgType.convert(args))
	else:
		mnemoic_code = mnemoic
		args = ArgsNone()

	flags = list(x.strip() for x in flags.split())
	
	if '-' in opcode:
		bopcode, topcode = (int(x, 16) for x in opcode.split('-'))
	else:
		bopcode = topcode = int(opcode, 16)
	opcodes = [hex(x) for x in range(bopcode, topcode+1)]

	size = int(size)
	cycles = int(cycles)

	instructions.setdefault(mnemoic_code, []).append(
		Instruction(mnemoic_code, args, desc, size, cycles, flags)) #, opcodes))



def parse(s):
	"""
	"""

	output = []
	for line in s.splitlines():
		if not line.strip():
			output.append(None)
			continue

		lline = line.lower()

		matches = []
		for op in instructions:
			if op.lower() not in lline:
				continue

			for i in instructions[op]:
				r = re.search(i.regex(), line)
				if r:
					matches.append((i, r.groups()[1:]))

		assert len(matches) == 1, "%s\n%s" % (line, "\n".join(repr(x) for x in matches))
		output.append(matches[0])
	return output


if __name__ == "__main__":
	import pprint
	pprint.pprint(instructions)

	def parse_and_print(s):
		instructions = parse(s)
		for l, i in zip(s.splitlines(), instructions):
			print("%-60s %s" % (repr(l), i))

	print("-"*75)
	parse_and_print("""\
	orl	_IOA,#0x01
	anl	_IOA,#0xFE
	xrl	_IOA,#0x01
	setb	_PA0
	clr	_PA0
	cpl	_PA0
	mov	a,_IOA

	mov	ar4,r6
	orl	a,r4
	rl	a
	mov	r6,a
	clr	a
	mov	r5,a
	mov	r4,a
	mov	a,r6
	add	a,r7
""")
	print("-"*75)
	parse_and_print("""\
	__asm__ ('nop');
        __asm__ ("mov c,DIN_BIT"); /* din->carry */
        __asm__ ("rlc a"); /* data->carry->data */
	__asm__ ("mov DOUT_BIT,c"); /* carry->dout */
""")
