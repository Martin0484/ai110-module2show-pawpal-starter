from pawpal_system import Pet, Owner, Task, Schedule


def print_schedule_header(pet_name, owner_name):
    """Print a formatted schedule header."""
    print("\n" + "=" * 60)
    print(f"  🐾 Today's Schedule for {pet_name}")
    print(f"  Owner: {owner_name}")
    print("=" * 60)


def print_schedule_item(index, start_time, end_time, task_name, priority):
    """Print a formatted schedule item."""
    priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}
    emoji = priority_emoji.get(priority, "⚪")
    start = start_time.strftime("%I:%M %p")
    end = end_time.strftime("%I:%M %p")
    print(f"{index}. {start} - {end}  {emoji}  {task_name}")


def main():
    # Create owner
    owner = Owner(name="Sarah", preferences={"early_riser": True})
    
    # Create two pets
    pet1 = Pet(name="Buddy", species="dog", age=3, breed="Golden Retriever")
    pet2 = Pet(name="Whiskers", species="cat", age=5, breed="Siamese")
    
    print(f"\n👤 Owner: {owner.name}")
    print(f"🐕 Pet 1: {pet1}")
    print(f"🐈 Pet 2: {pet2}")
    
    # ========== SCHEDULE FOR PET 1 (Buddy) ==========
    schedule1 = Schedule(pet=pet1, owner=owner)
    
    # Add tasks for Buddy
    task1_1 = Task(title="Morning Walk", duration_minutes=30, priority="high", task_type="walking")
    task1_2 = Task(title="Breakfast", duration_minutes=15, priority="high", task_type="feeding")
    task1_3 = Task(title="Afternoon Play", duration_minutes=45, priority="medium", task_type="play")
    
    schedule1.add_task(task1_1)
    schedule1.add_task(task1_2)
    schedule1.add_task(task1_3)
    
    # Generate and display schedule for Buddy
    buddy_schedule = schedule1.generate_schedule()
    print_schedule_header(pet1.name, owner.name)
    for i, item in enumerate(buddy_schedule, 1):
        task = item['task']
        print_schedule_item(i, item['start_time'], item['end_time'], str(task), task.priority)
    
    # ========== SCHEDULE FOR PET 2 (Whiskers) ==========
    schedule2 = Schedule(pet=pet2, owner=owner)
    
    # Add tasks for Whiskers
    task2_1 = Task(title="Breakfast", duration_minutes=10, priority="high", task_type="feeding")
    task2_2 = Task(title="Litter Box", duration_minutes=5, priority="high", task_type="hygiene")
    task2_3 = Task(title="Play with Toy", duration_minutes=20, priority="medium", task_type="play")
    
    schedule2.add_task(task2_1)
    schedule2.add_task(task2_2)
    schedule2.add_task(task2_3)
    
    # Generate and display schedule for Whiskers
    whiskers_schedule = schedule2.generate_schedule()
    print_schedule_header(pet2.name, owner.name)
    for i, item in enumerate(whiskers_schedule, 1):
        task = item['task']
        print_schedule_item(i, item['start_time'], item['end_time'], str(task), task.priority)
    
    # Print summary
    print("\n" + "=" * 60)
    print(f"Total tasks scheduled: {len(buddy_schedule) + len(whiskers_schedule)}")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
