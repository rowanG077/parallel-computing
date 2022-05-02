CFLAGS := -O3 -pg -fopenmp

CC := gcc
EXECUTABLE := relax-fix relax-fix-omp

all: $(EXECUTABLE)

%: %.c
	$(CC) -o $@ $< $(CFLAGS)

clean:
	rm -f $(EXECUTABLE)