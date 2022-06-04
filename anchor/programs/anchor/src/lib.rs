use anchor_lang::prelude::*;

declare_id!("ANVbZZvJUDY6Dy5mMYraY6uD6aUcmSrKNYCFxfUBheYK");

#[program]
pub mod anchor {
    use super::*;

    pub fn initialize(ctx: Context<Initialize>) -> Result<()> {
        Ok(())
    }
}

#[derive(Accounts)]
pub struct Initialize {}
