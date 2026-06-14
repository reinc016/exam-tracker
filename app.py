import asyncio
import sys

# Force selector loop for Windows compatibility
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import streamlit as st
from database import init_db, SessionLocal
from models import Subject, Module

# Initialize the database
init_db()

# Page configuration
st.set_page_config(page_title="Exam Readiness Tracker", layout="wide")

# Sidebar navigation
menu = st.sidebar.selectbox("Menu", ["Dashboard", "Manage Subjects", "Add Progress"])

# --- DASHBOARD SECTION ---
if menu == "Dashboard":
    st.title("📊 Exam Readiness Overview")
    session = SessionLocal()
    subjects = session.query(Subject).all()
    
    if not subjects:
        st.info("No subjects added yet. Go to 'Manage Subjects' to get started!")
    else:
        for sub in subjects:
            modules = session.query(Module).filter_by(subject_id=sub.id).all()
            total = len(modules)
            completed = len([m for m in modules if m.is_completed])
            progress = (completed / total) if total > 0 else 0
            
            with st.expander(f"📚 {sub.name} (Progress: {int(progress*100)}%)"):
                st.progress(progress)
                if modules:
                    for mod in modules:
                        st.write(f"- {mod.name} {'✅' if mod.is_completed else '⏳'}")
                else:
                    st.write("No modules added yet.")
    session.close()

# --- MANAGE SUBJECTS SECTION ---
elif menu == "Manage Subjects":
    st.title("📚 Add or Delete Subjects & Modules")
    
    # 1. Add Subject
    with st.form("subject_form"):
        subject_name = st.text_input("Subject Name")
        target_hours = st.number_input("Target Hours", min_value=1, value=50)
        if st.form_submit_button("Add Subject"):
            session = SessionLocal()
            session.add(Subject(name=subject_name, target_hours=target_hours))
            session.commit()
            session.close()
            st.rerun()

    # 2. Add Module
    st.subheader("Add Module to Subject")
    session = SessionLocal()
    subjects = session.query(Subject).all()
    if subjects:
        with st.form("module_form"):
            selected_sub = st.selectbox("Choose Subject", [s.name for s in subjects])
            module_name = st.text_input("Module Name")
            if st.form_submit_button("Add Module"):
                subject = session.query(Subject).filter_by(name=selected_sub).first()
                session.add(Module(name=module_name, subject_id=subject.id))
                session.commit()
                st.success(f"Added {module_name} to {selected_sub}!")
                st.rerun()

    # 3. Delete Subject
    st.divider()
    st.subheader("⚠️ Delete Subject")
    if subjects:
        del_sub_name = st.selectbox("Select subject to DELETE", [s.name for s in subjects])
        if st.button("Delete Subject"):
            sub_to_del = session.query(Subject).filter_by(name=del_sub_name).first()
            # Clean up modules first (cascading delete)
            session.query(Module).filter_by(subject_id=sub_to_del.id).delete()
            session.delete(sub_to_del)
            session.commit()
            st.success(f"Deleted {del_sub_name} and its modules.")
            st.rerun()
    session.close()

# --- ADD PROGRESS SECTION ---
elif menu == "Add Progress":
    st.title("✅ Update Study Session")
    session = SessionLocal()
    subjects = session.query(Subject).all()
    
    if not subjects:
        st.warning("No subjects available. Add them in 'Manage Subjects' first.")
    else:
        selected_sub_name = st.selectbox("Select Subject", [s.name for s in subjects])
        subject = session.query(Subject).filter_by(name=selected_sub_name).first()
        modules = session.query(Module).filter_by(subject_id=subject.id).all()
        
        if not modules:
            st.info("This subject has no modules yet.")
        else:
            st.subheader(f"Update Modules for {selected_sub_name}")
            for mod in modules:
                is_checked = st.checkbox(mod.name, value=mod.is_completed, key=mod.id)
                if is_checked != mod.is_completed:
                    mod.is_completed = is_checked
                    session.commit()
                    st.rerun()
    session.close()