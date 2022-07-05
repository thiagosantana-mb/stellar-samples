from click.testing import CliRunner

from stellar_samples import cmds


def test_root():
    """
    Usage: stellar_samples.py [OPTIONS] COMMAND [ARGS]...

    Options:
      --version   Show the version and exit.
      -h, --help  Show this message and exit.

    Commands:
      gen-account  Generate an account from a random mnemonic phrase
    """

    runner = CliRunner()
    result = runner.invoke(cmds, [])

    assert result.exit_code == 0
    assert "gen-account" in result.stdout


def test_subcmd_help():
    runner = CliRunner()
    result = runner.invoke(cmds, ["gen-account", "--help"])

    assert result.exit_code == 0
    assert "gen-account" in result.stdout


def test_version():
    from stellar_samples import VERSION

    runner = CliRunner()
    result = runner.invoke(cmds, ["--version"])

    assert result.exit_code == 0
    assert f"version {VERSION}" in result.stdout
