import inspect
import typing
from dataclasses import dataclass

from di import Container, Dependant, SyncExecutor
from di.api.dependencies import DependantBase


@dataclass
class Foo:
    bar: str = "bar"


def match_by_parameter_name(
    param: typing.Optional[inspect.Parameter], dependant: DependantBase[typing.Any]
) -> typing.Optional[DependantBase[typing.Any]]:
    if param is not None and param.name == "bar":
        return Dependant(lambda: "baz", scope=None)
    return None


container = Container(scopes=(None,))

container.register_bind_hook(match_by_parameter_name)

solved = container.solve(Dependant(Foo, scope=None))


def main():
    with container.enter_scope(None):
        foo = container.execute_sync(solved, executor=SyncExecutor())
    assert foo.bar == "baz"
