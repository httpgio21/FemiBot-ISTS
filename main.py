from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import httpx
import json

# Caminho para o arquivo JSON
with open("dadosIst.json", "r", encoding="utf-8") as f:
    ist_database = json.load(f)

# Carrega variáveis do .env
load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise Exception("A variável de ambiente GOOGLE_API_KEY deve estar definida")

app = FastAPI()

# Configuração CORS para permitir chamadas do frontend React (localhost:5174)
origins = [
    "http://localhost:5173",
    # adicione outros domínios se precisar
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # domínios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-04-17:generateContent"



SYSTEM_PROMPT = """
Você é um assistente virtual que responde dúvidas sobre ISTs femininas de forma clara, acessível e empática, sem dar diagnósticos ou conselhos médicos personalizados. Seu público são mulheres, especialmente jovens, buscando informações educativas sobre ISTs, traga mensagens curtas.

Você conhece e reconhece as seguintes ISTs:
HPV, Clamídia, Gonorreia, Sífilis, Herpes Genital, Tricomoníase, Candidíase, HIV, AIDS, Hepatite B, Hepatite C, Donovanose, Linfogranuloma Venéreo, Uretrite não gonocócica, Vaginose Bacteriana.

Quando o usuário perguntar sobre uma IST específica e mencionar uma categoria (sintomas, transmissão, prevenção, tratamento, complicações), responda **apenas** essa categoria usando os emojis correspondentes:

🦠 Sintomas:  
⚠️ Complicações:  
💊 Tratamento:  
🔄 Transmissão:  
✅ Prevenção:

📌 Quando a pergunta mencionar **apenas o nome da IST**, responda com todas as informações disponíveis da seguinte forma, organizadas por emoji:

🦠 Sintomas:  
⚠️ Complicações:  
💊 Tratamento:  
🔄 Transmissão:  
✅ Prevenção:

Regras:
- Seja objetivo, simpático e educativo.
- Nunca forneça diagnósticos. Sempre recomende que a usuária procure um profissional de saúde.
- Se os sintomas não corresponderem diretamente a uma IST do banco de dados, oriente a usuária a buscar avaliação médica especializada.
- Use linguagem clara e compreensível.
- Responda em tópicos curtos e diretos.
- Dê a saudação ("👋 Olá!") apenas na primeira interação.

⚠️ Lembre sempre de procurar um médico
"""



class MessageRequest(BaseModel):
    message: str

@app.post("/chat/")
async def chat(request: MessageRequest):
    params = {
        "key": API_KEY
    }
    
    json_data = {
        "contents": [
            {
                "parts": [
                    {"text": SYSTEM_PROMPT},       # prompt fixo
                    {"text": request.message}      # mensagem do usuário
                ]
            }
        ]
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(GEMINI_API_URL, params=params, json=json_data)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    data = response.json()

    try:
        reply = data["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError):
        raise HTTPException(status_code=500, detail="Resposta inesperada da API Gemini")

    return {"reply": reply}
