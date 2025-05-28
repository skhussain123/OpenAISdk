# Output types
By default, agents produce plain text (i.e. str) outputs. If you want the agent to produce a particular type of output, you can use the output_type parameter. A common choice is to use Pydantic objects, but we support any type that can be wrapped in a Pydantic TypeAdapter - dataclasses, lists, TypedDict, etc.

## install Packages
uv add openai-agents


# Pydantic
Pydantic is the most widely used data validation library for Python.

## Why use Pydantic?
The schema that Pydantic validates against is generally defined by Python type hints.

* Powered by type hints — with Pydantic, schema validation and serialization are controlled by type annotations; less to learn, less code to write, and seamless integration with your IDE and static analysis tools. [Learn More..](https://docs.pydantic.dev/latest/why/#type-hints)
* Speed — Pydantic's core validation logic is written in Rust. As a result, Pydantic is among the fastest data validation libraries for Python. Learn more…
* JSON Schema — Pydantic models can emit JSON Schema, allowing for easy integration with other tools. [Learn More..](https://docs.pydantic.dev/latest/why/#json-schema)
* Strict and Lax mode — Pydantic can run in either strict mode (where data is not converted) or lax mode where Pydantic tries to coerce data to the correct type where appropriate. [Learn More..] (https://docs.pydantic.dev/latest/why/#strict-lax)
Dataclasses, TypedDicts and more — Pydantic supports validation of many standard library types including dataclass and TypedDict. [Learn More..] (https://docs.pydantic.dev/latest/why/#dataclasses-typeddict-more)
* Customisation — Pydantic allows custom validators and serializers to alter how data is processed in many powerful ways. Learn more…
* Ecosystem — around 8,000 packages on PyPI use Pydantic, including massively popular libraries like FastAPI, huggingface, Django Ninja, SQLModel, & LangChain. [Learn More..](https://docs.pydantic.dev/latest/why/#ecosystem)
* Battle tested — Pydantic is downloaded over 360M times/month and is used by all FAANG companies and 20 of the 25 largest companies on NASDAQ. If you're trying to do something with Pydantic, someone else has probably already done it. [Learn More..](https://docs.pydantic.dev/latest/why/#using-pydantic)

