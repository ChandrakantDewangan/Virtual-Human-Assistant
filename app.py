import json
import os
import queue
import re
import threading
import time
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

import tkinter as tk
from tkinter import ttk, messagebox

try:
    import requests
except ImportError:
    requests = None

MEMORY_PATH = Path("memory.json")


@dataclass
class TaskPlan:
    intent: str
    strategy: str
    steps: List[str]
    risk_notes: List[str]


class MemoryStore:
    def __init__(self, path: Path):
        self.path = path
        self.data = {"preferences": {}, "history": []}
        self.load()

    def load(self):
        if self.path.exists():
            self.data = json.loads(self.path.read_text(encoding="utf-8"))

    def save(self):
        self.path.write_text(json.dumps(self.data, indent=2), encoding="utf-8")

    def add_history(self, item: Dict):
        self.data["history"].append(item)
        self.data["history"] = self.data["history"][-50:]
        self.save()


class FreeModelRouter:
    """Uses only free/open models: local Ollama first, Hugging Face Inference fallback."""

    def __init__(self):
        self.hf_token = os.getenv("HUGGINGFACE_API_KEY", "")
        self.ollama_model = os.getenv("OLLAMA_MODEL", "llama3.1:8b")
        self.hf_model = os.getenv("HF_MODEL", "HuggingFaceH4/zephyr-7b-beta")

    def ask(self, prompt: str) -> str:
        local = self._ask_ollama(prompt)
        if local:
            return local
        remote = self._ask_huggingface(prompt)
        if remote:
            return remote
        return "I could not reach any free model. Start Ollama or set HUGGINGFACE_API_KEY."

    def _ask_ollama(self, prompt: str) -> Optional[str]:
        if not requests:
            return None
        try:
            res = requests.post(
                "http://localhost:11434/api/generate",
                json={"model": self.ollama_model, "prompt": prompt, "stream": False},
                timeout=40,
            )
            if res.ok:
                return res.json().get("response", "").strip()
        except Exception:
            return None
        return None

    def _ask_huggingface(self, prompt: str) -> Optional[str]:
        if not requests or not self.hf_token:
            return None
        try:
            url = f"https://api-inference.huggingface.co/models/{self.hf_model}"
            headers = {"Authorization": f"Bearer {self.hf_token}"}
            payload = {"inputs": prompt, "parameters": {"max_new_tokens": 300, "temperature": 0.2}}
            res = requests.post(url, headers=headers, json=payload, timeout=60)
            if not res.ok:
                return None
            data = res.json()
            if isinstance(data, list) and data:
                txt = data[0].get("generated_text", "")
                return txt[len(prompt):].strip() if txt.startswith(prompt) else txt.strip()
        except Exception:
            return None
        return None


class VirtualHumanCore:
    def __init__(self, memory: MemoryStore):
        self.memory = memory
        self.router = FreeModelRouter()

    def understand(self, user_text: str) -> str:
        text = user_text.lower()
        if any(w in text for w in ["create", "build", "do", "open", "fill", "update"]):
            return "task"
        if any(w in text for w in ["why", "what", "how", "explain"]):
            return "question"
        return "goal"

    def plan(self, user_text: str) -> TaskPlan:
        intent = self.understand(user_text)
        strategy = "tool" if any(k in user_text.lower() for k in ["file", "web", "data", "code"]) else "manual"
        steps = [
            "Understand the requested outcome.",
            "Select best free agent/tool.",
            "Execute with safety checks.",
            "Verify output quality.",
            "Store memory for future improvement.",
        ]
        risk = ["Never run destructive actions without confirmation.", "Pause and ask user if ambiguous."]
        return TaskPlan(intent=intent, strategy=strategy, steps=steps, risk_notes=risk)

    def respond(self, user_text: str) -> Dict:
        plan = self.plan(user_text)
        prompt = (
            "You are a Virtual Human Assistant. Think step-by-step internally and answer clearly. "
            "User request: " + user_text
        )
        answer = self.router.ask(prompt)
        result = {"plan": asdict(plan), "answer": answer, "timestamp": datetime.utcnow().isoformat()}
        self.memory.add_history(result)
        return result


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Virtual Human Assistant (Free AI)")
        self.geometry("980x700")
        self.memory = MemoryStore(MEMORY_PATH)
        self.core = VirtualHumanCore(self.memory)
        self.out_queue = queue.Queue()
        self._build_ui()
        self.after(200, self._poll_queue)

    def _build_ui(self):
        top = ttk.Frame(self)
        top.pack(fill="x", padx=10, pady=8)
        ttk.Label(top, text="Goal / Task:").pack(anchor="w")
        self.input_text = tk.Text(top, height=5)
        self.input_text.pack(fill="x")

        btns = ttk.Frame(top)
        btns.pack(fill="x", pady=6)
        ttk.Button(btns, text="Think + Act", command=self.on_run).pack(side="left")
        ttk.Button(btns, text="Clear", command=lambda: self.input_text.delete("1.0", "end")).pack(side="left", padx=6)

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=10, pady=8)

        self.plan_box = tk.Text(notebook, wrap="word")
        self.answer_box = tk.Text(notebook, wrap="word")
        self.memory_box = tk.Text(notebook, wrap="word")
        notebook.add(self.plan_box, text="Plan")
        notebook.add(self.answer_box, text="Response")
        notebook.add(self.memory_box, text="Memory")

        self._refresh_memory()

    def on_run(self):
        text = self.input_text.get("1.0", "end").strip()
        if not text:
            messagebox.showwarning("Missing input", "Please enter a goal or task.")
            return
        threading.Thread(target=self._worker, args=(text,), daemon=True).start()

    def _worker(self, text: str):
        result = self.core.respond(text)
        self.out_queue.put(result)

    def _poll_queue(self):
        while not self.out_queue.empty():
            item = self.out_queue.get()
            self.render_result(item)
        self.after(200, self._poll_queue)

    def render_result(self, item: Dict):
        plan = item["plan"]
        self.plan_box.delete("1.0", "end")
        self.plan_box.insert("end", json.dumps(plan, indent=2))

        self.answer_box.delete("1.0", "end")
        self.answer_box.insert("end", item["answer"])
        self._refresh_memory()

    def _refresh_memory(self):
        self.memory_box.delete("1.0", "end")
        self.memory_box.insert("end", json.dumps(self.memory.data, indent=2))


if __name__ == "__main__":
    App().mainloop()
