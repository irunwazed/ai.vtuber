import json
import ollama # type: ignore

# MODEL = "llama3.2" # "deepseek-r1:8b" # "llama3.2"

def ollama_chat(text, model = "deepseek-r1:8b"):
  result = "Maaf saya tidak mengerti!"
  try:
    conversation = []
    conversation.append({"role": "user", "content": text})
    response = ollama.chat(model=model, messages=conversation)
    result = response['message']['content']
  except Exception as e:
    print("ERROR : ", e)
  return result

def chat_with_ollama():
  print("Start chatting with Ollama. Type 'exit' to quit.\n")
  conversation_history = []

  while True:
    user_input = input("You: ")
    
    if user_input.lower() == 'exit':
      print("Exiting the conversation.")
      break

    try:
      conversation_history.append({"role": "user", "content": user_input})
      response = ollama.chat(model="llama3.2", messages=conversation_history)
      
      ollama_response = response['message']['content']
      print(f"Ollama: {ollama_response}")

      conversation_history.append({"role": "assistant", "content": ollama_response})
      with open("temp/conversation_history.json", "w") as history_file:
        json.dump(conversation_history, history_file, indent=4)
  
    except Exception as e:
      print(f"Error occurred: {e}")
      break