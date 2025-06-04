from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import httpx

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
Você é um assistente especializado em informações sobre Infecções Sexualmente Transmissíveis (ISTs) em mulheres. Responda perguntas com base nos seguintes dados estruturados.

Sua função é:
1. Analisar os sintomas descritos pela usuária.
2. Listar as ISTs mais compatíveis com os sintomas mencionados.
3. Para cada IST compatível, apresentar as informações no seguinte formato padronizado:

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

Base de dados de ISTs:

[
  {
    "Nome": "HPV",
    "Sintomas_em_Mulheres": "Verrugas genitais, lesões no colo do útero, coceira",
    "Complicações": "Câncer de colo do útero, vulva e vagina",
    "Tratamento": "Controle das lesões, monitoramento periódico",
    "Transmissão": "Contato pele com pele, sexo oral, vaginal ou anal",
    "Prevenção": "Vacinação, uso de preservativo, exames ginecológicos"
  },
  {
    "Nome": "Clamídia",
    "Sintomas_em_Mulheres": "Corrimento vaginal anormal, dor pélvica, sangramento fora do ciclo, dor ao urinar",
    "Complicações": "Doença inflamatória pélvica, infertilidade",
    "Tratamento": "Antibiótico sob prescrição médica",
    "Transmissão": "Sexo vaginal, anal ou oral desprotegido",
    "Prevenção": "Preservativo, exames regulares, testagem de parceiros"
  },
  {
    "Nome": "Gonorreia",
    "Sintomas_em_Mulheres": "Corrimento amarelado, dor ao urinar, dor abdominal, sangramento entre menstruações",
    "Complicações": "Infertilidade, gravidez ectópica",
    "Tratamento": "Antibiótico sob prescrição médica",
    "Transmissão": "Sexo vaginal, anal ou oral desprotegido",
    "Prevenção": "Preservativo, testagem, educação sexual"
  },
  {
    "Nome": "Sífilis",
    "Sintomas_em_Mulheres": "Ferida indolor, manchas no corpo, lesões internas",
    "Complicações": "Comprometimento cardíaco, neurológico, fetal",
    "Tratamento": "Antibiótico injetável supervisionado por profissional",
    "Transmissão": "Contato sexual direto, da mãe para o feto",
    "Prevenção": "Preservativo, pré-natal, diagnóstico precoce"
  },
  {
    "Nome": "Herpes Genital",
    "Sintomas_em_Mulheres": "Bolhas ou feridas dolorosas, coceira, queimação",
    "Complicações": "Crises recorrentes, risco de transmissão neonatal",
    "Tratamento": "Uso contínuo de antivirais para controle dos sintomas",
    "Transmissão": "Contato com feridas ativas durante o sexo",
    "Prevenção": "Preservativo (parcial), evitar contato com lesões ativas"
  },
  {
    "Nome": "Tricomoníase",
    "Sintomas_em_Mulheres": "Corrimento espumoso com odor forte, coceira, dor ao urinar",
    "Complicações": "Parto prematuro, maior risco de outras ISTs",
    "Tratamento": "Tratamento com antibiótico e abstinência durante o período",
    "Transmissão": "Sexo vaginal desprotegido, compartilhamento de toalhas íntimas",
    "Prevenção": "Preservativo, higiene íntima adequada"
  },
  {
    "Nome": "Candidíase",
    "Sintomas_em_Mulheres": "Corrimento branco espesso, coceira intensa, vermelhidão",
    "Complicações": "Desconforto recorrente, infecções secundárias",
    "Tratamento": "Uso de antifúngicos tópicos ou orais, dependendo da gravidade",
    "Transmissão": "Desequilíbrio da flora vaginal (não é IST, mas pode ser agravada por sexo)",
    "Prevenção": "Higiene íntima, roupas leves, controle de fatores de risco"
  },
  {
    "Nome": "HIV",
    "Sintomas_em_Mulheres": "Fadiga, febre, infecções recorrentes, perda de peso (quando não tratado). Muitas vezes é assintomático nas fases iniciais.",
    "Complicações": "Enfraquecimento progressivo do sistema imunológico, predisposição a infecções e desenvolvimento de AIDS se não tratado.",
    "Tratamento": "Terapia antirretroviral contínua e acompanhamento médico para manter a carga viral indetectável.",
    "Transmissão": "Sangue, sêmen, secreções vaginais, leite materno, compartilhamento de seringas, sexo desprotegido, da mãe para o bebê na gestação, parto ou amamentação.",
    "Prevenção": "Uso de preservativo, testagem regular, PrEP (profilaxia pré-exposição), PEP (profilaxia pós-exposição), não compartilhar objetos perfurocortantes."
  },
  {
    "Nome": "AIDS",
    "Sintomas_em_Mulheres": "Infecções oportunistas como pneumonia, tuberculose, candidíase oral persistente, perda acentuada de peso, febres recorrentes, diarreia crônica e lesões na pele.",
    "Complicações": "Doenças oportunistas graves, cânceres relacionados (como sarcoma de Kaposi e linfomas), comprometimento neurológico e morte se não tratada.",
    "Tratamento": "Terapia antirretroviral contínua para controle do HIV e tratamento específico para cada doença oportunista que surgir.",
    "Transmissão": "A AIDS não é transmitida diretamente. Ela é consequência da infecção prolongada e não tratada pelo HIV.",
    "Prevenção": "Prevenção da AIDS é feita evitando a infecção pelo HIV ou mantendo o HIV controlado com tratamento adequado."
  },
  {
    "Nome": "Hepatite B",
    "Sintomas_em_Mulheres": "Náuseas, dor abdominal, icterícia, urina escura",
    "Complicações": "Doença hepática crônica, cirrose",
    "Tratamento": "Acompanhamento com antivirais e monitoramento hepático",
    "Transmissão": "Sangue, sexo desprotegido, compartilhamento de objetos",
    "Prevenção": "Vacinação, preservativo, evitar compartilhamento de objetos cortantes"
  },
  {
    "Nome": "Hepatite C",
    "Sintomas_em_Mulheres": "Assintomática inicialmente; pode causar cansaço, icterícia",
    "Complicações": "Cirrose hepática, câncer de fígado",
    "Tratamento": "Tratamento com antivirais específicos e controle médico",
    "Transmissão": "Contato com sangue contaminado, raramente por sexo",
    "Prevenção": "Evitar compartilhamento de seringas, testagem de sangue"
  },
  {
    "Nome": "Donovanose",
    "Sintomas_em_Mulheres": "Úlceras genitais de aparência carnosa, sangramento fácil",
    "Complicações": "Destruição de tecidos genitais, deformidades",
    "Tratamento": "Antibiótico de longa duração com acompanhamento",
    "Transmissão": "Sexo vaginal ou anal com contato direto com lesões",
    "Prevenção": "Preservativo, higiene, diagnóstico precoce"
  },
  {
    "Nome": "Linfogranuloma Venéreo",
    "Sintomas_em_Mulheres": "Inflamação dos gânglios linfáticos genitais, feridas",
    "Complicações": "Drenagem purulenta, cicatrizes e obstruções linfáticas",
    "Tratamento": "Antibiótico específico, drenagem de linfonodos se necessário",
    "Transmissão": "Sexo desprotegido, contato com secreções infectadas",
    "Prevenção": "Preservativo, identificação e tratamento precoce"
  },
  {
    "Nome": "Uretrite não gonocócica",
    "Sintomas_em_Mulheres": "Corrimento uretral, dor ao urinar, coceira",
    "Complicações": "Infecções persistentes, complicações pélvicas",
    "Tratamento": "Tratamento medicamentoso orientado por profissional",
    "Transmissão": "Sexo desprotegido, contato com secreções uretrais",
    "Prevenção": "Preservativo, boa higiene, evitar múltiplos parceiros"
  },
  {
    "Nome": "Vaginose Bacteriana",
    "Sintomas_em_Mulheres": "Corrimento vaginal com odor forte, irritação",
    "Complicações": "Desequilíbrio da flora vaginal, infecções recorrentes",
    "Tratamento": "Tratamento antibacteriano e correção da flora vaginal",
    "Transmissão": "Desequilíbrio bacteriano, sexo, duchas vaginais frequentes",
    "Prevenção": "Higiene íntima, evitar duchas vaginais, uso de preservativos"
  }
]
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
