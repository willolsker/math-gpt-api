import openai
import sympy.parsing.mathematica as parser
import json
import dotenv
import os
dotenv.load_dotenv()

functions = [
    {
        "name": "solve",
        "description": "Solves a mathematical expression.",
        "parameters": {
            "type": "object",
            "properties": {
                "problem": {
                    "type": "string",
                    "description": "The expression to simplify, in Mathematica expression format.",
                    "example": "D[x^2, x]"
                }
            }
        }
    }
]


def simplify(problem):
    parsed = parser.parse_mathematica(problem)
    return str(parsed.evalf())


def run_conversation(word_problem):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=[
            {"role": "system", "content": "Solve the problem provided by the user with step by step instructions."},
            {"role": "user", "content": word_problem},
        ],
        functions=functions,
        function_call="auto",
    )

    message = response["choices"][0]["message"]

    if message.get("function_call"):
        function_name = message["function_call"]["name"]
        function_args = json.loads(message["function_call"]["arguments"])

        function_response = simplify(function_args["problem"])
        print(function_response)

        second_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=[
                {"role": "system", "content": "Solve the problem provided by the user with step by step instructions."},
                {"role": "user", "content": word_problem},
                message,
                {"role": "function", "name": function_name, "content": function_response}
            ],
            functions=functions,
            function_call="auto",
        )

        return second_response["choices"][0]["message"]["content"]
    else:
        return message["content"]

