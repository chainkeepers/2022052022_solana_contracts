from solana.publickey import PublicKey
from typing import List, Tuple

SEED = b"counter-contract"

def int_to_bytes(x: int) -> bytes:
    to_bytes_lenght = (x.bit_length() + 7) // 8
    if to_bytes_lenght == 0:
        to_bytes_lenght = 1  # we want the number 0 will be bytes of zeros
    return x.to_bytes(to_bytes_lenght, 'little')


def get_pda_address(
    seed: bytes,
    program_id: PublicKey,
    pda_public_key: PublicKey,
    *numbers: List[int],
) -> Tuple[PublicKey, int]:
    public_key_bytes = pda_public_key.__bytes__()
    bytes_numbers: List[bytes] = [int_to_bytes(number) for number in numbers]

    return PublicKey.find_program_address(
        [seed, public_key_bytes] + bytes_numbers,
        program_id,
    )