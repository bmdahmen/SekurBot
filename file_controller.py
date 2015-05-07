import binascii
import sys


def split_file(file_path, num_bits=16):

    #Read file contents into memory
    with open(file_path, 'r') as f:
        file_contents = f.read()

    print(file_contents)

    print("-------------------------")

    #bin_string = ''.join(format(ord(x), 'b') for x in file_contents)
    bin_string = bin(int(binascii.hexlify(file_contents), 16)).replace('0b', '')
    print("Binary String:")
    print(bin_string)

    print("---------------------------")

    bin_strings = [bin_string[x:x+num_bits] for x in range(0, len(bin_string), num_bits)]

    special_num = num_bits - len(bin_strings[-1])

    print("Binary Splits:")
    print(str(bin_strings))

    print("------------------------")

    secret_numbers = [int(x, 2) for x in bin_strings]
    secret_numbers.append(special_num)
    print("Secret Numbers:")
    print(str(secret_numbers))

    return secret_numbers


def get_file(secret_numbers, num_bits=16):
    bin_strings = [bin(x).replace('0b', '') for x in secret_numbers]
    special_num = bin_strings[-1]
    bin_strings = bin_strings[:-1]

    print(bin(13106))

    bin_string = ''
    counter = 0
    bin_strings[-1] = '0' + str(bin_strings[-1])
    for binary in bin_strings:
        bin_val = binary.replace('0b', '')
        #print(bin_val)

        if counter < len(bin_strings) - 1:
            for x in range(0, num_bits-len(bin_val)):
                bin_val = '0' + bin_val
        else:
            for x in range(int(special_num) - 1):
                bin_val = '0' + bin_val

        print(bin_val)
        counter += 1

        bin_string += bin_val

    print("Binary Splits (Back):")
    print(str(bin_strings))


    print("---------------------")

    print("Binary String (Back):")
    print(str(bin_string))

    print("-----------------------")

    print("File Text:")
    n = int('0b' + bin_string, 2)

    file_contents = binascii.unhexlify('%x' % n)
    print(file_contents)
    #print(''.join(chr(int(bin_string[i:i+8], 2)) for i in range(0, len(bin_string), 8)))

    with open("data/test.txt", 'w') as f:
        f.write(file_contents)

if __name__ == '__main__':
    file_name = sys.argv[1]
    split = split_file(file_name)
    print("------------------------")

    print(str(split))

    get_file(split)