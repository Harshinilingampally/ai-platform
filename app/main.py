import uuid

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Doc QA Service")

documents: dict[str, str] = {}


class DocumentIn(BaseModel):
    text: str


class DocumentOut(BaseModel):
    id: str
    length: int


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/documents", response_model=DocumentOut)
def create_document(doc: DocumentIn):
    if not doc.text.strip():
        raise HTTPException(status_code=400, detail="text must not be empty")
    doc_id = str(uuid.uuid4())
    documents[doc_id] = doc.text
    return DocumentOut(id=doc_id, length=len(doc.text))


@app.get("/documents/{doc_id}", response_model=DocumentOut)
def get_document(doc_id: str):
    text = documents.get(doc_id)
    if text is None:
        raise HTTPException(status_code=404, detail="document not found")
    return DocumentOut(id=doc_id, length=len(text))