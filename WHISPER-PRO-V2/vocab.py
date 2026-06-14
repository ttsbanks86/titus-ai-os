"""Vocabulary Manager — Custom words/phrases for transcription accuracy"""
import json
from pathlib import Path
from constants import VOCAB_FILE

DEFAULT_VOCAB = {"words": [], "phrases": []}

def load_vocab():
    try:
        if VOCAB_FILE.exists():
            with open(VOCAB_FILE, encoding="utf-8") as f:
                return json.load(f)
    except:
        pass
    return dict(DEFAULT_VOCAB)

def save_vocab(vocab: dict):
    try:
        VOCAB_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(VOCAB_FILE, "w", encoding="utf-8") as f:
            json.dump(vocab, f, indent=2)
    except Exception as e:
        print(f"[Vocab] Save error: {e}")

def get_vocab() -> dict:
    return load_vocab()

def add_word(word: str, category: str = "words") -> dict:
    vocab = load_vocab()
    if word and word not in vocab.get(category, []):
        vocab.setdefault(category, []).append(word)
        # Keep alphabetical
        vocab[category].sort(key=str.lower)
        save_vocab(vocab)
    return vocab

def remove_word(word: str, category: str = "words") -> dict:
    vocab = load_vocab()
    if word in vocab.get(category, []):
        vocab[category].remove(word)
        save_vocab(vocab)
    return vocab

def get_all_terms() -> list:
    vocab = load_vocab()
    return vocab.get("words", []) + vocab.get("phrases", [])