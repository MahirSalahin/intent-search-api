from transformers import pipeline

pipe = pipeline("ner", model='roundspecs/minilm-finetuned-ner', aggregation_strategy="simple")

def extract_entities(text: str) -> list:
    """
    Extract named entities from a given text using a pre-trained model.

    Args:
        text (str): The input text to extract entities from.

    Returns:
        list: A list of dictionaries containing the extracted entities and their labels.
    """
    result = pipe(text)
    return [{"entity": entity['entity_group'], "word": entity['word']} for entity in result]

if __name__ == "__main__":
    # Example usage
    text = "Samsung smartphones between 10000 and 20000 BDT in red color"
    entities = extract_entities(text)
    print(entities)