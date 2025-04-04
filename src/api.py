from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import csv
import os
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Operadoras API", version="1.0")

origins = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Operadora(BaseModel):
    registro_ans: str
    razao_social: str
    cnpj: str
    modalidade: str

operadoras: list[Operadora] = []

def load_operadoras(csv_path: str) -> None:
    if not os.path.exists(csv_path):
        print(f"Arquivo {csv_path} não encontrado!")
        return

    with open(csv_path, mode="r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f, delimiter=';')
        print("Colunas do CSV:", reader.fieldnames)
        for row in reader:
            operadoras.append(Operadora(
                registro_ans=row["Registro_ANS"].strip(),
                razao_social=(row.get("Razão_Social") or row.get("Razao_Social") or "").strip(),
                cnpj=row["CNPJ"].strip(),
                modalidade=row["Modalidade"].strip()
            ))
    print(f"Carregadas {len(operadoras)} operadoras.")

@app.on_event("startup")
def startup_event():

    csv_file = "../Data/Relatorio_cadop_utf8.csv"
    load_operadoras(csv_file)

@app.get("/operadoras", response_model=list[Operadora])
def search_operadoras(q: str = Query("", description="Termo para busca na razão social")):
    if not q:
        return operadoras
    results = [op for op in operadoras if q.lower() in op.razao_social.lower()]
    if not results:
        raise HTTPException(status_code=404, detail="Operadora não encontrada")
    return results

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
