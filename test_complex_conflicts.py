from pawpal_system import Pet, Owner, Task, Schedule

# Test conflict resolution with overlapping tasks
pet = Pet('Mochi', 'dog', 3, 'Shih Tzu')
owner = Owner('Jordan')

# Create tasks that will definitely overlap
task1 = Task('Morning walk', 60, 'high', 'walking')        # 8:00-9:00
task2 = Task('Breakfast', 30, 'high', 'feeding')           # Overlaps!
task3 = Task('Play time', 45, 'medium', 'play')            # Medium priority
task4 = Task('Grooming', 30, 'low', 'grooming')            # Low priority
task5 = Task('Nap time', 90, 'low', 'rest')                # Low priority, long

schedule = Schedule(pet, owner)
schedule.add_task(task1)
schedule.add_task(task2)
schedule.add_task(task3)
schedule.add_task(task4)
schedule.add_task(task5)

result = schedule.generate_schedule()
print('=== CONFLICT RESOLUTION TEST ===\n')
print('Generated schedule:')
for i, item in enumerate(result, 1):
    task = item['task']
    start = item['start_time'].strftime('%I:%M %p')
    end = item['end_time'].strftime('%I:%M %p')
    rescheduled = ' [RESCHEDULED]' if item.get('conflict_resolved') else ''
    print(f'{i}. {start} - {end}: {task}{rescheduled}')

if schedule.get_unscheduled_tasks():
    print('\n⚠️  Unscheduled tasks due to conflicts:')
    for conflict in schedule.get_unscheduled_tasks():
        print(f'  - {conflict["item"]}: {conflict["reason"]}')
else:
    print('\n✓ All tasks successfully scheduled!')
