import os
import aes
import argparse
import sys

def createParser ():
    parser = argparse.ArgumentParser()
    parser.add_argument ('-e', '--filenameToEncode', nargs='+')
    parser.add_argument ('-d', '--filenameToDecode', nargs='+')
    requiredNamed = parser.add_argument_group('required named arguments')
    requiredNamed.add_argument('-k', '--key', help='Input key', required=True)
    return parser


if __name__ == '__main__':
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])

    key = namespace.key
    if len(key) < 16:
        print("Key must be 128 bit")
        exit()
    else:
        key = key[:16]

    way = 'e'
    if (namespace.filenameToDecode is not None):
        filename = namespace.filenameToDecode[0]
        way = 'd'
    elif (namespace.filenameToEncode is not None):
        filename = namespace.filenameToEncode[0]

    input_path = os.path.abspath(filename)

    if not os.path.isfile(input_path):
        print('This is not a file!')
        exit()

    with open(input_path, 'rb') as f:
        data = f.read()

    if way == 'e':
        crypted_data = []
        temp = []
        for byte in data:
            temp.append(byte)
            if len(temp) == 16:
                crypted_part = aes.encrypt(temp, key)
                crypted_data.extend(crypted_part)
                del temp[:]

        if 0 < len(temp) < 16:
            empty_spaces = 16 - len(temp)
            for i in range(empty_spaces - 1):
                temp.append(0)
            temp.append(0)
            crypted_part = aes.encrypt(temp, key)
            crypted_data.extend(crypted_part)

        out_path = os.path.join(os.path.dirname(input_path) , 'enc_' + os.path.basename(input_path))

        with open(out_path, 'xb') as ff:
            ff.write(bytes(crypted_data))

    if way == 'd':
        decrypted_data = []
        temp = []
        for byte in data:
            temp.append(byte)
            if len(temp) == 16:
                decrypted_part = aes.decrypt(temp, key)
                decrypted_data.extend(decrypted_part)
                del temp[:]

        if 0 < len(temp) < 16:
            t = len(temp)
            empty_spaces = 16 - len(temp)
            for i in range(empty_spaces - 1):
                temp.append(0)
            temp.append(0)
            decrypted_part = aes.decrypt(temp, key)
            decrypted_data.extend(decrypted_part)

        out_path = os.path.join(os.path.dirname(input_path) , 'dec_' + os.path.basename(input_path))

        i = -1
        while i > -len(decrypted_data) and decrypted_data[i] == 0:
            i -= 1

        with open(out_path, 'xb') as ff:
            ff.write(bytes(decrypted_data[:i]))

    print('New file here:', out_path)