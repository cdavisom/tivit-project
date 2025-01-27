from fastapi import HTTPException, status

class CredentialsValidationError(Exception):
    def __init__(self, authenticate_value: str):
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )

class GenericDatabaseError(Exception):
    def __init__(self):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Problems with DB, try again later."
        )

class InsufficientPermissionsError(Exception):
    def __init__(self, authenticate_value: str):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not enough permissions",
            headers={"WWW-Authenticate": authenticate_value},
        )

class InvalidCredentialsError(Exception):
    def __init__(self):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )