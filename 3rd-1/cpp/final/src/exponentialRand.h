#ifndef _EXPONENTIALRAND_H_
#define _EXPONENTIALRAND_H_

class exponentialRand
{
private:
	unsigned int seed;		// seed of a sequence of pseudo-random numbers
	double lambda;			// parameter of an exponential distribution
	double uniform_rand();	// generate a pseudo-random number in [0,1]
	

public:
	exponentialRand(unsigned int seed_in, double lambda_in);	// constructor
	double eRand();		//generate an exponentially distributed pseudo-random number with parameter lambda
	int uniform_rand_range(int lowerbound, int upperbound);
};


#endif