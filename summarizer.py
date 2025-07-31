import torch
import re
from transformers import pipeline

class TextSummarizer:
    """
    A class to handle text summarization using transformer models.
    Handles long texts by chunking and provides options for batch processing.
    """
    def __init__(self, model_name="sshleifer/distilbart-cnn-12-6"):
        """
        Initialize the text summarizer with a pre-trained model.

        Args:
            model_name (str): Name of the pre-trained model.
                - "sshleifer/distilbart-cnn-12-6" (Default): Great balance of speed and quality.
                - "facebook/bart-large-cnn": Higher quality but slower.
        """
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
            if device == 0:
                print("   -> Running on GPU with float16 optimization.")
            else:
                print("   -> Running on CPU.")

        except Exception as e:
            print(f"❌ Error loading model '{self.model_name}': {e}")
            raise

    def chunk_text(self, text, max_chunk_chars=4000):
        """
        Split text into chunks based on character length, respecting sentence boundaries.
        
        Args:
            text (str): Input text to chunk.
            max_chunk_chars (int): The approximate maximum number of characters for each chunk.
        
        Returns:
            list: A list of text chunks.
        """
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
        """
        Summarize text. Handles long text by chunking and performing recursive summarization.
        
        Args:
            text (str): Input text to summarize.
            summary_ratio (float): Desired ratio of summary length to original length.
            min_length (int): Minimum length of the final summary.
            max_length (int): Maximum length of the final summary.

        Returns:
            str: The final summary.
        """
        if not self.summarizer or not text or len(text.strip()) < 50:
            return "Text is too short to summarize or model not loaded."

        word_count = len(text.split())
        target_summary_length = max(min_length, int(word_count * summary_ratio))

        # For shorter texts, summarize directly
        if word_count <= 500:
            summary = self.summarizer(
                text,
                min_length=min(min_length, target_summary_length),
                max_length=min(max_length, target_summary_length + 20),
                do_sample=False,
                truncation=True
            )
            return summary[0]['summary_text']
        
        # For longer texts, chunk, summarize chunks, then summarize the result
        print(f"Text is long ({word_count} words). Chunking and summarizing...")
        chunks = self.chunk_text(text)
        
        # Summarize each chunk
        chunk_summaries = self.summarizer(
            chunks,
            min_length=20,
            max_length=100,
            do_sample=False,
            truncation=True
        )
        
        combined_summary = ' '.join([s['summary_text'] for s in chunk_summaries])
        
        # If the combined summary is still long, summarize it again
        if len(combined_summary.split()) > target_summary_length:
            print("Performing recursive summarization on combined chunks...")
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
        """
        Efficiently summarizes a batch of texts using the pipeline's batching capability.
        
        Args:
            texts_list (list): A list of strings to summarize.
            min_length (int): Minimum length for each summary.
            max_length (int): Maximum length for each summary.

        Returns:
            list: A list of summary strings.
        """
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

# --- Example Usage ---
if __name__ == "__main__":
    # Long text for demonstration
    long_article_text = (
        "Scientific inquiry is a systematic process that involves formulating a hypothesis, "
        "designing and conducting experiments, and analyzing the results to draw a conclusion. "
        "This method is the cornerstone of modern science, allowing researchers to understand "
        "the natural world in an objective and reproducible manner. A key aspect of this "
        "process is peer review, where other experts in the field evaluate the research for "
        "validity, significance, and originality before it is published. This ensures a high "
        "standard of quality and helps to filter out flawed or trivial work. The journey from "
        "a simple question to a validated scientific theory can take years, involving countless "
        "hours of meticulous work and collaboration among scientists across the globe. "
        "Furthermore, technology plays a crucial role in advancing scientific frontiers. "
        "Innovations in computing allow for complex simulations and data analysis, while "
        "new instruments enable measurements of unprecedented precision. The synergy between "
        "theoretical models and experimental verification drives progress, leading to "
        "discoveries that can fundamentally change our understanding of the universe and "
        "improve human life through new technologies and medicines."
    )

    # 1. Use the default fast summarizer for a single text
    print("--- Using default (fast) model for a single text ---")
    fast_summarizer = TextSummarizer() # Uses "sshleifer/distilbart-cnn-12-6"
    summary = fast_summarizer.summarize(long_article_text)
    print("\n[FAST SUMMARY]:")
    print(summary)
    print("-" * 50)

    # 2. Use the high-quality model for the same text
    try:
        print("\n--- Using high-quality (slower) model for a single text ---")
        quality_summarizer = TextSummarizer(model_name="facebook/bart-large-cnn")
        quality_summary = quality_summarizer.summarize(long_article_text)
        print("\n[HIGH-QUALITY SUMMARY]:")
        print(quality_summary)
        print("-" * 50)
    except Exception as e:
        print(f"Could not run high-quality model, likely due to resource constraints. Error: {e}")


    # 3. Use the batch summarization feature
    print("\n--- Using batch summarization ---")
    documents_to_summarize = [
        "The new electric car boasts a range of over 500 miles on a single charge, "
        "setting a new industry standard. Its acceleration is equally impressive.",
        "Local government announced a new initiative to plant 10,000 trees across the "
        "city parks by the end of next year, aiming to improve air quality.",
        "The stock market saw significant volatility this week, with tech stocks "
        "rebounding on Friday after a midweek dip caused by inflation fears."
    ]
    batch_summaries = fast_summarizer.summarize_batch(documents_to_summarize, min_length=10, max_length=30)
    
    print("\n[BATCH SUMMARIES]:")
    for i, s in enumerate(batch_summaries):
        print(f"Doc {i+1}: {s}")