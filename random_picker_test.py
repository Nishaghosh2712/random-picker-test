import streamlit as st
import pandas as pd
import random
import os

# File to store assignments
ASSIGNMENTS_FILE = "assignments_test.csv"

# Test list of participants
staff_names = ["Nisha", "Mahidhar", "Kishore", "Purshotham", "Brahma"]

# Initialize the assignments file if it doesn't exist
if not os.path.exists(ASSIGNMENTS_FILE):
    assignments_df = pd.DataFrame({
        "Participant": staff_names,
        "AssignedTo": [None] * len(staff_names)
    })
    assignments_df.to_csv(ASSIGNMENTS_FILE, index=False)

# Load the assignments
assignments_df = pd.read_csv(ASSIGNMENTS_FILE)

# Title
st.title("Secret Gift Exchange Test")

# Input for participant's name
participant_name = st.text_input("Enter your name:")

if st.button("Get Your Assignment"):
    if participant_name not in assignments_df["Participant"].values:
        st.error("Your name is not on the list. Please contact the organizer.")
    else:
        # Check if this participant already has an assignment
        current_assignment = assignments_df.loc[assignments_df["Participant"] == participant_name, "AssignedTo"].values[0]
        if pd.notna(current_assignment):
            st.info(f"You have already been assigned: {current_assignment}")
        else:
            # Get available names (those not already assigned)
            available_names = assignments_df.loc[assignments_df["AssignedTo"].isna(), "Participant"].tolist()
            available_names = [name for name in available_names if name != participant_name]

            if not available_names:
                st.error("No more names available to assign!")
            else:
                # Randomly assign a name
                assigned_name = random.choice(available_names)
                assignments_df.loc[assignments_df["Participant"] == participant_name, "AssignedTo"] = assigned_name
                assignments_df.to_csv(ASSIGNMENTS_FILE, index=False)  # Save the updated assignments
                st.success(f"You have been assigned: {assigned_name}")

# For the organizer (optional): View all assignments
if participant_name == "Nisha":
    if st.checkbox("Show all assignments (Organizer Only)"):
        st.write(assignments_df)
