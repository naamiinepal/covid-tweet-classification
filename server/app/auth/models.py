from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: bool = False


class Token(BaseModel):
    access_token: str
    token_type: str


class UserInDB(User):
    hashed_password: str


fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": (
            "$argon2id$v=19$m=102400,t=2,p=8$"
            "mVPqPUdISUmpdW4tZWzt3Q$q2WMmuALp5Nq9SmGSpBGYQ"
        ),  # secret
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": (
            "$argon2id$v=19$m=102400,t=2,p=8$"
            "fW8tpZRSSomR0lqLMca41w$zEsDdx97ejBsxbSOy6wIlQ"
        ),  # secret2
        "disabled": True,
    },
}
