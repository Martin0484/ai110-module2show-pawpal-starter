from pawpal_system import Pet, Owner, Task, Schedule
from datetime import time

# Create owner and pets
owner = Owner('Sarah')
pet1 = Pet('Buddy', 'dog')
pet2 = Pet('Whiskers', 'cat')

# Manually create items with overlaps
buddy_items = [
    {'task': Task('Morning walk', 45, 'high'), 'start_time': time(8, 0), 'end_time': time(8, 45), 'pet_name': 'Buddy'},
    {'task': Task('Breakfast', 30, 'high'), 'start_time': time(8, 30), 'end_time': time(9, 0), 'pet_name': 'Buddy'},
    {'task': Task('Playtime', 20, 'medium'), 'start_time': time(9, 0), 'end_time': time(9, 20), 'pet_name': 'Buddy'}
]

whiskers_items = [
    {'task': Task('Playtime', 20, 'medium'), 'start_time': time(8, 10), 'end_time': time(8, 30), 'pet_name': 'Whiskers'},
    {'task': Task('Nap time', 60, 'low'), 'start_time': time(9, 0), 'end_time': time(10, 0), 'pet_name': 'Whiskers'}
]

schedule = Schedule(pet1, owner)

# Test: Get conflict warnings
print('=== LIGHTWEIGHT CONFLICT DETECTION ===\n')

all_items = buddy_items + whiskers_items

warnings = schedule.get_conflict_warnings(all_items)

if warnings:
    print(f'Found {len(warnings)} conflict(s):\n')
    for warning in warnings:
        print(warning)
else:
    print('✓ No conflicts detected!')

print('\n=== SCHEDULE VIEW ===\n')
sorted_items = schedule.sort_by_time(all_items)
for item in sorted_items:
    start = item['start_time'].strftime('%I:%M %p')
    end = item['end_time'].strftime('%I:%M %p')
    pet = item.get('pet_name')
    task = item['task'].title
    print(f'{start}-{end}  [{pet}] {task}')
