import bcrypt


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_password.decode("utf-8")


# verifies whether the hashed password matches the input password
def verify_password(input_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        input_password.encode("utf-8"), hashed_password.encode("utf-8")
    )
