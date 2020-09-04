src = $(wildcard *.sh) $(wildcard *.py)
obj = $(patsubst %,$(dest)/%,$(basename $(src)))
dest = /usr/local/bin

.PHONY: install uninstall

install: $(obj)

$(dest)/%: %.sh
	cp -f $< $@
	chmod 755 $@

$(dest)/%: %.py
	cp -f $< $@
	chmod 755 $@

uninstall:
	rm -f $(obj)
