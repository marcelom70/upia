from pydantic import BaseModel, EmailStr
from typing import Optional, List

class CandidaturaBase(BaseModel):
    descricao: str

class CandidaturaCreate(CandidaturaBase):
    pass

class Candidatura(CandidaturaBase):
    id: int
    candidato_id: int

    class Config:
        from_attributes = True

class CandidatoBase(BaseModel):
    nome: str
    telefone: str
    email: Optional[str] = None

class CandidatoCreate(CandidatoBase):
    pass

class Candidato(CandidatoBase):
    id: int
    candidaturas: List[Candidatura] = []

    class Config:
        from_attributes = True

class VagaBase(BaseModel):
    descricao: str

class VagaCreate(VagaBase):
    pass

class Vaga(VagaBase):
    id: int
    empresa_id: int

    class Config:
        from_attributes = True

class EmpresaBase(BaseModel):
    nome: str
    telefone: str
    email: str
    endereco: str

class EmpresaCreate(EmpresaBase):
    pass

class Empresa(EmpresaBase):
    id: int
    vagas: List[Vaga] = []

    class Config:
        from_attributes = True 

class ChatPergunta(BaseModel):
    pergunta: str
    tipo_usuario: str  # "candidato" ou "empresa"

class ChatResposta(BaseModel):
    resposta: str 