from Crypto.Hash import keccak  # pycryptodome


def to_checksum_address(address: str):
    address = address.lower()
    hash = '0x' + keccak.new(data=address[2:].encode(), digest_bits=256).hexdigest()
    return '0x' + ''.join(address[i].upper() if int(hash[i], 16) > 7 else address[i] for i in range(2, 42))
