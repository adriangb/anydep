from di.container import Container
from di.dependant import Dependant, Marker
from di.typing import Annotated


class Request:
    ...


RequestDep = Annotated[Request, Marker(scope="request")]


class DBConnection:
    def __init__(self, request: RequestDep) -> None:
        ...


DBConnDep = Annotated[DBConnection, Marker(scope="app")]


def controller(conn: DBConnDep) -> None:
    ...


def framework() -> None:
    container = Container()
    container.solve(Dependant(controller, scope="request"), scopes=["app", "request"])
