"""Integration tests covering habit completion across model and persistence layers."""

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from src.data.db_functionality.db_interface import DB_Interface
from src.data.db_manager import CompleteHabit, Habits


class TestHabitCompletionWorkflow(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        database_path = Path(self.temp_dir.name) / "integration_test.db"
        self.db_interface = DB_Interface(str(database_path))

        # CompleteHabit and Habits normally open the application's default DB.
        # Route both through this isolated test database without changing app code.
        self.db_patch = patch(
            "src.data.db_manager.DB_Interface",
            return_value=self.db_interface,
        )
        self.db_patch.start()

    def tearDown(self):
        self.db_patch.stop()
        self.db_interface.close()
        self.temp_dir.cleanup()

    def create_confirmable_habit(self):
        result, habit_id = self.db_interface.add_habit(
            "Study Python",
            "2026-11-12 15:00:00",
            "00:30:00",
            "TO_BE_CONFIRMED",
            None,
        )
        self.assertEqual("success", result)
        return CompleteHabit(
            name="Study Python",
            session_duration="00:30:00",
            start_date="2026-11-12 15:00:00",
            status="TO_BE_CONFIRMED",
            id=habit_id,
        )

    def test_completion_updates_database_and_status_queries(self):
        habit = self.create_confirmable_habit()

        result, message = habit.complete_habit()

        self.assertEqual("success", result, message)
        completed = Habits().get_habit_by_status("COMPLETED")
        self.assertEqual(1, len(completed))
        self.assertEqual(habit.get_id(), completed[0][0])
        self.assertEqual("Study Python", completed[0][1])
        self.assertEqual("TO_BE_CONFIRMED", habit.get_status())

    def test_completion_removes_habit_from_pending_status_query(self):
        habit = self.create_confirmable_habit()

        result, message = habit.complete_habit()

        self.assertEqual("success", result, message)
        self.assertEqual([], Habits().get_habit_by_status("TO_BE_CONFIRMED"))

    def test_habit_with_non_confirmable_status_cannot_be_completed(self):
        result, habit_id = self.db_interface.add_habit(
            "Already completed",
            "2026-11-12 15:00:00",
            "00:30:00",
            "COMPLETED",
            None,
        )
        self.assertEqual("success", result)
        habit = CompleteHabit(
            name="Already completed",
            session_duration="00:30:00",
            start_date="2026-11-12 15:00:00",
            status="COMPLETED",
            id=habit_id,
        )

        result, message = habit.complete_habit()

        self.assertFalse(result)
        self.assertIn("does not allow", message)
        stored_habit = Habits().get_habit_by_status("COMPLETED")
        self.assertEqual(1, len(stored_habit))
        self.assertEqual(habit_id, stored_habit[0][0])


if __name__ == "__main__":
    unittest.main()
