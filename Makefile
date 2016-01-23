all:

install:
	cp -f scorelib.py scorelib
	install scorelib /usr/bin
	rm scorelib
uninstall:
	rm /usr/bin/scorelib
