import sys
import hashlib
import time


class Parameters:
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
        self.a_mod = self.public_a % self.prime
        self.b_mod = self.public_b % self.prime
        self.a_mod_actual = 1
        self.b_mod_actual = 1

    def add_entry_a(self, hash_a, private_a):
        self.hashes_a[hash_a] = private_a

    def add_entry_b(self, hash_b, private_b):
        self.hashes_b[hash_b] = private_b

    def clear_dicts(self):
        self.hashes_a.clear()
        self.hashes_b.clear()


def run():
    if len(sys.argv[1:]) < 2:
        sys.exit("Bitte A und B, als Argumente angeben! Optional als drittes Argument: Länge der Kollision.")

    public_a = hex_string_to_int(sys.argv[1])
    public_b = hex_string_to_int(sys.argv[2])

    params = Parameters(public_a, public_b)

    if len(sys.argv[1:]) == 3:
        n_collisions = int(sys.argv[3])
    else:
        n_collisions = 12

    params.clear_dicts()
    start_time = time.time()
    collision = find_collision(n_collisions, params)
    print('{} byte collision.'.format(n_collisions))
    print('Private key a: {}, Private key b: {}'.format(collision[0], collision[1]))
    print('Time needed: {}'.format(time.time() - start_time))
    print('Size of hash tables: a({}) b({})'.format(len(params.hashes_a), len(params.hashes_b)))
    print("----------------------")


def find_collision(n_collisions, params):
    for i in range(1, params.prime):
        private_a = i
        private_b = i
        hash_a = calculate_hash(params, 0)[0:n_collisions]
        hash_b = calculate_hash(params, 1)[0:n_collisions]
        if hash_a in params.hashes_b:
            return [int_to_hex_string(private_a), int_to_hex_string(params.hashes_b[hash_a])]
        else:
            params.add_entry_a(hash_a, private_a)
        if hash_b in params.hashes_a:
            return [int_to_hex_string(params.hashes_a[hash_b]), int_to_hex_string(private_b)]
        else:
            params.add_entry_b(hash_b, private_b)


def calculate_hash(params, witch):
    if witch == 0:
        secret_k = (params.a_mod_actual * params.a_mod) % params.prime
        params.a_mod_actual = secret_k
    else:
        secret_k = (params.b_mod_actual * params.b_mod) % params.prime
        params.b_mod_actual = secret_k

    return hashlib.sha512(int_to_hex_string(secret_k).encode('utf-8')).hexdigest()


def int_to_hex_string(int_value):
    return '{0:02x}'.format(int_value)


def hex_string_to_int(hex_string):
    return int(hex_string, 16)


if __name__ == '__main__':
    run()
