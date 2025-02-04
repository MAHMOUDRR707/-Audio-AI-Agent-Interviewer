import torchaudio
from transformers import pipeline, AutoProcessor, SpeechT5Model
import sounddevice as sd
import soundfile as sf

def speech_to_text(audio_path, model, processor, target_lang="eng"):
    """
    Converts spoken audio into transcribed text using a speech-to-text model.

    Args:
        audio_path (str): Path to the input audio file.
        model (transformers.PreTrainedModel): A pre-trained speech-to-text model.
        processor (transformers.PreTrainedProcessor): Processor for speech-to-text.
        target_lang (str): Target language for transcription (default is "eng").

    Returns:
        str: The transcribed text from the audio.
    """
    # Modify the audio file name to store the user's recorded answer
    audio_path = audio_path.split(".")[0] + "_answer.wav"

    # Record user audio input
    record_audio(audio_path)

    # Load the recorded audio file
    audio, orig_freq = torchaudio.load(audio_path)

    # Resample the audio to 16 kHz as required by the model
    audio = torchaudio.functional.resample(audio, orig_freq=orig_freq, new_freq=16_000)

    # Process the audio for the model
    audio_inputs = processor(audios=audio, return_tensors="pt")

    # Generate text from the audio input
    output_tokens = model.generate(**audio_inputs, tgt_lang=target_lang, generate_speech=False)

    # Decode the output tokens into a human-readable text format
    translated_text_from_audio = processor.decode(output_tokens[0].tolist()[0], skip_special_tokens=True)

    return translated_text_from_audio


def record_audio(filename, duration=45, sample_rate=44100):
    """
    Records audio from the user's microphone and saves it to a file.

    Args:
        filename (str): Path to save the recorded audio.
        duration (int): Duration of the recording in seconds (default is 45).
        sample_rate (int): Sample rate for recording in Hz (default is 44100).

    Returns:
        None
    """
    print(f"Recording for {duration} seconds...")

    # Start recording audio
    recording = sd.rec(
        int(duration * sample_rate), 
        samplerate=sample_rate, 
        channels=1,  # Mono audio channel
        dtype='float64'
    )

    # Wait until the recording is complete
    sd.wait()

    # Save the recorded audio to a file
    sf.write(filename, recording, sample_rate)

    print("Finished recording.")
