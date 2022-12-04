import gtp

chat = gtp.gpt3()

resp = chat.chat(
    "Can you write a python to read data from a public web api, then store the response in a database using a sqlalchemy model?"
)

print(resp)