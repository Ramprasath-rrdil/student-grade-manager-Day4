"""Week 1 · Day 4 — Student Grade Manager (Streamlit).

Run with:  streamlit run grade_app.py
"""

import sys

import streamlit as st
from streamlit import runtime

# If started with plain `python grade_app.py` (e.g. VS Code's Run button),
# relaunch through Streamlit so the app opens in the browser.
if __name__ == "__main__" and not runtime.exists():
    from streamlit.web import cli as stcli

    sys.argv = ["streamlit", "run", __file__]
    sys.exit(stcli.main())


# ---------------------------------------------------------------------------
# Grading logic (brought over from Day 2, unchanged)
# ---------------------------------------------------------------------------
def get_grade(mark):
    """Return the letter grade for a mark between 0 and 100."""
    if mark >= 90:
        return "A"
    elif mark >= 80:
        return "B"
    elif mark >= 70:
        return "C"
    elif mark >= 60:
        return "D"
    else:
        return "F"


# ---------------------------------------------------------------------------
# Page setup
# ---------------------------------------------------------------------------
st.set_page_config(page_title="Student Grade Manager", page_icon="🎓")
st.title("🎓 Student Grade Manager")

# Streamlit reruns this whole script on every interaction, so a plain
# `students = []` would be reset to empty each time. session_state survives
# the reruns, so the list is created only once per browser session.
if "students" not in st.session_state:
    st.session_state.students = []


# ---------------------------------------------------------------------------
# Form to add a student
# ---------------------------------------------------------------------------
with st.form("add", clear_on_submit=True):
    col_name, col_mark = st.columns([2, 1])
    with col_name:
        name = st.text_input("Name")
    with col_mark:
        # min_value / max_value reject anything outside 0 to 100 in the UI.
        mark = st.number_input("Mark", min_value=0, max_value=100, step=1, value=0)

    submitted = st.form_submit_button("Add")

    if submitted:
        name = name.strip()
        if not name:
            st.error("Please enter a student name.")
        elif not 0 <= mark <= 100:
            st.error("Mark must be between 0 and 100.")
        else:
            st.session_state.students.append(
                {"Name": name, "Mark": int(mark), "Grade": get_grade(mark)}
            )
            st.success(f"Added {name} ({int(mark)} → {get_grade(mark)})")


# ---------------------------------------------------------------------------
# Results table and class figures
# ---------------------------------------------------------------------------
students = st.session_state.students

if students:
    marks = [s["Mark"] for s in students]
    average = sum(marks) / len(marks)

    col_table, col_stats = st.columns([2, 1])

    with col_table:
        st.subheader("Students")
        st.table(students)

    with col_stats:
        st.subheader("Class figures")
        st.metric("Average", f"{average:.1f}")
        st.metric("Highest", max(marks))
        st.metric("Lowest", min(marks))

    if st.button("Clear all students"):
        st.session_state.students = []
        st.rerun()
else:
    st.info("No students yet. Add one using the form above.")
