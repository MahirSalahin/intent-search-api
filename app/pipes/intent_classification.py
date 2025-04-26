from transformers import pipeline
from pipes.utils.semantics import keywords_for_semantics
pipe = pipeline("text-classification", model="roundspecs/minilm-finetuned-intent-classification")

def classify_intent(text: str) -> str:
    """
    Classify the intent of a given text using a pre-trained model.

    Args:
        text (str): The input text to classify.

    Returns:
        str: The predicted intent label.
    """
    for keyword in keywords_for_semantics:
        if keyword in text.lower():
            return "semantic"
    result = pipe(text)
    return result[0]['label']

if __name__ == "__main__":
    # Example usage
    text = "Find me a red dress under $50"
    intent = classify_intent(text)
    print(f"Predicted intent: {intent}")

    # Example usage
    text = "Macbook pro 16 inch"
    intent = classify_intent(text)
    print(f"Predicted intent: {intent}")