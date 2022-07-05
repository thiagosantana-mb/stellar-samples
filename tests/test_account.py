from click.testing import CliRunner

from stellar_samples import cmds


def test_gen_account():
    runner = CliRunner()
    result = runner.invoke(cmds, ["gen-account"], input="y\n")

    assert result.exit_code == 0
    assert "Mnemonic phrase: '" in result.stdout
    assert "Private key: " in result.stdout
    assert "Now you can send XLM to" in result.stdout


def test_gen_account_not_saved():
    runner = CliRunner()
    result = runner.invoke(cmds, ["gen-account"], input="n\n")

    assert result.exit_code == 1
    assert "Now you can send" not in result.stdout
