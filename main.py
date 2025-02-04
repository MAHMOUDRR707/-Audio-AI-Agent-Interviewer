from utils import load_model, load_audio, load_text, clean_text, generate_response
import subprocess
import sys
from Modules import text_chunking, audio_chunking, text_to_speech, speech_to_text, record_audio, play_audio
from config import scoring_prompt_system
import json
import pandas as pd

"""  
*"For two or more candidates, we will iterate through the same steps below and save the results in a CSV file 
For each candidate would have a seprate folder with his name."*

"""
# Load necessary models for processing
models = load_model()

# Load interview questions, max scores, and competencies from JSON dataset
questions, max_scores, competencies = load_text(".\\Dataset\\questions.json")

# Initialize a list to store evaluation scores
scores_df = []

# Loop through all interview questions
for i in range(len(questions)):
    # Preprocess the question text
    question = clean_text(questions[i])
    score = max_scores[i]
    competency = competencies[i]

    # Define output file paths for audio and reports
    output_path_wav = f"generated_audio_question_{i}.wav"
    output_path_docx = f"./Reports/Question_{i}.txt"

    # Convert text question to speech and save it as an audio file
    text_to_speech(
        output_path=output_path_wav,
        model=models["st_model"],
        processor=models["processor"],
        question=question,
        target_lang="eng"
    )

    print("You can answer the question now. You have 45 seconds to answer.")

    # Convert the recorded speech response to text
    answer = speech_to_text(
        output_path_wav,
        model=models["st_model"],
        processor=models["processor"]
    )

    # Generate a formatted system prompt for scoring
    system_prompt = scoring_prompt_system % (question, competency, score, score)

    final_score = None

    # Ensure a valid response is received before proceeding
    while final_score is None:
        response, final_score = generate_response(
            models["llama_model"], answer, system_prompt
        )

    # Extract the correct response from the model output
    correct_response = response["Best Response"]

    # Save the evaluation response to a text report
    with open(output_path_docx, "w") as file:
        file.write(response)

    # Append the evaluation results to the dataframe
    scores_df.append({
        "question": question,
        "final_score": final_score,
        "correct_response": correct_response,
        "answer": answer,
    })

# Convert results to a Pandas DataFrame and save as CSV report
df = pd.DataFrame(scores_df)
df.to_csv("./Reports/Report.csv", index=False)

print("Evaluation completed. Report saved successfully!")
