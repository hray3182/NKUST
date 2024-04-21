import random
import os
path = ["N", "S", "P", "R"]
for p in path:
    rs = random.sample(range(1, 101), 20)
    for r in rs:
        test =  f"test/{p}/{str(r * 2)}.jpg"
        train = f"train/{p}/{str(r * 2)}.jpg"
        os.rename(train, test)