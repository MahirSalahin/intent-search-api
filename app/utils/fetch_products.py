from pipes.embedding import embed_text
from pipes.ner import extract_entities
from pipes.intent_classification import classify_intent
from pinecone import Pinecone, ServerlessSpec
import os
from dotenv import load_dotenv

load_dotenv()


PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
print(f"Pinecone API Key: {PINECONE_API_KEY}")
pc = Pinecone(api_key=PINECONE_API_KEY)

index_name = "tech-products"
index = pc.Index(index_name)

async def fetch_products(
        query: str,
        category: str = None,
        brand: str = None,
        min_price: float = None,
        max_price: float = None,
        sort_by: str = None,
):
    """
    Fetch products from the database.
    """
    intent = classify_intent(query)
    if intent == "semantic":
        return await semantic_search(
            query=query,
            category=category,
            brand=brand,
            price_min=min_price,
            price_max=max_price,
            sort_by=sort_by,
        )
    else:
        return await keyword_search(
            query=query,
            category=category,
            brand=brand,
            min_price=min_price,
            max_price=max_price,
            sort_by=sort_by,
        )

async def semantic_search(
        query: str,
        category: str = None,
        brand: str = None,
        price_min: float = None,
        price_max: float = None,
        sort_by: str = None,
):
    entities = extract_entities(query)
    query_embedding = embed_text(query)

    categories = entities.get("CATEGORY")
    brands = entities.get("BRAND")
    min_price = entities.get("PRICE_MIN")
    max_price = entities.get("PRICE_MAX", None)

    if category is not None:
        categories.append(category)
    if brand is not None:
        brands.append(brand)
    if price_min is not None:
        min_price = min(price_min, min_price)
    if price_max is not None:
        max_price = max(price_max, max_price)

    print(f"Query: {query}")
    print(f"Categories: {categories}, Brands: {brands}, Min Price: {min_price}, Max Price: {max_price}")

    filter = {}

    if min_price is not None:
        filter["price"] = {"$gte": min_price}
    if max_price is not None:
        filter["price"] = {"$lte": max_price}
    if categories is not None:
        filter["category"] = {"$in": categories}
    if brands is not None:
        filter["brand"] = {"$in": brands}

    result = index.query(
        vector=query_embedding,
        top_k=5,
        include_metadata=True,
        # filter=filter
    )

    return [x['id'] for x in result['matches']]

async def keyword_search(
        query: str,
        category: str = None,
        brand: str = None,
        min_price: float = None,
        max_price: float = None,
        sort_by: str = None,
):
    pass

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()

    # Example usage
    query = "Apple iPhone 14 Pro Max"
    result = fetch_products(query)
    print(result)