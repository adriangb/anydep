# Solving

Solving a dependency means build a directed acyclic graph (DAG) of dependencies by inspecting sub dependencies and resolving binds.
Once we solve a dependency, we can execute it without doing any introspection.

Solving is done by the `Container`.
The result of solving is stored in a `SolvedDependant` object which you can pass to `Container.execute` to get back the result.
The simplest form of executing a dependency is thus:

```python
result = container.execute(container.solve(Dependant(lambda: 1)))
```

For a more comprehensive overview, see the [architecture] section.

During solving, several things are checked:

1. Any dependencies that can't be fully autowirired have binds.
2. The same dependency is not used twice with different scopes.

However, other things are not checked and are deffered to execution time. Namely, *scopes are not validated during solving*.
This means that you can solve a DAG including `"request"` scoped depdendencies before entering the `"request"` scope.
But it also means that any errors (like a missing scope) won't be caught until runtime.

## SolvedDependant

`di` lets you pre-solve your dependencies so that you don't have to run the solver each time you execute.
This usually comes with a huge performance boost, but only works if you have a static dependency graph.
In practice, this just means that solving captures the current binds and won't be updated if there are changes to binds.
Note that you can still have *values* in your DAG change, just not the shape of the DAG itself.

For example, here is a more advanced use case where the framework solves the endpoint and then provides the `Request` as a value each time the endpoint is called.

This means that `di` does *not* do any reflection for each request, nor does it have to do dependency resolution.
Instead, only some basic checks on scopes are done and the dependencies are executed with almost no overhead.

```Python hl_lines="11-13 15"
--8<-- "docs/src/solved_dependant.py"
```

## Getting a list of dependencies

`di` provides a convenience function to flatten the dependency DAG into a list off all sub dependencies in `Container.get_flat_subdependants`.

```Python hl_lines="17-19"
--8<-- "docs/src/solved_dependant.py"
```

This lists all of the *Dependants* for the solved dependency.

This means that you can create custom markers and easily enumerate them.
For example, you might make a `Header` dependency and then want to know what headers are being requested by the controller, even if they are nested inside other dependencies:

```python
from di import Dependant

class Header(Dependant[str]):
    ...
```

See the [dependants] section for a more complete example of this.

[architecture]: architecture.md
[Performance section of the Wiring docs]: wiring.md#performance
[dependants]: dependants.md
