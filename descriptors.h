
#include <stddef.h>

#include "date.h"
#include "uvclocal.h"
#include "descriptors_strings.h"

#include <linux/ch9.h>
#include <linux/ch9-extra.h>

#ifndef DESCRIPTORS_H_

struct usb_descriptors {
	struct usb_device_descriptor device;
	struct usb_section {
		struct usb_config_descriptor config;
		struct usb_interface_descriptor interface0;
		struct usb_endpoint_descriptor endpoints0[2];
		struct usb_interface_descriptor interface1;
		struct usb_endpoint_descriptor endpoints1[2];
	};
	struct usb_qualifier_descriptor qualifier;
	WORD fullspeed;
	struct usb_descriptors_strings strings;
};

__xdata __at(DSCR_AREA) struct usb_descriptors descriptors;

__code __at(DSCR_AREA+offsetof(struct usb_descriptors, device)) WORD dev_dscr;
__code __at(DSCR_AREA+offsetof(struct usb_descriptors, qualifier)) WORD dev_qual_dscr;
__code __at(DSCR_AREA+offsetof(struct usb_descriptors, highspeed)) WORD highspd_dscr;
__code __at(DSCR_AREA+offsetof(struct usb_descriptors, fullspeed)) WORD fullspd_dscr;
__code __at(DSCR_AREA+offsetof(struct usb_descriptors, strings)) WORD dev_strings;

#endif // DESCRIPTORS_H_
