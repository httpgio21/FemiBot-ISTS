from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import httpx
import json
from rapidfuzz import process

# Carregar banco de dados IST (se quiser usar futuramente)
with open("dadosIst.json", "r", encoding="utf-8") as f:
    ist_database = json.load(f)

# Carregar variáveis do .env
load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise Exception("A variável de ambiente GOOGLE_API_KEY deve estar definida")

app = FastAPI()

# Configuração CORS para seu frontend React
origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-04-17:generateContent"

SYSTEM_PROMPT = """
Você é um assistente virtual que responde dúvidas sobre ISTs femininas de forma clara, acessível e empática, sem dar diagnósticos ou conselhos médicos personalizados. Seu público são mulheres, especialmente jovens, buscando informações educativas sobre ISTs, traga mensagens curtas.

Você conhece e reconhece as seguintes ISTs:
HPV, Clamídia, Gonorreia, Sífilis, Herpes Genital, Tricomoníase, Candidíase, HIV, AIDS, Hepatite B, Hepatite C, Donovanose, Linfogranuloma Venéreo, Uretrite não gonocócica, Vaginose Bacteriana.


- Dê a saudação ("👋 Olá!") apenas na primeira interação.
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


⚠️ Lembre sempre de procurar um médico
"""

# Lista oficial das ISTs reconhecidas para fuzzy matching
ist_list = [
    "HPV", "Clamídia", "Gonorreia", "Sífilis", "Herpes Genital",
    "Tricomoníase", "Candidíase", "HIV", "AIDS", "Hepatite B",
    "Hepatite C", "Donovanose", "Linfogranuloma Venéreo",
    "Uretrite não gonocócica", "Vaginose Bacteriana"
]

FUZZY_SCORE_THRESHOLD = 70

class MessageRequest(BaseModel):
    message: str

@app.post("/chat/")
async def chat(request: MessageRequest):
    user_message = request.message

    # Fuzzy matching para identificar IST no texto do usuário
    match = process.extractOne(user_message, ist_list, score_cutoff=FUZZY_SCORE_THRESHOLD)

    if match:
        ist_encontrada = match[0]
        prompt_extra = f"\n\nNota: O usuário está perguntando sobre a IST '{ist_encontrada}'. Por favor, responda focando nela conforme as regras do sistema."
        prompt_final = SYSTEM_PROMPT + prompt_extra
    else:
        prompt_final = SYSTEM_PROMPT

    params = {
        "key": API_KEY
    }
    
    json_data = {
        "contents": [
            {
                "parts": [
                    {"text": prompt_final},
                    {"text": user_message}
                ]
            }
        ]
    }

    try:
        async with httpx.AsyncClient(timeout=20) as client:
            response = await client.post(GEMINI_API_URL, params=params, json=json_data)
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail="Erro ao conectar com a API Gemini. Tente novamente mais tarde.")

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    data = response.json()

    try:
        reply = data["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError):
        raise HTTPException(status_code=500, detail="Resposta inesperada da API Gemini")

    return {"reply": reply}
