import asyncio
import aiohttp
import json
import sys
import os
import re
from colorama import init, Fore, Style

init(autoreset=True)

class MassScanner:
    def __init__(self, wordlist="wordlist.txt"):
        self.wordlist = self.load_file(wordlist)
        self.semaphore = asyncio.Semaphore(20)

    def load_file(self, filename):
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                return [line.strip() for line in f if line.strip()]
        return []

    # محرك البحث عن الكنوز (البيانات الحساسة)
    def extract_sensitive_data(self, content):
        patterns = {
            "API_KEY": r"(?i)(api_key|apikey|secret|key)['\s]*[:=]['\s]*([a-zA-Z0-9_-]{20,})",
            "PASSWORD": r"(?i)(password|passwd|pwd)['\s]*[:=]['\s]*([a-zA-Z0-9_-]{6,})"
        }
        found = {}
        for name, pattern in patterns.items():
            match = re.search(pattern, content)
            if match:
                found[name] = match.group(2)
        return found

    async def scan_target(self, target):
        target = target if target.startswith("http") else f"http://{target}"
        print(f"{Fore.CYAN}[*] Deep Scanning: {target}{Style.RESET_ALL}")
        
        results = {"target": target, "paths": []}
        
        async with aiohttp.ClientSession(headers={'User-Agent': 'Mozilla/5.0'}) as session:
            try:
                async with session.get(f"{target}/nonexistent_12345", timeout=5) as resp:
                    error_page_size = len(await resp.text())
            except: error_page_size = 0
            
            tasks = [self.check_path(session, target, path, results, error_page_size) for path in self.wordlist]
            await asyncio.gather(*tasks)
            
            clean_name = target.replace("http://", "").replace("https://", "").replace("/", "_")
            with open(f"report_{clean_name}.json", "w") as f:
                json.dump(results, f, indent=4)
            print(f"{Fore.GREEN}[+] Audit for {target} finished.{Style.RESET_ALL}")

    async def check_path(self, session, target, path, results, error_page_size):
        url = f"{target.rstrip('/')}/{path}"
        try:
            async with self.semaphore:
                async with session.get(url, timeout=5) as resp:
                    content = await resp.text()
                    content_len = len(content)
                    
                    if resp.status in [200, 301, 403] and content_len != error_page_size:
                        # استخراج البيانات الحساسة إذا وجدت
                        sensitive = self.extract_sensitive_data(content)
                        if sensitive:
                            print(f"{Fore.RED}[!] SENSITIVE DATA FOUND: {url} -> {sensitive}{Style.RESET_ALL}")
                        
                        results["paths"].append({"url": url, "status": resp.status, "sensitive": sensitive})
        except: pass

async def main():
    if not os.path.exists("targets.txt"): return
    targets = [line.strip() for line in open("targets.txt") if line.strip()]
    scanner = MassScanner()
    await asyncio.gather(*[scanner.scan_target(t) for t in targets])

if __name__ == "__main__":
    try: asyncio.run(main())
    except KeyboardInterrupt: pass
