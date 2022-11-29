build:
	make clear
	gcc ping.c
#	./a.out 8.8.8.8
	./a.out google.com

build-udp:
	make clear
	gcc ping_udp.c
	./a.out 8.8.8.8

clear:
	rm -f a.out