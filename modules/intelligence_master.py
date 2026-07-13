import asyncio
import aiohttp
import json
import os

class AdvancedIntelEngine:
    def __init__(self, target):
        self.target = target.rstrip('/')
        self.report = {"server_info": {}, "findings": []}

    async def probe(self, session, path):
        url = f"{self.target}/{path}"
        try:
            async with session.get(url, timeout=3) as resp:
                # 1. كشف هوية السيرفر (Fingerprinting)
                if not self.report["server_info"]:
                    self.report["server_info"] = dict(resp.headers)
                
                # 2. تحليل الاستجابة
                if resp.status < 400:
                    data = {"url": url, "status": resp.status, "type": resp.content_type}
                    self.report["findings"].append(data)
                    print(f"[!] Found: {url} | Type: {resp.content_type}")
        except:
            pass

    async def run(self, wordlist_path):
        if not os.path.exists(wordlist_path):
            print(f"[!] Error: Wordlist {wordlist_path} not found!")
            return

        with open(wordlist_path, 'r') as f:
            paths = [line.strip() for line in f]

        async with aiohttp.ClientSession() as session:
            print(f"[*] Starting Intel Recon on {self.target} with {len(paths)} paths...")
            tasks = [self.probe(session, path) for path in paths]
            await asyncio.gather(*tasks)

        # 3. حفظ التقرير الاستخباري
        with open("recon_intel.json", "w") as f:
            json.dump(self.report, f, indent=4)
        print("[!] Intel report saved to recon_intel.json")

if __name__ == "__main__":
    # إنشاء ملف wordlist.txt تجريبي إذا لم يكن موجوداً
    if not os.path.exists("wordlist.txt"):
        with open("wordlist.txt", "w") as f:
            f.write("admin\nconfig\n.env\nlogin\nbackup")
            
    target = "http://127.0.0.1:8080"
    engine = AdvancedIntelEngine(target)
    asyncio.run(engine.run("wordlist.txt"))
