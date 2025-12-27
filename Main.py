from TaskManager import TaskManager
from IO import IO
import Time
import time
import threading


class Main:
    def __init__(self) -> None:
            self.tm = TaskManager()
            self.io = IO()
            self.running = True
            self._reminder_thread = threading.Thread(target=self.reminder_loop, daemon=True)
            self._reminder_thread.start()

    def reminder_loop(self) -> None:
            while self.running:
                due = self.tm.get_due_reminders()
                for t in due:
                    self.io.show_reminder(t)
                    self.tm.mark_reminded(t.id)
                time.sleep(1)

    def run(self) -> None:
            while self.running:
                self.io.show_menu()
                choice = self.io.ask("Choose: ")
                self.handle_choice(choice)

    def handle_choice(self, choice: str) -> None:
        if choice == "0":
            self.running = False
            self.io.info("Bye!")

        elif choice == "1":
            self.add_task()

        elif choice == "2":
            self.list_tasks()

        elif choice == "3":
            self.list_tasks("pending")

        elif choice == "4":
            self.list_tasks("done")

        elif choice == "5":
            self.mark_done()

        elif choice == "6":
            self.mark_pending()

        elif choice == "7":
            self.delete_task()

        elif choice == "8":
            self.set_reminder_at()

        elif choice == "9":
            self.set_timer()

        else:
            self.io.error("Invalid choice.")

    def check_reminders(self) -> None:
        due = self.tm.get_due_reminders()
        for t in due:
            self.io.show_reminder(t)
            self.tm.mark_reminded(t.id)


    def add_task(self) -> None:
        title = self.io.ask("Title: ")
        note = self.io.ask_optional("Note (optional): ")

        try:
            task = self.tm.add_task(title, note)
            self.io.info(f"Added: [{task.id}] {task.title}")
        except ValueError as e:
            self.io.error(str(e))

    def list_tasks(self, status: str | None = None) -> None:
        try:
            tasks = self.tm.list_tasks(status)
            self.io.show_tasks(tasks)
        except ValueError as e:
            self.io.error(str(e))

    def mark_done(self) -> None:
        task_id = self.io.ask_int("Task id to mark DONE: ")
        if self.tm.mark_done(task_id):
            self.io.info("Updated.")
        else:
            self.io.error("Task not found.")

    def mark_pending(self) -> None:
        task_id = self.io.ask_int("Task id to mark PENDING: ")
        if self.tm.mark_pending(task_id):
            self.io.info("Updated.")
        else:
            self.io.error("Task not found.")

    def delete_task(self) -> None:
        task_id = self.io.ask_int("Task id to DELETE: ")
        if self.tm.delete_task(task_id):
            self.io.info("Deleted.")
        else:
            self.io.error("Task not found.")


    def set_reminder_at(self) -> None:
        task_id = self.io.ask_int("Task id: ")
        raw = self.io.ask_datetime("Reminder time (YYYY-MM-DD HH:MM) or empty to clear: ")

        if not raw:
            if self.tm.set_reminder(task_id, None):
                self.io.info("Reminder cleared.")
            else:
                self.io.error("Task not found.")
            return

        dt = Time.parse_user_datetime(raw)
        if dt is None:
            self.io.error("Invalid datetime format.")
            return

        if self.tm.set_reminder(task_id, Time.to_iso(dt)):
            self.io.info("Reminder set.")
        else:
            self.io.error("Task not found.")

    def set_timer(self) -> None:
        task_id = self.io.ask_int("Task id: ")
        minutes = self.io.ask_int("Minutes from now: ")

        if self.tm.set_timer_minutes(task_id, minutes):
            self.io.info("Timer set.")
        else:
            self.io.error("Could not set timer (check task id and minutes).")


if __name__ == "__main__":
    Main().run()
