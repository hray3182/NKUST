CXX = g++
CXXFLAGS = -std=c++11

SRCDIR = src
SRCS = $(SRCDIR)/main.cpp $(SRCDIR)/exponentialRand.cpp $(SRCDIR)/PKTArrivalEventGenerator.cpp $(SRCDIR)/Schedule.cpp $(SRCDIR)/MLO.cpp
LIBS = $(SRCDIR)/exponentialRand.cpp $(SRCDIR)/PKTArrivalEventGenerator.cpp $(SRCDIR)/Schedule.cpp $(SRCDIR)/MLO.cpp

all: test

test: $(SRCS)
	$(CXX) $(CXXFLAGS) -o test $(SRCS)

demo: $(SRCDIR)/demo.cpp $(LIBS)
	$(CXX) $(CXXFLAGS) -o demo $(SRCDIR)/demo.cpp $(LIBS)

clean:
	rm -f test demo

run: test
	./test

run-demo: demo
	./demo
