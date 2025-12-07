import secrets

def generator(data):
    for value in data:
        yield value


def generate_state():
    return secrets.token_urlsafe(32)



