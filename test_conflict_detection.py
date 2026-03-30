from pawpal_system import Pet, Owner, Task, Schedule
from datetime import time

# Create owner and pets
owner = Owner('Sarah')
pet1 = Pet('Buddy', 'dog')
pet2 = Pet('Whiskers', 'cat')

# Create schedules for both pets
schedule1 = Schedule(pet1, owner)
schedule2 = Schedule(pet2, owner)

# Add overlapping tasks to same pet
task1 = Task('Morning walk', 30, 'high')
task2 = Task('Feeding', 15, 'high')
schedule1.add_task(task1)
schedule1.add_task(task2)

# Add tasks to second pet
task3 = Task('Playtime', 20, 'medium')
schedule2.add_task(task3)

# Generate both schedules
sched1_items = schedule1.generate_schedule()
sched2_items = schedule2.generate_schedule()

# Combine schedules for unified analysis
all_items = sched1_items + sched2_items

print('=== ALL SCHEDULED ITEMS ===\n')
for i, item in enumerate(all_items, 1):
    task = item['task']
    pet = item.get('pet_name', 'Unknown')
    start = item['start_time'].strftime('%I:%M %p')
    end = item['end_time'].strftime('%I:%M %p')
    print(f'{i}. [{pet}] {start}-{end}: {task.title}')

print('\n=== CHECKING FOR TIME CONFLICTS ===\n')

# Check conflicts in schedule1 (same pet)
conflicts1 = schedule1.find_time_conflicts(sched1_items)
print(f'Conflicts in Buddy\'s schedule: {len(conflicts1)}')
if conflicts1:
    for conflict in conflicts1:
        start = conflict['overlap_start'].strftime('%I:%M %p')
        end = conflict['overlap_end'].strftime('%I:%M %p')
        print(f'  ✗ "{conflict["task1"].title}" and "{conflict["task2"].title}"')
        print(f'    Overlap: {start}-{end} ({conflict["overlap_minutes"]} minutes)')

# Check conflicts across all schedules
all_conflicts = schedule1.find_time_conflicts(all_items)
print(f'\nTotal conflicts across all pets: {len(all_conflicts)}')
if all_conflicts:
    for conflict in all_conflicts:
        start = conflict['overlap_start'].strftime('%I:%M %p')
        end = conflict['overlap_end'].strftime('%I:%M %p')
        pet1 = conflict['pet1']
        pet2 = conflict['pet2']
        same = '(same pet)' if conflict['same_pet'] else '(different pets)'
        print(f'  ✗ [{pet1}] "{conflict["task1"].title}" vs [{pet2}] "{conflict["task2"].title}"')
        print(f'    Overlap: {start}-{end} ({conflict["overlap_minutes"]} min) {same}')
else:
    print('  ✓ No conflicts detected!')

print('\n=== DETAILED SCHEDULE VIEW ===\n')
sorted_all = schedule1.sort_by_time(all_items)
for i, item in enumerate(sorted_all, 1):
    task = item['task']
    pet = item.get('pet_name', 'Unknown')
    start = item['start_time'].strftime('%I:%M %p')
    end = item['end_time'].strftime('%I:%M %p')
    print(f'{i}. {start}-{end}  [{pet}] {task.title}')
