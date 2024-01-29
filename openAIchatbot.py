import openai
import os
import dotenv

dotenv.load_dotenv()
openai.api_key = os.getenv("OPENAI")

def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()

def simplechat(message,conversation):
    prompt = open_file('prompt.txt')
    
    #Limit converstation to only x previous statements
    limit = 2 # Change this to limit the conversation length, Each conversation is 2 statements so 2*limit is the number of statements
    if len(conversation) > limit:
        conversation = conversation[limit:len(conversation)+1] # If you want zero conversations remebered then change this to conversation = []
        
    #Add input message to conversation
    conversation.append(
		{"role": "user", "content": message},
    )
    
	#Create message to give model
    messagesinput = conversation.copy()
    
	#Add prompt to message
    promptinput = [{"role": "system", "content": prompt}]
    messagesinput.insert(0,promptinput[0])
    
	#Ask model
    chat = openai.ChatCompletion.create(
			model="gpt-3.5-turbo", 
			messages=messagesinput
		)
    reply = chat.choices[0].message.content
    
	#Add model's response to conversation
    conversation.append({"role": "assistant", "content": reply})
    return reply, conversation