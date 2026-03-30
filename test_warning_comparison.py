from pawpal_system import Pet, Owner, Task, Schedule
from datetime import time

owner = Owner('Jordan')
pet = Pet('Max', 'dog')
schedule = Schedule(pet, owner)

# Create items with overlaps
items = [
    {'task': Task('Morning walk', 30, 'high'), 'start_time': time(8, 0), 'end_time': time(8, 30), 'pet_name': 'Max'},
    {'task': Task('Breakfast', 20, 'high'), 'start_time': time(8, 15), 'end_time': time(8, 35), 'pet_name': 'Max'},
    {'task': Task('Training', 45, 'medium'), 'start_time': time(9, 0), 'end_time': time(9, 45), 'pet_name': 'Max'}
]

print('=== LIGHTWEIGHT CONFLICT DETECTION DEMO ===\n')

# Method 1: Detailed conflict objects (useful for analytics/reports)
print('METHOD 1: Detailed Conflict Info')
print('-' * 50)
conflicts = schedule.find_time_conflicts(items)
print(f'Detailed conflicts found: {len(conflicts)}\n')
for i, c in enumerate(conflicts, 1):
    print(f'{i}. {c["task1"].title} vs {c["task2"].title}')
    print(f'   Overlap: {c["overlap_minutes"]} minutes')
    print(f'   Time window: {c["overlap_start"].strftime("%I:%M %p")}-{c["overlap_end"].strftime("%I:%M %p")}')
    print()

# Method 2: Lightweight warning messages (ideal for UI/logs)
print('\nMETHOD 2: User-Friendly Warnings')
print('-' * 50)
warnings = schedule.get_conflict_warnings(items)
print(f'Warnings generated: {len(warnings)}\n')
for warning in warnings:
    print(warning)

print('\n✓ Program continues running - no crashes!')
print('✓ Can display warnings to user via UI')
print('✓ Lightweight and efficient')
