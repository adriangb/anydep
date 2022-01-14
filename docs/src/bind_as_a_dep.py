import sys
from dataclasses import dataclass

if sys.version_info < (3, 8):
    from typing_extensions import Protocol
else:
    from typing import Protocol

from di import Container, Dependant


class DBProtocol(Protocol):
    async def execute(self, sql: str) -> None:
        ...


async def controller(db: DBProtocol) -> None:
    await db.execute("SELECT *")


@dataclass
class DBConfig:
    host: str = "localhost"


class Postgres(DBProtocol):
    def __init__(self, config: DBConfig) -> None:
        self.host = config.host

    async def execute(self, sql: str) -> None:
        print(sql)


async def framework() -> None:
    container = Container()
    container.bind(Dependant(Postgres), DBProtocol)
    solved = container.solve(Dependant(controller))
    # this next line would fail without the bind
    await container.execute_async(solved)
    # and we can double check that the bind worked
    # by requesting the instance directly
    db = await container.execute_async(container.solve(Dependant(DBProtocol)))
    assert isinstance(db, Postgres)
