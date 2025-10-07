import fifty_primes

primes = fifty_primes.list_primes(50)

for i in range(len(primes)):
    print(f"{primes[i]:3d}", end=" ")
    if (i + 1) % 10 == 0:
        print("")
