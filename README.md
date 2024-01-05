# method-python
Python library for the Method API

## Install

```bash
pip install method-python
```

## Usage

```python
from method import Method

method = Method(env='production', api_key='{API_KEY}')

# or 

method = Method({'env': 'production', 'api_key': '{API_KEY}'})
```

## Entities

### Create Individual Entity

```python
entity = method.entities.create({
  'type': 'individual',
  'individual': {
    'first_name': 'Kevin',
    'last_name': 'Doyle',
    'phone': '+16505555555',
    'email': 'kevin.doyle@gmail.com',
    'dob': '1997-03-18',
  },
  'address': {
    'line1': '3300 N Interstate 35',
    'line2': None,
    'city': 'Austin',
    'state': 'TX',
    'zip': '78705'
  }
})
```

### Create Corporation Entity

```python
entity = method.entities.create({
  'type': 'c_corporation',
  'corporation': {
    'name': 'Alphabet Inc.',
    'dba': 'Google',
    'ein': '641234567',
    'owners': [
      {
        'first_name': 'Sergey',
        'last_name': 'Brin',
        'phone': '+16505555555',
        'email': 'sergey@google.com',
        'dob': '1973-08-21',
        'address': {
          'line1': '600 Amphitheatre Parkway',
          'line2': None,
          'city': 'Mountain View',
          'state': 'CA',
          'zip': '94043'
        }
      }
    ]
  },
  'address': {
    'line1': '1600 Amphitheatre Parkway',
    'line2': None,
    'city': 'Mountain View',
    'state': 'CA',
    'zip': '94043'
  }
})
```

### Retrieve Entity

```python
entity = method.entities.get('ent_au22b1fbFJbp8')
```

### Update Entity

```python
entity = method.entities.update('ent_au22b1fbFJbp8', {
  'individual': {
    'first_name': 'Kevin',
    'last_name': 'Doyle',
    'email': 'kevin.doyle@gmail.com',
    'dob': '1997-03-18',
  }
})
```

### List Entities

```python
entities = method.entities.list()
```

### Refresh Capabilities

```python
entity = method.entities.refresh_capabilities('ent_au22b1fbFJbp8')
```

### Create Individual Auth Session

```python
response = method.entities.create_auth_session('ent_au22b1fbFJbp8')
```

### Update Individual Auth Session

```python
response = method.entities.update_auth_session('ent_au22b1fbFJbp8', {
  "answers": [
    {
      "question_id": "qtn_ywWqCnXDGGmmg",
      "answer_id": "ans_74H68MJjqNhk8"
    },
    ...
  ]
})
```

## Accounts

### Create Ach Account

```python
account = method.accounts.create({
  'holder_id': 'ent_y1a9e1fbnJ1f3',
  'ach': {
    'routing': '367537407',
    'number': '57838927',
    'type': 'checking'
  }
})
```

### Create Liability Account

```python
account = method.accounts.create({
  'holder_id': 'ent_au22b1fbFJbp8',
  'liability': {
    'mch_id': 'mch_2',
    'account_number': '1122334455'
  }
})
```

### Retrieve Account

```python
account = method.accounts.get('acc_Zc4F2aTLt8CBt')
```

### List Accounts

```python
accounts = method.accounts.list()
```

## ACH Verification

### Create Micro-Deposits Verification

```python
verification = method
  .accounts('acc_b9q2XVAnNFbp3')
  .verification
  .create({ 'type': 'micro_deposits' })
```

### Create Plaid Verification

```python
verification = method
  .accounts('acc_b9q2XVAnNFbp3')
  .verification
  .create({
    'type': 'plaid',
    'plaid': {
      'balances': {
        'available': 100,
        'current': 110,
        'iso_currency_code': 'USD',
        'limit': None,
        'unofficial_currency_code': None
      },
      'transactions': [
        ...
      ]
    }
  })
```

### Create Teller Verification

```python
verification = method
  .accounts('acc_b9q2XVAnNFbp3')
  .verification
  .create({
    'type': 'teller',
    'teller': {
      'balances': {
        'account_id': 'acc_ns9gkibeia6ad0rr6s00q',
        'available': '93011.13',
        'ledger': '93011.13',
        'links': {
          'account': 'https://api.teller.io/accounts/acc_ns9gkibeia6ad0rr6s00q',
          'self': 'https://api.teller.io/accounts/acc_ns9gkibeia6ad0rr6s00q/balances'
        }
      },
      'transactions': [
        {
          'account_id': 'acc_ns9gkia42a6ad0rr6s000',
          'amount': '-51.19',
          'date': '2022-01-04',
          'description': 'Venmo Payment',
          'details': {
            'category': 'services',
            'counterparty': {
              'name': 'LOUISE BENTLEY',
              'type': 'person'
            },
            'processing_status': 'complete'
          },
          'id': 'txn_ns9gkiph2a6ad0rr6s000',
          'links': {
            'account': 'https://api.teller.io/accounts/acc_ns9gkia42a6ad0rr6s000',
            'self': 'https://api.teller.io/accounts/acc_ns9gkia42a6ad0rr6s000/transactions/txn_ns9gkiph2a6ad0rr6s000'
          },
          'running_balance': None,
          'status': 'pending',
          'type': 'digital_payment'
        }
      ]
    }
  })
```

### Create MX Verification

```python
verification = method
  .accounts('acc_b9q2XVAnNFbp3')
  .verification
  .create({
    'type': 'mx',
    'mx': {
      'account ': {
        'institution_code': 'chase',
        'guid': 'ACT-06d7f44b-caae-0f6e-1384-01f52e75dcb1',
        'account_number': None,
        'apr': None,
        'apy': None,
        'available_balance': 1000.23,
        'available_credit': None,
        'balance': 1000.23,
        'cash_balance': 1000.32,
        'cash_surrender_value': 1000.23,
        'created_at': '2016-10-13T17:57:37+00:00'
        ...
      },
      'transactions': [
        ...
      ]
    } 
  )
```

### Update Verification

```python
verification = method
  .accounts('acc_b9q2XVAnNFbp3')
  .verification
  .update({
    'micro_deposits': {
      'amounts': [10, 4]
    }
  })
```

### Retrieve Verification

```python
verification = method
  .accounts('acc_b9q2XVAnNFbp3')
  .verification
  .get()
```

## Merchants 

### List Merchants

```python
merchants = method.merchants.list()
```

### Retrieve Merchant

```python
merchant = method.merchants.get('mch_1')
```

## Payments

### Create Payment

```python
payment = method.payments.create({
  'amount': 5000,
  'source': 'acc_JMJZT6r7iHi8e',
  'destination': 'acc_AXthnzpBnxxWP',
  'description': 'Loan Pmt'
})
```

### Retrieve Payment

```python
payment = method.payments.get('pmt_rPrDPEwyCVUcm')
```

### Delete Payment

```python
payment = method.payments.delete('pmt_rPrDPEwyCVUcm')
```

### List Payments

```python
payments = method.payments.list()
```

## Reversals

### Retrieve Reversal

```python
reversal = method.payments('pmt_rPrDPEwyCVUcm').reversals.get('rvs_eaBAUJtetgMdR')
```

### Update Reversal

```python
reversal = method
  .payments('pmt_rPrDPEwyCVUcm')
  .reversals
  .update('rvs_eaBAUJtetgMdR', { 'status': 'pending' })
```

### List Reversals for Payment

```python
reversals = method.payments('pmt_rPrDPEwyCVUcm').reversals.list()
```

## Webhooks

### Create Webhook

```python
webhook = method.webhooks.create({
  'type': 'payment.update',
  'url': 'https://api.example.app/webhook',
  'auth_token': 'md7UqcTSmvXCBzPORDwOkE'
})
```

### Retrieve Webhook

```python
webhook = method.webhooks.get('whk_cSGjA6d9N8y8R')
```

### Delete Webhoook

```python
webhook = method.webhooks.delete('whk_cSGjA6d9N8y8R')
```

### List Webhooks

```python
webhooks = method.webhooks.list()
```

## Reports

### Create Report

```python
report = method.reports.create({ 'type': 'payments.created.current' })
```

### Retrieve Report

```python
report = method.reports.get('rpt_cj2mkA3hFyHT5')
```

### Download Report

```python
report_csv = method.reports.download('rpt_cj2mkA3hFyHT5')
```
