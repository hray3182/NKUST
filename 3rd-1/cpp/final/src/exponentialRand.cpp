#include "exponentialRand.h"
#include <cmath>

// 使用線性同餘生成器 (Linear Congruential Generator, LCG)
// 參數來自 glibc
static const unsigned int LCG_A = 1103515245;
static const unsigned int LCG_C = 12345;
static const unsigned int LCG_M = 2147483648U; // 2^31

exponentialRand::exponentialRand(unsigned int seed_in, double lambda_in)
    : seed(seed_in), lambda(lambda_in)
{
}

// 產生 [0, 1) 之間的均勻分布隨機數
double exponentialRand::uniform_rand()
{
    seed = (LCG_A * seed + LCG_C) % LCG_M;
    return static_cast<double>(seed) / LCG_M;
}

// 產生指數分布的隨機數
// 使用逆變換法: X = -ln(U) / lambda
double exponentialRand::eRand()
{
    double u = uniform_rand();
    // 避免 log(0) 的問題
    while (u == 0.0) {
        u = uniform_rand();
    }
    return -std::log(u) / lambda;
}

// 產生 [lowerbound, upperbound] 之間的均勻分布整數
int exponentialRand::uniform_rand_range(int lowerbound, int upperbound)
{
    double u = uniform_rand();
    int range = upperbound - lowerbound + 1;
    return lowerbound + static_cast<int>(u * range);
}
