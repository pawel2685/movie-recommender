"""
utils/history.py
Zarządzanie historią rozmów za pomocą cookies.
"""

from __future__ import annotations

import json
from datetime import datetime
from typing import TypedDict

import streamlit as st
from streamlit_cookies_manager import CookieManager


class ConversationEntry(TypedDict):
    """Struktura wpisu do historii."""
    time: str
    title: str
    excerpt: str
    question: str
    answer: str


class ConversationHistory:
    """Zarządza historią rozmów za pomocą cookies."""

    COOKIE_KEY = "cinerag_history"
    MAX_ENTRIES = 20

    def __init__(self) -> None:
        """Inicjalizuje historię rozmów."""
        self._cookies: CookieManager | None = None

    def _get_cookies(self) -> CookieManager | None:
        """
        Pobiera lub inicjalizuje CookieManager (lazy initialization).
        
        Returns:
            CookieManager jeśli cookies są ready, None w innym wypadku.
        """
        if self._cookies is not None:
            return self._cookies

        try:
            cookies = CookieManager()
            # Test czy cookies są ready
            _ = cookies.get("_test_ready")
            self._cookies = cookies
            return self._cookies
        except Exception:
            # Cookies nie są jeszcze ready lub inny błąd
            return None

    def add_conversation(
        self,
        question: str,
        answer: str,
    ) -> None:
        """
        Dodaje nową rozmowę do historii.

        Args:
            question: Pytanie użytkownika.
            answer: Odpowiedź asystenta.
        """
        cookies = self._get_cookies()
        if cookies is None:
            return

        try:
            history = self.get_history()

            title = question[:50] + "..." if len(question) > 50 else question
            now = datetime.now().strftime("%Y-%m-%d %H:%M")

            entry: ConversationEntry = {
                "time": now,
                "title": title,
                "excerpt": answer[:80] + "..." if len(answer) > 80 else answer,
                "question": question,
                "answer": answer,
            }

            history.insert(0, entry)
            history = history[:self.MAX_ENTRIES]

            cookies[self.COOKIE_KEY] = json.dumps(history)
            cookies.save()
        except Exception:
            pass  # Historia jest opcjonalna

    def get_history(self) -> list[ConversationEntry]:
        """
        Pobiera historię rozmów.

        Returns:
            Lista wpisów historii.
        """
        cookies = self._get_cookies()
        if cookies is None:
            return []

        try:
            data = cookies.get(self.COOKIE_KEY)
            if not data:
                return []
            return json.loads(data)
        except (json.JSONDecodeError, Exception):
            return []

    def clear_history(self) -> None:
        """Czyści całą historię rozmów."""
        cookies = self._get_cookies()
        if cookies is None:
            return

        try:
            cookies[self.COOKIE_KEY] = json.dumps([])
            cookies.save()
        except Exception:
            pass

    def delete_entry(self, index: int) -> None:
        """
        Usuwa konkretny wpis z historii.

        Args:
            index: Indeks wpisu do usunięcia.
        """
        cookies = self._get_cookies()
        if cookies is None:
            return

        try:
            history = self.get_history()
            if 0 <= index < len(history):
                history.pop(index)
                cookies[self.COOKIE_KEY] = json.dumps(history)
                cookies.save()
        except Exception:
            pass
