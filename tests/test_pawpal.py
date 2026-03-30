import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from pawpal_system import Pet, Owner, Task, Schedule
from datetime import time

def test_chronological_order():
    """Test that tasks are returned in chronological order."""
    # Create a pet and owner
    pet = Pet("Buddy", "Dog")
    owner = Owner("Alice")

    # Create a schedule
    schedule = Schedule(pet, owner)

    # Add tasks with different priorities to potentially disrupt order
    task1 = Task("Evening walk", 30, "low")
    task2 = Task("Morning walk", 45, "high")
    task3 = Task("Afternoon nap", 60, "medium")

    schedule.add_task(task1)
    schedule.add_task(task2)
    schedule.add_task(task3)

    # Generate the schedule
    generated_schedule = schedule.generate_schedule()

    # Sort by time to ensure chronological order
    sorted_schedule = schedule.sort_by_time(generated_schedule)

    # Check if the sorted schedule is in chronological order
    previous_time = time(0, 0)  # Midnight as baseline
    for item in sorted_schedule:
        start_time = item['start_time']
        assert start_time >= previous_time, f"Task '{item['task'].title}' at {start_time} is not after {previous_time}"
        previous_time = start_time

def test_recurring_task_creation():
    """Test that marking a daily task complete creates a new task."""
    # Create a pet and owner
    pet = Pet("Max", "Cat")
    owner = Owner("Bob")

    # Create a schedule
    schedule = Schedule(pet, owner)

    # Add a daily task
    daily_task = Task("Daily feeding", 10, "high", frequency="daily")
    schedule.add_task(daily_task)

    # Initially, there should be 1 task
    assert len(schedule.tasks) == 1

    # Mark the task complete
    new_task = schedule.mark_task_complete(daily_task)

    # Check that a new task was created and returned
    assert new_task is not None
    assert new_task.title == "Daily feeding"
    assert new_task.frequency == "daily"
    assert new_task.completed == False  # New task is not completed

    # Check that the new task was added to the schedule
    assert len(schedule.tasks) == 2
    assert schedule.tasks[1] == new_task

    # Check that the original task is marked complete
    assert daily_task.completed == True

def test_duplicate_times_flagging():
    """Test that the scheduler flags duplicate/overlapping times."""
    # Create a pet and owner
    pet = Pet("Rex", "Dog")
    owner = Owner("Charlie")

    # Create a schedule
    schedule = Schedule(pet, owner)

    # Manually create scheduled items with overlapping times
    task1 = Task("Walk", 30, "high")
    task2 = Task("Feed", 20, "medium")

    schedule.scheduled_items = [
        {
            'task': task1,
            'start_time': time(8, 0),
            'end_time': time(8, 30),
            'pet_name': 'Rex'
        },
        {
            'task': task2,
            'start_time': time(8, 15),  # Overlaps with task1
            'end_time': time(8, 35),
            'pet_name': 'Rex'
        }
    ]

    # Check for conflicts
    conflicts = schedule.find_time_conflicts()

    # Should detect the overlap
    assert len(conflicts) == 1
    conflict = conflicts[0]
    assert conflict['task1'].title == "Walk"
    assert conflict['task2'].title == "Feed"
    assert conflict['overlap_minutes'] == 15  # 8:15 to 8:30

    # Also check get_conflict_warnings
    warnings = schedule.get_conflict_warnings()
    assert len(warnings) == 1
    assert "overlap" in warnings[0]

    print("✅ Scheduler flags duplicate/overlapping times.")

if __name__ == "__main__":
    test_chronological_order()
    test_recurring_task_creation()
    test_duplicate_times_flagging()