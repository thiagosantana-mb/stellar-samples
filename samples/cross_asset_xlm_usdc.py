from decimal import Decimal

import click
from stellar_sdk import Asset, Keypair, Network, TransactionBuilder, Server, IdMemo


MAX_AMOUNT = 500  # XLM
USDC_MIN = 1


def send_tx(cfg, key, fee, memo, destination, xlm_amount, usdc_amount):
    horizon = cfg["horizon"]
    account = horizon.load_account(key.public_key)
    usdc = Asset("USDC", cfg["issuer"])

    transaction = (
        TransactionBuilder(
            source_account=account,
            network_passphrase=cfg["network_passphrase"],
            base_fee=int(fee),
        )
        .add_memo(IdMemo(memo))
        .append_path_payment_strict_send_op(
            destination=destination,
            send_asset=Asset.native(),
            send_amount=str(xlm_amount),
            dest_asset=usdc,
            dest_min=str(usdc_amount),
            path=[Asset.native(), usdc],
        )
        .set_timeout(30)
        .build()
    )

    transaction.sign(key)

    click.echo("Broadcasting...")
    res = horizon.submit_transaction(transaction)

    return res['hash']


@click.command(help="Send cross-asset XLM/USDC")
@click.option("--testnet", "-t", is_flag=True, help="Use testnet setup")
def send_cross_asset(testnet):
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
    destination = click.prompt("Destination account")
    memo = int(click.prompt("Memo"))
    click.echo("See XLM/USDC prices")
    click.echo("https://stellar.expert/explorer/public/asset/"
               "USDC-GA5ZSEJYB37JRC5AVCIA5MOP4RHTM335X2KGX3IHOJAPP5RE34K4KZVN?filter=markets")
    xlm_amount = Decimal(click.prompt("XLM Amount"))

    if xlm_amount > MAX_AMOUNT:
        click.get_current_context().fail(
            f"This script is not intended for any serious usage. Max amount: {MAX_AMOUNT} XLM"
        )

    usdc_amount = Decimal(click.prompt("USDC Min Amount"))

    if usdc_amount < USDC_MIN:
        click.get_current_context().fail(f"USDC amount is too low. Min: {USDC_MIN}")

    fee = Decimal(click.prompt("Fee", default=100))



    xlm_fee = fee / 10 ** 7

    click.echo(f"""
        USDC issuer: {cfg['issuer']},
        from: {key.public_key},
        to: {destination},
        fee: {xlm_fee} XLM,
        amount: {xlm_amount} XLM,
        min amount: {usdc_amount} USDC
    """)

    click.confirm("Can we sign and broadcast this TX?", default=False, abort=True)

    tx_hash = send_tx(cfg, key, fee, memo, destination, xlm_amount, usdc_amount)

    click.echo(f"TX sent: {tx_hash}")
    click.echo(f"{explorer_url}/{tx_hash}\n")
