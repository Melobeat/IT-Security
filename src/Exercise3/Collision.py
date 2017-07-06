"""Find hashcollisions for Diffie-Hellman."""
import sys
import hashlib
import time


class Alice:
    """Information of Alice."""

    def __init__(self, public_key, prime):
        """Init for Alice."""
        self.name = "Alice"
        self.public_key = public_key
        self.hashes = {}
        self.public_mod = self.public_key % prime
        self.actual_private_key = 1

    def add_entry(self, hashed_k, private_key):
        """Add entry to hashtable."""
        self.hashes[hashed_k] = private_key

    def clear_dict(self):
        """Clear hashtable."""
        self.hashes.clear()


class Bob:
    """Information of Bob."""

    def __init__(self, public_key, prime):
        """Init for Bob."""
        self.name = "Bob"
        self.public_key = public_key
        self.hashes = {}
        self.public_mod = self.public_key % prime
        self.actual_private_key = 1

    def add_entry(self, hashed_k, private_key):
        """Add entry to hashtable."""
        self.hashes[hashed_k] = private_key

    def clear_dict(self):
        """Clear hashtable."""
        self.hashes.clear()


def run():
    """Run main code."""
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

    if len(sys.argv[1:]) < 2:
        sys.exit("Bitte A und B, als Argumente angeben!\n"
                 "Optional als drittes Argument: Länge der Kollision.")

    alice = Alice(hex_string_to_int(sys.argv[1]), prime)
    bob = Bob(hex_string_to_int(sys.argv[2]), prime)

    if len(sys.argv[1:]) == 3:
        n_collisions = int(sys.argv[3])
    else:
        n_collisions = 12

    start_time = time.time()
    collision = find_collision(n_collisions, alice, bob, prime)
    print("----------------------")
    print('{} byte collision.'.format(n_collisions))
    print('Private key a: {}, Private key b: {}'.format(
        collision[0], collision[1]))
    print('Time needed: {}'.format(time.time() - start_time))
    print('Size of hash tables: a({}) b({})'.format(
        len(alice.hashes), len(bob.hashes)))
    print("----------------------")
    alice.clear_dict()
    bob.clear_dict()


def find_collision(n_collisions, alice, bob, prime):
    """Search for a hashcollision of length n_collisions."""
    for i in range(1, prime):
        private_key = i
        hash_alice = calculate_hash(alice, prime)[0:n_collisions]
        hash_bob = calculate_hash(bob, prime)[0:n_collisions]
        if hash_alice in bob.hashes:
            return [
                int_to_hex_string(private_key),
                int_to_hex_string(bob.hashes[hash_alice])
            ]
        else:
            alice.add_entry(hash_alice, private_key)
        if hash_bob in alice.hashes:
            return [
                int_to_hex_string(alice.hashes[hash_bob]),
                int_to_hex_string(private_key)
            ]
        else:
            bob.add_entry(hash_bob, private_key)


def calculate_hash(person, prime):
    """Calculate hash and secret K."""
    secret_k = (person.actual_private_key * person.public_mod) % prime
    person.actual_private_key = secret_k

    return hashlib.sha512(
        int_to_hex_string(secret_k).encode('utf-8')).hexdigest()


def int_to_hex_string(int_value):
    """Convert int to hex string."""
    return '{0:02x}'.format(int_value)


def hex_string_to_int(hex_string):
    """Convert hex string to int."""
    return int(hex_string, 16)


if __name__ == '__main__':
    run()
