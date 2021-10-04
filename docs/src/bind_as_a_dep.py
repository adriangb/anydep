from dataclasses import dataclass
from typing import List

try:
    from typing import Protocol
except ImportError:
    from typing_extensions import Protocol  # type: ignore

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
        self.log: List[str] = []

    async def execute(self, sql: str) -> None:
        self.log.append(sql)


async def framework() -> None:
    container = Container()
    container.bind(Dependant(Postgres, scope="app"), DBProtocol)  # type: ignore
    solved = container.solve(Dependant(controller))
    async with container.enter_local_scope("app"):
        # type: ignore
        await container.execute_async(solved)
        db = await container.execute_async(container.solve(Dependant(DBProtocol)))
        assert isinstance(db, Postgres)
        assert db.log == ["SELECT *"]
