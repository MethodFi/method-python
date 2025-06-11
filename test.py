from method import Method

method = Method({"api_key":"sk_R6PLdTR9gPnBH9hqHVGnzbD9", "env" : "dev"})

Entity = method.entities.create(
    opts={
    "type": "individual",
    "individual": {
        "first_name": "John",
        "last_name": "Doe",
        "phone": "+15121231123",
        "dob": "1997-03-18",
        "email": "john_doe@gmail.com"
    },
    "address": {
        "line1": "3300 N Interstate 35",
        "line2": None,
        "city": "Austin",
        "state": "TX",
        "zip": "78705"
    }
}
)

# print(Entity)
cxn = method.entities(Entity["id"]).connect.create(products=["balance", "card_brand"], params={"expand": ["accounts"]})
cxn_get = method.entities(Entity["id"]).connect.retrieve(cxn["id"], params={"expand": ["accounts"]})
cxn_list = method.entities(Entity["id"]).connect.list(params={"expand": ["accounts"]})


# account_expanded = method.accounts.retrieve("acc_yL8VxnkUJg33f", {"expand": ["update"]})

import json
print(json.dumps(dict(cxn_list[0]), indent=2))
