obj = $(basename $(wildcard *.sh) $(wildcard *.py))
dest = /usr/local/bin

.PHONY: all

all: $(patsubst %, $(dest)/%, $(obj))

$(dest)/%: %.sh
	cp -f $< $@
	chmod 755 $@

$(dest)/%: %.py
	cp -f $< $@
	chmod 755 $@
