# utils/quiz_generator.py
import openai
import json

# Try to import transformers, but handle gracefully if it fails
try:
    from transformers import AutoModelForCausalLM, AutoTokenizer
    import torch
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    print("Warning: transformers not available. Only OpenAI model will work.")

class QuizGenerator:
    def __init__(self, api_key=None, model_type="openai"):
        self.model_type = model_type
        if model_type == "openai":
            self.client = openai.OpenAI(api_key=api_key)
        elif model_type == "mixtral":
            if not TRANSFORMERS_AVAILABLE:
                raise ImportError("transformers library is required for Mixtral model. Please install it with: pip install transformers torch")
            self.tokenizer = AutoTokenizer.from_pretrained("mistralai/Mixtral-8x7B-Instruct-v0.1")
            self.model = AutoModelForCausalLM.from_pretrained(
                "mistralai/Mixtral-8x7B-Instruct-v0.1",
                torch_dtype=torch.float16,
                device_map="auto"
            )

    def generate_quiz_with_openai(self, transcript, num_questions=5):
        """Generate quiz questions using OpenAI's GPT-4."""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            f"You are an expert educator. Generate {num_questions} quiz questions based on the following transcript from an educational video. "
                            "For each question, provide 4 multiple-choice options and indicate the correct answer. "
                            "Format your response as a JSON object with a 'questions' key containing an array of objects. "
                            "Each question object should have 'question', 'options' (array of 4 strings), and 'correct_answer' (index of correct option, 0-based)."
                        )
                    },
                    {"role": "user", "content": transcript}
                ],
                response_format={"type": "json_object"},
                max_tokens=2000,
                temperature=0.7
            )
            result = json.loads(response.choices[0].message.content)
            return result.get("questions", [])
        except Exception as e:
            print(f"[OpenAI Quiz Error] {e}")
            return []

    def generate_quiz_with_mixtral(self, transcript, num_questions=5):
        """Generate quiz questions using Mixtral model."""
        if not TRANSFORMERS_AVAILABLE:
            raise ImportError("transformers library is required for Mixtral model")
        
        prompt = (
            f"<s>[INST] You are an expert educator. Generate {num_questions} quiz questions based on the following transcript from an educational video. "
            "For each question, provide 4 multiple-choice options and indicate the correct answer. "
            "Format your response as a JSON array with objects containing 'question', 'options' (array of 4 strings), and 'correct_answer' (index of correct option, 0-based).\n"
            f"Transcript:\n{transcript}\n[/INST]</s>"
        )
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        outputs = self.model.generate(
            inputs["input_ids"],
            max_new_tokens=1024,
            temperature=0.7,
            top_p=0.9
        )
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        # Extract only the response part and parse JSON
        json_str = response.split("[/INST]")[1].strip()
        # Find JSON content between ```json and ```
        if "```json" in json_str and "```" in json_str.split("```json")[1]:
            json_content = json_str.split("```json")[1].split("```")[0].strip()
        else:
            # Try to extract JSON directly
            start_idx = json_str.find("[")
            end_idx = json_str.rfind("]") + 1
            if start_idx != -1 and end_idx != 0:
                json_content = json_str[start_idx:end_idx]
            else:
                return []  # Failed to extract JSON
        try:
            return json.loads(json_content)
        except json.JSONDecodeError:
            return []  # Failed to parse JSON

    def generate_quiz(self, transcript, num_questions=5):
        """Generate quiz questions using the selected model."""
        if self.model_type == "openai":
            return self.generate_quiz_with_openai(transcript, num_questions)
        elif self.model_type == "mixtral":
            return self.generate_quiz_with_mixtral(transcript, num_questions)