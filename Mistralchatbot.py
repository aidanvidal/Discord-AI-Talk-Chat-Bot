from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
import os
from dotenv import load_dotenv

load_dotenv()

#Open file contents
def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()

#Talk with MistralAI chatbot
def chatbot(userinput, conversation):
    chatbotprompt = open_file("prompt.txt")
    apikey = os.getenv("MISTRAL")
    model = "mistral-tiny"

    client = MistralClient(api_key=apikey)
    
    #Limit converstation to only x previous statements
    limit = 2 # Change this to limit the conversation length, Each conversation is 2 statements so 2*limit is the number of statements
    if len(conversation) > limit:
        conversation = conversation[limit:len(conversation)+1] # If you want zero conversations remebered then change this to conversation = []

    #Creates the message to send to the model based on the conversation and prompt
    conversation.append(ChatMessage(role="user", content=userinput))
    message = conversation.copy()
    prompt = [ChatMessage(role="system", content=chatbotprompt)]
    message.insert(0, prompt[0])

    #No Streaming
    chatresopnse = client.chat(
        model=model,
        messages=message
    )
    conversation.append(ChatMessage(role="assistant", content=chatresopnse.choices[0].message.content))
    return chatresopnse.choices[0].message.content, conversation