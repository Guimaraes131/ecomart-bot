from flask import Flask,render_template, request, Response
from openai import OpenAI
from dotenv import load_dotenv
from time import sleep
from helpers import *
from select_persona import *
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
model = "gpt-4.1-nano"

app = Flask(__name__)
app.secret_key = 'alura'

context = load("data/ecomart.txt")

def bot(prompt):
  max_attempts = 1
  loop = 0
  persona = personas[select_persona(prompt)]

  while True:
    try:
      instructions = f"""
        Você é um chatbot de atendimento a clientes de um e-commerce.
        Você não deve responder perguntas que não sejam dados do ecommerce informado!
        
        Você deve gerar respostas utilizando o contexto abaixo.

        # Contexto
        {context}
        
        Você deve adotar a persona abaixo.
        
        # Persona
        {persona}
      """
      
      response = client.responses.create(
        model=model,
        instructions=instructions,
        temperature=1,
        max_output_tokens=256,
        top_p=1,
        input=[{"role":"user", "content":prompt}]
      )
      
      return response
      
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
