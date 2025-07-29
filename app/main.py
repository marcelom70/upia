from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from . import models, schemas
from .database import engine, get_db
from .services.chat_service import processar_pergunta

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="UPIA - API de Conexão entre Empregados e Empregadores")

# Rotas para Candidatos
@app.post("/candidatos/", response_model=schemas.Candidato)
def create_candidato(candidato: schemas.CandidatoCreate, db: Session = Depends(get_db)):
    db_candidato = models.Candidato(**candidato.dict())
    db.add(db_candidato)
    db.commit()
    db.refresh(db_candidato)
    return db_candidato

@app.get("/candidatos/", response_model=List[schemas.Candidato])
def read_candidatos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    candidatos = db.query(models.Candidato).offset(skip).limit(limit).all()
    return candidatos

@app.get("/candidatos/{candidato_id}", response_model=schemas.Candidato)
def read_candidato(candidato_id: int, db: Session = Depends(get_db)):
    candidato = db.query(models.Candidato).filter(models.Candidato.id == candidato_id).first()
    if candidato is None:
        raise HTTPException(status_code=404, detail="Candidato não encontrado")
    return candidato

# Rotas para Candidaturas
@app.post("/candidatos/{candidato_id}/candidaturas/", response_model=schemas.Candidatura)
def create_candidatura(
    candidato_id: int,
    candidatura: schemas.CandidaturaCreate,
    db: Session = Depends(get_db)
):
    db_candidatura = models.Candidatura(**candidatura.dict(), candidato_id=candidato_id)
    db.add(db_candidatura)
    db.commit()
    db.refresh(db_candidatura)
    return db_candidatura

# Rotas para Empresas
@app.post("/empresas/", response_model=schemas.Empresa)
def create_empresa(empresa: schemas.EmpresaCreate, db: Session = Depends(get_db)):
    db_empresa = models.Empresa(**empresa.dict())
    db.add(db_empresa)
    db.commit()
    db.refresh(db_empresa)
    return db_empresa

@app.get("/empresas/", response_model=List[schemas.Empresa])
def read_empresas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    empresas = db.query(models.Empresa).offset(skip).limit(limit).all()
    return empresas

@app.get("/empresas/{empresa_id}", response_model=schemas.Empresa)
def read_empresa(empresa_id: int, db: Session = Depends(get_db)):
    empresa = db.query(models.Empresa).filter(models.Empresa.id == empresa_id).first()
    if empresa is None:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")
    return empresa

# Rotas para Vagas
@app.post("/empresas/{empresa_id}/vagas/", response_model=schemas.Vaga)
def create_vaga(
    empresa_id: int,
    vaga: schemas.VagaCreate,
    db: Session = Depends(get_db)
):
    db_vaga = models.Vaga(**vaga.dict(), empresa_id=empresa_id)
    db.add(db_vaga)
    db.commit()
    db.refresh(db_vaga)
    return db_vaga

@app.get("/vagas/", response_model=List[schemas.Vaga])
def read_vagas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    vagas = db.query(models.Vaga).offset(skip).limit(limit).all()
    return vagas 

# Rota para o chat
@app.post("/chat/", response_model=schemas.ChatResposta)
def chat(pergunta: schemas.ChatPergunta, db: Session = Depends(get_db)):
    try:
        resposta = processar_pergunta(pergunta.pergunta, db)
        return {"resposta": resposta}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 