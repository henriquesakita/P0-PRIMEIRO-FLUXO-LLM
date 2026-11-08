import os
import sys
import json
from dotenv import load_dotenv
from openai import OpenAI
from prompt import PROMPT_SISTEMA

load_dotenv()

VARIAVEIS_OBRIGATORIAS = ["NVIDIA_API_KEY", "NVIDIA_BASE_URL", "MODEL_NAME"]

faltando = []
for nome in VARIAVEIS_OBRIGATORIAS:
    if not os.getenv(nome):
        faltando.append(nome)
if faltando:
    sys.exit("Erro: defina no arquivo .env: " + ", ".join(faltando))

if len(sys.argv) < 2:
    sys.exit("Uso: python main.py caminho/do/texto.txt")

caminho = sys.argv[1]


cliente = OpenAI(
    base_url=os.getenv("NVIDIA_BASE_URL"),
    api_key=os.getenv("NVIDIA_API_KEY"),
)

try:
    with open(caminho, encoding="utf-8") as arquivo:
        texto = arquivo.read().strip()
except FileNotFoundError:
    sys.exit(f"Erro: arquivo '{caminho}' não encontrado.")

resposta = cliente.chat.completions.create(
    model=os.getenv("MODEL_NAME"),
    messages=[
        {"role": "system", "content": PROMPT_SISTEMA},
        {"role": "user", "content": f"Crie 3 questões a partir deste texto:\n\n{texto}"},
    ],
    temperature=0.3,
    max_tokens=3000,
)

print("finish_reason:", resposta.choices[0].finish_reason)
conteudo = resposta.choices[0].message.content
print("----- resposta bruta -----")
print(conteudo)

print("----- teste de JSON -----")
try:
    dados = json.loads(conteudo)
    print("JSON válido. Questões recebidas:", len(dados["questoes"]))
except json.JSONDecodeError as erro:
    print("JSON inválido:", erro)

