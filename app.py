import streamlit as st
from pawpal_system import Pet, Owner, Task, Medication, Schedule

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs")
col1, col2, col3 = st.columns(3)
with col1:
    owner_name = st.text_input("Owner name", value="Jordan", key="owner_input")
with col2:
    pet_name = st.text_input("Pet name", value="Mochi", key="pet_input")
with col3:
    species = st.selectbox("Species", ["dog", "cat", "other"], key="species_input")

# Initialize session state for owner and pet
if "owner" not in st.session_state:
    st.session_state.owner = None
if "pet" not in st.session_state:
    st.session_state.pet = None
if "schedule" not in st.session_state:
    st.session_state.schedule = None
if "tasks" not in st.session_state:
    st.session_state.tasks = []

# Create/update Owner and Pet objects based on inputs
st.session_state.owner = Owner(name=owner_name)
st.session_state.pet = Pet(name=pet_name, species=species)

st.success(f"✓ Owner: {st.session_state.owner.name} | Pet: {st.session_state.pet}")

st.markdown("### Add Tasks")
col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

if st.button("Add task"):
    task = Task(title=task_title, duration_minutes=int(duration), priority=priority)
    st.session_state.tasks.append(task)
    st.success(f"✓ Added: {task}")

if st.session_state.tasks:
    st.write("**Current tasks:**")
    task_data = [{"Title": t.title, "Duration": f"{t.duration_minutes} min", "Priority": t.priority} for t in st.session_state.tasks]
    st.table(task_data)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Generate Schedule")

if st.button("Generate schedule"):
    if not st.session_state.tasks:
        st.warning("⚠️ Please add some tasks first.")
    else:
        # Create schedule object and add tasks
        schedule_obj = Schedule(pet=st.session_state.pet, owner=st.session_state.owner)
        
        for task in st.session_state.tasks:
            schedule_obj.add_task(task)
        
        # Generate the schedule with conflict resolution
        generated_schedule = schedule_obj.generate_schedule()
        st.session_state.schedule = generated_schedule
        
        st.success("✓ Schedule generated with conflict resolution!")
        
        # Display the schedule
        st.subheader("Today's Schedule")
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Pet:** {st.session_state.pet}")
        with col2:
            st.write(f"**Owner:** {st.session_state.owner.name}")
        
        st.write("")
        for i, item in enumerate(generated_schedule, 1):
            task = item['task']
            start = item['start_time'].strftime("%I:%M %p")
            end = item['end_time'].strftime("%I:%M %p")
            st.write(f"{i}. **{start} - {end}:** {task}")
        
        # Show any unscheduled tasks
        if schedule_obj.get_unscheduled_tasks():
            st.warning("⚠️ Some tasks could not be scheduled:")
            for conflict in schedule_obj.get_unscheduled_tasks():
                st.write(f"  • {conflict['item']}: {conflict['reason']}")
