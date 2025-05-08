# Function to shift a character by a specified amount in the alphabet
def shift_char(c, shift):
    if c.islower():  # Handle lowercase letters
        return chr((ord(c) - ord('a') + shift) % 26 + ord('a'))
    elif c.isupper():  # Handle uppercase letters
        return chr((ord(c) - ord('A') + shift) % 26 + ord('A'))
    else:  # Return non-alphabetic characters unchanged
        return c 

# Function to encrypt text using custom shift rules based on character position
def encrypt_with_shifts(text, n, m):
    encrypted = ""
    shifts = []  # Store shifts for each character (for decryption later)

    for c in text:
        # Determine shift amount based on character case and position in alphabet
        if c.islower():
            if 'a' <= c <= 'm':  # First half of lowercase alphabet
                shift = n * m
            else:  # Second half of lowercase alphabet
                shift = -(n + m)
        elif c.isupper():
            if 'A' <= c <= 'M':  # First half of uppercase alphabet
                shift = -n
            else:  # Second half of uppercase alphabet
                shift = m ** 2
        else:  # Non-alphabetic characters get no shift
            shift = 0
        
        # Apply the shift and record it
        encrypted += shift_char(c, shift)
        shifts.append(shift)
    
    return encrypted, shifts

# Function to decrypt text using the recorded shifts
def decrypt_with_shifts(encrypted_text, shifts):
    decrypted = ""
    # Reverse each shift by applying the opposite shift amount
    for c, shift in zip(encrypted_text, shifts):
        decrypted += shift_char(c, -shift)  
    return decrypted

# Function to verify decrypted text matches original
def check_correctness(original, decrypted):
    return original == decrypted

# Main program execution
def main():
    # Get encryption parameters from user
    n = int(input("Enter value for n: "))
    m = int(input("Enter value for m: "))

    # Read original text from file
    with open("raw_text.txt", "r", encoding="utf-8") as f:
        original_text = f.read()

    # Encrypt the text
    encrypted_text, shifts = encrypt_with_shifts(original_text, n, m)

    # Write encrypted text to file
    with open("encrypted_text.txt", "w", encoding="utf-8") as f:
        f.write(encrypted_text)

    # Decrypt the text using the recorded shifts
    decrypted_text = decrypt_with_shifts(encrypted_text, shifts)

    # Verify and display results
    if check_correctness(original_text, decrypted_text):
        print("\n✅ Decryption successful! Text matches original.")
    else:
        print("\n❌ Decryption failed! Text does NOT match original.")

    # Display all versions of the text for comparison
    print("\n--- Original Text ---")
    print(original_text)
    print("\n--- Encrypted Text ---")
    print(encrypted_text)
    print("\n--- Decrypted Text ---")
    print(decrypted_text)

if __name__ == "__main__":
    main()