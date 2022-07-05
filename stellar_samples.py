import click

from samples.account import gen_account
from samples.cross_asset_xlm_usdc import send_cross_asset
from samples.send_usdc import send_usdc
from samples.change_trust import change_trust_usdc


VERSION = "0.0.2"


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.version_option(version=VERSION)
def cmds():
    pass


cmds.add_command(gen_account)
cmds.add_command(send_cross_asset)
cmds.add_command(send_usdc)
cmds.add_command(change_trust_usdc)


if __name__ == '__main__':
    cmds()
