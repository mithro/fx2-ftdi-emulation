
| Mnemoic		| Desc								| Byte Size | Cycles | Flags	| Opcode|
| ---------------------	| ---------------------------------------------------------------------	| - | - | --------------| ----- |
| ADD A, Rn		| Add register to A 							| 1 | 1 | CY OV AC	| 28-2F |
| ADD A, direct		| Add direct byte to A 							| 2 | 2 | CY OV AC	| 25	|
| ADD A, @Ri		| Add data memory to A 							| 1 | 1 | CY OV AC	| 26-27 |
| ADD A, #data		| Add immediate to A 							| 2 | 2 | CY OV AC	| 24	|
| ADDC A, Rn		| Add register to A with carry 						| 1 | 1 | CY OV AC	| 38-3F |
| ADDC A, direct	| Add direct byte to A with carry 					| 2 | 2 | CY OV AC	| 35	|
| ADDC A, @Ri		| Add data memory to A with carry 					| 1 | 1 | CY OV AC	| 36-37 |
| ADDC A, #data		| Add immediate to A with carry 					| 2 | 2 | CY OV AC	| 34	|
| SUBB A, Rn		| Subtract register from A with borrow 					| 1 | 1 | CY OV AC	| 98-9F |
| SUBB A, direct	| Subtract direct byte from A with borrow 				| 2 | 2 | CY OV AC	| 95	|
| SUBB A, @Ri		| Subtract data memory from A with borrow 				| 1 | 1 | CY OV AC	| 96-97 |
| SUBB A, #data		| Subtract immediate from A with borrow 				| 2 | 2 | CY OV AC	| 94	|
| INC A			| Increment A 								| 1 | 1 | 		| 04	|
| INC Rn		| Increment register 							| 1 | 1 | 		| 08-0F |
| INC direct		| Increment direct byte 						| 2 | 2 | 		| 05 	|
| INC @Ri		| Increment data memory 						| 1 | 1 | 		| 06-07 |
| DEC A			| Decrement A 								| 1 | 1 | 		| 14 	|
| DEC Rn		| Decrement Register 							| 1 | 1 | 		| 18-1F |
| DEC direct		| Decrement direct byte 						| 2 | 2 | 		| 15 	|
| DEC @Ri		| Decrement data memory 						| 1 | 1 |		| 16-17 |
| INC DPTR		| Increment data pointer 						| 1 | 3 |		| A3 	|
| MUL AB		| Multiply A and B (unsigned; product in B:A) 				| 1 | 5 | CY=0 OV 	| A4 	|
| DIV AB		| Divide A by B (unsigned; quotient in A, remainder in B)  		| 1 | 5 | CY=0 OV 	| 84 	|
| DA A			| Decimal adjust A 							| 1 | 1 | CY 		| D4 	|
| ANL A, Rn		| AND register to A 							| 1 | 1 | 		| 58-5F |
| ANL A, direct		| AND direct byte to A 							| 2 | 2 | 		| 55 	|
| ANL A, @Ri		| AND data memory to A 							| 1 | 1 | 		| 56-57 |
| ANL A, #data		| AND immediate to A 							| 2 | 2 | 		| 54 	|
| ANL direct, A		| AND A to direct byte 							| 2 | 2 | 		| 52 	|
| ANL direct, #data	| AND immediate data to direct byte 					| 3 | 3 | 		| 53 	|
| ORL A, Rn		| OR register to A 							| 1 | 1 | 		| 48-4F |
| ORL A, direct		| OR direct byte to A 							| 2 | 2 | 		| 45 	|
| ORL A, @Ri		| OR data memory to A 							| 1 | 1 |       	| 46-47 |
| ORL A, #data		| OR immediate to A 							| 2 | 2 |       	| 44 	|
| ORL direct, A		| OR A to direct byte 							| 2 | 2 | 		| 42 	|
| ORL direct, #data	| OR immediate data to direct byte 					| 3 | 3 | 		| 43 	|
| XRL A, Rn		| Exclusive-OR register to A 						| 1 | 1 | 		| 68-6F |
| XRL A, direct		| Exclusive-OR direct byte to A 					| 2 | 2 | 		| 65 	|
| XRL A, @Ri		| Exclusive-OR data memory to A 					| 1 | 1 | 		| 66-67 |
| XRL A, #data		| Exclusive-OR immediate to A 						| 2 | 2 | 		| 64 	|
| XRL direct, A		| Exclusive-OR A to direct byte 					| 2 | 2 | 		| 62 	|
| XRL direct, #data	| Exclusive-OR immediate to direct byte 				| 3 | 3 |       	| 63 	|
| CLR A			| Clear A 								| 1 | 1 |       	| E4 	|
| CPL A			| Complement A 								| 1 | 1 | 		| F4 	|
| SWAP A		| Swap nibbles of a 							| 1 | 1 | 		| C4 	|
| RL A			| Rotate A left 							| 1 | 1 | 		| 23 	|
| RLC A			| Rotate A left through carry 						| 1 | 1 | CY		| 33 	|
| RR A			| Rotate A right 							| 1 | 1 | 		| 03 	|
| RRC A			| Rotate A right through carry 						| 1 | 1 | CY		| 13 	|
| MOV A, Rn		| Move register to A 							| 1 | 1 | 		| E8-EF |
| MOV A, direct		| Move direct byte to A 						| 2 | 2 | 		| E5 	|
| MOV A, @Ri		| Move data byte at Ri to A 						| 1 | 1 | 		| E6-E7 |
| MOV A, #data		| Move immediate to A 							| 2 | 2 | 		| 74 	|
| MOV Rn, A		| Move A to register 							| 1 | 1 | 		| F8-FF |
| MOV Rn, direct	| Move direct byte to register 						| 2 | 2 | 		| A8-AF |
| MOV Rn, #data		| Move immediate to register 						| 2 | 2 | 		| 78-7F |
| MOV direct, A		| Move A to direct byte 						| 2 | 2 |       	| F5 	|
| MOV direct, Rn	| Move register to direct byte 						| 2 | 2 |       	| 88-8F |
| MOV direct, direct	| Move direct byte to direct byte 					| 3 | 3 | 		| 85 	|
| MOV direct, @Ri	| Move data byte at Ri to direct byte 					| 2 | 2 | 		| 86-87 |
| MOV direct, #data	| Move immediate to direct byte 					| 3 | 3 | 		| 75 	|
| MOV @Ri, A		| Move A to data memory at address Ri 					| 1 | 1 | 		| F6-F7 |
| MOV @Ri, direct	| Move direct byte to data memory at address Ri 			| 2 | 2 | 		| A6-A7 |
| MOV @Ri, #data	| Move immediate to data memory at address Ri 				| 2 | 2 | 		| 76-77 |
| MOV DPTR, #data16	| Move 16-bit immediate to data pointer 				| 3 | 3 | 		| 90 	|
| MOVC A, @A+DPTR	| Move code byte at address DPTR+A to A 				| 1 | 3 |       	| 93 	|
| MOVC A, @A+PC		| Move code byte at address PC+A to A 					| 1 | 3 |       	| 83 	|
| MOVX A, @Ri		| Move external data at address Ri to A 				| 1 | 2 | 		| E2-E3 |
| MOVX A, @DPTR		| Move external data at address DPTR to A 				| 1 | 2 | 		| E0 	|
| MOVX @Ri, A		| Move A to external data at address Ri 				| 1 | 2 | 		| F2-F3 |
| MOVX @DPTR, A		| Move A to external data at address DPTR 				| 1 | 2 | 		| F0 	|
| PUSH direct		| Push direct byte onto stack						| 2 | 2 | 		| C0 	|
| POP direct		| Pop direct byte from stack 						| 2 | 2 | 		| D0 	|
| XCH A, Rn		| Exchange A and register 						| 1 | 1 | 		| C8-CF |
| XCH A, direct		| Exchange A and direct byte 						| 2 | 2 |       	| C5 	|
| XCH A, @Ri		| Exchange A and data memory at address Ri 				| 1 | 1 |       	| C6-C7 |
| XCHD A, @Ri		| Exchange the low-order nibbles of A and data memory at address Ri	| 1 | 1 | 		| D6-D7 |
| CLR C			| Clear carry 								| 1 | 1 | CY=0 		| C3 	|
| CLR bit		| Clear direct bit 							| 2 | 2 | 		| C2 	|
| SETB C		| Set carry 								| 1 | 1 | CY=1 		| D3 	|
| SETB bit		| Set direct bit 							| 2 | 2 | 		| D2 	|
| CPL C			| Complement carry 							| 1 | 1 | CY 		| B3 	|
| CPL bit		| Complement direct bit 						| 2 | 2 | 		| B2 	|
| ANL C, bit		| AND direct bit to carry 						| 2 | 2 | CY 		| 82 	|
| ANL C, /bit		| AND inverse of direct bit to carry 					| 2 | 2 | CY 		| B0 	|
| ORL C, bit		| OR direct bit to carry 						| 2 | 2 | CY 		| 72 	|
| ORL C, /bit		| OR inverse of direct bit to carry 					| 2 | 2 | CY 		| A0 	|
| MOV C, bit		| Move direct bit to carry 						| 2 | 2 | CY 		| A2 	|
| MOV bit, C		| Move carry to direct bit 						| 2 | 2 |    	   	| 92 	|
| ACALL addr11		| Absolute call to subroutine 						| 2 | 3 |    	   	| 11-F1 |
| LCALL addr16		| Long call to subroutine 						| 3 | 4 |      	   	| 12 	|
| RET 			| Return from subroutine 						| 1 | 4 |      	   	| 22 	|
| RETI 			| Return from interrupt 						| 1 | 4 | 		| 32 	|
| AJMP addr11		| Absolute jump unconditional 						| 2 | 3 | 		| 01-E1 |
| LJMP addr16		| Long jump unconditional 						| 3 | 4 | 		| 02 	|
| SJMP rel		| Short jump (relative address) 					| 2 | 3 |       	| 80 	|
| JC rel		| Jump if carry = 1 							| 2 | 3 |       	| 40 	|
| JNC rel		| Jump if carry = 0 							| 2 | 3 | 		| 50 	|
| JB bit, rel		| Jump if direct bit = 1 						| 3 | 4 | 		| 20 	|
| JNB bit, rel		| Jump if direct bit = 0 						| 3 | 4 | 		| 30 	|
| JBC bit, rel		| Jump if direct bit = 1, then clear the bit 				| 3 | 4 | 		| 10 	|
| JMP @A+DPTR		| Jump indirect to address DPTR+A 					| 1 | 3 | 		| 73 	|
| JZ rel		| Jump if accumulator = 0						| 2 | 3 |		| 60    |
| JNZ rel		| Jump if accumulator is non-zero					| 2 | 3 | 		| 70    |
| CJNE A, direct, rel 	| Compare A to direct byte; jump if not equal				| 3 | 4 | CY		| B5    |
| CJNE A, #data, rel 	| Compare A to immediate; jump if not equal				| 3 | 4 | CY		| B4    |
| CJNE Rn, #data, rel 	| Compare register to immediate; jump if not equal			| 3 | 4 | CY		| B8-BF |
| CJNE @Ri, #data, rel	| Compare data memory to immediate; jump if not equal			| 3 | 4 | CY		| B6-B7 |
| DJNZ Rn, rel		| Decrement register; jump if not zero					| 2 | 3 | 		| D8-DF |
| DJNZ direct, rel	| Decrement direct byte; jump if not zero				| 3 | 4 | 		| D5    |
| NOP			| No operation								| 1 | 1 | 		| 00    |
