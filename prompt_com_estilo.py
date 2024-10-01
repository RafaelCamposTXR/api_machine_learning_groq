from groq import Groq
import os
import json

client = Groq(api_key="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")
# client = Groq(api_key=os.getenv('GROQ_API_KEY'))

MODEL = 'llama3-70b-8192'

def generate_response(prompt):
    return json.dumps({"response": f"I'd be happy to help with {prompt}!"})

def run_conversation(user_prompt, style):
    messages = [
        {
            "role": "system",
            # "content": f'You are a helpful assistant who responds in a {style} tone, and in portuguese.',
            "content": f'Você é um assistente atencioso que responde em um tom {style}, e em português. Você não se desculpa por confusões, apenas dá a resposta'
        },
        {
            "role": "user",
            "content": user_prompt
        }
    ]
    tools = [
        {
            "type": "function",
            "function": {
                "name": "generate_response",
                "description": "Generate a response",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "prompt": {
                            "type": "string",
                            "description": "The user's prompt"
                        }
                    },
                    "required": ["prompt"]
                }
            }
        }
    ]
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=tools,
        tool_choice="auto",
        max_tokens=4096
    )

    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls

    if tool_calls:
        available_functions = {
            "generate_response": generate_response
        }
        messages.append(response_message)  # extende a conversa com a resposta do assistente
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            function_response = function_to_call(prompt=function_args.get("prompt"))
            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                }
            )  # extende a conversa com a resposta da função
        second_response = client.chat.completions.create(
            model=MODEL,
            messages=messages
        )  # consegue uma nova resposta do modelo
        print(f'RESPOSTA: {second_response.choices[0].message.content}')  # exibe a resposta final

style= input("ESTILO: ")
user_prompt = input("PROMPT: ")
run_conversation(user_prompt, style)