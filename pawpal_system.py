from datetime import time
from typing import List, Optional


class Pet:
    """Represents a pet in the PawPal+ system."""

    def __init__(self, name: str, species: str, age: Optional[int] = None, breed: Optional[str] = None):
        """Initialize a pet with name, species, age, and breed."""
        self.name = name
        self.species = species
        self.age = age
        self.breed = breed

    def __str__(self):
        """Return string representation of pet."""
        return f"{self.name} ({self.species})"


class Owner:
    """Represents a pet owner in the PawPal+ system."""

    def __init__(self, name: str, preferences: Optional[dict] = None):
        """Initialize an owner with name and optional preferences."""
        self.name = name
        self.preferences = preferences or {}

    def __str__(self):
        """Return string representation of owner."""
        return f"Owner: {self.name}"


class Task:
    """Represents a pet care task."""

    def __init__(self, title: str, duration_minutes: int, priority: str, task_type: Optional[str] = None, frequency: str = "one_time"):
        """Initialize a task with title, duration, priority, optional type, and recurrence frequency."""
        self.title = title
        self.duration_minutes = duration_minutes
        self.priority = priority
        self.task_type = task_type
        self.frequency = frequency  # 'one_time', 'daily', 'weekly'
        self.completed = False

    def __str__(self):
        """Return string representation of task."""
        return f"{self.title} ({self.duration_minutes} min, {self.priority} priority)"

    def mark_complete(self):
        """Mark the task as completed."""
        self.completed = True

    def is_recurring(self) -> bool:
        """Check if task is recurring (daily or weekly)."""
        return self.frequency in ['daily', 'weekly']


class Medication:
    """Represents a medication for a pet."""

    def __init__(self, name: str, dosage: str, frequency: str, duration_minutes: int = 5):
        """Initialize a medication with name, dosage, frequency, and administration time."""
        self.name = name
        self.dosage = dosage
        self.frequency = frequency
        self.duration_minutes = duration_minutes

    def __str__(self):
        """Return string representation of medication."""
        return f"{self.name} ({self.dosage}, {self.frequency})"


class Schedule:
    """Manages scheduling of tasks for a pet with conflict resolution."""

    def __init__(self, pet: Pet, owner: Owner):
        """Initialize a schedule for a pet and owner."""
        self.pet = pet
        self.owner = owner
        self.tasks: List[Task] = []
        self.medications: List[Medication] = []
        self.scheduled_items: List[dict] = []  # Tracks what's actually scheduled
        self.conflicts: List[dict] = []  # Tracks unresolved conflicts

    def add_task(self, task: Task):
        """Add a task to the schedule."""
        self.tasks.append(task)

    def add_medication(self, medication: Medication):
        """Add a medication to the schedule."""
        self.medications.append(medication)

    def _has_time_conflict(self, start_time, end_time) -> bool:
        """Check if a time slot conflicts with already scheduled items."""
        for item in self.scheduled_items:
            item_start = item['start_time']
            item_end = item['end_time']
            # Check for any overlap
            if not (end_time <= item_start or start_time >= item_end):
                return True
        return False

    def _get_conflicting_item(self, start_time, end_time) -> Optional[dict]:
        """Return the first item that conflicts with the given time slot."""
        for item in self.scheduled_items:
            item_start = item['start_time']
            item_end = item['end_time']
            if not (end_time <= item_start or start_time >= item_end):
                return item
        return None

    def _try_reschedule_item(self, item: dict, conflicts_encountered: int = 0) -> bool:
        """Attempt to reschedule an item to a later available time slot."""
        if conflicts_encountered > 5:  # Prevent deep recursion
            return False

        # Remove item temporarily to find next available slot
        self.scheduled_items.remove(item)
        
        item_duration = self._time_diff(item['start_time'], item['end_time'])
        proposed_start = item['end_time']
        
        # Try to find a slot after the original time
        max_attempts = 10
        for _ in range(max_attempts):
            proposed_end = self._add_minutes(proposed_start, item_duration)
            
            if not self._has_time_conflict(proposed_start, proposed_end):
                # Found a slot, update and reschedule
                item['start_time'] = proposed_start
                item['end_time'] = proposed_end
                item['rescheduled'] = True
                self.scheduled_items.append(item)
                return True
            
            # Move forward by a small increment to try next slot
            proposed_start = self._add_minutes(proposed_start, 15)
        
        # Could not find a slot, restore item and mark as conflict
        self.scheduled_items.append(item)
        return False

    def generate_schedule(self) -> List[dict]:
        """Generate schedule with automatic conflict detection and resolution by priority."""
        self.scheduled_items = []
        self.conflicts = []
        
        # Combine and sort all items by priority
        priority_order = {'high': 0, 'medium': 1, 'low': 2}
        
        all_items = []
        for task in self.tasks:
            all_items.append({'type': 'task', 'item': task, 'priority': priority_order.get(task.priority, 2)})
        for med in self.medications:
            all_items.append({'type': 'medication', 'item': med, 'priority': 1})  # Medications are medium priority
        
        # Sort by priority (high first)
        all_items.sort(key=lambda x: x['priority'])
        
        current_time = time(8, 0)  # Start at 8 AM
        
        for item_entry in all_items:
            item = item_entry['item']
            item_type = item_entry['type']
            duration = item.duration_minutes if hasattr(item, 'duration_minutes') else 5
            
            proposed_end = self._add_minutes(current_time, duration)
            
            # Check for conflicts
            if self._has_time_conflict(current_time, proposed_end):
                conflicting_item = self._get_conflicting_item(current_time, proposed_end)
                
                # Try to reschedule the conflicting item if it's lower priority
                if conflicting_item.get('priority', 2) >= item_entry['priority']:
                    if self._try_reschedule_item(conflicting_item):
                        # Conflict resolved, schedule the new item
                        self.scheduled_items.append({
                            'task': item,
                            'start_time': current_time,
                            'end_time': proposed_end,
                            'priority': item_entry['priority'],
                            'type': item_type,
                            'conflict_resolved': True,
                            'pet_name': self.pet.name
                        })
                        current_time = self._add_minutes(proposed_end, 15)  # 15 min break
                    else:
                        # Could not resolve, log conflict
                        self.conflicts.append({
                            'item': item,
                            'requested_time': (current_time, proposed_end),
                            'reason': 'Unable to find available time slot'
                        })
                else:
                    # Lower priority item, reschedule this item instead
                    if self._try_reschedule_item({'task': item, 'start_time': current_time, 'end_time': proposed_end, 'priority': item_entry['priority'], 'type': item_type}):
                        self.scheduled_items.append({'task': item, 'start_time': current_time, 'end_time': proposed_end, 'priority': item_entry['priority'], 'type': item_type, 'pet_name': self.pet.name})
                    else:
                        self.conflicts.append({
                            'item': item,
                            'requested_time': (current_time, proposed_end),
                            'reason': 'Unable to reschedule'
                        })
            else:
                # No conflict, schedule normally
                self.scheduled_items.append({
                    'task': item,
                    'start_time': current_time,
                    'end_time': proposed_end,
                    'priority': item_entry['priority'],
                    'type': item_type,
                    'pet_name': self.pet.name
                })
                current_time = self._add_minutes(proposed_end, 15)  # 15 min break
        
        return self.scheduled_items

    def get_unscheduled_tasks(self) -> List[dict]:
        """Return list of tasks that couldn't be scheduled due to conflicts."""
        return self.conflicts

    def sort_by_time(self, schedule: List[dict]) -> List[dict]:
        """Sort schedule items chronologically by start time."""
        return sorted(schedule, key=lambda x: (x['start_time'].hour, x['start_time'].minute))

    def filter_by_pet(self, pet_name: str, schedule: List[dict] = None) -> List[dict]:
        """Filter schedule items by pet name."""
        if schedule is None:
            schedule = self.scheduled_items
        return [item for item in schedule if item.get('pet_name') == pet_name]

    def mark_task_complete(self, task: Task) -> Optional[Task]:
        """Mark a task as complete and create next occurrence if recurring. Returns new task if created, None otherwise."""
        task.mark_complete()
        
        if task.is_recurring():
            # Create new instance of the recurring task
            new_task = Task(
                title=task.title,
                duration_minutes=task.duration_minutes,
                priority=task.priority,
                task_type=task.task_type,
                frequency=task.frequency
            )
            # Add the new task to the schedule
            self.add_task(new_task)
            return new_task
        
        return None

    def find_time_conflicts(self, schedule: List[dict] = None) -> List[dict]:
        """Detect overlapping tasks and return list of conflicts."""
        if schedule is None:
            schedule = self.scheduled_items
        
        conflicts = []
        
        # Compare each pair of scheduled items
        for i in range(len(schedule)):
            for j in range(i + 1, len(schedule)):
                item1 = schedule[i]
                item2 = schedule[j]
                
                start1 = item1['start_time']
                end1 = item1['end_time']
                start2 = item2['start_time']
                end2 = item2['end_time']
                
                # Check if time ranges overlap
                has_overlap = not (end1 <= start2 or start2 >= end1)
                
                if has_overlap:
                    pet1 = item1.get('pet_name', 'Unknown')
                    pet2 = item2.get('pet_name', 'Unknown')
                    same_pet = pet1 == pet2
                    
                    conflicts.append({
                        'task1': item1['task'],
                        'task2': item2['task'],
                        'pet1': pet1,
                        'pet2': pet2,
                        'same_pet': same_pet,
                        'overlap_start': max(start1, start2),
                        'overlap_end': min(end1, end2),
                        'overlap_minutes': self._time_diff(max(start1, start2), min(end1, end2))
                    })
        
        return conflicts

    def get_conflict_warnings(self, schedule: List[dict] = None) -> List[str]:
        """Return lightweight warning messages for any detected conflicts without crashing."""
        conflicts = self.find_time_conflicts(schedule)
        warnings = []
        
        if not conflicts:
            return warnings
        
        for conflict in conflicts:
            pet1 = conflict['pet1']
            pet2 = conflict['pet2']
            task1 = conflict['task1'].title
            task2 = conflict['task2'].title
            overlap_start = conflict['overlap_start'].strftime('%I:%M %p')
            overlap_end = conflict['overlap_end'].strftime('%I:%M %p')
            overlap_min = conflict['overlap_minutes']
            
            if conflict['same_pet']:
                msg = f"⚠️  {pet1}: '{task1}' and '{task2}' overlap ({overlap_start}-{overlap_end}, {overlap_min} min)"
            else:
                msg = f"⚠️  {pet1} and {pet2}: '{task1}' overlaps with '{task2}' ({overlap_start}-{overlap_end}, {overlap_min} min)"
            
            warnings.append(msg)
        
        return warnings

    def _add_minutes(self, start_time, minutes: int):
        """Add minutes to a time object."""
        total_minutes = start_time.hour * 60 + start_time.minute + minutes
        hour = (total_minutes // 60) % 24
        minute = total_minutes % 60
        return time(hour, minute)

    def _time_diff(self, start_time, end_time) -> int:
        """Calculate the difference in minutes between two time objects."""
        start_total = start_time.hour * 60 + start_time.minute
        end_total = end_time.hour * 60 + end_time.minute
        return end_total - start_total
