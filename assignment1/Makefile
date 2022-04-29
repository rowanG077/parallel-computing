CFLAGS := -O3 -g -fopenmp

CC := gcc
EXECUTABLE := relax-fix

all: $(EXECUTABLE)

%: %.c
	$(CC) -o $@ $< $(CFLAGS)

clean:
	rm -f $(EXECUTABLE)