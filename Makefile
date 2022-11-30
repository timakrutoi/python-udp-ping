build:
	@make clear
	@gcc ping.c
#	./a.out 8.8.8.8
	@./a.out google.com

clear:
	@rm -f a.out