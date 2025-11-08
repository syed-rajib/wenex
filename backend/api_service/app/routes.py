from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.elastic_client import es
from app.redis_client import r   # 👈 add this import
import json

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
        # Clear cache for search results when data changes (optional)
        r.flushdb()
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
        # Clear cache because data changed
        r.flushdb()
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
        # Clear cache because data changed
        r.flushdb()
        return {"result": res["result"], "id": item_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/items/search/{query}")
async def search_items(query: str):
    """Search documents by title or description, with Redis cache"""
    try:
        # Check cache first
        cached_result = r.get(f"search:{query}")
        if cached_result:
            print("⚡ From Redis Cache")
            return json.loads(cached_result)

        # Otherwise, fetch from Elasticsearch
        print("🔍 From Elasticsearch")
        res = es.search(
            index="items",
            query={
                "multi_match": {
                    "query": query,
                    "fields": ["title", "description"]
                }
            }
        )
        items = [hit["_source"] for hit in res["hits"]["hits"]]

        # Save to cache for 60 seconds
        r.setex(f"search:{query}", 60, json.dumps(items))

        return items

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
