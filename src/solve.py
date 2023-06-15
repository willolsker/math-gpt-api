import openai
import json
import functions
import dotenv
import os
dotenv.load_dotenv()


def run_conversation(word_problem):
    steps = []

    openai.api_key = os.getenv("OPENAI_API_KEY")
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=[
            {"role": "system", "content": "Solve the problem provided by the user using a formula."},
            {"role": "user", "content": word_problem},
        ],
        functions=functions.functions,
        function_call="auto",
        temperature=0.2,
    )

    message = response["choices"][0]["message"]
    print(message["function_call"]["arguments"])

    if message.get("function_call"):
        function_name = message["function_call"]["name"]
        function_arguments = json.loads(message["function_call"]["arguments"])

        if function_name == "use_formula":
            steps.append(function_arguments)

            result = functions.use_formula(function_arguments["formula"], function_arguments["values"])
            steps.append(result)

    return steps