
TARGET := ftdi
FX2LIBDIR := ./fx2lib
LIBS := $(FX2LIBDIR)/lib/fx2.lib
INCS :=  -I$(FX2LIBDIR)/include

CC_SRCS := descriptors.c #bitbang/mpsse.c bitbang/i2c.c
CC_OBJS := $(CC_SRCS:%.c=%.rel)

CC := sdcc

# Compiler options
CFLAGS += --verbose --std-c99 -mmcs51 -Wa"-p"
# Where to put things in the memory
CFLAGS += --code-size 0x3e00 --xram-size 0x0200 -Wl"-b DSCR_AREA=0x2e00" -Wl"-b INT2JT=0x3f00"

# Use make V=1 for a verbose build.
ifndef V
	Q_CC=@echo      '      CC ' $@;
	Q_AS=@echo      '      AS ' $@;
	Q_LINK=@echo    '    LINK ' $@;
	Q_RM=@echo      '   CLEAN ';
	Q_OBJCOPY=@echo ' OBJCOPY ' $@;
	Q_GEN=@echo     '     GEN ' $@;
endif

.PHONY: all clean check check_int2jt

all: $(TARGET).hex

$(CC_SRCS): $(FX2LIBDIR)/lib/fx2.lib

$(FX2LIBDIR)/.git:
	git submodule init $@
	git submodule update --recursive $@

$(FX2LIBDIR)/lib/fx2.lib: $(FX2LIBDIR)/.git
	cd $(dir $@) && make -j1

$(TARGET).hex: $(CC_OBJS)
	$(Q_LINK)$(CC) $(CFLAGS) -o $@ $+ $(LIBS)

%.rel: %.c
	$(Q_CC)$(CC) $(CFLAGS) -c $(INCS) $?

%.asm: %.c
	$(Q_CC)$(CC) $(CFLAGS) -c $(INCS) $?

# Generate the bit banging code
bitbang/mpsse.c: bitbang/*.py
	cd bitbang; python3 mpsse.py > mpsse.c

bitbang/i2c.c: bitbang/*.py
	cd bitbang; python3 i2c.py > i2c.c

# Generate the descriptor strings
descriptors_strings.h: descriptors_string_table.py descriptors.strings
	@python2 descriptors_string_table.py --header < descriptors.strings > descriptors_strings.h
descriptors_strings.inc: descriptors_string_table.py descriptors.strings
	@python2 descriptors_string_table.py --cfile < descriptors.strings > descriptors_strings.inc

descriptors.c: descriptors_strings.h descriptors_strings.inc

# Check the descriptors with GCC rather then sdcc
check_descriptors: descriptors.c
	gcc -Wall -Werror $(INCS) descriptors.c
	@rm -f a.out

# Check that the interrupt vector table ended up were we asked it too.
check_int2jt: $(TARGET).hex
	@export REQUESTED=$(shell grep "INT2JT=" $(TARGET).map | sed -e's/INT2JT=//'); \
	export ACTUAL=$(shell grep "C:.*INT2JT" $(TARGET).map | sed -e's/C: *0*\([^ ]*\)  _INT2JT.*/0x\1/' | tr A-Z a-z ); \
	if [ "$$REQUESTED" != "$$ACTUAL" ]; then \
		echo "INT2JT at $$ACTUAL but requested $$REQUESTED"; \
		exit 1; \
	fi

check: check_int2jt check_descriptors

clean:
	$(Q_RM)$(RM) *.iic *.asm *.lnk *.lst *.map *.mem *.rel *.rst *.sym \
		*.lk $(TARGET).hex
	cd $(FX2LIBDIR) && make clean

distclean: clean
	$(RM) -r $(FX2LIBDIR)
