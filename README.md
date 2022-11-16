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
