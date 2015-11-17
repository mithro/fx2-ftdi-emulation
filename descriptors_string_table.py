#!/usr/bin/python3

import sys

import subprocess
git_id = subprocess.check_output("git describe --dirty --long", shell=True).strip().decode('utf-8')
serialno = '0123456789abcdef ' + git_id

strings = [x.strip() for x in sys.stdin.readlines()]+[serialno]

if sys.argv[1] == "--header":
	print("""\
// This is an auto-generated file!
#include <linux/ch9.h>
#include <linux/ch9-extra.h>

#ifndef DESCRIPTORS_STRING_TABLE_H_
#define DESCRIPTORS_STRING_TABLE_H_

#define USB_STRING_SERIAL_INDEX USB_STRING_INDEX(%i)

struct usb_descriptors_strings {
	struct usb_string_lang {
		__u8 bLength;
		__u8 bDescriptorType;
		__le16 wData[1];
	} language;""" % len(strings))
	for i, string in enumerate(strings):
		print("""\
	struct usb_string_%(i)i {
		__u8 bLength;
		__u8 bDescriptorType;
		__le16 wData[%(l)i];
	} string%(i)i;""" % {'l': len(string), 'i': i})
	print("""\
};

#endif // DESCRIPTORS_STRING_TABLE_H_
""")

if sys.argv[1] == "--cfile":
	print("""\
	.strings = {
		// English language header
		.language = {
			.bLength = sizeof(struct usb_string_lang),
			.bDescriptorType = USB_DT_STRING,
			.wData = { 0x0409 }, // 0x0409 is English
		},""")
	for i, string in enumerate(strings):
		d = ["((__le16)('%s'))" % s for s in string]

		print("""\
		// "%(s)s"
		.string%(i)i = {
			.bLength = sizeof(struct usb_string_%(i)i),
			.bDescriptorType = USB_DT_STRING,
			.wData = {%(d)s},
		},""" % {
		's': string,
		'i': i,
		'l': len(string),
		'd': ", ".join(d),
		})
	print("""\
	},
""")
