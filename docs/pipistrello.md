
# Pipistrello Rev 2.0

 * http://pipistrello.saanlima.com/index.php?title=Welcome_to_Pipistrello

## dmesg output

```
usb 3-2: new high-speed USB device number 3 using xhci_hcd
usb 3-2: New USB device found, idVendor=0403, idProduct=6010
usb 3-2: New USB device strings: Mfr=1, Product=2, SerialNumber=3
usb 3-2: Product: Pipistrello LX45
usb 3-2: Manufacturer: Saanlima
usb 3-2: SerialNumber: 400100527273
usbcore: registered new interface driver usbserial
usbcore: registered new interface driver usbserial_generic
usbserial: USB Serial support registered for generic
usbcore: registered new interface driver ftdi_sio
usbserial: USB Serial support registered for FTDI USB Serial Device
ftdi_sio 3-2:1.0: FTDI USB Serial Device converter detected
usb 3-2: Detected FT2232H
usb 3-2: Number of endpoints 2
usb 3-2: Endpoint 1 MaxPacketSize 512
usb 3-2: Endpoint 2 MaxPacketSize 512
usb 3-2: Setting MaxPacketSize 512
usb 3-2: FTDI USB Serial Device converter now attached to ttyUSB0
ftdi_sio 3-2:1.1: FTDI USB Serial Device converter detected
usb 3-2: Detected FT2232H
usb 3-2: Number of endpoints 2
usb 3-2: Endpoint 1 MaxPacketSize 512
usb 3-2: Endpoint 2 MaxPacketSize 512
usb 3-2: Setting MaxPacketSize 512
usb 3-2: FTDI USB Serial Device converter now attached to ttyUSB1
```

## lsusb output

```
Bus 003 Device 003: ID 0403:6010 Future Technology Devices International, Ltd FT2232C Dual USB-UART/FIFO IC
```

## Descriptors

```
Bus 003 Device 003: ID 0403:6010 Future Technology Devices International, Ltd FT2232C Dual USB-UART/FIFO IC
Device Descriptor:
  bLength                18
  bDescriptorType         1
  bcdUSB               2.00
  bDeviceClass            0 (Defined at Interface level)
  bDeviceSubClass         0 
  bDeviceProtocol         0 
  bMaxPacketSize0        64
  idVendor           0x0403 Future Technology Devices International, Ltd
  idProduct          0x6010 FT2232C Dual USB-UART/FIFO IC
  bcdDevice            7.00
  iManufacturer           1 Saanlima
  iProduct                2 Pipistrello LX45
  iSerial                 3 400100527273
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
    MaxPower              300mA
    Interface Descriptor:
      bLength                 9
      bDescriptorType         4
      bInterfaceNumber        0
      bAlternateSetting       0
      bNumEndpoints           2
      bInterfaceClass       255 Vendor Specific Class
      bInterfaceSubClass    255 Vendor Specific Subclass
      bInterfaceProtocol    255 Vendor Specific Protocol
      iInterface              2 Pipistrello LX45
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
      iInterface              2 Pipistrello LX45
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
