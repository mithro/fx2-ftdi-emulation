"""
Class for abstracting FX2 IO pins
"""

from enum import Enum


class PinDirection(Enum):
	output = 'out'
	input = 'in'
	high_impedance = input
	bidirectional = 'bidir'


class Pin(object):
	def __init__(self, port, index):
		assert port in "ABCDE", port
		assert 0 <= index <= 7, index
		self.port = port
		self.index = index

		self.port_name = 'IO%s' % port
		self.output_name = 'OE%s' % port

		if self.bit_accessible:
			self.bit_name = 'P%s%i' % (port, index)
			
	@property
	def bit_accessible(self):
		return self.port != "E"

	@property
	def mask(self):
		return (1 << self.index)

	@property
	def nask(self):
		return ~(1 << self.index) & 0xff

