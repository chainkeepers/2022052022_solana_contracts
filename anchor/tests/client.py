import asyncio
import json
import logging

from anchorpy import Idl, Program, Wallet, Context, Provider
from argparse import ArgumentParser, Namespace
from pathlib import Path
from solana.keypair import Keypair
from solana.publickey import PublicKey
from solana.rpc.async_api import AsyncClient
from solana.rpc.commitment import Confirmed, Finalized
from solana.system_program import SYS_PROGRAM_ID
from solana.transaction import Transaction, TransactionSignature, TransactionInstruction
from typing import Union

logging.basicConfig(level=logging.INFO)

def get_args() -> Namespace:
    parser = ArgumentParser(description="PySerum API testing program")
    parser.add_argument(
        "-t",
        "--type",
        type=str.upper,
        default="SHOW",
        choices=["INIT", "ADD", "CLOSE", "SHOW"],
        help="What operation to execute",
    )
    parser.add_argument(
        "-c",
        "--counter-pubkey",
        type=str,
        help="Public key that will be used for counter",
    )
    return parser.parse_args()

def load_keypair(path: Union[str, Path]):
    if isinstance(path, str):
        path = Path(path)
    if not path.exists():
        raise Exception(f"Keypair file {path} does not exist")
    with path.open() as f:
        keypair_json = json.load(f)
        return Keypair.from_secret_key(bytes(keypair_json))

async def main():
    args = get_args()

    # Read Anchor IDL
    with Path("target/idl/anchor.json").open() as f:
        raw_idl = json.load(f)
    idl = Idl.from_json(raw_idl)

    # Address of the deployed program - where to call it
    program_id = PublicKey("ANVbZZvJUDY6Dy5mMYraY6uD6aUcmSrKNYCFxfUBheYK")

    # Read Solana Wallet
    keypair_path = Path.home().joinpath(".config/solana/id.json")
    keypair = load_keypair(keypair_path)

    # Solana wallet to sign the transaction
    # for default Solana keypair we can use call `Wallet.local()``
    wallet: Wallet = Wallet(keypair)
    # AnchorPy providers
    async_client = AsyncClient()
    anchorpy_provider = Provider(async_client, wallet)

    account_keypair = None
    if args.counter_pubkey:
        account_keypair = load_keypair(args.counter_pubkey)
    else:
        account_keypair = Keypair()
    logging.info(f"Counter account pubkey: {account_keypair.public_key}")

    # Generate the program client from IDL
    async with Program(idl, program_id, anchorpy_provider) as program:
        # Execute the RPC.
        logging.info(f"Running program {program_id}, authority: {program.provider.wallet.public_key}")

        if args.type == "INIT":
            txn_signature: TransactionSignature = await program.rpc["initialize"](
                ctx=Context(
                    # TODO: add 3 accounts
                ),
            )
            logging.info(f"Program {program_id}/initialize, txn {txn_signature} was run")

        elif args.type == "ADD":
            ix1: TransactionInstruction = program.instruction["set_counter"](
                # TODO: add parmeter and accounts
            )
            ix2: TransactionInstruction = program.instruction["add_counter"](
                ctx=Context(
                    accounts={
                        "counter": account_keypair.public_key,
                        "authority": program.provider.wallet.public_key,
                    },
                    signers=[],
                ),
            )
            txn = Transaction()
            txn.add(ix1)
            txn.add(ix2)
            txn_signature: TransactionSignature = await anchorpy_provider.send(txn)
            # logging.info(f"Transaction size: {len(txn.serialize())}")

        elif args.type == "CLOSE":
            txn_signature: TransactionSignature = await program.rpc["close"](
                ctx=Context(
                    accounts={
                        "counter": account_keypair.public_key,
                        "authority": program.provider.wallet.public_key,
                        "system_program": SYS_PROGRAM_ID,
                    },
                    signers=[],
                ),
            )
            logging.info(f"Program {program_id}/close, txn {txn_signature} was run")

        elif args.type == "SHOW":
            counter_account = await program.account["Counter"].fetch(
                account_keypair.public_key,
                # Confirmed,
                Finalized,
            )
            logging.info(f"{program_id}/show : {counter_account} ")

asyncio.run(main())