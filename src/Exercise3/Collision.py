""" Find a hash collision of length n for Diffie-Hellman MITM-Attack """

import sys
import hashlib
import time


class Parameters:
    """ Class """

    def __init__(self, public_a, public_b):
        self.public_a = public_a
        self.public_b = public_b
        self.generator = 2
        self.prime_hex = ("FFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD1"
                          "29024E088A67CC74020BBEA63B139B22514A08798E3404DD"
                          "EF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245"
                          "E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7ED"
                          "EE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3D"
                          "C2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F"
                          "83655D23DCA3AD961C62F356208552BB9ED529077096966D"
                          "670C354E4ABC9804F1746C08CA18217C32905E462E36CE3B"
                          "E39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9"
                          "DE2BCBF6955817183995497CEA956AE515D2261898FA0510"
                          "15728E5A8AACAA68FFFFFFFFFFFFFFFF")
        self.prime = hex_string_to_int(self.prime_hex)
        self.hashes_a = {}
        self.hashes_b = {}

    def add_entry_a(self, hash_a, private_a):
        """ Adds entry to hashes_a """
        self.hashes_a[hash_a] = private_a

    def add_entry_b(self, hash_b, private_b):
        """ Adds entry to hashes_b """
        self.hashes_b[hash_b] = private_b

    def clear_dicts(self):
        """ Clears hashes_a and hashes_b"""
        self.hashes_a.clear()
        self.hashes_b.clear()


def run():
    """ Main function """
    if len(sys.argv[1:]) != 2:
        sys.exit("Bitte A und B, als Argumente angeben!")

    public_a = hex_string_to_int(sys.argv[1])
    public_b = hex_string_to_int(sys.argv[2])

    params = Parameters(public_a, public_b)

    n_collisions = 6
    start_time = time.time()
    print(find_collision(n_collisions, params))
    print(time.time() - start_time)


def find_collision(n_collisions, params):
    """ Calculates hashes and compares them """
    for i in range(1, 2**24):
        private_a = i
        private_b = i
        hash_a = calculate_hash(params.public_b,
                                private_a, params.prime)[0:n_collisions]
        hash_b = calculate_hash(params.public_a,
                                private_b, params.prime)[0:n_collisions]
        if hash_a in params.hashes_b:
            return [int_to_hex_string(private_a),
                    int_to_hex_string(
                        params.hashes_b[hash_a])]
        else:
            params.add_entry_a(hash_a, private_a)
        if hash_b in params.hashes_a:
            return [int_to_hex_string(
                params.hashes_a[hash_b]),
                    int_to_hex_string(private_b)]
        else:
            params.add_entry_b(hash_b, private_b)


def calculate_hash(public_key, private_key, prime):
    """ Calculates Sha512 """
    secret_k = pow(public_key, private_key, prime)
    return hashlib.sha512(int_to_hex_string(
        secret_k).encode('utf-8')).hexdigest()


def int_to_hex_string(int_value):
    """ Takes an int and converts it to hexadecimal """
    return '{0:02x}'.format(int_value)


def hex_string_to_int(hex_string):
    """ Takes an hexadecimal and converts it to int """
    return int(hex_string, 16)


if __name__ == '__main__':
    run()
