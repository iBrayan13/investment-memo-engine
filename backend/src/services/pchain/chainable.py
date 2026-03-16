import json
import logging
from typing import Any, Literal

import instructor
from openai import AsyncOpenAI
from pydantic import BaseModel
from anthropic import AsyncAnthropic
from anthropic.types.text_block import TextBlock
from tenacity import retry, stop_after_attempt, wait_exponential

from src.core.settings import Settings
from src.services.pchain.responses import Response
from src.services.pchain.chain_prompt_manager import ClientPrompt

logger = logging.getLogger(__name__)


class UnsupportedContentTypeError(Exception):
    pass


class APICallError(Exception):
    pass


class MinimalChainable:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.model_supported_types = {
            "openai": {"text", "image"},
            "anthropic": {"text", "image"},
            "deepseek": {"text"},
            "openrouter": {"text"},
        }

        self.model_supported_by_client = {
            "openai": {"gpt-4o-mini", "gpt-4o"},
            "anthropic": {"claude-3-5-sonnet"},
            "deepseek": {"deepseek-chat", "deepseek-reasoner"},
            "openrouter": {"openai/gpt-4o-mini"},
        }

        self.openai_client = AsyncOpenAI(api_key=self.settings.OPENAI_API_KEY)
        self.anthropic_client = AsyncAnthropic(api_key=self.settings.ANTHROPIC_API_KEY)
        self.deepseek_client = AsyncOpenAI(api_key=self.settings.DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")
        self.openrouter_client = AsyncOpenAI(api_key=self.settings.OPENROUTER_API_KEY, base_url="https://openrouter.ai/api/v1")

    def _get_instructor(
        self, client: AsyncOpenAI | AsyncAnthropic
    ) -> instructor.AsyncInstructor:
        if isinstance(client, AsyncOpenAI):
            return instructor.from_openai(client)
        elif isinstance(client, AsyncAnthropic):
            return instructor.from_anthropic(client)

    def _convert_value_to_string(self, value: Any) -> str:
        """Convert any value to a string representation"""
        if isinstance(value, dict | BaseModel):
            return json.dumps(value if isinstance(value, dict) else value.model_dump())
        elif isinstance(value, list):
            if not value:  # Empty list
                return "[]"
            return json.dumps(value)
        else:
            return str(value)

    def _prepare_content_for_llm(
        self, prompt: ClientPrompt, context: dict[str, Any]
    ) -> str:
        """Prepare content for LLMs (OpenAI, Anthropic, DeepSeek, OpenRouter) newer API format"""
        # Start with the prompt
        content = prompt.prompt

        # For each content key, append the content with clear separation
        for key in prompt.content_keys:
            if key in context:
                try:
                    value = context[key]
                    value_str = self._convert_value_to_string(value)
                    content += f"\n\n{key}:\n{value_str}"
                except Exception as e:
                    logger.error(f"Error preparing content for key {key}: {str(e)}")
                    content += f"\n\n{key}:\n{str(context[key])}"

        return content

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def _handle_anthropic_call(
        self, prompt: ClientPrompt, model: str, context: dict[str, Any]
    ) -> Response:
        try:
            content = self._prepare_content_for_llm(prompt, context)

            if prompt.return_model is not None:
                llm = self._get_instructor(self.anthropic_client)
                response = await llm.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": content}],
                    response_model=prompt.return_model,
                    max_tokens=4096,
                    temperature=0,
                )

            else:
                message = await self.anthropic_client.messages.create(
                    model=model,
                    max_tokens=4096,
                    temperature=0,
                    messages=[{"role": "user", "content": content}],
                )

                if isinstance(message.content[0], TextBlock):
                    response = message.content[0].text
                else:
                    response = ""

            return Response(response=response)
        except Exception as e:
            logger.error(f"Error in Anthropic API call: {str(e)}")
            raise APICallError(f"Error in Anthropic API call: {str(e)}") from e
        
    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def _handle_openrouter_call(
        self, prompt: ClientPrompt, model: str, context: dict[str, Any]
    ) -> Response:
        try:
            message = self._prepare_content_for_llm(prompt, context)

            if prompt.return_model is not None:
                llm = self._get_instructor(self.openrouter_client)
                response_obj = await llm.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": message}],
                    response_model=prompt.return_model,
                    temperature=0,
                )

                return Response(response=response_obj)
            else:
                raw_response = await self.openrouter_client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": message}],
                    temperature=0,
                )

                response = raw_response.choices[0].message.content

                return Response(response=response)

        except Exception as e:
            logger.error(f"Error in OpenRouter API call: {str(e)}")
            raise APICallError(f"Error in OpenRouter API call: {str(e)}") from e

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def _handle_openai_call(
        self, prompt: ClientPrompt, model: str, context: dict[str, Any]
    ) -> Response:
        try:
            message = self._prepare_content_for_llm(prompt, context)

            if prompt.return_model is not None:
                llm = self._get_instructor(self.openai_client)
                response_obj = await llm.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": message}],
                    response_model=prompt.return_model,
                    temperature=0,
                )

                return Response(response=response_obj)
            else:
                raw_response = await self.openai_client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": message}],
                    temperature=0,
                )

                response = raw_response.choices[0].message.content

                return Response(response=response)

        except Exception as e:
            logger.error(f"Error in OpenAI API call: {str(e)}")
            raise APICallError(f"Error in OpenAI API call: {str(e)}") from e
    
    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def _handle_deepseek_reasoner_call(
        self, prompt: ClientPrompt, context: dict[str, Any]
    ) -> Response:
        try:
            message = self._prepare_content_for_llm(prompt, context)

            if prompt.return_model is not None:
                raw_response = await self.deepseek_client.chat.completions.create(
                    model="deepseek-reasoner",
                    messages=[
                        {
                            "role": "system", 
                            "content": f"Output your response as a valid JSON object that conforms to this schema: {json.dumps(prompt.return_model.model_json_schema())}"
                        },
                        {
                            "role": "user",
                            "content": message
                        }
                    ],
                    temperature=0,
                    response_format={
                        'type': 'json_object'
                    }
                )

                response = prompt.return_model.model_validate_json(raw_response.choices[0].message.content)

                return Response(response=response)
            else:
                raw_response = await self.deepseek_client.chat.completions.create(
                    model="deepseek-reasoner",
                    messages=[{"role": "user", "content": message}],
                    temperature=0,
                )

                response = raw_response.choices[0].message.content

                return Response(response=response)

        except Exception as e:
            logger.error(f"Error in DeepSeek API call: {str(e)}")
            raise APICallError(f"Error in DeepSeek API call: {str(e)}") from e

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def _handle_deepseek_chat_call(
        self, prompt: ClientPrompt, context: dict[str, Any]
    ) -> Response:
        try:
            message = self._prepare_content_for_llm(prompt, context)

            if prompt.return_model is not None:
                llm = self._get_instructor(self.deepseek_client)
                response_obj = await llm.chat.completions.create(
                    model="deepseek-chat",
                    messages=[{"role": "user", "content": message}],
                    response_model=prompt.return_model,
                    temperature=0,
                )

                return Response(response=response_obj)
            else:
                raw_response = await self.deepseek_client.chat.completions.create(
                    model="deepseek-chat",
                    messages=[{"role": "user", "content": message}],
                    temperature=0,
                )

                response = raw_response.choices[0].message.content

                return Response(response=response)

        except Exception as e:
            logger.error(f"Error in DeepSeek API call: {str(e)}")
            raise APICallError(f"Error in DeepSeek API call: {str(e)}") from e

    async def _handle_prompt(
        self,
        client: Literal['openai', 'anthropic', 'deepseek', 'openrouter'],
        model: str,
        prompt: ClientPrompt,
        context: dict[str, Any],
    ) -> Response:
        if not model in self.model_supported_by_client[client]:
            raise ValueError(f"Unsupported model type: {model}")

        if client == 'openai':
            return await self._handle_openai_call(prompt, model, context)
        
        elif client == 'deepseek':
            if model == 'deepseek-chat':
                return await self._handle_deepseek_chat_call(prompt, context)
            if model == 'deepseek-reasoner':
                return await self._handle_deepseek_reasoner_call(prompt, context)
            else:
                raise ValueError(f"Unsupported model type: {model}")
        
        elif client == 'openrouter':
            return await self._handle_openrouter_call(prompt, model, context)
            
        elif client == 'anthropic':
            return await self._handle_anthropic_call(prompt, model, context)
        
        else:
            raise ValueError(f"Unsupported client type: {client}")

    async def run(
        self,
        client: Literal['openai', 'anthropic', 'deepseek', 'openrouter'],
        model: str,
        prompts: list[ClientPrompt],
        context: dict[str, Any] | None = None,
        returns_model: dict[int, type[BaseModel]] | None = None,
    ) -> list[Response]:

        logger.info(f"Run method called with client type: {client}")
        output: list[Response] = []

        if context is None:
            context = {}

        if returns_model is None:
            returns_model = {}

        for k, v in returns_model.items():
            prompts[k].return_model = v
            prompts[k].prompt = (
                prompts[k].prompt
                + "\n\n Model schema: "
                + json.dumps(v.model_json_schema())
            )

        for prompt in prompts:
            for key, value in context.items():
                prompt.prompt = prompt.prompt.replace(f"{{{{{key}}}}}", str(value))

            for i, previous_output in enumerate(output):
                if isinstance(previous_output.response, dict):
                    prompt.prompt = prompt.prompt.replace(
                        f"{{{{output[-{len(output)-i}]}}}}",
                        json.dumps(previous_output.response),
                    )
                    for key, value in previous_output.response.items():
                        prompt.prompt = prompt.prompt.replace(
                            f"{{{{output[-{len(output)-i}].{key}}}}}", str(value)
                        )
                else:
                    prompt.prompt = prompt.prompt.replace(
                        f"{{{{output[-{len(output)-i}]}}}}",
                        str(previous_output.response),
                    )

            try:
                result = await self._handle_prompt(client, model, prompt, context)
                output.append(result)
            except APICallError as e:
                logger.error(f"Error in API call: {str(e)}")
                output.append(Response(response=f"Error: {str(e)}"))

        return output