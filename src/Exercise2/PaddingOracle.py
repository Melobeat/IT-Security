import urllib.parse
import base64
import array
import http.client
import random


def run():
    url_query = "NkivYeRHPWegVIG%2FgiptBChbA8%2BZtjWslmOGB58oathyv1U13KIYy4kVC3Wuq4LcahaFL8lrxTl76VU921AVJw%3D%3D"
    block_size = 16
    ciphertext = decode(url_query)
    cipher_blocks = split_list(ciphertext, block_size)
    plain_blocks = list(cipher_blocks)

    connection = http.client.HTTPConnection("gruenau4.informatik.hu-berlin.de", 8888)

    for l in reversed(range(1, len(cipher_blocks))):
        print("{} {} {}".format("+++++++++++++++++++++ Block:", l + 1, "+++++++++++++++++++++"))
        c1 = cipher_blocks[l - 1]
        c2 = cipher_blocks[l]
        i2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        p2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        c1_mod = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        padding_length = 1

        for i in reversed(range(0, block_size)):
            print("{} {} {}".format("--------------------- Position:", i + 1, "---------------------"))
            for j in range(0, i + 1):
                c1_mod[j] = random.randint(0, 255)
            c1_mod = search_r(c1_mod, c2, i, connection)
            print("{}: {}".format("C1'", c1_mod))
            i2[i] = c1_mod[i] ^ padding_length
            print("{}: {}".format("I2'", i2))
            p2[i] = c1[i] ^ i2[i]
            print("{}: {}".format("P2", p2))
            padding_length += 1
            for j in reversed(range(block_size - (padding_length - 1), block_size)):
                c1_mod[j] = padding_length ^ i2[j]

        plain_blocks[l] = p2

    connection.close()
    plaintext = concat_list(plain_blocks[1:])
    print("{}: {}".format("Plaintext", array.array('B', plaintext).tostring()))


def decode(url_query):
    decoded_url = urllib.parse.unquote(url_query)
    return list(base64.b64decode(decoded_url))


def encode(ciphertext):
    as_string = array.array('B', ciphertext).tostring()
    encoded_base64 = base64.b64encode(as_string)
    encoded_url = urllib.parse.quote(encoded_base64, safe='')
    return encoded_url


def split_list(ls, chunk_size):
    return [ls[i:i + chunk_size] for i in range(0, len(ls), chunk_size)]


def concat_list(ls):
    concat_ls = []
    for item in ls:
        concat_ls += item
    return concat_ls


def search_r(c1_mod, c2, position, connection):
    c1_mod[position] = 0
    for i in range(1, 256):
        oracle_request = concat_list([c1_mod, c2])
        if send_request(encode(oracle_request), connection) == 200:
            break

        else:
            c1_mod[position] = 0 ^ i
    return c1_mod


def send_request(query, connection):
    connection.request("GET", "/store_secret/?secret=" + query)
    response = connection.getresponse()
    status = response.status
    response.read()
    return status


if __name__ == "__main__":
    run()
