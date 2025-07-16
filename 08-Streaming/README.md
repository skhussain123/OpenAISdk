
### what is streaming in openai sdk
In the OpenAI SDK, streaming refers to the ability to receive the response from the model token-by-token (or chunk-by-chunk) as it's generated, instead of waiting for the entire response to complete before you get any output.


### Why Use Streaming?

* Faster feedback: You see results instantly as they are generated.
* Better user experience: Useful in chat apps, terminals, or any interactive UI.
* Ideal for long responses: Reduces perceived latency for long outputs.