import binascii
import sys


def split_file(file_path, num_bits=16):
    #Read file contents into memory
    with open(file_path, 'r') as f:
        file_contents = f.read()
    #Turn it into a binary string
    bin_string = bin(int(binascii.hexlify(file_contents), 16)).replace('0b', '')
    #Split the string into % numbits pieces as an array
    bin_strings = [bin_string[x:x+num_bits] for x in range(0, len(bin_string), num_bits)]
    special_num=0
    #Find out how many zeros are on the last number in the array, its a special case
    for x in range(0,len(bin_strings[-1])):
        if(bin_strings[-1][x]=='0'):
            special_num+=1
        else:
            break
    secret_numbers = [int(x, 2) for x in bin_strings]
    secret_numbers.append(special_num)
    return secret_numbers


def get_file(secret_numbers, num_bits=16):
    special_num = secret_numbers[-1]
    bin_strings = []
    for x in range(0,len(secret_numbers)-1):
        bin_strings.append(bin(secret_numbers[x]).replace("0b",""))
    bin_string = ''
    zeroString=""
    for i in range(int(special_num)):
        zeroString+= "0" 
    bin_strings[-1] = zeroString + bin_strings[-1]
    count=0
    for binary in bin_strings:
        if(len(binary)<16 and count!=len(bin_strings)-1):
            x = 16-len(binary)
            for y in range(0,x):
                binary = "0" + str(binary)
            bin_strings[count] = binary
        bin_string += str(binary)
        count+=1

    n = int('0b' + bin_string, 2)
    file_contents = binascii.unhexlify('%x' % n)
    print(file_contents)
    with open("data/test.txt", 'w') as f:
        f.write(file_contents)

if __name__ == '__main__':
    file_name = sys.argv[1]
    split = split_file(file_name)
    get_file(split)