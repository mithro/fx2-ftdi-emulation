"""
Generate functions for the sdcc calling convention.
"""

import software

def generate(name, read_on, write_on, body):

	defs = ''
	args = ''

	if write_on != software.ShiftOp.ClockMode.none:
		args = 'BYTE data'
		defs = """
	(data);
	__asm__("mov	a,dpl");	/* Move arg0->a */
"""
	else:
		args = ''

	if read_on != software.ShiftOp.ClockMode.none:
		if write_on == software.ShiftOp.ClockMode.none:
			defs += """
	__asm__("clr	a");		/* Get accumulator ready */
"""

		rettype = 'BYTE'
		ret = """
	__asm__("mov	dpl,a");	/* Move a->retvalue */
	return;				/* return */
"""
	else:
		rettype = 'void'
		ret = 'return;'

	output = "\n	".join(body)

	return """\
/* ---------------------------- */
%(rettype)s %(name)s(%(args)s) {
	%(defs)s
	%(output)s
	%(ret)s
}
/* ---------------------------- */
""" % locals()

