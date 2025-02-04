import scipy
import sounddevice as sd
import soundfile as sf
import time

def text_to_speech(output_path, model, processor, question, target_lang="eng"):
    """
    Converts text into speech audio and saves it as a file.

    Args:
        output_path (str): Path to save the generated audio file.
        model (transformers.PreTrainedModel): A pre-trained text-to-speech model.
        processor (transformers.PreTrainedProcessor): Processor for text-to-speech.
        question (str): The text to be converted into speech.
        target_lang (str): Target language for the generated speech (default is "eng").

    Returns:
        None
    """
    # Process the input text into model-compatible tensors
    text_inputs = processor(text=question, src_lang=target_lang, return_tensors="pt")
    
    # Generate audio data from the text input
    audio_array_from_text = model.generate(**text_inputs, tgt_lang=target_lang)[0].cpu().numpy().squeeze()
    
    # Retrieve the model's sampling rate
    sample_rate = model.config.sampling_rate
    
    # Save the generated audio as a WAV file
    scipy.io.wavfile.write(output_path, rate=sample_rate, data=audio_array_from_text)
    
    # Inform the user and play the generated audio
    print("Here's the question:", question)
    play_audio(output_path)


def play_audio(filename):
    """
    Plays an audio file.

    Args:
        filename (str): Path to the audio file to play.

    Returns:
        None
    """
    # Read the audio file using soundfile
    data, sample_rate = sf.read(filename)
    
    print(f"Playing {filename}...")
    
    # Play the audio data
    sd.play(data, sample_rate)
    
    # Wait for the playback to finish
    time.sleep(len(data) / sample_rate)  # Wait based on audio duration
    sd.wait()
    
    print("Audio playback finished.")
