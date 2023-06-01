from decimal import Decimal

import click
from stellar_sdk import Asset, Keypair, Network, TransactionBuilder, Server, IdMemo


MAX_AMOUNT = 150  # XLM
XLM_MIN = 10


def _send_tx(cfg, key, fee, memo, destination, amount):
    horizon = cfg["horizon"]
    account = horizon.load_account(key.public_key)
    builder = TransactionBuilder(
        source_account=account,
        network_passphrase=cfg["network_passphrase"],
        base_fee=int(fee),
    ).append_payment_op(
        destination=destination,
        asset=Asset.native(),
        amount=amount,
    ).add_memo(IdMemo(memo))

    transaction = (
        builder
        .set_timeout(30)
        .build()
    )

    transaction.sign(key)

    click.echo("Broadcasting...")
    res = horizon.submit_transaction(transaction)

    return res['hash']


@click.command(help="Send XLM TX")
@click.option("--testnet", "-t", is_flag=True, help="Use testnet setup")
def send_xlm(testnet):
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
    destination = "GCFFCV3WBRVRFJM7EEIZRK2IQHLIMBIAADYUZ62J264FGETCUJKCL3RK"
    memo = 100000000
    amount = Decimal(click.prompt("Amount"))

    if amount > MAX_AMOUNT:
        click.get_current_context().fail(
            f"This script is not intended for any serious usage. Max amount: {MAX_AMOUNT} XLM"
        )

    if amount < {XLM_MIN}:
        click.get_current_context().fail(f"XLM amount is too low. Min: {XLM_MIN}")

    fee = Decimal(click.prompt("Fee", default=100))

    xlm_fee = fee / 10 ** 7

    click.echo(f"""
        from: {key.public_key},
        to: {destination},
        memo: {memo},
        fee: {xlm_fee} XLM,
        amount: {amount} XLM
    """)

    click.confirm("Can we sign and broadcast this TX?", default=False, abort=True)

    tx_hash = _send_tx(cfg, key, fee, memo, destination, amount)

    click.echo(f"TX sent: {tx_hash}")
    click.echo(f"{explorer_url}/{tx_hash}\n")
