# tests/basic-0.py
import asyncio
from pytest import fixture, mark
from solana.keypair import Keypair
from anchorpy import (
    create_workspace, close_workspace, Context, Program
)
from solana.system_program import SYS_PROGRAM_ID

# see more at
# https://kevinheavey.github.io/anchorpy/testing/

@fixture(scope="module")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@fixture(scope="module")
async def program() -> Program:
    workspace = create_workspace()
    yield workspace["anchor"]
    await close_workspace(workspace)

@fixture(scope="module")
async def initialized_account(program: Program) -> Keypair:
    counter = Keypair()
    await program.rpc["initialize"](
        ctx=Context(
            accounts={
                "counter": counter.public_key,
                "authority": program.provider.wallet.public_key,
                "system_program": SYS_PROGRAM_ID,
            },
            signers=[counter],
        ),
    )
    return counter


@mark.asyncio
async def test_is_initialized(
    program: Program, initialized_account: Keypair
) -> None:
    counter_account = await program.account["Counter"].fetch(initialized_account.public_key)
    assert counter_account.authority == program.provider.wallet.public_key
    assert counter_account.counter == 0


@mark.asyncio
async def test_increment(
    program: Program, initialized_account: Keypair
) -> None:
    await program.rpc["add_counter"](
        ctx=Context(
            accounts={
                "counter": initialized_account.public_key,
                "authority": program.provider.wallet.public_key
            }
        )
    )
    counter_account = await program.account["Counter"].fetch(initialized_account.public_key)
    assert counter_account.authority == program.provider.wallet.public_key
    assert counter_account.counter == 1