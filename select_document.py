from openai import OpenAI
from dotenv import load_dotenv
from time import sleep
from helpers import *
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
model = "gpt-4.1-nano"

ecomart_politics = load("data/politicas_ecomart.txt")
ecomart_data = load("data/dados_ecomart.txt")
ecomart_products = load("data/produtos_ecomart.txt")


def select_document(context):
  if "políticas" in context:
    return ecomart_data + "\n" + ecomart_politics
  elif "produtos" in context:
    return ecomart_data + "\n" + ecomart_products
  
  return ecomart_data


def select_context(user_prompt):
  instructions = f"""
    A empresa EcoMart possui três documentos principais que detalham diferentes aspectos do negócio:

    #Documento 1 "\n {ecomart_data} "\n"
    #Documento 2 "\n" {ecomart_politics} "\n"
    #Documento 3 "\n" {ecomart_products} "\n"

    Avalie o prompt do usuário e retorne o documento mais indicado para ser usado no contexto da resposta. Retorne dados se for o Documento 1, políticas se for o Documento 2 e produtos se for o Documento 3.
    """
  
  response = client.responses.create(
    model=model,
    instructions=instructions,
    input=[
      {"role":"user", "content":user_prompt}
    ]
  )
  
  return response.output_text.lower()