from transformers import pipeline

pipe = pipeline("text-classification", model="roundspecs/minilm-finetuned-intent-classification")

def classify_intent(text: str) -> str:
    """
    Classify the intent of a given text using a pre-trained model.

    Args:
        text (str): The input text to classify.

    Returns:
        str: The predicted intent label.
    """
    result = pipe(text)
    return result[0]['label']