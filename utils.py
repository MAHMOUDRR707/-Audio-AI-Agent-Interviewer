from transformers import pipeline, AutoProcessor, SeamlessM4Tv2Model
import torchaudio
import torch
import spacy 
import re 
import string
import unicodedata
import inflect
import json
import openai
from config import together_api_key

def load_model():
    """
    Loads and initializes various models for processing.
    
    Returns:
        dict: A dictionary containing:
            - processor: The SeamlessM4T processor.
            - st_model: The SeamlessM4T speech-to-text model.
            - nlp_model: The Spacy NLP model.
            - llama_model: The Llama generation model.
    """
    processor = AutoProcessor.from_pretrained("facebook/seamless-m4t-v2-large")
    st_model = SeamlessM4Tv2Model.from_pretrained("facebook/seamless-m4t-v2-large")
    nlp_model = spacy.load("en_core_web_sm")
    models = {
        "processor": processor,
        "st_model": st_model,
        "nlp_model": nlp_model,
        "llama_model": load_generation_model(),
    }
    return models


def load_audio(path):
    """
    Loads an audio file using Torchaudio.

    Args:
        path (str): Path to the audio file.

    Returns:
        tuple: A tuple containing the waveform tensor and sample rate.
    """
    audio = torchaudio.load(path)
    return audio


def load_text(path):
    """
    Loads text data from a JSON file.

    Args:
        path (str): Path to the JSON file.

    Returns:
        tuple: A tuple containing:
            - questions (list): List of question texts.
            - max_scores (list): List of maximum scores.
            - competencies (list): List of competencies.
    """
    with open(path, "rb") as f:
        text = json.load(f)
    questions, max_scores, competencies = extract_text_from_json(text)
    return questions, max_scores, competencies


def clean_text(text):
    """
    Cleans and preprocesses input text by normalizing, expanding contractions,
    removing punctuation, converting numbers to words, and removing accents.

    Args:
        text (str): The text to clean.

    Returns:
        str: The cleaned text.
    """
    text = text.lower()
    text = re.sub(r"\r", "", text)

    contractions = {
        "i'm": "i am", "he's": "he is", "she's": "she is", "it's": "it is",
        "that's": "that is", "what's": "what is", "where's": "where is",
        "how's": "how is", "won't": "will not", "can't": "cannot",
        "n't": " not", "'ll": " will", "'ve": " have", "'re": " are",
        "'d": " would", "n'": "ng", "'bout": "about", "'til": "until"
    }
    for contraction, expansion in contractions.items():
        text = re.sub(contraction, expansion, text)

    text = text.translate(str.maketrans("", "", string.punctuation))

    p = inflect.engine()
    words = text.split()
    text = " ".join([p.number_to_words(word) if word.isdigit() else word for word in words])

    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("utf-8")
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()

    return text


def extract_text_from_json(json_data):
    """
    Extracts questions, maximum scores, and competencies from JSON data.

    Args:
        json_data (list): A list of JSON objects.

    Returns:
        tuple: A tuple containing:
            - questions (list): List of question texts.
            - max_scores (list): List of maximum scores.
            - competencies (list): List of competencies.
    """
    questions, max_scores, competencies = [], [], []
    for meta_data in json_data:
        questions.append(meta_data["text"])
        max_scores.append(meta_data["max_score"])
        competencies.append(meta_data["competency"])
    return questions, max_scores, competencies


def insert_text_into_json(json_data, questions, max_scores, competencies, input_path):
    """
    Inserts questions, maximum scores, and competencies into a JSON file.

    Args:
        json_data (list): The JSON data to append to.
        questions (list): List of question texts.
        max_scores (list): List of maximum scores.
        competencies (list): List of competencies.
        input_path (str): Path to the JSON file to save the data.
    """
    for i in range(len(questions)):
        json_data.append({
            "id": questions[i],
            "text": questions[i],
            "max_score": max_scores[i],
            "competency": competencies[i]
        })
    with open(input_path, "w") as f:
        json.dump(json_data, f, indent=4)


def load_generation_model():
    """
    Loads the Llama generation model using OpenAI API.

    Returns:
        OpenAI: The initialized Llama model instance.
    """
    _llama_llm = openai.OpenAI(
        api_key=together_api_key,
        base_url="https://api.together.xyz/v1",
    )
    return _llama_llm


def generate_response(llama_llm, answer, system_prompt):
    """
    Generates a response using the Llama language model.

    Args:
        llama_llm (OpenAI): The Llama language model instance.
        answer (str): The user-provided answer.
        system_prompt (str): The system prompt for generating the response.

    Returns:
        tuple: A tuple containing:
            - response (str): The model-generated response.
            - final_score (int): The final score extracted from the response.
    """
    response = llama_llm.chat.completions.create(
        model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
        messages=[{"role": "system", "content": system_prompt},
                  {"role": "user", "content": "Here's the answer of the user: " + answer}],
        temperature=0,
        max_tokens=5000,
    )
    response = response.choices[0].message.content
    final_score = json.loads(response)["final_score"]
    return response, final_score
