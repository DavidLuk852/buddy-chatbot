from huggingface_hub import InferenceClient

def get_bot_response(user_message):
    client = InferenceClient(token="")  # Replace with your token
    messages = [
        {"role": "user", "content": user_message},
    ]
    try:
        response = client.chat_completion(messages, model="meta-llama/Llama-3.1-70B-Instruct")
        return response.choices[0].message.content if response.choices else "No response"
    except Exception as e:
        print(f"Error in API call: {str(e)}")
        return "Error processing request."

if __name__ == "__main__":
    user_input = "Explain quantum mechanics clearly and concisely."
    bot_reply = get_bot_response(user_input)
    print(f"User: {user_input}")
    print(f"Bot: {bot_reply}")