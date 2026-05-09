import os
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types
from prompts import *
from call_function import *
from functions.get_file_content import *
from functions.get_files_info import *
from functions.run_python_file import *
from functions.write_file import *

def generate_content(client, messages, verbose):
    #can edit model here if needed
    model = "gemini-2.5-flash"
    generated_content = client.models.generate_content(
        model=model, 
        contents=messages, 
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            tools=[available_functions],
            temperature=0
        ),
    )
    
    #add candidates to messages
    if generated_content.candidates:
        for candidate in generated_content.candidates:
            messages.append(candidate.content)

    #print the generated response & number of tokens
    if generated_content.usage_metadata is not None:
        if verbose:
            print(f"User prompt: {messages[-1].parts[-1].text}")
            print(f"Prompt tokens: {generated_content.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {generated_content.usage_metadata.candidates_token_count}")

        if not generated_content.function_calls:
            print(f"Response: {generated_content.text}")
            return False
        else:
            func_responses = []
            for func_call in generated_content.function_calls:
                function_call_result = call_function(func_call, verbose)
                if function_call_result.parts is None or len(function_call_result.parts) == 0:
                    raise Exception("Error: function call result not reported")
                if function_call_result.parts[0].function_response is None:
                    raise Exception("Error: function call result is none")
                if function_call_result.parts[0].function_response.response is None:
                    raise Exception("Error: function call result string is none")
                if verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
                func_responses.append(function_call_result.parts[0])
        
            #add results from function calls & the model to messages
            messages.append(types.Content(role="user", parts=func_responses))
            return True
    else:
        raise RuntimeError("Response has empty usage metadata, likely a failed API request")


def main():
    #load api key, set up model
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None: raise RuntimeError("Gemini API key not found")
    client = genai.Client(api_key=api_key)
    
    #read args from command line
    parser = argparse.ArgumentParser(description="chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    
    #parse & handle args (note: load prompt into content list, history for client)
    args = parser.parse_args()
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    verbose = args.verbose

    #generate
    cont = True
    for _ in range(20):
        cont = generate_content(client, messages, verbose)
        if not cont: break
    if cont: raise Exception("Max number of iterations reached without solving prompt")



if __name__ == "__main__":
    main()
