import argparse
import os
from functions.call_function import call_function
from dotenv import load_dotenv
from functions.call_function import available_functions
from google import genai
from google.genai import types
from prompts import system_prompt

load_dotenv()

try:
    api_key = os.environ.get("GEMINI_API_KEY")
except RuntimeError:
    print("Please provide a valid Gemini API Key")

parser = argparse.ArgumentParser(description="Prompt for Gemini AI 2.5-flash model.")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

client = genai.Client(api_key=api_key)
messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

def main():
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            tools=[available_functions],
            )    
        )
    if response.usage_metadata != None:
        prompt_tokens = response.usage_metadata.prompt_token_count
        response_tokens = response.usage_metadata.candidates_token_count
    else:
        raise RuntimeError("API request has failed, please retry.")

    if args.verbose == True:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")   
    if response.function_calls == None: 
        print(response.text)
    function_results = []
    for function_call in response.function_calls:
        function_call_result = call_function(function_call)
        if function_call_result.parts == []:
            raise Exception("Error: Expected a non-empty object .parts list")
        if function_call_result.parts[0].function_response == None:
            raise Exception("Error: Expected a FunctionResponse object in the first item of the .parts list")
        if function_call_result.parts[0].function_response.response == None:
            raise Exception("Error: Expected a non-empty response from the function call")
        function_results.append(function_call_result.parts[0])
        if args.verbose == True:
            print(f"-> {function_call_result.parts[0].function_response.response}")

if __name__ == "__main__":
    main()
