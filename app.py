import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# Database connection and initialization
def connect_db():
    conn = sqlite3.connect('work_tracking.db')
    c = conn.cursor()
    return conn, c

def init_db():
    conn, c = connect_db()
    c.execute('''DROP TABLE IF EXISTS work_entries''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS work_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            datetime TEXT NOT NULL,
            task TEXT NOT NULL,
            status TEXT NOT NULL,
            employee TEXT NOT NULL
        )
    ''')

    initial_entries = [
        (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'Task 1', 'Open', 'Employee 1'),
        (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'Task 2', 'Close', 'Employee 2'),
        (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'Task 3', 'Ongoing', 'Employee 3')
    ]
    c.executemany('INSERT INTO work_entries (datetime, task, status, employee) VALUES (?, ?, ?, ?)', initial_entries)

    conn.commit()
    conn.close()

# CRUD Operations
def add_entry(task, status, employee):
    conn, c = connect_db()
    current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    c.execute('INSERT INTO work_entries (datetime, task, status, employee) VALUES (?, ?, ?, ?)', (current_datetime, task, status, employee))
    conn.commit()
    conn.close()

def get_all_entries():
    conn, c = connect_db()
    c.execute('SELECT * FROM work_entries')
    entries = c.fetchall()
    conn.close()
    return entries

def update_entry(entry_id, status):
    conn, c = connect_db()
    c.execute('UPDATE work_entries SET status = ? WHERE id = ?', (status, entry_id))
    conn.commit()
    conn.close()

# Streamlit App Layout
st.title('Work Tracker')

menu = ['Add Entry', 'View Entries', 'Update Status', 'Download CSV']
choice = st.sidebar.selectbox('Menu', menu)

# Add Entry
if choice == 'Add Entry':
    st.subheader('Add a new work entry')
    task = st.text_area('Task')
    status = st.selectbox('Status', ['Open', 'Close', 'Ongoing'])
    employee = st.selectbox('Employee Name', ['Pritam Basu', 'Nibedan Bhattacharjee', 'Kousik Dey'])  # Provide actual employee names here
    
    if st.button('Add Entry'):
        add_entry(task, status, employee)
        st.success('Entry added successfully!')

# View Entries
elif choice == 'View Entries':
    st.subheader('All work entries')
    entries = get_all_entries()
    
    if entries:
        df = pd.DataFrame(entries, columns=['ID', 'Datetime', 'Task', 'Status', 'Employee'])
        st.dataframe(df)
        st.download_button(label='Download Excel', data=df.to_csv(index=False), file_name='work_entries.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    else:
        st.write("No entries found.")

# Update Status
elif choice == 'Update Status':
    st.subheader('Update status of a work entry')
    entries = get_all_entries()
    entry_dict = {f"ID: {entry[0]}, Task: {entry[2]}, Employee: {entry[4]}": entry[0] for entry in entries}
    
    selected_entry = st.selectbox('Select Entry', list(entry_dict.keys()))
    new_status = st.selectbox('New Status', ['Open', 'Close', 'Ongoing'])
    
    if st.button('Update Status'):
        update_entry(entry_dict[selected_entry], new_status)
        st.success('Status updated successfully!')

# Download CSV
elif choice == 'Download CSV':
    st.subheader('Download all work entries as CSV')
    entries = get_all_entries()
    if entries:
        df = pd.DataFrame(entries, columns=['ID', 'Datetime', 'Task', 'Status', 'Employee'])
        st.download_button(label='Download CSV', data=df.to_csv(index=False), file_name='work_entries.csv', mime='text/csv')
    else:
        st.write("No entries found.")
