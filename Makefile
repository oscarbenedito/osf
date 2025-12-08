src = $(wildcard *.sh) $(wildcard *.py)
obj = $(patsubst %,$(dest)/%,$(basename $(src)))
ifeq ($(origin out), environment)
	dest = $(out)/bin
else
	dest = /usr/local/bin
endif

.PHONY: install uninstall

install: $(obj)

$(dest)/%: %.sh | $(dest)
	cp -f $< $@
	chmod 755 $@

$(dest)/%: %.py | $(dest)
	cp -f $< $@
	chmod 755 $@

$(dest):
	mkdir -p $@

uninstall:
	rm -f $(obj)
