from method import Method

method = Method(
env="dev",
api_key="sk_5MicRAJFaJr6iJXmmJJ2wrCw",
)

new_entity = method.entities.create({
    "type": "individual",
    "individual": {
    "first_name": "Test",
    "last_name": "User",
    "phone": "+15121231111",
    "email": "test.user@example.com",
    "dob": "1990-01-01",
    }
})

entities = method.entities(new_entity['id']).connect.create()
