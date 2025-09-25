primes = [2]
n = 2
i = 0
while n < 51:
    if n % 2 == 0:
        n += 1
        continue
    for i in range(2, n):
        if n % i == 0:
            break
    primes.append(n)
    n += 1


print(primes)
