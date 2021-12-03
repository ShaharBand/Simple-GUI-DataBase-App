from tkinter import *
import sqlite3

# Program window setup:
root = Tk()
root.title('Database App')
root.iconbitmap('database_icon.ico')
root.geometry("400x600")
frame = Frame(root)
frame.pack(pady=10, padx=10)

# Create Text Box Labels:
Label(frame, text="First Name:").grid(row=0, column=0, padx=20)
Label(frame, text="Last Name:").grid(row=1, column=0, padx=20)
Label(frame, text="Address:").grid(row=2, column=0, padx=20)
Label(frame, text="City:").grid(row=3, column=0, padx=20)
Label(frame, text="State:").grid(row=4, column=0, padx=20)
Label(frame, text="Zipcode:").grid(row=5, column=0, padx=20)
Label(frame, text="Select ID:").grid(row=8, column=0, padx=20)

query_label = StringVar()
query_label.set("RECORDS")
Label(frame, textvariable=query_label, justify=LEFT).grid(row=11, column=0, columnspan=2)

# Create Text Boxes:
f_name = Entry(frame, width=30)
f_name.grid(row=0, column=1, padx=20)
l_name = Entry(frame, width=30)
l_name.grid(row=1, column=1, padx=20)
address = Entry(frame, width=30)
address.grid(row=2, column=1, padx=20)
city = Entry(frame, width=30)
city.grid(row=3, column=1, padx=20)
state = Entry(frame, width=30)
state.grid(row=4, column=1, padx=20)
zipcode = Entry(frame, width=30)
zipcode.grid(row=5, column=1, padx=20)
select_box = Entry(frame, width=30)
select_box.grid(row=8, column=1, padx=20)


# Create Function to Submit Record into the Database:
def submit():
    # Create a database or connect to existing one:
    connection = sqlite3.connect('address_book.db')

    # Create cursor:
    c = connection.cursor()

    # Create table:
    c.execute("""CREATE TABLE IF NOT EXISTS addresses (
            first_name text,
            last_name text,
            address text,
            city text,
            state text,
            zipcode integer
            )""")

    # Insert Into Table
    c.execute("INSERT INTO addresses VALUES (:f_name, :l_name, :address, :city, :state, :zipcode)",
              {
                  'f_name': f_name.get(),
                  'l_name': l_name.get(),
                  'address': address.get(),
                  'city': city.get(),
                  'state': state.get(),
                  'zipcode': zipcode.get()
              })

    # Commit changes:
    connection.commit()

    # Close connection:
    connection.close()

    # Clear the text boxes:
    f_name.delete(0, END)
    l_name.delete(0, END)
    address.delete(0, END)
    city.delete(0, END)
    state.delete(0, END)
    zipcode.delete(0, END)


# Create Function to Fetch Records:
def query():
    # Create a database or connect to existing one:
    connection = sqlite3.connect('address_book.db')

    # Create cursor:
    c = connection.cursor()

    # Query the database:
    c.execute("SELECT *, oid FROM addresses")
    records = c.fetchall()

    print_records = ''
    for record in records:
        print_records += str(record[6]) + ") " + str(record[0]) + " " + str(record[1]) \
                         + ", " + str(record[2]) + ", " + str(record[3]) + ", " + str(record[4]) + "\n"

    query_label.set(print_records)

    # Commit changes:
    connection.commit()

    # Close connection:
    connection.close()


# Create Function to edit Records:
def edit():
    # Create a database or connect to existing one:
    connection = sqlite3.connect('address_book.db')

    # Create cursor:
    c = connection.cursor()

    # Query the database:
    global selected_id
    selected_id = select_box.get()
    c.execute("SELECT * FROM addresses WHERE oid = " + selected_id)
    record = c.fetchone()

    # Commit changes:
    connection.commit()

    # Close connection:
    connection.close()

    # Editor Window Setup:
    global editor
    editor = Tk()
    editor.title('Database App: Edit')
    editor.iconbitmap('database_icon.ico')
    editor.geometry("400x190")

    editor_frame = Frame(editor)
    editor_frame.pack(pady=10, padx=10)

    # Create Text Box Labels:
    Label(editor_frame, text="First Name:").grid(row=0, column=0, padx=20)
    Label(editor_frame, text="Last Name:").grid(row=1, column=0, padx=20)
    Label(editor_frame, text="Address:").grid(row=2, column=0, padx=20)
    Label(editor_frame, text="City:").grid(row=3, column=0, padx=20)
    Label(editor_frame, text="State:").grid(row=4, column=0, padx=20)
    Label(editor_frame, text="Zipcode:").grid(row=5, column=0, padx=20)

    # Create Global Variables for text box names:
    global editor_f_name
    global editor_l_name
    global editor_address
    global editor_city
    global editor_state
    global editor_zipcode

    # Create Text Boxes:
    editor_f_name = Entry(editor_frame, width=30)
    editor_f_name.grid(row=0, column=1, padx=20)
    editor_f_name.insert(0, record[0])

    editor_l_name = Entry(editor_frame, width=30)
    editor_l_name.grid(row=1, column=1, padx=20)
    editor_l_name.insert(0, record[1])

    editor_address = Entry(editor_frame, width=30)
    editor_address.grid(row=2, column=1, padx=20)
    editor_address.insert(0, record[2])

    editor_city = Entry(editor_frame, width=30)
    editor_city.grid(row=3, column=1, padx=20)
    editor_city.insert(0, record[3])

    editor_state = Entry(editor_frame, width=30)
    editor_state.grid(row=4, column=1, padx=20)
    editor_state.insert(0, record[4])

    editor_zipcode = Entry(editor_frame, width=30)
    editor_zipcode.grid(row=5, column=1, padx=20)
    editor_zipcode.insert(0, record[5])

    # Create a Update Button:
    update_btn = Button(editor_frame, text="Update Record", command=update) \
        .grid(row=6, column=0, columnspan=2, padx=20, pady=(10, 0), ipadx=136)


# Create Function to Delete A Record:
def delete():
    # Create a database or connect to existing one:
    connection = sqlite3.connect('address_book.db')

    # Create cursor:
    c = connection.cursor()

    c.execute("DELETE from addresses WHERE oid=" + select_box.get())

    # Commit changes:
    connection.commit()

    # Close connection:
    connection.close()


# Create Function to Update A Record:
def update():
    # Create a database or connect to existing one:
    connection = sqlite3.connect('address_book.db')

    # Create cursor:
    c = connection.cursor()

    c.execute("""UPDATE addresses SET
    first_name = :first,
    last_name = :last,
    address = :address,
    city = :city,
    state = :state,
    zipcode = :zipcode
    
    WHERE oid = :oid""",
              {
                  'first': editor_f_name.get(),
                  'last': editor_l_name.get(),
                  'address': editor_address.get(),
                  'city': editor_city.get(),
                  'state': editor_state.get(),
                  'zipcode': editor_zipcode.get(),
                  'oid': selected_id
              })

    # Commit changes:
    connection.commit()

    # Close connection:
    connection.close()

    # Close editor window:
    editor.destroy()


# Create Submit Button:
submit_btn = Button(frame, text="Add Record to Database", command=submit) \
    .grid(row=6, column=0, columnspan=2, padx=20, pady=(10, 0), ipadx=110)

# Create a Query Button:
query_btn = Button(frame, text="Show Records", command=query) \
    .grid(row=7, column=0, columnspan=2, padx=20, pady=10, ipadx=135.8)

# Create a Delete Button:
delete_btn = Button(frame, text="Delete Record", command=delete) \
    .grid(row=9, column=0, columnspan=2, padx=20, pady=(10, 0), ipadx=136)

# Create a Edit Button:
edit_btn = Button(frame, text="Edit Record", command=edit) \
    .grid(row=10, column=0, columnspan=2, padx=20, pady=10, ipadx=143)

root.mainloop()
