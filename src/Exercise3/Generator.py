"""Generates Sha512 of a key made by Diffie-Hellman."""

import hashlib
import sys


def run():
    """Run main code."""
    if len(sys.argv[1:]) != 2:
        sys.exit("Bitte a und b, als Argumente angeben!")

    private_a = hex_string_to_int(sys.argv[1])
    private_b = hex_string_to_int(sys.argv[2])

    generator = 2
    prime_hex = ("FFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD1"
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
    prime = hex_string_to_int(prime_hex)

    public_a = pow(generator, private_a, prime)
    public_b = pow(generator, private_b, prime)
    print('A = {}'.format(int_to_hex_string(public_a)))
    print('B = {}'.format(int_to_hex_string(public_b)))

    secret_k = pow(public_b, private_a, prime)
    print('K = {}'.format(int_to_hex_string(secret_k)))

    hashed_k = hashlib.sha512(
        int_to_hex_string(secret_k).encode('utf-8')).hexdigest()
    print('H = {}'.format(hashed_k))


def int_to_hex_string(int_value):
    """Take an int and convert it to hexadecimal."""
    return '{0:02x}'.format(int_value)


def hex_string_to_int(hex_string):
    """Take an hexadecimal and convert it to int."""
    return int(hex_string, 16)


if __name__ == '__main__':
    run()
