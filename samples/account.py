import click
from stellar_sdk import Keypair


STRENGTH = 256


@click.command(help="Generate an account from a random mnemonic phrase")
def gen_account():
    mnemonic = Keypair.generate_mnemonic_phrase(strength=STRENGTH)
    keypair = Keypair.from_mnemonic_phrase(mnemonic)

    click.echo(f"\nMnemonic phrase: '{mnemonic}'")
    click.echo(f"Private key: {keypair.secret}")
    click.echo(f"Account (pubkey): {keypair.public_key}")
    click.echo("Save your private key on a safe place!\n")

    click.confirm("Did you saved your private key?", default=False, abort=True)

    click.echo(f"Now you can send XLM to this address: {keypair.public_key}\n")
