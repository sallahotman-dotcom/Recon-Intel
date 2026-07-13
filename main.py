import os
import json
from llama_cpp import Llama
from modules import shadow_fuzzer, exploit_architect, scanner

class CyberCore:
    def __init__(self):
        self.model = Llama(model_path="models/Phi-3-mini-4k-instruct-q4.gguf", n_ctx=2048, verbose=False)
        self.findings = []

    def run_recon(self, target):
        print(f"[*] Starting reconnaissance on: {target}")
        self.findings = scanner.run(target)
        
    def orchestrate_attack(self):
        print("[*] AI Architect: Analyzing findings for exploitation path...")
        context = json.dumps(self.findings)
        prompt = f"Analyze these vulnerabilities: {context}. Define the most critical exploit chain. Output in JSON format."
        
        response = self.model(prompt, max_tokens=300)
        plan = json.loads(response['choices'][0]['text'])
        
        for step in plan['steps']:
            print(f"[!] Executing: {step}")
            shadow_fuzzer.execute(step)

if __name__ == "__main__":
    core = CyberCore()
    target = input("Enter Target: ")
    core.run_recon(target)
    core.orchestrate_attack()
