from transformers import pipeline
from pipes.utils.brands import brands_mapping
from pipes.utils.categories import categories_mapping

pipe = pipeline(
    "ner", model="roundspecs/minilm-finetuned-ner", aggregation_strategy="simple"
)


def extract_entities(text: str) -> list:
    """
    Extract named entities from a given text using a pre-trained model.

    Args:
        text (str): The input text to extract entities from.

    Returns:
        list: A list of dictionaries containing the extracted entities and their labels.
    """
    result = pipe(text)
    return clean_entities(result)


def clean_entities(entities: list) -> dict:
    print(entities)
    result = {
        "CATEGORY": [],
        "PRICE_MAX": "",
        "PRICE_MIN": "",
        "BRAND": [],
    }
    for entity in entities:
        if entity["entity_group"] == "CATEGORY":
            result["CATEGORY"].append(entity["word"])
        elif entity["entity_group"] == "PRICE_MAX":
            result["PRICE_MAX"] += entity["word"]
        elif entity["entity_group"] == "PRICE_MIN":
            result["PRICE_MIN"] += entity["word"]
        elif entity["entity_group"] == "BRAND":
            result["BRAND"].append(entity["word"])

    min_price = result["PRICE_MIN"]
    max_price = result["PRICE_MAX"]
    result["PRICE_MIN"] = ""
    result["PRICE_MAX"] = ""
    for ch in min_price:
        if ch.isdigit():
            result["PRICE_MIN"] += ch
    for ch in max_price:
        if ch.isdigit():
            result["PRICE_MAX"] += ch

    category = set()
    brand = set()

    for cat in result["CATEGORY"]:
        for key, values in categories_mapping.items():
            for value in values:
                if value in cat.lower():
                    category.add(key)

    for br in result["BRAND"]:
        for key, values in brands_mapping.items():
            for value in values:
                if value in br.lower():
                    brand.add(key)

    for cat in result["CATEGORY"]:
        for key, values in brands_mapping.items():
            for value in values:
                if value in cat.lower():
                    brand.add(key)

    result["CATEGORY"] = list(category)
    result["BRAND"] = list(brand)
    result["PRICE_MAX"] = float(result["PRICE_MAX"]) if result["PRICE_MAX"] else None
    result["PRICE_MIN"] = float(result["PRICE_MIN"]) if result["PRICE_MIN"] else None

    reminder = ""
    for entity in entities:
        if entity["entity_group"] not in ["PRICE_MAX", "PRICE_MIN"] and '#' not in entity["word"]:
            reminder += entity["word"] + " "
    result["REMINDER"] = reminder.strip()

    return result


if __name__ == "__main__":
    text = "Samsung smartphones between 10000 and 20000 BDT in red color"
    entities = extract_entities(text)
    print(entities)

    text = "Macbook Pro 16-inch with M1 Pro chip, 16GB RAM, 512GB SSD, and 8-core GPU"
    entities = extract_entities(text)
    print(entities)
