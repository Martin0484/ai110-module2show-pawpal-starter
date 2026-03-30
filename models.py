from datetime import time
from typing import List, Optional


class Pet:
    """Represents a pet in the PawPal+ system."""

    def __init__(self, name: str, species: str, age: Optional[int] = None, breed: Optional[str] = None):
        self.name = name
        self.species = species
        self.age = age
        self.breed = breed

    def __str__(self):
        return f"{self.name} ({self.species})"


class Owner:
    """Represents a pet owner in the PawPal+ system."""

    def __init__(self, name: str, preferences: Optional[dict] = None):
        self.name = name
        self.preferences = preferences or {}

    def __str__(self):
        return f"Owner: {self.name}"


class Task:
    """Represents a pet care task."""

    def __init__(self, title: str, duration_minutes: int, priority: str, task_type: Optional[str] = None):
        self.title = title
        self.duration_minutes = duration_minutes
        self.priority = priority  # 'low', 'medium', 'high'
        self.task_type = task_type  # e.g., 'feeding', 'walking', 'grooming'

    def __str__(self):
        return f"{self.title} ({self.duration_minutes} min, {self.priority} priority)"


class Medication:
    """Represents a medication for a pet."""

    def __init__(self, name: str, dosage: str, frequency: str, duration_minutes: int = 5):
        self.name = name
        self.dosage = dosage
        self.frequency = frequency  # e.g., 'daily', 'twice daily'
        self.duration_minutes = duration_minutes  # time to administer

    def __str__(self):
        return f"{self.name} ({self.dosage}, {self.frequency})"


class Schedule:
    """Manages scheduling of tasks for a pet."""

    def __init__(self, pet: Pet, owner: Owner):
        self.pet = pet
        self.owner = owner
        self.tasks: List[Task] = []
        self.medications: List[Medication] = []

    def add_task(self, task: Task):
        self.tasks.append(task)

    def add_medication(self, medication: Medication):
        self.medications.append(medication)

    def generate_schedule(self) -> List[dict]:
        """
        Generate a simple schedule prioritizing high priority tasks first.
        This is a basic implementation - can be enhanced with time constraints.
        """
        # Sort tasks by priority (high first)
        priority_order = {'high': 0, 'medium': 1, 'low': 2}
        sorted_tasks = sorted(self.tasks, key=lambda t: priority_order.get(t.priority, 2))

        schedule = []
        current_time = time(8, 0)  # Start at 8 AM

        for task in sorted_tasks:
            schedule.append({
                'task': task,
                'start_time': current_time,
                'end_time': self._add_minutes(current_time, task.duration_minutes)
            })
            current_time = self._add_minutes(current_time, task.duration_minutes + 15)  # 15 min break

        # Add medications (assuming they need to be scheduled too)
        for med in self.medications:
            # Simple scheduling - add at end for now
            schedule.append({
                'task': med,
                'start_time': current_time,
                'end_time': self._add_minutes(current_time, med.duration_minutes)
            })
            current_time = self._add_minutes(current_time, med.duration_minutes + 5)

        return schedule

    def _add_minutes(self, start_time, minutes: int):
        """Add minutes to a time object."""
        total_minutes = start_time.hour * 60 + start_time.minute + minutes
        hour = (total_minutes // 60) % 24
        minute = total_minutes % 60
        return time(hour, minute)