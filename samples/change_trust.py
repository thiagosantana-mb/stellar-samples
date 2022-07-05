from decimal import Decimal

import click
from stellar_sdk import Asset, Keypair, Network, TransactionBuilder, Server


def _send_tx(cfg, key, fee):
    horizon = cfg["horizon"]
    account = horizon.load_account(key.public_key)
    usdc = Asset("USDC", cfg["issuer"])

    transaction = (
        TransactionBuilder(
            source_account=account,
            network_passphrase=cfg["network_passphrase"],
            base_fee=int(fee),
        )
        .append_change_trust_op(
            asset=usdc,
            # limit="0"  # revoke trust line
        )
        .set_timeout(30)
        .build()
    )

    transaction.sign(key)

    click.echo("Broadcasting...")
    res = horizon.submit_transaction(transaction)

    return res['hash']


@click.command(help="Change Trust USDC")
@click.option("--testnet", "-t", is_flag=True, help="Use testnet setup")
def change_trust_usdc(testnet):
    if testnet:
        cfg = {
            "issuer": "GBBD47IF6LWK7P7MDEVSCWR7DPUWV3NY3DTQEVFL4NAT4AQH3ZLLFLA5",
            "horizon": Server(horizon_url="https://horizon-testnet.stellar.org"),
            "network_passphrase": Network.TESTNET_NETWORK_PASSPHRASE,
        }
        explorer_url = "https://stellar.expert/explorer/testnet/tx"
    else:
        cfg = {
            "issuer": "GA5ZSEJYB37JRC5AVCIA5MOP4RHTM335X2KGX3IHOJAPP5RE34K4KZVN",
            "horizon": Server(horizon_url="https://horizon.stellar.org"),
            "network_passphrase": Network.PUBLIC_NETWORK_PASSPHRASE,
        }
        explorer_url = "https://stellar.expert/explorer/public/tx"

    secret = click.prompt("\nPaste your private key", hide_input=True)
    key = Keypair.from_secret(secret)

    click.echo(f"Account: {key.public_key}")
    fee = Decimal(click.prompt("Fee", default=100))

    xlm_fee = fee / 10 ** 7

    click.echo(f"""
        USDC issuer: {cfg['issuer']},
        from: {key.public_key},
        fee: {xlm_fee} XLM,
    """)

    click.confirm("Can we sign and broadcast this TX?", default=False, abort=True)

    tx_hash = _send_tx(cfg, key, fee)

    click.echo(f"TX sent: {tx_hash}")
    click.echo(f"{explorer_url}/{tx_hash}\n")
