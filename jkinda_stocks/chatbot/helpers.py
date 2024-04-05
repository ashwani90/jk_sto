import openai 

def get_reply(message):

    openai.api_base = "http://localhost:4891/v1"
    openai.api_key = "not needed for a local LLM"

    # Set up the prompt and other parameters for the API request
    prompt = message

    # model = "gpt-3.5-turbo"
    #model = "mpt-7b-chat"
    #model = "gpt4all-j-v1.3-groovy"
    model = "nomic-ai/gpt4all-falcon"

    # Make the API request
    response = openai.Completion.create(
        model=model,
        prompt=prompt,
        max_tokens=50,
        temperature=0.28,
        top_p=0.95,
        n=1,
        echo=True,
        stream=False # <--- this is the line that I changed
    )

    # Print the generated completion
    result = ''
    result = response.get('choices')[0].text.split("\n")[1]
    return result
    