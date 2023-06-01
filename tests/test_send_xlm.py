from click.testing import CliRunner
from stellar_sdk import Keypair

from stellar_samples import cmds


def test_send_xlm(requests_mock):
    key = Keypair.random()
    requests_mock.get(f"https://horizon.stellar.org/accounts/{key.public_key}", json={"sequence": 1})
    requests_mock.post("https://horizon.stellar.org/transactions", json={"hash": "myhash"})
    runner = CliRunner()
    inputs = [key.secret, key.public_key, "1234", "10", "", "y"]
    result = runner.invoke(cmds, ["send-xlm"], input="\n".join(inputs))

    assert result.exit_code == 0
    assert "https://stellar.expert/explorer/public/tx/myhash" in result.stdout


def test_create_account(requests_mock):
    key = Keypair.random()
    requests_mock.get(f"https://horizon.stellar.org/accounts/{key.public_key}", [
        {"json": {"sequence": 1}},
        {"status_code": 404}
    ])
    requests_mock.post("https://horizon.stellar.org/transactions", json={"hash": "myhash"})
    runner = CliRunner()
    inputs = [key.secret, key.public_key, "1234", "10", "", "y"]
    result = runner.invoke(cmds, ["send-xlm"], input="\n".join(inputs))

    assert result.exit_code == 0
    assert "https://stellar.expert/explorer/public/tx/myhash" in result.stdout


def test_send_xlm_invalid_key():
    key = Keypair.random()
    runner = CliRunner()
    inputs = ["whatever", key.public_key, "1234", "10", "", "y"]
    result = runner.invoke(cmds, ["send-xlm"], input="\n".join(inputs))

    assert result.exit_code == 1
    assert "Invalid Ed25519 Secret Seed" in str(result.exception)


def test_send_xlm_invalid_destination(requests_mock):
    key = Keypair.random()
    requests_mock.get(f"https://horizon.stellar.org/accounts/{key.public_key}", json={"sequence": 1})
    requests_mock.post("https://horizon.stellar.org/transactions", json={"hash": "myhash"})
    runner = CliRunner()
    inputs = [key.secret, "invalid", "1234", "10", "", "y"]
    result = runner.invoke(cmds, ["send-xlm"], input="\n".join(inputs))

    assert result.exit_code == 1
    assert "This is not a valid account" in str(result.exception)


def test_send_xlm_invalid_memo(requests_mock):
    key = Keypair.random()
    requests_mock.get(f"https://horizon.stellar.org/accounts/{key.public_key}", json={"sequence": 1})
    requests_mock.post("https://horizon.stellar.org/transactions", json={"hash": "myhash"})
    runner = CliRunner()
    inputs = [key.secret, key.public_key, "expects memo id (int)", "10", "", "y"]
    result = runner.invoke(cmds, ["send-xlm"], input="\n".join(inputs))

    assert result.exit_code == 1
    assert result.exception


def test_send_xlm_max_amount():
    key = Keypair.random()
    runner = CliRunner()
    inputs = [key.secret, key.public_key, "1234", "1000", "", "y"]
    result = runner.invoke(cmds, ["send-xlm"], input="\n".join(inputs))

    assert result.exit_code == 2
    assert "This script is not intended for any serious usage" in result.stdout


def test_send_xlm_min_amount(requests_mock):
    key = Keypair.random()
    requests_mock.get(f"https://horizon.stellar.org/accounts/{key.public_key}", json={"sequence": 1})
    requests_mock.post("https://horizon.stellar.org/transactions", json={"hash": "myhash"})
    runner = CliRunner()
    inputs = [key.secret, key.public_key, "1234", "1", "", "y"]
    result = runner.invoke(cmds, ["send-xlm"], input="\n".join(inputs))

    assert result.exit_code == 2
    assert "amount is too low" in result.stdout


def test_send_xlm_testnet(requests_mock):
    key = Keypair.random()
    requests_mock.get(f"https://horizon-testnet.stellar.org/accounts/{key.public_key}", json={"sequence": 1})
    requests_mock.post("https://horizon-testnet.stellar.org/transactions", json={"hash": "myhash"})
    runner = CliRunner()
    inputs = [key.secret, key.public_key, "1234", "10", "", "y"]
    result = runner.invoke(cmds, ["send-xlm", "--testnet"], input="\n".join(inputs))

    assert result.exit_code == 0
    assert "https://stellar.expert/explorer/testnet/tx/myhash" in result.stdout
