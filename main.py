import streamlit as st
import pyodbc
import datetime
import  pandas as pd

# Page Configuration
st.set_page_config(
    page_title="CRUD",
    page_icon="📱",
    layout="wide",
)

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}

            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# connect to MS SQL Server database
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=APURBA;'
                      'Database=attendanceDB;'
                      'Trusted_Connection=yes;')
cursor = conn.cursor()
cursor.execute("select * from students")
students = cursor.fetchall();
#st.write(students)

#query = 'select * from personal_details'
df = pd.read_sql('select * from students',conn)
#st.dataframe(df)


# Create Streamlit web interface
def main():
    st.title("MS SQL Server CRUD Operations")

    menu = ["Create", "Read", "Update", "Delete"]
    choice = st.sidebar.selectbox("Select CRUD Operation", menu)

    if choice == "Create":
        create_data()
    elif choice == "Read":
        read_data()
    elif choice == "Update":
        update_data()
    elif choice == "Delete":
        delete_data()

# Function to create data
def create_data():
    st.subheader("Insert New Record")
    name = st.text_input("Enter Name")
    city = st.text_input("Enter City")
    age = st.number_input("Enter Age")
    phone = st.number_input("Enter Phone No.")
    emailId = st.text_input("Enter Email Id ")
    if st.button("Add"):
        cursor = conn.cursor()
        cursor.execute("INSERT INTO students (name, age, city, phoneNo, emailId) VALUES (?, ?, ?, ?, ?)", (name, age, city, phone, emailId))
        conn.commit()
        st.success("Record Added")

# Function to read data
def read_data():
    st.subheader("View Records")
    st.dataframe(df)

# Function to update data
def update_data():
    st.subheader("Edit Record")
    st.dataframe(df)
    cursor = conn.cursor()
    record_id = st.text_input("Enter ID of Record to Edit")
    result = cursor.execute("SELECT * FROM students WHERE studentId = ?", (record_id))
    row = result.fetchone()
    if row:
        name = st.text_input("Name", row[1])
        city = st.text_input("City", row[2])
        age = st.number_input("Age", row[3])
        phone = st.number_input("phoneNo", row[4])
        emailId = st.text_input("emailId", row[5])
        if st.button("Update"):
            cursor.execute("UPDATE students SET name = ?, age = ?, city = ?, phoneNo = ?, emailId = ? WHERE studentId = ?", (name, age, city,phone,emailId, record_id))
            conn.commit()
            st.success("Record Updated")
    else:
        st.warning("Record Not Found")

# Function to delete data
def delete_data():
    st.subheader("Delete Record")
    st.dataframe(df)
    cursor = conn.cursor()
    record_id = st.text_input("Enter ID of Record to Delete")


    result = cursor.execute("SELECT * FROM students WHERE studentId = ?", (record_id))

    row = result.fetchone()
    if row:
        if st.button("Delete"):
            cursor.execute("DELETE FROM students WHERE studentId = ?", (record_id))
            conn.commit()
            st.success("Record Deleted")
    else:
        st.warning("Record Not Found")

if __name__ == '__main__':
    main()
