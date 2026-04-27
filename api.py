from fastapi import FastAPI
from pydantic import BaseModel
import openai
from pinecone import Pinecone
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
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
