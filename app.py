from flask import Flask,render_template, request, session
from openai import OpenAI
from dotenv import load_dotenv
from time import sleep
from helpers import *
from select_persona import *
from select_document import *
from ecomart_assistant import *
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
model = "gpt-4.1-nano"

app = Flask(__name__)
app.secret_key = 'alura'

conversation = create_conversation()


def get_conv_id():
  if "conversation_id" not in session:
    session["conversation_id"] = conversation

  return session["conversation_id"]


def bot(prompt):
  max_attempts = 1
  loop = 0

  while True:
    try:
      response = send_message(conversation, prompt)

      return response.output_text
    except Exception as e:
      loop += 1
      if loop >= max_attempts:
        return f"Erro no GPT {e}"
      
      print("Erro de comunicação com OpenAI: ", e)
      sleep(1)

@app.route("/chat", methods=["POST"])
def chat():
  prompt = request.json["msg"]
  response = bot(prompt)
  
  return response.output_text

@app.route("/")
def home():
  return render_template("index.html")

if __name__ == "__main__":
  app.run(debug = True)
