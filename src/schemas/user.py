from pydantic import BaseModel, ConfigDict


class UserCreds(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    username: str
    role: str


class UserCredsDB(UserCreds):
    password: str
