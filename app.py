"""Streamlit UI for PawPal+."""

import streamlit as st
from pawpal_system import Owner, Pet, Task, Priority, Scheduler, Plan

# Configure the Streamlit page (Must be the first st command)
st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="wide")

# 1. Initialize State Data
if "owner" not in st.session_state:
    # Create a default owner and a sample pet so the app isn't empty on first load
    default_owner = Owner(owner_id="u1", name="Jordan", email="jordan@example.com")
    default_pet = Pet(pet_id="p1", name="Mochi", species="Dog", age=3.0)
    default_owner.add_pet(default_pet)
    st.session_state.owner = default_owner

if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler()

st.title("🐾 PawPal+ Care Planner")
st.write(f"Welcome back, {st.session_state.owner.name}!")

# Create Tabs for organization
tab1, tab2 = st.tabs(["👤 Profile & Pets", "📅 Schedule & Tasks"])

# --- TAB 1: USER & PET MANAGEMENT ---
with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Update Owner Profile")
        with st.form("owner_form"):
            new_name = st.text_input("Name", value=st.session_state.owner.name)
            new_email = st.text_input("Email", value=st.session_state.owner.email)
            if st.form_submit_button("Update Profile"):
                st.session_state.owner.name = new_name
                st.session_state.owner.email = new_email
                st.success("Profile updated!")
                st.rerun()

    with col2:
        st.subheader("Add a New Pet")
        with st.form("pet_form"):
            pet_name = st.text_input("Pet Name")
            pet_species = st.text_input("Species (e.g., Dog, Cat)")
            pet_age = st.number_input("Age", min_value=0.0, step=0.5)
            if st.form_submit_button("Add Pet") and pet_name:
                new_pet_id = f"p{len(st.session_state.owner.get_pets()) + 1}"
                new_pet = Pet(pet_id=new_pet_id, name=pet_name, species=pet_species, age=pet_age)
                st.session_state.owner.add_pet(new_pet)
                st.success(f"{pet_name} added to your family!")
                st.rerun()
                
    st.divider()
    st.write("**Current Pets:**")
    for pet in st.session_state.owner.get_pets():
        st.write(f"- {pet.name} ({pet.species}, {pet.age} yrs old)")


# --- TAB 2: MAIN DASHBOARD & SCHEDULE GENERATION ---
with tab2:
    # SIDEBAR: Add Tasks
    st.sidebar.header("Add a Care Task")
    with st.sidebar.form("add_task_form"):
        # Let the user pick which pet this task is for
        pet_names = {pet.name: pet.pet_id for pet in st.session_state.owner.get_pets()}
        
        if not pet_names:
            st.warning("Please add a pet first.")
            st.form_submit_button("Add Task", disabled=True)
        else:
            selected_pet_name = st.selectbox("Select Pet", options=list(pet_names.keys()))
            title = st.text_input("Task Title", placeholder="e.g., Morning Walk")
            duration = st.number_input("Duration (minutes)", min_value=1, value=15)
            priority_map = {"Low": Priority.LOW, "Medium": Priority.MEDIUM, "High": Priority.HIGH, "Critical": Priority.CRITICAL}
            priority_selection = st.selectbox("Priority", options=list(priority_map.keys()), index=2)
            scheduled_time = st.text_input("Scheduled Time", placeholder="08:00 AM")
            
            submitted = st.form_submit_button("Add Task")
            if submitted and title:
                new_task = Task(
                    task_id=f"t{len(st.session_state.owner.get_all_tasks()) + 1}",
                    pet_id=pet_names[selected_pet_name],
                    title=title,
                    duration=duration,
                    priority=priority_map[priority_selection],
                    scheduled_time=scheduled_time
                )
                for pet in st.session_state.owner.get_pets():
                    if pet.pet_id == new_task.pet_id:
                        pet.add_task(new_task)
                        break
                st.sidebar.success(f"Added '{title}' for {selected_pet_name}!")
                st.rerun()

    st.header("Daily Schedule Generation")
    time_budget = st.slider("How much time do you have today? (minutes)", min_value=15, max_value=300, value=120, step=15)

    if st.button("Generate Daily Plan", type="primary"):
        plan: Plan = st.session_state.scheduler.generate_daily_plan(
            st.session_state.owner, time_limit_minutes=time_budget
        )
        
        st.subheader(f"Scheduled Tasks ({time_budget - plan.remaining_minutes} mins used)")
        if not plan.scheduled:
            st.info("No tasks fit the schedule.")
        else:
            for task in plan.scheduled:
                pet_name = next(p.name for p in st.session_state.owner.get_pets() if p.pet_id == task.pet_id)
                st.success(f"✅ **{task.scheduled_time}** — {task.title} for {pet_name} ({task.duration} mins) [Priority: {task.priority.name}]")