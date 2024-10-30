def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    if y == 0:
        raise ValueError("Cannot divide by zero.")
    return x / y

def get_number(prompt):
    while True:
        try:
            number = float(input(prompt))
            return number
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def get_operation():
    operations = {
        '1': ('Addition', add),
        '2': ('Subtraction', subtract),
        '3': ('Multiplication', multiply),
        '4': ('Division', divide)
    }
    print("\nSelect operation:")
    for key, (name, _) in operations.items():
        print(f"{key}. {name}")
    
    while True:
        choice = input("Enter choice (1/2/3/4): ").strip()
        if choice in operations:
            return operations[choice]
        else:
            print("Invalid choice. Please select a valid operation.")

def calculator():
    print("=== Simple Calculator ===")
    while True:
        num1 = get_number("\nEnter the first number: ")
        num2 = get_number("Enter the second number: ")
        operation_name, operation_func = get_operation()
        
        try:
            result = operation_func(num1, num2)
            print(f"\nResult of {operation_name.lower()} between {num1} and {num2} is: {result}")
        except ValueError as ve:
            print(f"Error: {ve}")
        
        # Ask if the user wants to perform another calculation
        again = input("\nDo you want to perform another calculation? (y/n): ").strip().lower()
        if again != 'y':
            print("Thank you for using the calculator. Goodbye!")
            break

if __name__ == "__main__":
    calculator()
