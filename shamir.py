from random import randint

sharedPrime = 257
def splitSecret(inputNumber, splitParts, needed):
    #Generate the needed-1 coefficients
    coefs = (inputNumber,)
    for i in range(1,needed):
        randomNum = randint(0,sharedPrime-1)
        coefs = coefs + (randomNum,)
    shares = []
    for i in range(1,splitParts+1):
        accum = coefs[0]
        for exp in range(1,needed):
            accum = (accum + (coefs[exp] * ((i**exp) % sharedPrime) %sharedPrime)) % sharedPrime
        shares.append((i,accum))
    return shares


def gcd(a,b):
    if b==0:
        return (a,1,0)
    else:
        n = a/b
        c = a % b
        r = gcd(b,c)
        return (r[0],r[2],r[1]-r[2]*n)

def modInverse(k):
    k = k % sharedPrime
    if(k<0):
        r = - (gcd(sharedPrime,-k)[2])
    else:
        r = gcd(sharedPrime,k)[2]
    return (sharedPrime + r) % sharedPrime


def joinSecret(shares):
    accum=0
    for formula in range(0,len(shares)):
        #La-Grange Interpolation - See 357, or don't. probably don't
        numerator,denominator= 1,1
        for count in range(0, len(shares)):
            if(formula==count):
                continue
            startposition = shares[formula][0]
            nextposition = shares[count][0]
            numerator = (numerator * -nextposition)%sharedPrime
            denominator = (denominator * (startposition - nextposition))%sharedPrime
        
        value = shares[formula][1]
        accum = (sharedPrime + accum + (value * numerator * modInverse(denominator))) % sharedPrime
    return accum

# split the number 169 into 6 parts such that we only need 4 to reconstruct
shares = splitSecret(169,6,4)
print(shares)
secret = joinSecret(shares[:4])
print(secret)
