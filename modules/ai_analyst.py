from ctransformers import AutoModelForCausalLM

class AIAnalyst:
    def __init__(self):
        self.llm = AutoModelForCausalLM.from_pretrained(
            "models/Phi-3-mini-4k-instruct-q4.gguf", 
            model_type="llama"
        )

    def analyze(self, data):
        prompt = f"Analyze security vulnerability: {data}. Assess severity."
        return self.llm(prompt)
