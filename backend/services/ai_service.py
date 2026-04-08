import os
import logging
from openai import OpenAI

logger = logging.getLogger(__name__)

_client = None


def _get_client():
    global _client
    if _client is None:
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            raise RuntimeError("GROQ_API_KEY not set in .env")
        _client = OpenAI(
            api_key=api_key,
            base_url="https://api.groq.com/openai/v1",
            timeout=45,
        )
    return _client


def _load_file(filename):
    path = os.path.join(os.path.dirname(__file__), "../prompts", filename)
    with open(path, encoding="utf-8") as f:
        return f.read()


SYSTEM_PROMPT = _load_file("system_prompt.txt")
MODE_PROMPTS = {}


def _load_mode_prompts():
    current = None
    for line in _load_file("mode_prompts.txt").splitlines():
        if line.startswith("[") and line.endswith("]"):
            current = line[1:-1]
            MODE_PROMPTS[current] = ""
        elif current is not None:
            MODE_PROMPTS[current] += line + "\n"
    for k in MODE_PROMPTS:
        MODE_PROMPTS[k] = MODE_PROMPTS[k].strip()


_load_mode_prompts()

VALID_MODES = {"concise", "detailed", "keypoints", "flashcards", "keywords"}


def _call(messages):
    response = _get_client().chat.completions.create(
        model="llama-3.3-70b-versatile",
        temperature=0.2,
        messages=messages,
    )
    return response.choices[0].message.content.strip()


def generate_summary(content, mode):
    if mode not in VALID_MODES:
        raise ValueError(f"Invalid mode: {mode}")
    prompt = f"{MODE_PROMPTS.get(mode, '')}\n\n---NOTE START---\n{content}\n---NOTE END---"
    return _call([{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": prompt}])


def answer_question(content, question):
    prompt = (
        f"Notes:\n\n---NOTE START---\n{content}\n---NOTE END---\n\n"
        f"Question: {question}\n\n"
        "Answer using only the notes above. "
        'If not found, say: "Not specified in the notes."'
    )
    return _call([{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": prompt}])
