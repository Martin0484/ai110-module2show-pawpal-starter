from pawpal_system import Pet, Owner, Task, Schedule

# Create pet, owner, and schedule
pet = Pet('Buddy', 'dog')
owner = Owner('Sarah')
schedule = Schedule(pet, owner)

# Create a recurring daily task and a one-time task
daily_task = Task('Morning feeding', 15, 'high', frequency='daily')
weekly_task = Task('Bath time', 30, 'medium', frequency='weekly')
one_time_task = Task('Vet checkup', 60, 'high', frequency='one_time')

schedule.add_task(daily_task)
schedule.add_task(weekly_task)
schedule.add_task(one_time_task)

print('Initial tasks:')
for i, task in enumerate(schedule.tasks, 1):
    print(f'{i}. {task.title} (frequency: {task.frequency}, completed: {task.completed})')

print('\n--- Marking daily task as complete ---')
new_daily = schedule.mark_task_complete(daily_task)
print(f'Original task completed: {daily_task.completed}')
print(f'New task created: {new_daily is not None}')
if new_daily:
    print(f'New task: {new_daily.title} (frequency: {new_daily.frequency}, completed: {new_daily.completed})')

print('\n--- Marking weekly task as complete ---')
new_weekly = schedule.mark_task_complete(weekly_task)
print(f'Original task completed: {weekly_task.completed}')
print(f'New task created: {new_weekly is not None}')
if new_weekly:
    print(f'New task: {new_weekly.title} (frequency: {new_weekly.frequency}, completed: {new_weekly.completed})')

print('\n--- Marking one-time task as complete ---')
new_one_time = schedule.mark_task_complete(one_time_task)
print(f'Original task completed: {one_time_task.completed}')
print(f'New task created: {new_one_time is not None}')

print('\nFinal tasks in schedule:')
for i, task in enumerate(schedule.tasks, 1):
    print(f'{i}. {task.title} (frequency: {task.frequency}, completed: {task.completed})')
