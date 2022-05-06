CC := gcc
CFLAGS := -O3 -g -march=native
LDFLAGS := -lprofiler

all: single openmp

single: relax-fix.c
	$(CC) $(CFLAGS) $? $(LDFLAGS) -o $@

openmp: relax-fix.c
	$(CC) -fopenmp $(CFLAGS) $? $(LDFLAGS) -o $@

clean:
	rm -f $(EXECUTABLE)