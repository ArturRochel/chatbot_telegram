from typing import Annotated
from fastapi import Depends
from app.repositories import RepositoryRedis

repository_redis = Annotated[RepositoryRedis, Depends()]

class MachineState():

    def __init__(self, repository: repository_redis):
        self.repository = repository