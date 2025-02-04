from pydub import AudioSegment
from pydub.silence import split_on_silence

def text_chunking(tokens: str, max_tokens: int = 1024):
    """
    Splits a text string into smaller chunks based on a maximum token limit.

    Args:
        tokens (str): The input text string to be chunked.
        max_tokens (int): The maximum number of tokens per chunk (default is 1024).

    Returns:
        list: A list of text chunks, each containing up to `max_tokens` words.
    """
    chunks = []
    current_chunk = []
    current_length = 0

    # Tokenize text into words
    tokens = tokens.split()

    for token in tokens:
        # Add token to current chunk if it doesn't exceed the limit
        if current_length + 1 <= max_tokens:
            current_chunk.append(token)
            current_length += 1
        else:
            # Save the current chunk and start a new one
            chunks.append(" ".join(current_chunk))
            current_chunk = [token]
            current_length = 1

    # Add the last chunk if it's not empty
    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks


def audio_chunking(audio: AudioSegment, chunk_size: int = 5000):
    """
    Splits an audio file into chunks based on silence detection.

    Args:
        audio (AudioSegment): The input audio file (Pydub AudioSegment).
        chunk_size (int): The minimum silence length in milliseconds (default is 5000 ms).

    Returns:
        list: A list of audio chunks.
    """
    # Split audio based on silence detection
    chunks = split_on_silence(
        audio,
        min_silence_len=chunk_size,  # Minimum silence length in milliseconds
        silence_thresh=-40  # Silence threshold in dB
    )

    # Export each chunk as a separate file
    for i, chunk in enumerate(chunks):
        chunk.export(f"chunk_silence_{i + 1}.wav", format="wav")

    return chunks
