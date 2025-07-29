import openai
from sqlalchemy.orm import Session
from typing import List, Optional
import json
import os
from .. import models, config

# Configuração do OpenAI
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Funções de consulta ao banco de dados
def buscar_vagas_por_descricao(db: Session, termo: str) -> List[dict]:
    vagas = db.query(models.Vaga, models.Empresa).join(models.Empresa).filter(
        models.Vaga.descricao.ilike(f"%{termo}%")
    ).all()
    
    return [
        {
            "id": vaga.id,
            "descricao": vaga.descricao,
            "empresa": {
                "nome": empresa.nome,
                "email": empresa.email
            }
        }
        for vaga, empresa in vagas
    ]

def buscar_candidatos_por_vaga(db: Session, termo: str) -> List[dict]:
    candidaturas = db.query(
        models.Candidatura,
        models.Candidato,
        models.Vaga
    ).join(
        models.Candidato
    ).join(
        models.Vaga
    ).filter(
        models.Vaga.descricao.ilike(f"%{termo}%")
    ).all()
    
    return [
        {
            "candidato": {
                "nome": candidato.nome,
                "email": candidato.email
            },
            "vaga": {
                "descricao": vaga.descricao
            },
            "candidatura": {
                "descricao": candidatura.descricao
            }
        }
        for candidatura, candidato, vaga in candidaturas
    ]

# Funções disponíveis para o OpenAI
FUNCTIONS = [
    {
        "name": "buscar_vagas",
        "description": "Busca vagas de emprego baseado em um termo de pesquisa",
        "parameters": {
            "type": "object",
            "properties": {
                "termo_busca": {
                    "type": "string",
                    "description": "Termo para buscar nas descrições das vagas"
                }
            },
            "required": ["termo_busca"]
        }
    },
    {
        "name": "buscar_candidatos",
        "description": "Busca candidatos que se candidataram a vagas específicas",
        "parameters": {
            "type": "object",
            "properties": {
                "tipo_vaga": {
                    "type": "string",
                    "description": "Tipo ou descrição da vaga para buscar candidatos"
                }
            },
            "required": ["tipo_vaga"]
        }
    }
]

def processar_pergunta(pergunta: str, db: Session) -> str:
    try:
        # Primeiro, enviamos a pergunta para o OpenAI decidir qual função chamar
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": pergunta}],
            functions=FUNCTIONS,
            function_call="auto"
        )
        
        response_message = response["choices"][0]["message"]
        
        # Se não houver uma chamada de função, retornamos a resposta direta
        if "function_call" not in response_message:
            return "Desculpe, não entendi sua pergunta. Pode reformular?"
            
        # Processamos a chamada da função
        function_call = response_message["function_call"]
        function_name = function_call["name"]
        function_args = json.loads(function_call["arguments"])
        
        # Executamos a função apropriada
        if function_name == "buscar_vagas":
            resultado = buscar_vagas_por_descricao(db, function_args["termo_busca"])
        elif function_name == "buscar_candidatos":
            resultado = buscar_candidatos_por_vaga(db, function_args["tipo_vaga"])
        else:
            return "Função não reconhecida"
            
        # Enviamos o resultado para o OpenAI formatar a resposta
        response_final = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": pergunta},
                {"role": "assistant", "content": None, "function_call": function_call},
                {"role": "function", "name": function_name, "content": json.dumps(resultado)}
            ]
        )
        
        return response_final["choices"][0]["message"]["content"]
        
    except Exception as e:
        return f"Erro ao processar sua pergunta: {str(e)}" 