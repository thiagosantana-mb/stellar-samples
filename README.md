# Stellar Samples
## Requirements
* Python >= 3.7

### Setup
```
$ python -m venv .venv
$ source .venv/bin/active
$ pip install -r requirements.txt
```

### Unit tests
```
$ pytest tests --cov=. --cov-report term-missing
```

### Generate an account
```
$ python stellar_samples.py gen-account

Mnemonic phrase: 'my words...'
Private key: ********************************************************
Account (pubkey): ******************************************************** 
Save your private key on a safe place!

Did you saved your private key? [y/N]: y
Now you can send XLM to this address: ********************************************************

```

### Cross-asset payment
https://developers.stellar.org/docs/glossary/decentralized-exchange/#cross-asset-payments
```
$ python stellar_samples.py send-cross-asset

Paste your private key: 
Account: ********************************************************
Destination account: ********************************************************
Memo: 1234
See XLM/USDC prices
https://stellar.expert/explorer/public/asset/USDC-GA5ZSEJYB37JRC5AVCIA5MOP4RHTM335X2KGX3IHOJAPP5RE34K4KZVN?filter=markets
XLM Amount: 7
USDC Min Amount: 1
Fee [100]: 

        USDC issuer: GBBD47IF6LWK7P7MDEVSCWR7DPUWV3NY3DTQEVFL4NAT4AQH3ZLLFLA5,
        from: ********************************************************,
        to: ********************************************************,
        fee: 0.00001 XLM,
        amount: 7 XLM,
        min amount: 1 USDC
    
Can we sign and broadcast this TX? [y/N]: y
Broadcasting...
TX sent: ****************************************************************
https://stellar.expert/explorer/public/tx/****************************************************************
```
