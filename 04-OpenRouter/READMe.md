## What is OpenRouter?
OpenRouter is a service that provides a single unified API to access multiple large language models (LLMs) from different providers like OpenAI, Anthropic (Claude), Google Gemini, and others. Instead of managing separate API keys and endpoints for each AI model, you can use OpenRouter’s API to seamlessly switch between and use various AI models through one interface.


**Key points:**

* Unified access to many AI models.
* Simplifies API management — one key, one endpoint.
* Supports popular models like GPT-4, Claude, Gemini, and more.
* Allows easy switching between models without changing your code much.
* Often more cost-effective and flexible for developers.


### User Interface and API
OpenRouter provides both a user interface and an API. The user interface includes a chatroom where users can interact with multiple LLMs at once, as well as tools for managing accounts and monitoring usage, such as viewing token usage and costs. The API is designed for developers, offering a standardized way to integrate LLM capabilities into applications.


### Support for Function Calling
The evidence leans toward OpenRouter supporting function calling (also known as tool calling), allowing the AI to suggest using external tools based on input. This feature is standardized across compatible models, enabling developers to integrate functions like weather APIs into their applications.

### Hosting Models: Proxy or Host?
It seems likely that OpenRouter acts as a proxy, routing API requests to models hosted by third-party providers rather than hosting the models itself. This approach allows access to over 200 models without the infrastructure costs of hosting, with OpenRouter handling translations and authentications.


| **Feature**             | **Description**                                                                                     |
| ----------------------- | --------------------------------------------------------------------------------------------------- |
| **User Interface**      | Includes a chatroom to interact with LLMs and tools for managing user accounts.                     |
| **API Compatibility**   | Works with the OpenAI Chat Completion API and supports the OpenAI SDK.                              |
| **Function Calling**    | Allows calling tools/functions, standardized across compatible models/providers.                    |
| **Model Hosting**       | Functions as a proxy that routes requests to third-party providers; it does not host models itself. |
| **Pricing Model**       | Pay-per-use pricing based on tokens; some models are free; pricing is transparent.                  |
| **Additional Features** | Includes a playground for testing, supports streaming, and offers optional prompt logging.          |


