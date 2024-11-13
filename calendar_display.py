import calendar
import json
from colorama import Fore, Style

holidays = {"01-01", "02-11", "04-29", "05-03", "05-04", "05-05", "11-03", "11-23", "12-23"}
schedule_file = "schedule.json"

def load_schedule():
    try:
        with open(schedule_file, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_schedule():
    with open(schedule_file, "w") as file:
        json.dump(schedule, file, indent=2)

def manage_schedule(action, year=None, month=None, day=None, event=None):
    date_key = f"{year}-{month:02}-{day:02}"
    if action == "add":
        schedule.setdefault(date_key, []).append(event)
        print(f"Added event: {event} on {date_key}")
    elif action == "view":
        print(f"Events on {date_key}:")
        for i, evt in enumerate(schedule.get(date_key, ["No events"])):
            print(f"{i}. {evt}")
    elif action == "delete":
        events = schedule.get(date_key, [])
        if 0 <= event < len(events):
            print(f"Removed event: {events.pop(event)} on {date_key}")
            if not events: del schedule[date_key]

    save_schedule()

def display_month(year, month):
    print(f"\n{calendar.month_name[month]} {year}")
    print("Mon Tue Wed Thu Fri", Fore.BLUE + "Sat" + Style.RESET_ALL, Fore.RED + "Sun" + Style.RESET_ALL)
    for week in calendar.monthcalendar(year, month)[:5]:
        for i, day in enumerate(week):
            date_key = f"{month:02}-{day:02}"
            day_str = (Fore.BLUE if i == 5 else Fore.RED if i == 6 or date_key in holidays else "") + (f"{day:2}" if day else "  ") + Style.RESET_ALL
            print(day_str, end=" ")
        print()

def main_menu():
    while True:
        choice = input("\n1. View Calendar\n2. Add Event\n3. View Event\n4. Delete Event\n5. Exit\nSelect an option: ")
        if choice == "1":
            display_month(int(input("Enter year: ")), int(input("Enter month: ")))
        elif choice in {"2", "3", "4"}:
            y, m, d = int(input("Year: ")), int(input("Month: ")), int(input("Day: "))
            if choice == "2":
                manage_schedule("add", y, m, d, input("Enter event: "))
            elif choice == "3":
                manage_schedule("view", y, m, d)
            elif choice == "4":
                manage_schedule("view", y, m, d)
                manage_schedule("delete", y, m, d, int(input("Enter event index to delete: ")))
        elif choice == "5":
            print("Exiting..."); break
        else:
            print("Invalid choice.")

schedule = load_schedule()
main_menu()

