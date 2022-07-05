from click.testing import CliRunner
from stellar_sdk import Keypair

from stellar_samples import cmds


def test_change_trust_usdc(requests_mock):
    key = Keypair.random()
    requests_mock.get(f"https://horizon.stellar.org/accounts/{key.public_key}", json={"sequence": 1})
    requests_mock.post("https://horizon.stellar.org/transactions", json={"hash": "myhash"})
    runner = CliRunner()
    inputs = [key.secret, "", "y"]
    result = runner.invoke(cmds, ["change-trust-usdc"], input="\n".join(inputs))

    assert result.exit_code == 0
    assert "https://stellar.expert/explorer/public/tx/myhash" in result.stdout


def test_change_trust_usdc_invalid_key():
    runner = CliRunner()
    inputs = ["whatever", "", "y"]
    result = runner.invoke(cmds, ["change-trust-usdc"], input="\n".join(inputs))

    assert result.exit_code == 1
    assert "Invalid Ed25519 Secret Seed" in str(result.exception)


def test_change_trust_usdc_testnet(requests_mock):
    key = Keypair.random()
    requests_mock.get(f"https://horizon-testnet.stellar.org/accounts/{key.public_key}", json={"sequence": 1})
    requests_mock.post("https://horizon-testnet.stellar.org/transactions", json={"hash": "myhash"})
    runner = CliRunner()
    inputs = [key.secret, "", "y"]
    result = runner.invoke(cmds, ["change-trust-usdc", "--testnet"], input="\n".join(inputs))

    assert result.exit_code == 0
    assert "https://stellar.expert/explorer/testnet/tx/myhash" in result.stdout
