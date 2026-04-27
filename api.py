from fastapi import FastAPI
from pydantic import BaseModel
import openai
from pinecone import Pinecone
import os

openai.api_key = os.getenv("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")

pc = Pinecone(api_key=os.getenv("https://real-estate-y1lrj3c.svc.aped-4627-b74a.pinecone.io"))
index = pc.Index("real-estate")

app = FastAPI()

class Land(BaseModel):
    id: str
    tinh: str
    huyen: str
    xa: str
    gia: int
    dien_tich: float
    tieu_de: str
    mo_ta: str
    diem_noi_bat: str
    tu_khoa: str
    link_anh: str

@app.post("/sync")
def sync_land(land: Land):

    text = f"""
    Đất tại {land.xa}, {land.huyen}, {land.tinh}.
    Diện tích {land.dien_tich}m2, giá {land.gia} VNĐ.

    {land.tieu_de}
    {land.mo_ta}
    {land.diem_noi_bat}
    {land.tu_khoa}
    """

    embedding = openai.embeddings.create(
        model="text-embedding-3-small",
        input=text
    ).data[0].embedding

    index.upsert([
        (land.id, embedding, {
            "tinh": land.tinh,
            "huyen": land.huyen,
            "xa": land.xa,
            "gia": land.gia,
            "dien_tich": land.dien_tich,
            "tieu_de": land.tieu_de,
            "link_anh": land.link_anh
        })
    ])

    return {"ok": True}