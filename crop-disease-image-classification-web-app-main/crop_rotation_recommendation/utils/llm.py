from groq import Groq
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.outputs import ChatGeneration, ChatResult
from typing import List, Any, Dict, Optional
from pydantic import PrivateAttr
import os

class GroqLlamaLLM(BaseChatModel):
    model_name: str = "llama-3.3-70b-versatile"
    temperature: float = 0.7
    max_tokens: int = 1024

   
    _client: Groq = PrivateAttr(default_factory=lambda: Groq(api_key=os.getenv("GROQ_API_KEY")))

    def _call(self, messages: List[HumanMessage], stop=None) -> AIMessage:
        chat_messages = [
            {"role": "user" if isinstance(m, HumanMessage) else "assistant", "content": m.content}
            for m in messages
        ]
        stream = self._client.chat.completions.create(
            model=self.model_name,
            messages=chat_messages,
            temperature=self.temperature,
            max_completion_tokens=self.max_tokens,
            top_p=1,
            stream=True,
            stop=stop,
        )

        full_response = ""
        for chunk in stream:
            delta = chunk.choices[0].delta.content
            if delta:
                full_response += delta
        return AIMessage(content=full_response)

    def _generate(self, messages: List[Any], stop: Optional[List[str]] = None,
                  run_manager: Optional[Any] = None, **kwargs: Any) -> ChatResult:
        message = self._call(messages, stop=stop)
        generation = ChatGeneration(message=message)
        return ChatResult(generations=[generation])

    @property
    def _llm_type(self): return "groq_llama"

    @property
    def _identifying_params(self): return {"model_name": self.model_name}
