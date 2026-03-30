from pawpal_system import Pet, Owner, Task, Schedule

# Create pets and owner
pet = Pet('Max', 'dog')
owner = Owner('John')
schedule = Schedule(pet, owner)

# Create tasks with different frequencies
morning_walk = Task('Morning walk', 30, 'high', frequency='daily')
weekly_grooming = Task('Grooming', 60, 'medium', frequency='weekly')
medication = Task('Take medication', 5, 'high', frequency='daily')
vet_visit = Task('Annual vet checkup', 90, 'high', frequency='one_time')

schedule.add_task(morning_walk)
schedule.add_task(weekly_grooming)
schedule.add_task(medication)
schedule.add_task(vet_visit)

# Generate initial schedule
generated_schedule = schedule.generate_schedule()

print('=== INITIAL SCHEDULE ===\n')
for i, item in enumerate(generated_schedule, 1):
    task = item['task']
    start = item['start_time'].strftime('%I:%M %p')
    print(f'{i}. {start}: {task.title} (frequency: {task.frequency})')

print('\n=== COMPLETING DAILY TASKS ===\n')

# Complete the morning walk
new_walk = schedule.mark_task_complete(morning_walk)
print(f'✓ Marked "{morning_walk.title}" as complete')
if new_walk:
    print(f'✓ Created new instance of "{new_walk.title}" for tomorrow')

# Complete the medication
new_med = schedule.mark_task_complete(medication)
print(f'✓ Marked "{medication.title}" as complete')
if new_med:
    print(f'✓ Created new instance of "{new_med.title}" for tomorrow')

print('\n=== COMPLETING ONE-TIME TASK ===\n')

# Complete vet visit (no new instance created)
result = schedule.mark_task_complete(vet_visit)
print(f'✓ Marked "{vet_visit.title}" as complete')
if result is None:
    print(f'✗ No new instance created (one-time task)')

print('\n=== TASKS IN SCHEDULE ===\n')
print('Total tasks (including completed):', len(schedule.tasks))
print('\nCompleted tasks:')
for task in schedule.tasks:
    if task.completed:
        print(f'  ✓ {task.title} ({task.frequency})')

print('\nPending tasks:')
for task in schedule.tasks:
    if not task.completed:
        print(f'  ○ {task.title} ({task.frequency})')
