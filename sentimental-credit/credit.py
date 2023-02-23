# TODO
import math 
from decimal import Decimal

number = int(input("Number: "))
l = len(str(number))
half = int(l / 2)
i = 0
j = 0
temp = int(number / 10)
product = 0
sum = 0
num = number

# Checksum
while (i < half):
    prod = int((int((temp % 10)) * 2))
    len_prod = len(str(prod))
    if (len_prod == 2):
        product += int(prod / 10)
        product += int(prod % 10)
    else:
        product += prod
    i += 1
    temp = int(temp / 100)

# Checksum
while (j <= half):
    su = int(num % 10)
    sum += su
    j += 1
    num = int(num / 100)

# Checksum's value
value = (product + sum)
# Checks for validity and react appropraitely
if (value % 10 == 0):
    firstDigs = int((number / int(math.pow(10, l - 2))))
    firstDig = int((number / int(math.pow(10, l - 1))))
    # Checks for American Express validity
    if ((firstDigs == 34 or firstDigs == 37) and l == 15):
        print("AMEX\n")
    # Checks for Mastercard validity
    elif ((firstDigs in range(51, 56)) and l == 16):
        print("MASTERCARD\n")
    # Checks for VISA validity
    elif ((firstDig == 4 and l == 13) or (firstDig == 4 and l == 16)):
        print("VISA\n")
    else:
        print("INVALID\n")
else:
    print("INVALID\n")