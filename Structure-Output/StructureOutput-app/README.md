# Output types
By default, agents produce plain text (i.e. str) outputs. If you want the agent to produce a particular type of output, you can use the output_type parameter. A common choice is to use Pydantic objects, but we support any type that can be wrapped in a Pydantic TypeAdapter - dataclasses, lists, TypedDict, etc.

## install Packages
uv add openai-agents


# Pydantic
Pydantic is the most widely used data validation library for Python.

## Why use Pydantic?
The schema that Pydantic validates against is generally defined by Python type hints.

### Type hints powering schema validation

Type hints are great for this since, if you're writing modern Python, you already know how to use them. Using type hints also means that Pydantic integrates well with static typing tools (like mypy and Pyright) and IDEs (like PyCharm and VSCode).

```bash
from typing import Annotated, Literal

from annotated_types import Gt

from pydantic import BaseModel


class Fruit(BaseModel):
    name: str  
    color: Literal['red', 'green']  
    weight: Annotated[float, Gt(0)]  
    bazam: dict[str, list[tuple[int, bool, float]]]  


print(
    Fruit(
        name='Apple',
        color='red',
        weight=4.2,
        bazam={'foobar': [(1, True, 0.1)]},
    )
)
#> name='Apple' color='red' weight=4.2 bazam={'foobar': [(1, True, 0.1)]}

```