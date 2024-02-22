from Crypto.Hash import keccak  # pycryptodome


def keccak256(data: bytes, /) -> str:
    """
    :param data:
    :return: '0x' + keccak256.hexdigest().
    """
    return '0x' + keccak.new(data=data, digest_bits=256).hexdigest()


def to_checksum_address(address: str):
    address = address.lower()
    hash = keccak256(address[2:].encode())
    return '0x' + ''.join(address[i].upper() if int(hash[i], 16) > 7 else address[i] for i in range(2, 42))
