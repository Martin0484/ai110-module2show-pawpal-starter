from pawpal_system import Pet, Owner, Task, Schedule

# Test conflict resolution
pet = Pet('Mochi', 'dog', 3, 'Shih Tzu')
owner = Owner('Jordan')

# Create tasks that will overlap
task1 = Task('Morning walk', 20, 'high', 'walking')
task2 = Task('Breakfast', 15, 'high', 'feeding')
task3 = Task('Play time', 30, 'medium', 'play')

schedule = Schedule(pet, owner)
schedule.add_task(task1)
schedule.add_task(task2)
schedule.add_task(task3)

result = schedule.generate_schedule()
print('Generated schedule with conflict resolution:')
for item in result:
    task = item['task']
    start = item['start_time'].strftime('%I:%M %p')
    end = item['end_time'].strftime('%I:%M %p')
    rescheduled = ' (conflict resolved)' if item.get('conflict_resolved') else ''
    print(f'{start} - {end}: {task}{rescheduled}')

if schedule.get_unscheduled_tasks():
    print('\nUnscheduled tasks due to conflicts:')
    for conflict in schedule.get_unscheduled_tasks():
        print(f'  - {conflict["item"]}: {conflict["reason"]}')
else:
    print('\nAll tasks successfully scheduled!')
