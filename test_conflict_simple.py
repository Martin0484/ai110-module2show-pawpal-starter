from pawpal_system import Pet, Owner, Task, Schedule
from datetime import time

# Create owner and pets
owner = Owner('Sarah')
pet1 = Pet('Buddy', 'dog')
pet2 = Pet('Whiskers', 'cat')

# Manually create items with overlaps
buddy_items = [
    {'task': Task('Morning walk', 45, 'high'), 'start_time': time(8, 0), 'end_time': time(8, 45), 'pet_name': 'Buddy'},
    {'task': Task('Breakfast', 30, 'high'), 'start_time': time(8, 30), 'end_time': time(9, 0), 'pet_name': 'Buddy'}
]

whiskers_items = [
    {'task': Task('Playtime', 20, 'medium'), 'start_time': time(8, 0), 'end_time': time(8, 20), 'pet_name': 'Whiskers'}
]

schedule = Schedule(pet1, owner)

# Test 1: Same pet conflicts
print('=== TEST 1: SAME PET OVERLAPS ===\n')
conflicts = schedule.find_time_conflicts(buddy_items)
print(f'Buddy\'s schedule conflicts: {len(conflicts)}')
if conflicts:
    for c in conflicts:
        print(f'  ✗ "{c["task1"].title}" overlaps "{c["task2"].title}"')

# Test 2: Cross-pet conflicts
print('\n=== TEST 2: DIFFERENT PETS ===\n')
all_items = buddy_items + whiskers_items
conflicts = schedule.find_time_conflicts(all_items)
print(f'Total conflicts: {len(conflicts)}')
for c in conflicts:
    pet1_name = c['pet1']
    pet2_name = c['pet2']
    same = '(same pet)' if c['same_pet'] else '(different pets)'
    print(f'  ✗ [{pet1_name}] "{c["task1"].title}" vs [{pet2_name}] "{c["task2"].title}" {same}')
