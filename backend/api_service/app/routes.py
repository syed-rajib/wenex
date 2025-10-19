from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.elastic_client import es

router = APIRouter()


# ---------- Models ----------
class Item(BaseModel):
    id: str
    title: str
    description: str


# ---------- Routes ----------
@router.get("/")
async def home():
    return {"message": "Welcome to API Services"}


@router.post("/items")
async def create_item(item: Item):
    """Insert a document into Elasticsearch"""
    try:
        res = es.index(index="items", id=item.id, document=item.dict())
        return {"result": res["result"], "id": item.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/items/{item_id}")
async def get_item(item_id: str):
    """Fetch a document by ID"""
    try:
        if not es.exists(index="items", id=item_id):
            raise HTTPException(status_code=404, detail="Item not found")
        res = es.get(index="items", id=item_id)
        return res["_source"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/items/{item_id}")
async def update_item(item_id: str, item: Item):
    """Update a document by ID"""
    try:
        if not es.exists(index="items", id=item_id):
            raise HTTPException(status_code=404, detail="Item not found")
        res = es.update(index="items", id=item_id, doc=item.dict())
        return {"result": res["result"], "id": item_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/items/{item_id}")
async def delete_item(item_id: str):
    """Delete a document by ID"""
    try:
        if not es.exists(index="items", id=item_id):
            raise HTTPException(status_code=404, detail="Item not found")
        res = es.delete(index="items", id=item_id)
        return {"result": res["result"], "id": item_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/items/search/{query}")
async def search_items(query: str):
    """Search documents by title or description"""
    try:
        res = es.search(
            index="items",
            query={
                "multi_match": {
                    "query": query,
                    "fields": ["title", "description"]
                }
            }
        )
        return [hit["_source"] for hit in res["hits"]["hits"]]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
