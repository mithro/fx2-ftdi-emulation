
# TIAO USB Multi-Protocol Adapter (JTAG, SPI, I2C, Serial)

 * http://www.diygadget.com/tiao-usb-multi-protocol-adapter-jtag-spi-i2c-serial.html
 * http://www.tiaowiki.com/w/JTAG_Tutorials

## dmesg output

```
usb 3-2: new high-speed USB device number 4 using xhci_hcd
usb 3-2: New USB device found, idVendor=0403, idProduct=8a98
usb 3-2: New USB device strings: Mfr=1, Product=2, SerialNumber=3
usb 3-2: Product: TIAO USB Multi-Protocol Adapter
usb 3-2: Manufacturer: TIAO
usb 3-2: SerialNumber: TIM01168
usb 3-2: Ignoring serial port reserved for JTAG
ftdi_sio 3-2:1.1: FTDI USB Serial Device converter detected
usb 3-2: Detected FT2232H
usb 3-2: Number of endpoints 2
usb 3-2: Endpoint 1 MaxPacketSize 512
usb 3-2: Endpoint 2 MaxPacketSize 512
usb 3-2: Setting MaxPacketSize 512
usb 3-2: FTDI USB Serial Device converter now attached to ttyUSB0
```

## lsusb output

```
Bus 003 Device 004: ID 0403:8a98 Future Technology Devices International, Ltd TIAO Multi-Protocol Adapter
```

## Descriptors

```
Bus 003 Device 004: ID 0403:8a98 Future Technology Devices International, Ltd TIAO Multi-Protocol Adapter
Device Descriptor:
  bLength                18
  bDescriptorType         1
  bcdUSB               2.00
  bDeviceClass            0 (Defined at Interface level)
  bDeviceSubClass         0 
  bDeviceProtocol         0 
  bMaxPacketSize0        64
  idVendor           0x0403 Future Technology Devices International, Ltd
  idProduct          0x8a98 TIAO Multi-Protocol Adapter
  bcdDevice            7.00
  iManufacturer           1 TIAO
  iProduct                2 TIAO USB Multi-Protocol Adapter
  iSerial                 3 TIM01168
  bNumConfigurations      1
  Configuration Descriptor:
    bLength                 9
    bDescriptorType         2
    wTotalLength           55
    bNumInterfaces          2
    bConfigurationValue     1
    iConfiguration          0 
    bmAttributes         0x80
      (Bus Powered)
    MaxPower              450mA
    Interface Descriptor:
      bLength                 9
      bDescriptorType         4
      bInterfaceNumber        0
      bAlternateSetting       0
      bNumEndpoints           2
      bInterfaceClass       255 Vendor Specific Class
      bInterfaceSubClass    255 Vendor Specific Subclass
      bInterfaceProtocol    255 Vendor Specific Protocol
      iInterface              2 TIAO USB Multi-Protocol Adapter
      Endpoint Descriptor:
        bLength                 7
        bDescriptorType         5
        bEndpointAddress     0x81  EP 1 IN
        bmAttributes            2
          Transfer Type            Bulk
          Synch Type               None
          Usage Type               Data
        wMaxPacketSize     0x0200  1x 512 bytes
        bInterval               0
      Endpoint Descriptor:
        bLength                 7
        bDescriptorType         5
        bEndpointAddress     0x02  EP 2 OUT
        bmAttributes            2
          Transfer Type            Bulk
          Synch Type               None
          Usage Type               Data
        wMaxPacketSize     0x0200  1x 512 bytes
        bInterval               0
    Interface Descriptor:
      bLength                 9
      bDescriptorType         4
      bInterfaceNumber        1
      bAlternateSetting       0
      bNumEndpoints           2
      bInterfaceClass       255 Vendor Specific Class
      bInterfaceSubClass    255 Vendor Specific Subclass
      bInterfaceProtocol    255 Vendor Specific Protocol
      iInterface              2 TIAO USB Multi-Protocol Adapter
      Endpoint Descriptor:
        bLength                 7
        bDescriptorType         5
        bEndpointAddress     0x83  EP 3 IN
        bmAttributes            2
          Transfer Type            Bulk
          Synch Type               None
          Usage Type               Data
        wMaxPacketSize     0x0200  1x 512 bytes
        bInterval               0
      Endpoint Descriptor:
        bLength                 7
        bDescriptorType         5
        bEndpointAddress     0x04  EP 4 OUT
        bmAttributes            2
          Transfer Type            Bulk
          Synch Type               None
          Usage Type               Data
        wMaxPacketSize     0x0200  1x 512 bytes
        bInterval               0
Device Qualifier (for other device speed):
  bLength                10
  bDescriptorType         6
  bcdUSB               2.00
  bDeviceClass            0 (Defined at Interface level)
  bDeviceSubClass         0 
  bDeviceProtocol         0 
  bMaxPacketSize0        64
  bNumConfigurations      1
Device Status:     0x0000
  (Bus Powered)
```
