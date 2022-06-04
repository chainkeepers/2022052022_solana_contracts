use anchor_lang::prelude::*;
use solana_program::system_program;

declare_id!("ANVbZZvJUDY6Dy5mMYraY6uD6aUcmSrKNYCFxfUBheYK");

#[program]
mod anchor {
    use super::*;

    pub fn initialize(ctx: Context<Initialize>) -> Result<()> {
        let counter_account = &mut ctx.accounts.counter;
        counter_account.authority = ctx.accounts.authority.key();
        counter_account.counter = 0;
        msg!("Initializing counter to 0 with authority {}", counter_account.authority);
        Ok(())
    }

    pub fn add_counter(ctx: Context<Increment>) -> Result<()> {
        let counter = &mut ctx.accounts.counter;
        counter.counter += 1;
        msg!("Increasing counter by one to {}", counter.counter);
        Ok(())
    }

    pub fn set_counter(ctx: Context<Increment>, new_counter: u64) -> Result<()> {
        let counter = &mut ctx.accounts.counter;
        msg!("Counter set from {} to new value {}", counter.counter, new_counter);
        counter.counter = new_counter;
        Ok(())
    }

    pub fn close(ctx: Context<Close>) -> Result<()> {
        let counter_account = &ctx.accounts.counter;
        msg!("Closing contract account {}", counter_account.key());
        Ok(())
    }
}

#[derive(Accounts)]
pub struct Initialize<'info> {
    #[account(init, payer = authority, space = 8 + 8 + 32)]
    pub counter: Account<'info, Counter>,
    #[account(mut)]
    pub authority: Signer<'info>,
    #[account(address = system_program::ID)]
    pub system_program: Program<'info, System>,
}

#[derive(Accounts)]
pub struct Increment<'info> {
    #[account(mut, has_one = authority)]
    pub counter: Account<'info, Counter>,
    pub authority: Signer<'info>,
}

#[derive(Accounts)]
pub struct Close<'info> {
    pub authority: Signer<'info>,
    #[account(mut, has_one = authority, close = authority)]
    pub counter: Account<'info, Counter>,
    #[account(address = system_program::ID)]
    pub system_program: Program<'info, System>,
}

#[account]
pub struct Counter {
    pub authority: Pubkey,
    pub counter: u64,
}
