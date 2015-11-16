
#include "descriptors.h"

__code __at(DSCR_AREA) struct usb_descriptors code_descriptors = {
	.device = {
		.bLength		= USB_DT_DEVICE_SIZE,
		.bDescriptorType	= USB_DT_DEVICE,
		.bcdUSB			= USB_BCD_V20,
		.bDeviceClass 		= USB_CLASS_MISC,
		.bDeviceSubClass	= UVC_SC_VIDEOSTREAMING,
		.bDeviceProtocol	= 0x01, // ?? Protocol code?
		.bMaxPacketSize0	= 64,
		.idVendor		= FTDI_VID,
		.idProduct		= PID,
		.bcdDevice		= DID,
		.iManufacturer		= USB_STRING_INDEX(0),
		.iProduct		= USB_STRING_INDEX(1),
		.iSerialNumber		= USB_STRING_INDEX(2),
		.bNumConfigurations	= 1
	},
	.highspeed = {
		.config = {
			.bLength		= USB_DT_CONFIG_SIZE,
			.bDescriptorType	= USB_DT_CONFIG,
			.wTotalLength		= sizeof(descriptors.highspeed),
			.bNumInterfaces		= 2,
			.bConfigurationValue	= 1,
			.iConfiguration		= USB_STRING_INDEX_NONE,
			.bmAttributes		= USB_CONFIG_ATT_ONE,
			.bMaxPower		= 250, // FIXME: ???
		},
		.interface0 = {
			.bLength		= USB_DT_INTERFACE_SIZE,
			.bDescriptorType	= USB_DT_INTERFACE,
			.bInterfaceNumber	= 0,
			.bAlternateSetting	= 0,
			.bNumEndpoints		= 2,
			.bInterfaceClass	= USB_CLASS_VENDOR_SPEC,
			.bInterfaceSubClass	= USB_SUBCLASS_VENDOR_SPEC,
			.bInterfaceProtocol	= USB_PROTOCOL_VENDOR_SPEC,
			.iInterface		= USB_STRING(1),
		},
		.endpoints0 = {
			{
				.bLength		= USB_DT_ENDPOINT_SIZE,
				.bDescriptorType 	= USB_DT_ENDPOINT,
				.bEndpointAddress	= USB_ENDPOINT_NUMBER(0x1) | USB_DIR_IN,
				.bmAttributes		= USB_ENDPOINT_XFER_BULK,
				.wMaxPacketSize		= 64, // EP1 only supports 64 bytes on the FX2
				.bInterval		= 0,
			},
			{
				.bLength		= USB_DT_ENDPOINT_SIZE,
				.bDescriptorType 	= USB_DT_ENDPOINT,
				.bEndpointAddress	= USB_ENDPOINT_NUMBER(0x2) | USB_DIR_OUT,
				.bmAttributes		= USB_ENDPOINT_XFER_BULK,
				.wMaxPacketSize		= 512,
				.bInterval		= 0,
			},
		},
		.interface1 = {
			.bLength		= USB_DT_INTERFACE_SIZE,
			.bDescriptorType	= USB_DT_INTERFACE,
			.bInterfaceNumber	= 1,
			.bAlternateSetting	= 0,
			.bNumEndpoints		= 2,
			.bInterfaceClass	= USB_CLASS_VENDOR_SPEC,
			.bInterfaceSubClass	= USB_SUBCLASS_VENDOR_SPEC,
			.bInterfaceProtocol	= USB_PROTOCOL_VENDOR_SPEC,
			.iInterface		= USB_STRING(1),
		},
		.endpoints1 = {
			{
				.bLength		= USB_DT_ENDPOINT_SIZE,
				.bDescriptorType 	= USB_DT_ENDPOINT,
				.bEndpointAddress	= USB_ENDPOINT_NUMBER(0x3) | USB_DIR_IN,
				.bmAttributes		= USB_ENDPOINT_XFER_BULK,
				.wMaxPacketSize		= 512,
				.bInterval		= 0,
			},
			{
				.bLength		= USB_DT_ENDPOINT_SIZE,
				.bDescriptorType 	= USB_DT_ENDPOINT,
				.bEndpointAddress	= USB_ENDPOINT_NUMBER(0x4) | USB_DIR_OUT,
				.bmAttributes		= USB_ENDPOINT_XFER_BULK,
				.wMaxPacketSize		= 512,
				.bInterval		= 0,
			},
		},
	},
	.qualifier = {
		.bLength = USB_DT_DEVICE_QUALIFIER_SIZE,
		.bDescriptorType = USB_DT_DEVICE_QUALIFIER,
		.bcdUSB = USB_BCD_V20,
		.bDeviceClass = USB_CLASS_PER_INTERFACE,
		.bDeviceSubClass = 0,
		.bDeviceProtocol = 0,
		.bMaxPacketSize0 = 64,
		.bNumConfigurations = 1,
		.bRESERVED = 0,
	},
	.fullspeed = 0x0,
#include "descriptors_strings.inc"
};
