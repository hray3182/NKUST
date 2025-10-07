def list_primes(n):
    array = [2]
    i = 3
    while len(array) < n:
        is_prime = True
        for j in range(0, len(array)):
            if i % array[j] == 0:
                is_prime = False
                break

        if is_prime:
            array.append(i)
        i += 2

    return array
