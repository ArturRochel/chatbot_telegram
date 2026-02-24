from typing import Annotated
from fastapi import Depends
from app.repositories import RepositoryRedis

class MessageSendService:
    def __init__(self, repository: Annotated[RepositoryRedis, Depends()]):
        self.repository = repository