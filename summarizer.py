import torch
import re
from transformers import pipeline

class TextSummarizer:
    """
    A class to handle text summarization using transformer models.
    Handles long texts by chunking and provides options for batch processing.
    """
    def __init__(self, model_name="sshleifer/distilbart-cnn-12-6"):
        self.model_name = model_name
        self.summarizer = None
        self.load_model()

    def load_model(self):
        """
        Load the summarization model and pipeline.
        Attempts to use GPU and float16 for performance.
        """
        print(f"Attempting to load model: {self.model_name}...")
        try:
            device = 0 if torch.cuda.is_available() else -1
            torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

            self.summarizer = pipeline(
                "summarization",
                model=self.model_name,
                device=device,
                torch_dtype=torch_dtype
            )
            print(f"✅ Model '{self.model_name}' loaded successfully.")
            print("   -> Running on GPU." if device == 0 else "   -> Running on CPU.")
        except Exception as e:
            print(f"❌ Error loading model '{self.model_name}': {e}")
            raise

    def chunk_text(self, text, max_chunk_chars=4000):
        sentences = re.split(r'(?<=[.!?])\s+', text.strip())
        chunks = []
        current_chunk = ""
        for sentence in sentences:
            if len(current_chunk) + len(sentence) > max_chunk_chars and current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = sentence
            else:
                current_chunk += " " + sentence if current_chunk else sentence
        if current_chunk.strip():
            chunks.append(current_chunk.strip())
        return chunks

    def summarize(self, text, summary_ratio=0.3, min_length=30, max_length=150):
        if not self.summarizer or not text or len(text.strip()) < 50:
            return "Text is too short to summarize or model not loaded."

        word_count = len(text.split())
        target_summary_length = max(min_length, int(word_count * summary_ratio))

        if word_count <= 500:
            summary = self.summarizer(
                text,
                min_length=min(min_length, target_summary_length),
                max_length=min(max_length, target_summary_length + 20),
                do_sample=False,
                truncation=True
            )
            return summary[0]['summary_text']

        chunks = self.chunk_text(text)
        chunk_summaries = self.summarizer(
            chunks,
            min_length=20,
            max_length=100,
            do_sample=False,
            truncation=True
        )
        combined_summary = ' '.join([s['summary_text'] for s in chunk_summaries])

        if len(combined_summary.split()) > target_summary_length:
            final_summary = self.summarizer(
                combined_summary,
                min_length=min_length,
                max_length=min(max_length, target_summary_length),
                do_sample=False,
                truncation=True
            )
            return final_summary[0]['summary_text']
        else:
            return combined_summary

    def summarize_batch(self, texts_list, min_length=30, max_length=150):
        if not self.summarizer:
            return ["Model not loaded." for _ in texts_list]

        summaries = self.summarizer(
            texts_list,
            min_length=min_length,
            max_length=max_length,
            do_sample=False,
            truncation=True
        )
        return [s['summary_text'] for s in summaries]
