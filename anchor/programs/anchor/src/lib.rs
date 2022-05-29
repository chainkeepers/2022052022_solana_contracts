use anchor_lang::prelude::*;
use solana_program::system_program;

declare_id!("52nm5mLXp6rEu5Qr27Y3u2ycveB43eGkRxABiiMQcrbE");

const SEED_PHRASE: &[u8; 16] = b"counter-contract";

#[program]
mod anchor {
    use super::*;

    pub fn initialize(ctx: Context<Initialize>, pda_index: u8) -> Result<()> {
        let counter_account = &mut ctx.accounts.pda_counter_account;
        counter_account.authority = ctx.accounts.authority.key();
        counter_account.counter = 0;
        counter_account.pda_index = pda_index;
        counter_account.bump = *ctx.bumps.get("pda_counter_account").unwrap();
        msg!("Initializing counter to 0 with authority: {}, pda_index: {}",
            counter_account.authority, counter_account.pda_index);
        Ok(())
    }

    pub fn add_counter(ctx: Context<Increment>) -> Result<()> {
        let counter = &mut ctx.accounts.pda_counter_account;
        counter.counter += 1;
        msg!("Increasing counter by one to {}", counter.counter);
        Ok(())
    }

    pub fn set_counter(ctx: Context<Increment>, new_counter: u64) -> Result<()> {
        let counter = &mut ctx.accounts.pda_counter_account;
        msg!("Counter set from {} to new value {}", counter.counter, new_counter);
        counter.counter = new_counter;
        Ok(())
    }

    pub fn close(ctx: Context<Close>) -> Result<()> {
        let counter_account = &ctx.accounts.pda_counter_account;
        msg!("Closing contract account {}", counter_account.key());
        Ok(())
    }
}

#[derive(Accounts)]
#[instruction(pda_index: u8)]
pub struct Initialize<'info> {
    #[account(
        init,
        payer = authority,
        space = 8 + 32 + 1 + 1 + 8,
        seeds = [
            SEED_PHRASE,
            authority.key().as_ref(),
            [pda_index].as_ref()
        ],
        bump
    )]
    pub pda_counter_account: Account<'info, Counter>,
    #[account(mut)]
    pub authority: Signer<'info>,
    #[account(address = system_program::ID)]
    pub system_program: Program<'info, System>,
}

#[derive(Accounts)]
pub struct Increment<'info> {
    pub authority: Signer<'info>,
    #[account(mut, has_one = authority)]
    pub pda_counter_account: Account<'info, Counter>,
}

#[derive(Accounts)]
pub struct Close<'info> {
    pub authority: Signer<'info>,
    #[account(mut, has_one = authority, close = authority)]
    pub pda_counter_account: Account<'info, Counter>,
    #[account(address = system_program::ID)]
    pub system_program: Program<'info, System>,
}

#[account]
pub struct Counter {
    pub authority: Pubkey,
    pub bump: u8,
    pub pda_index: u8,
    pub counter: u64,
}
