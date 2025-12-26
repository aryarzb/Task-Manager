from __future__ import annotations
from typing import Optional
from TaskManager import Task
from pathlib import Path
import pygame

pygame.mixer.init()




class IO:
    def show_title(self) -> None:
        print("\n--- Task Manager ---")

    def play_alarm(self) -> None:
        mp3 = Path("infection-signal-sound.mp3")
        if mp3.exists():
            pygame.mixer.music.load(str(mp3))
            pygame.mixer.music.play()
        else:
            print("alarm.mp3 not found")


    def show_menu(self) -> None:
        self.show_title()
        print("1) Add task")
        print("2) List tasks (all)")
        print("3) List tasks (pending)")
        print("4) List tasks (done)")
        print("5) Mark done")
        print("6) Mark pending")
        print("7) Delete task")
        print("8) Set reminder (date & time)")
        print("9) Set timer (minutes from now)")
        print("0) Exit")

    def info(self, msg: str) -> None:
        print(msg)

    def error(self, msg: str) -> None:
        print(f"Error: {msg}")

    def show_tasks(self, tasks) -> None:
        if not tasks:
            print("No tasks.")
            return
        for t in tasks:
            note = t.note if t.note is not None else "-"
            due = t.due_at if t.due_at is not None else "-"
            rem = t.remind_at if t.remind_at is not None else "-"
            print(f"[{t.id}] {t.title} | {t.status} | note: {note} | due: {due} | remind: {rem}")

    def show_reminder(self, task: Task) -> None:
        print(f"\n⏰ REMINDER: [{task.id}] {task.title}")
        if task.note:
            print(f"   note: {task.note}")
        self.play_alarm()

    def ask(self, prompt: str) -> str:
        return input(prompt).strip()

    def ask_optional(self, prompt: str) -> Optional[str]:
        value = input(prompt).strip()
        return value if value else None

    def ask_datetime(self, prompt: str) -> str:
        return input(prompt).strip()

    def ask_int(self, prompt: str) -> int:
        while True:
            raw = input(prompt).strip()
            try:
                return int(raw)
            except ValueError:
                print("Please enter a number.")
