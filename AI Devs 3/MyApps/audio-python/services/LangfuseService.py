from typing import Dict, Any, List, Optional, Union
import os
from langfuse import Langfuse
from langfuse.model import ChatMessage

class LangfuseService:
    def __init__(self):
        self.langfuse = Langfuse(
            public_key= "pk-lf-81f85c3f-1eeb-443b-849d-a723c264b798",
            secret_key= "sk-lf-e48102fe-9894-454f-b63e-91a246fc97de",
            host="https://cloud.langfuse.com"
        )


   # Coroutine to flush data to Langfuse asynchronously
    async def flush_async(self) -> None:
        self.langfuse.flush()  # Remove await - this is a synchronous method

    def create_trace(self, options: Dict[str, str]) -> Any:
        # Create a new trace for tracking a sequence of operations
        return self.langfuse.trace(
            id=options.get("id"),
            name=options.get("name"),
            session_id=options.get("session_id")
        )

    def create_span(self, trace: Any, name: str, input: Optional[Any] = None) -> Any:
        # Create a span within a trace to track a specific operation
        return trace.span(
            name=name,
            input=input
        )

    def finalize_span(self, span: Any, name: str, input: Any, output: Any) -> None:
        # Update and complete a span with its final data
        span.update(
            name=name,
            output=output
        )
        span.end()

    # Coroutine to finalize a trace with input and output data
    
    async def finalize_trace(self, trace: Any, input: Any, output: Any) -> None:
        # Update the trace with final input/output data
        trace.update(
            input=input,    # What was initially sent/requested
            output=output   # The final result/response
        )
        # Ensure data is actually sent to Langfuse servers
        await self.flush_async()

    # Coroutine to properly shutdown the Langfuse client
    async def shutdown_async(self) -> None:
        await self.langfuse.shutdown()

    def create_generation(self, trace: Any, name: str, input: Any, prompt: Optional[Any] = None) -> Any:
        # Create a new generation event within a trace
        return trace.generation(
            name=name,
            input=input,
            prompt=prompt
        )

    def create_event(self, trace: Any, name: str, input: Optional[Any] = None, output: Optional[Any] = None) -> None:
        # Create an event with optional input and output data
        trace.event(
            name=name,
            input=str(input) if input is not None else None,
            output=str(output) if output is not None else None
        )

    def finalize_generation(
        self,
        generation: Any,
        output: Any,
        model: str,
        usage: Optional[Dict[str, int]] = None
    ) -> None:
        # Complete a generation event with its results and usage statistics
        generation.update(
            output=output,
            model=model,
            usage=usage
        )
        generation.end()

    # Coroutine to create a new prompt template
    async def create_prompt(self, body: Dict[str, Any]) -> Any:
        return await self.langfuse.create_prompt(body)

    # Coroutine to retrieve a prompt template
    async def get_prompt(
        self,
        name: str,
        version: Optional[int] = None,
        options: Optional[Dict[str, Any]] = None
    ) -> Any:
        return await self.langfuse.get_prompt(name, version, options)

    def compile_prompt(
        self,
        prompt: Any,
        variables: Dict[str, Any]
    ) -> Union[str, List[ChatMessage]]:
        # Compile a prompt template with variables
        compiled = prompt.compile(variables)
        if isinstance(compiled, str):
            return compiled
        elif isinstance(compiled, list):
            # Convert compiled messages to a standard format
            return [{
                "role": msg.role,
                "content": msg.content
            } for msg in compiled]
        else:
            raise ValueError("Unexpected prompt compilation result")

    # Coroutine to fetch multiple prompts concurrently
    async def pre_fetch_prompts(self, prompt_names: List[str]) -> None:
        # Create a list of coroutines for each prompt fetch operation
        prompt_coroutines = [self.get_prompt(name) for name in prompt_names]
        
        # Use the * operator to unpack the list of coroutines as separate arguments
        # asyncio.gather runs all coroutines concurrently and waits for all to complete
        # Example: If prompt_names = ["greeting", "farewell"]
        # This becomes: await asyncio.gather(self.get_prompt("greeting"), self.get_prompt("farewell"))
        await asyncio.gather(*prompt_coroutines) 