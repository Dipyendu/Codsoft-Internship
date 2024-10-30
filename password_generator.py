import random
import string

def get_password_length():
    while True:
        try:
            length = int(input("Enter the desired password length (minimum 4): "))
            if length < 4:
                print("Password length should be at least 4 to include all character types.")
            else:
                return length
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def get_character_sets():
    print("\nSelect character sets to include in your password:")
    print("1. Uppercase Letters (A-Z)")
    print("2. Lowercase Letters (a-z)")
    print("3. Digits (0-9)")
    print("4. Symbols (!@#$%^&*(), etc.)")
    
    selected_sets = []
    
    # Flags to ensure at least one set is selected
    while True:
        try:
            choices = input("Enter choices separated by commas (e.g., 1,3,4): ").split(',')
            choices = [choice.strip() for choice in choices]
            for choice in choices:
                if choice == '1':
                    selected_sets.append(string.ascii_uppercase)
                elif choice == '2':
                    selected_sets.append(string.ascii_lowercase)
                elif choice == '3':
                    selected_sets.append(string.digits)
                elif choice == '4':
                    selected_sets.append(string.punctuation)
                else:
                    print(f"Invalid choice: {choice}. Please select from 1, 2, 3, 4.")
                    selected_sets = []
                    break
            if selected_sets:
                break
        except Exception as e:
            print(f"An error occurred: {e}. Please try again.")
    
    return selected_sets

def generate_password(length, character_sets):
    if not character_sets:
        raise ValueError("No character sets selected.")
    
    # Ensure the password has at least one character from each selected set
    password = [random.choice(char_set) for char_set in character_sets]
    
    # If password is shorter than the number of selected sets, adjust accordingly
    if length < len(password):
        raise ValueError(f"Password length must be at least {len(password)} to include all selected character types.")
    
    # Fill the remaining length with random choices from all selected sets combined
    all_chars = ''.join(character_sets)
    password += random.choices(all_chars, k=length - len(password))
    
    # Shuffle to prevent predictable sequences
    random.shuffle(password)
    
    return ''.join(password)

def main():
    print("=== Password Generator ===")
    length = get_password_length()
    character_sets = get_character_sets()
    
    try:
        password = generate_password(length, character_sets)
        print(f"\nGenerated Password: {password}\n")
    except ValueError as ve:
        print(f"Error: {ve}")
    
    # Optionally, ask if the user wants to generate another password
    while True:
        again = input("Do you want to generate another password? (y/n): ").strip().lower()
        if again == 'y':
            main()
            break
        elif again == 'n':
            print("Thank you for using the Password Generator. Goodbye!")
            break
        else:
            print("Invalid input. Please enter 'y' or 'n'.")

if __name__ == "__main__":
    main()
