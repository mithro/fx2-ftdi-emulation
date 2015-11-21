
 * (3cy) DJNZ Rn, rel - Decrement register, jump if not zero
 * (3cy) JC  - Jump if carry
 * (3cy) JNC - Jump if not carry

48MHz @ 4 clock per instruction cycle == 12MHz

OUT register
```
       +---+---+---+---+---+---+---+---+      +---+
  /--> | 7 | 6 | 5 | 4 | 3 | 2 | 1 | 0 | <--> | c | <--\
  |    +---+---+---+---+---+---+---+---+      +---+    |
  |                                                    |
  \----------------------------------------------------/
```

 * (1cy) RLC A - Rotate A left through carry
 * (1cy) RRC A - Rotate A right through carry

 * Most Significant Bit First  -> RRC
 * Least Significant Bit First -> RLC

 * TMS mode
 * Bit 7    -> TDO
 * Bit 6->0 -> TMS

# If data out/ data in pins are bit capable

```
     MOV dest, src
(2cy) MOV  C, bit - Move direct bit to carry
(2cy) MOV  bit, C - Move carry to direct bit
(2cy) CLR  bit    - Clear direct bit
(2cy) SETB bit    - Set direct bit
(2cy) CPL  bit    - Compliment direct bit

(1cy) CLR  C - Clear carry
(1cy) SETB C - Set carry
(1cy) CPL  C - Complement carry
```

## if READ and WRITE on same edge

```
a1^ (2cy) CPL pin_clk_out
a2  -- (2cy) MOV pin_data_out, C
a3  -- (2cy) MOV C, pin_data_in
b1^ (2cy) CPL pin_clk_out
b2  -- (2cy) ROTATE + NOP
b3  -- (2cy) NOP, NOP
== 6 cycles between clock edges
```

## if READ and WRITE on opposite edges

```
a1^ (2cy) CPL pin_clk_out
a3  -- (2cy) MOV pin_data_out, C
a3  -- (1cy) NOP
b1^ (2cy) CPL pin_clk_out
b2  -- (2cy) MOV C, pin_data_in
b3  -- (1cy) ROTATE
== 5 cycles between clock edges
```

 * 12MHz / 6 cycles per CLK == 2Mbit/s

# If only byte accessible

## Using proxy byte

"proxy byte" in bit addressable space == direct space

 * No ops touch register A

```
Toggle clock - 5 cycles
(2cy) CPL proxy_pin_clk
(3cy) MOV pins, proxy
```

```
Write data out - 5 cycles
(2cy) MOV proxy_pin_data_out, C
(3cy) MOV pins, proxy
```

```
Read data in - 5 cycles
(3cy) MOV proxy, pins
(2cy) MOV C, proxy_pin_data_in
```

### if READ and WRITE on same edge

```
b6  (2cy) CPL proxy_pin_clk
a1^ (3cy) MOV pins, proxy
a2  -- (2cy) MOV proxy_pin_data_out, C
a3  -- (3cy) MOV pins, proxy
a4  -- (3cy) MOV proxy, pins
a5  -- (2cy) MOV C, proxy_pin_data_in
a6  (2cy) CPL proxy_pin_clk
b1^ (3cy) MOV pins, proxy
b2  -- (2cy) ROTATE + NOP
b3  -- (3cy) NOP + NOP + NOP
b4  -- (3cy) NOP + NOP + NOP
b5  -- (2cy) NOP + NOP
== 15 cycles between CLK edges
```

#### Better version?
```
b4  (2cy) MOV proxy_pin_data_out, C
b5  (2cy) CPL proxy_pin_clk
a1^ (3cy) MOV pins, proxy
a2  (3cy) MOV proxy, pins
a3  (2cy) MOV C, proxy_pin_data_in

a4  (2cy) CPL proxy_pin_clk
a5  (2cy) ROTATE + NOP
b1^ (3cy) MOV pins, proxy
b2  (3cy) NOP + NOP + NOP
b3  (2cy) NOP + NOP
== 12 cycles between CLK edges
```

### if READ and WRITE on opposite edges

```
b5  (2cy) CPL R2_pin_clk
a1^ (3cy) MOV pins, proxy
a2  -- (2cy) MOV proxy_pin_data_out, C
a3  -- (3cy) MOV pins, proxy
a4  -- (1cy) NOP

a5  (2cy) CPL R2_pin_clk
b1^ (3cy)*MOV pins, proxy
b2  -- (3cy) MOV proxy, pins
b3  -- (2cy) MOV C, proxy_pin_data_in
b4  -- (1cy) ROTATE
== 11 cycles between CLK edges
```

#### Better version?
```
b4  (2cy) MOV proxy_pin_data_out, C
b5  (2cy) CPL proxy_pin_clk
a1^ (3cy)*MOV pins, R2
a2  (2cy) NOP + NOP
a3  (1cy) NOP
a4  (2cy) NOP + NOP

a5  (2cy) CPL proxy_pin_clk
b1^ (3cy)*MOV pins, proxy
b2  (2cy) MOV proxy, pins
b3  (1cy) ROTATE 
== 9 cycles between CLK edges
```

## Using proxy byte + @R0

```
MOV direct, @Ri    == 2 cycles
MOV @Ri, direct    == 2 cycles
compared too....
MOV direct, direct == 3 cycles
```

 * No ops touch register A
 * R0 == proxy

```
Toggle clock - 4 cycles
(2cy) CPL proxy_pin_clk
(2cy) MOV pins, @R0
```

```
Write data out - 4 cycles
(2cy) MOV proxy_pin_data_out, C
(2cy) MOV pins, @R0
```

```
Read data in - 4 cycles
(2cy) MOV @R0, pins
(2cy) MOV C, proxy_pin_data_in
```

### if READ and WRITE on same edge

```
a1^ (2cy) CPL proxy_pin_clk
a2  (2cy) MOV pins, @R0
a3  -- (2cy) MOV proxy_data_out, C
a4  -- (2cy) MOV pins, @R0
a5  -- (2cy) MOV @R0, pins
a6  -- (2cy) MOV C, proxy_data_in
b1^ (2cy) CPL pin_clk_out
b2  (2cy) MOV pins, @R0
b3  -- (2cy) ROTATE + NOP
b4  -- (2cy) NOP, NOP
b5  -- (2cy) NOP, NOP
b6  -- (2cy) NOP, NOP
== 12 cycles between clock edges
```

#### Better version?
```
b4  (2cy) MOV proxy_pin_data_out, C
b5  (2cy) CPL proxy_pin_clk
a1^ (2cy) MOV pins, @R0
a2  (2cy) MOV @R0, pins
a3  (2cy) MOV C, proxy_pin_data_in

a4  (2cy) CPL proxy_pin_clk
a5  (2cy) ROTATE + NOP
b1^ (2cy) MOV pins, @R0
b2  (2cy) NOP + NOP
b3  (2cy) NOP + NOP
== 10 cycles between CLK edges
```
 
### if READ and WRITE on opposite edges

```
a1^ (2cy) CPL proxy_clk_out
a2  (2cy) MOV pins, @R0
a4  -- (2cy) MOV proxy_data_out, C
a5  -- (2cy) MOV pins, @R0
a6  -- (1cy) NOP
b1^ (2cy) CPL proxy_clk_out
b2  (2cy) MOV pins, @R0
b3  -- (2cy) MOV @R0, pins
b4  -- (2cy) MOV C, proxy_data_in
b6  -- (1cy) ROTATE
== 9 cycles between clock edges
```

 * 12MHz / 12 cycles per CLK == 1.0Mbit/s
 * 12MHz / 10 cycles per CLK == 1.2Mbit/s
 * 12MHz /  9 cycles per CLK == 1.3Mbit/s

## Using lots of registers

```
      MOV dest, src
(2cy) MOV direct, Rn - Move direct byte to register
(2cy) MOV Rn, direct - Move register to direct byte
(3cy) MOV direct, direct - Move direct to direct
(1cy) XCH A, Rn     - Exchange A and register
(2cy) XCH A, direct - Exchange A and direct
```

 * `Rx_clk_out_mask`
 * `Rx_data_out_mask`
 * `Rx_data_out_store`
 * `Rx_data_in_mask`
 * `Rx_data_in_store`

```
Toggle clock, preserving A - 4 cycles
(1cy) XCH A, Rx_clk_out_mask
(2cy) XRL pins, A
(1cy) XCH A, Rx_clk_out_mask
```

```
Toggle clock, clobbering A - 3 cycles
(1cy) MOV A, Rx_clk_out_mask
(2cy) XRL pins, A
```

```
Write data out - 6 cycles
-- (1cy) MOV A, Rx_data_out
-- (1cy) ROTATE
-- (1cy) MOV Rx_data_out, A
-- (1cy) ORL A, Rx_data_out_mask
-- (2cy) ORL pins, A
```

```
Read data in - 6 cycles
-- (1cy) MOV A, Rx_data_in_mask
-- (2cy) ANL A, pins
-- (1cy) ORL A, Rx_data_in
-- (1cy) ROTATE
-- (1cy) MOV Rx_data_in, A
```

