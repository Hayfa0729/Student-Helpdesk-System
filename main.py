
import sqlite3


DB_NAME = "helpdesk.db"


def connect_db():
    return sqlite3.connect(DB_NAME)


def initialize_db():
    with connect_db() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS tickets (
                ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_name TEXT NOT NULL,
                category TEXT NOT NULL,
                description TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'Open'
                    CHECK (status IN ('Open', 'In Progress', 'Resolved'))
            )
        """)


def submit_ticket():
    student_name = input("Enter your name: ").strip()
    category = input("Enter category: ").strip()
    description = input("Describe your issue: ").strip()

    if not student_name or not category or not description:
        print("All fields are required.")
        return

    with connect_db() as connection:
        cursor = connection.execute("""
            INSERT INTO tickets (student_name, category, description)
            VALUES (?, ?, ?)
        """, (student_name, category, description))

        ticket_id = cursor.lastrowid

    print(f"Ticket submitted successfully! Ticket ID: {ticket_id}")


def view_tickets():
    with connect_db() as connection:
        tickets = connection.execute("""
            SELECT ticket_id, student_name, category, description, status
            FROM tickets
            ORDER BY ticket_id DESC
        """).fetchall()

    if not tickets:
        print("No tickets found.")
        return

    for ticket in tickets:
        print("-" * 45)
        print(f"Ticket ID: {ticket[0]}")
        print(f"Student: {ticket[1]}")
        print(f"Category: {ticket[2]}")
        print(f"Description: {ticket[3]}")
        print(f"Status: {ticket[4]}")


def search_ticket():
    try:
        ticket_id = int(input("Enter ticket ID: "))
    except ValueError:
        print("Ticket ID must be a number.")
        return

    with connect_db() as connection:
        ticket = connection.execute("""
            SELECT ticket_id, student_name, category, description, status
            FROM tickets
            WHERE ticket_id = ?
        """, (ticket_id,)).fetchone()

    if ticket is None:
        print("Ticket not found.")
        return

    print(f"Ticket ID: {ticket[0]}")
    print(f"Student: {ticket[1]}")
    print(f"Category: {ticket[2]}")
    print(f"Description: {ticket[3]}")
    print(f"Status: {ticket[4]}")


def update_status():
    try:
        ticket_id = int(input("Enter ticket ID: "))
    except ValueError:
        print("Ticket ID must be a number.")
        return

    print("1. Open")
    print("2. In Progress")
    print("3. Resolved")

    choices = {
        "1": "Open",
        "2": "In Progress",
        "3": "Resolved"
    }

    choice = input("Choose new status: ").strip()

    if choice not in choices:
        print("Invalid status choice.")
        return

    with connect_db() as connection:
        cursor = connection.execute("""
            UPDATE tickets
            SET status = ?
            WHERE ticket_id = ?
        """, (choices[choice], ticket_id))

        if cursor.rowcount == 0:
            print("Ticket not found.")
            return

    print("Ticket status updated successfully.")


def main():
    initialize_db()

    while True:
        print("\n===== STUDENT HELPDESK =====")
        print("1. Submit a ticket")
        print("2. View all tickets")
        print("3. Search ticket by ID")
        print("4. Update ticket status")
        print("5. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            submit_ticket()
        elif choice == "2":
            view_tickets()
        elif choice == "3":
            search_ticket()
        elif choice == "4":
            update_status()
        elif choice == "5":
            print("Exiting Student Helpdesk. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
