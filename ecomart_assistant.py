from openai import OpenAI
from dotenv import load_dotenv
from time import sleep
from helpers import *
from select_persona import *
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
model = "gpt-4.1-nano"
context = load("data/ecomart.txt")


def create_conversation():
  conv = client.conversations.create()
  
  return conv.id


def send_message(conversation, prompt):
  assistant = client.responses.create(
    model=model,
    instructions=f"""
          Você é um chatbot de atendimento a clientes de um e-commerce. 
          Você não deve responder perguntas que não sejam dados do ecommerce informado!
          Além disso, adote a persona abaixo para responder ao cliente.
          
          ## Contexto
          {context}
          
          ## Persona
          
          {personas["neutro"]}
      """,
      conversation=conversation,
      input=[
        {"role": "user", "content": prompt}
      ]
  )

  return assistant