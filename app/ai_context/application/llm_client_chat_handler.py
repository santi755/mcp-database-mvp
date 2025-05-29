from app.ai_context.domain.llm_client import LLMClient


async def llm_client_chat_handler(message: str, llm_client: LLMClient) -> str:
    """
    Handler to process chat messages using the provided LLM client.
    """
    try:
        response = llm_client.get_client().invoke(message)
        print("--------------------------------")
        print(response)
        print("--------------------------------")
        return response
    except Exception as e:
        raise Exception(f"Error processing the message: {str(e)}")
