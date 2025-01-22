import json
import ollama # type: ignore

def ollama_chat(text):
  result = "Maaf saya tidak mengerti!"
  try:
    conversation = []
    conversation.append({"role": "user", "content": text})
    response = ollama.chat(model="llama3.2", messages=conversation)
    result = response['message']['content']
  except Exception as e:
    print("ERROR : ", e)
  return result


def chat_with_ollama():
  # Start a conversation with an initial prompt
  print("Start chatting with Ollama. Type 'exit' to quit.\n")

  # Initialize the conversation history
  conversation_history = []

  while True:
    # Take user input
    user_input = input("You: ")
    
    if user_input.lower() == 'exit':
      print("Exiting the conversation.")
      break

    try:
      # Add user input to the conversation history
      conversation_history.append({"role": "user", "content": user_input})

      # Send the user's input to Ollama for processing
      response = ollama.chat(model="llama3.2", messages=conversation_history)
      
      # Get Ollama's response
      ollama_response = response['message']['content']
      print(f"Ollama: {ollama_response}")

      # Add Ollama's response to the conversation history
      conversation_history.append({"role": "assistant", "content": ollama_response})

      # Save the conversation history to a JSON file
      with open("temp/conversation_history.json", "w") as history_file:
        json.dump(conversation_history, history_file, indent=4)
  
    except Exception as e:
      print(f"Error occurred: {e}")
      break