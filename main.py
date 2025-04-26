# Simple To-Do List App

tasks = []

def show_tasks():
    if not tasks:
        print("No tasks yet.")
    else:
        print("\nYour tasks:")
        for i, task in enumerate(tasks, 1):
            print(f"{i}. {task}")

def add_task():
    task = input("Enter a new task: ")
    tasks.append(task)
    print(f"Task '{task}' added!")

def delete_task():
    show_tasks()
    try:
        num = int(input("Enter the task number to delete: "))
        if 1 <= num <= len(tasks):
            removed = tasks.pop(num - 1)
            print(f"Task '{removed}' deleted!")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Please enter a valid number.")

def main():
    while True:
        print("\n--- To-Do List Menu ---")
        print("1. Show tasks")
        print("2. Add task")
        print("3. Delete task")
        print("4. Exit")

        choice = input("Choose an option (1-4): ")
        if choice == '1':
            show_tasks()
        elif choice == '2':
            add_task()
        elif choice == '3':
            delete_task()
        elif choice == '4':
            print("Goodbye!")
            break
        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    main()
