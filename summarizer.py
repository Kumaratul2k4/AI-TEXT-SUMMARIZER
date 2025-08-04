import torch
import re
from transformers import pipeline

class TextSummarizer:
    """
    A class to handle text summarization using a lightweight transformer model.
    Handles long texts by chunking them.
    """
    def __init__(self, model_name="t5-small"):
        """
        Initializes the summarizer with a memory-efficient model.
        Good alternatives: 'mrm8488/t5-small-finetuned-summarize-news'
        """
        self.model_name = model_name
        self.summarizer = None
        self._load_model()

    def _load_model(self):
        """
        Load the summarization model and pipeline.
        This is designed to be CPU-friendly for free hosting tiers.
        """
        print(f"Attempting to load lightweight model: {self.model_name}...")
        try:
            # Forcing CPU usage as free tiers rarely have GPUs.
            # This prevents attempts to allocate CUDA memory.
            device = -1
            
            self.summarizer = pipeline(
                "summarization",
                model=self.model_name,
                tokenizer=self.model_name, # Explicitly define tokenizer
                device=device
            )
            print(f"✅ Model '{self.model_name}' loaded successfully on CPU.")
        except Exception as e:
            print(f"❌ Error loading model '{self.model_name}': {e}")
            # This allows the app to run, but summarization will fail.
            self.summarizer = None
            raise

    def _chunk_text(self, text, max_chunk_length=512):
        """
        Splits text into chunks suitable for the model's max input size.
        Uses sentences as split points to maintain context.
        """
        # T5 models often have a 512-token limit. We chunk based on that.
        # Using a simple word count as a proxy for token count.
        sentences = re.split(r'(?<=[.!?])\s+', text.strip())
        chunks = []
        current_chunk_words = []
        
        for sentence in sentences:
            sentence_words = sentence.split()
            if len(current_chunk_words) + len(sentence_words) > max_chunk_length:
                if current_chunk_words:
                    chunks.append(" ".join(current_chunk_words))
                current_chunk_words = sentence_words
            else:
                current_chunk_words.extend(sentence_words)

        if current_chunk_words:
            chunks.append(" ".join(current_chunk_words))
            
        return chunks

    def summarize(self, text, min_length=30, max_length=150):
        if not self.summarizer:
            return "Model is not available. The application might have failed to load it."
        if not text or len(text.strip()) < 100:
            return "Text is too short to provide a meaningful summary."

        # The t5 models require a prefix
        prefixed_text = "summarize: " + text

        # Check if text is long and needs chunking
        if len(prefixed_text.split()) > 500:
            print("📝 Text is long, processing in chunks...")
            chunks = self._chunk_text(prefixed_text)
            
            # Summarize each chunk individually
            chunk_summaries = self.summarizer(
                chunks,
                min_length=20,
                max_length=80, # Keep chunk summaries shorter
                truncation=True
            )
            
            # Combine the summaries of the chunks
            combined_summary = ' '.join([summ['summary_text'] for summ in chunk_summaries])
            return combined_summary
        else:
            # Process shorter texts directly
            print("📝 Processing a single block of text...")
            summary_list = self.summarizer(
                prefixed_text,
                min_length=min_length,
                max_length=max_length,
                truncation=True
            )
            return summary_list[0]['summary_text']
