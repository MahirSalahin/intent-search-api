from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_text(text: str) -> list:
    """
    Embed a given text using a pre-trained SentenceTransformer model.

    Args:
        text (str): The input text to embed.

    Returns:
        list: The embedded representation of the input text.
    """
    return model.encode(text).tolist()