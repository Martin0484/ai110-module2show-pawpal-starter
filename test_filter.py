from pawpal_system import Pet, Owner, Task, Schedule

# Create two pets and owner
pet1 = Pet('Buddy', 'dog')
pet2 = Pet('Whiskers', 'cat')
owner = Owner('Sarah')

# Create schedules for both pets
schedule1 = Schedule(pet1, owner)
schedule2 = Schedule(pet2, owner)

# Add tasks to pet1
task1 = Task('Morning walk', 30, 'high')
task2 = Task('Breakfast', 15, 'high')
schedule1.add_task(task1)
schedule1.add_task(task2)

# Add tasks to pet2
task3 = Task('Litter box', 5, 'high')
task4 = Task('Play time', 20, 'medium')
schedule2.add_task(task3)
schedule2.add_task(task4)

# Generate schedules
schedule1_items = schedule1.generate_schedule()
schedule2_items = schedule2.generate_schedule()

# Combine both schedules
all_items = schedule1_items + schedule2_items

print('All scheduled items:')
for i, item in enumerate(all_items, 1):
    print(f'{i}. {item["pet_name"]}: {item["task"]}')

print('\n--- Filter by pet name ---')
buddy_tasks = schedule1.filter_by_pet('Buddy', all_items)
print(f'\nBuddy\'s tasks ({len(buddy_tasks)}):')
for i, item in enumerate(buddy_tasks, 1):
    start = item['start_time'].strftime('%I:%M %p')
    print(f'{i}. {start}: {item["task"]}')

whiskers_tasks = schedule1.filter_by_pet('Whiskers', all_items)
print(f'\nWhiskers\' tasks ({len(whiskers_tasks)}):')
for i, item in enumerate(whiskers_tasks, 1):
    start = item['start_time'].strftime('%I:%M %p')
    print(f'{i}. {start}: {item["task"]}')
