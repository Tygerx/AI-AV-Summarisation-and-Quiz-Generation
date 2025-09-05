# utils/summarizer.py
import openai
import json

class ContentSummarizer:
    def __init__(self, api_key=None, model_type="openai"):
        self.model_type = model_type
        if model_type == "openai":
            self.client = openai.OpenAI(api_key=api_key)
        elif model_type == "mixtral":
            from transformers import AutoModelForCausalLM, AutoTokenizer
            import torch
            self.tokenizer = AutoTokenizer.from_pretrained("mistralai/Mixtral-8x7B-Instruct-v0.1")
            self.model = AutoModelForCausalLM.from_pretrained(
                "mistralai/Mixtral-8x7B-Instruct-v0.1",
                torch_dtype=torch.float16,
                device_map="auto"
            )

    def summarize_with_openai(self, transcript, max_length=500):
        """Generate a summary using OpenAI's GPT-4."""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": f"You are an expert content summarizer. Create a comprehensive summary of the following transcript in approximately {max_length} words. Focus on key points, main topics, and important insights."
                    },
                    {"role": "user", "content": transcript}
                ],
                max_tokens=1000,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"[OpenAI Summary Error] {e}")
            return "Error generating summary. Please try again."

    def summarize_with_mixtral(self, transcript, max_length=500):
        """Generate a summary using Mixtral model."""
        try:
            prompt = (
                f"<s>[INST] You are an expert content summarizer. Create a comprehensive summary of the following transcript in approximately {max_length} words. Focus on key points, main topics, and important insights.\n"
                f"Transcript:\n{transcript}\n[/INST]</s>"
            )
            inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
            outputs = self.model.generate(
                inputs["input_ids"],
                max_new_tokens=1000,
                temperature=0.7,
                top_p=0.9,
                do_sample=True
            )
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            # Extract only the response part
            summary = response.split("[/INST]")[1].strip()
            return summary
        except Exception as e:
            print(f"[Mixtral Summary Error] {e}")
            return "Error generating summary. Please try again."

    def summarize(self, transcript, max_length=500):
        """Generate a summary using the selected model."""
        if self.model_type == "openai":
            return self.summarize_with_openai(transcript, max_length)
        elif self.model_type == "mixtral":
            return self.summarize_with_mixtral(transcript, max_length)
        else:
            return "Invalid model type specified."