# Homework 3

蘇泓叡 C112156233

1. (20 credits) Assume that the number of hosts connected to the Internet at year 2025 is five hundred million. If the number of hosts increases only 20 per cent per year, what is the number of hosts in year 2035?

$$500,000,000 \times (1 + 0.2) ^ {10}$$ 

2. (20 credits) Assume a system uses five protocol layers. If the application program creates a message of 100 bytes and each layer (including the fifth and the first) adds a header of ten bytes to the data unit, what is the efficiency (the ratio of application-layer bytes to the number of bytes transmitted) of the system?

$$
\frac{100}{100 + 10 \times 4} = \frac{100}{140} = \frac{5}{7}
$$

3. (30 credits) Match the following to one or more layers of the TCP/IP protocol suite

 - 1. route determination
    - Network Layer
 - 2. connection to transmission media
    - Link Layer
 - 3. providing services for the end user
    - Application Layer
 - 4. creating user datagrams
    - Transport Layer
 - 5. responsibility for handling frames between adjacent nodes
    - Link Layer
 - 6. transforming bits to electromagnetic signals
    - Physical Layer

4. (15 credits) A device is sending out data at the rate of 100 bps

 - 1. How long does it take to send out 100 bits?
    $$\frac{100\text{bit}}{100\text{bps}} = 1 \text{ second}$$
 - 2. How long does it take to send out two characters (assume 8 bits per character)?
    $$\frac{2 \times 8\text{bit}}{100\text{bps}} = 0.16 \text{ second}$$
 - 3. How long does it take to send a file of 100,000 characters?
    $$\frac{100,000 \times 8\text{bit}}{100\text{bps}} = 8,000 \text{ seconds}$$
5. (15 credits) Find out what applications are the following port numbers for?

 - 1. 80
    - HTTP
 - 2. 443
    - HTTPS
 - 3. 3389
    - Remote Desktop Protocol
