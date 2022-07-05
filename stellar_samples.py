import click

from samples.account import gen_account
from samples.cross_asset_xlm_usdc import send_cross_asset


VERSION = "0.0.1"


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.version_option(version=VERSION)
def cmds():
    pass


cmds.add_command(gen_account)
cmds.add_command(send_cross_asset)


if __name__ == '__main__':
    cmds()
