use anchor_lang::prelude::*;
use solana_program::system_program;

declare_id!("ANVbZZvJUDY6Dy5mMYraY6uD6aUcmSrKNYCFxfUBheYK");

#[program]
mod anchor {
    use super::*;

    pub fn initialize(ctx: Context<Initialize>) -> Result<()> {
        // TODO: initialize values
        // TODO: msg!
        Ok(())
    }
    
    // add_account, set_account

    pub fn close(ctx: Context<Close>) -> Result<()> {
        let counter_account = &ctx.accounts.counter;
        msg!("Closing contract account {}", counter_account.key());
        Ok(())
    }
}

#[derive(Accounts)]
pub struct Initialize<'info> {
    // TODO: init
    pub counter: Account<'info, Counter>,
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
    // authority Pubkey, counter u32
}
