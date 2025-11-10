import base64
import cv2
import numpy as np


def load(file_name):
  try:
    with open(file_name, "r") as file:
      return file.read()
  except IOError as e:
    print(f"erro ao tentar ler arquivo: {e}")


def save(file_name, content):
  try:
    with open(file_name, "w", encoding="utf-8") as file:
      file.write(content)
  except IOError as e:
    print(f"erro ao tentar salvar arquivo: {e}")

