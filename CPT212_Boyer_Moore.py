ALPHABET_SIZE = 256  # Total number of ASCII characters (0–255)

# Build the Bad Character Table (last occurrence of each character in the pattern)
def build_bad_char_table(pattern):
    bad_char = [-1] * ALPHABET_SIZE  # Initialize all to -1
    for i in range(len(pattern)): # Loop through each character in the pattern
        char = pattern[i]  # Get the current character
        bad_char[ord(char)] = i  # Record the last position of each character in the pattern
    return bad_char
    
# Print Bad Character Table
def print_bad_char_table(bad_char, pattern):
    m = len(pattern)  # Length of the pattern
    unique_chars = sorted(set(pattern))  # Display each unique character in the pattern
    
    print("Bad Character Table:")
    for c in unique_chars:   # Loop through each unique character
        # Calculate shift using max(1, m - last_pos - 1)
        last_pos = bad_char[ord(c)]  # Get the last recorded position
        print(f"'{c}': Last Position at {last_pos}") # Print the position
    print(f"*: Last position at -1")  # For wildcard (any other character not in pattern)
    print("-" * 40)


# Preprocessing for strong good suffix rule
def good_preprocess_strong_suffix(shift, bpos, pat, m):
    i = m  # Start from end of pattern
    j = m + 1  # j points to the next border position
    bpos[i] = j  # Set border position for full length of pattern

    # Loop backward through the pattern
    while i > 0:
        # If mismatch, find next border position
        while j <= m and pat[i - 1] != pat[j - 1]:
            if shift[j] == 0:  # If shift not yet set
                shift[j] = j - i   # Set shift to gap between j and i
            j = bpos[j]  # Jump to next known border position
        i -= 1  # Move i backward
        j -= 1  # Move j backward
        bpos[i] = j  # Save new border position

# Preprocessing for case 2
def good_preprocess_case2(shift, bpos, pat, m):
    j = bpos[0]  # Start from first border position
    for i in range(m + 1):  # Loop over all positions
        if shift[i] == 0:  # If no shift was set
            shift[i] = j  # Use the fallback shift from bpos
        if i == j:  # If i reaches current border
            j = bpos[j]  # Move to next fallback border

def print_good_suffix_shifts(shift, pattern):
    m = len(pattern)
    print("Good Suffix Shifts:")
    for i in range(m + 1):  # Go through shift values
        if i == 0:
            print(f"Entire pattern match: shift {shift[i]}")  # Case when full match happens
        else:
            print(f"After mismatch at {i-1}: shift {shift[i]}")  # Mismatch occurs at position i-1
    print("-" * 40)

def boyer_moore_search(text, pattern):
    n = len(text)
    m = len(pattern)

    # Bad character heuristic preprocessing
    bad_char = build_bad_char_table(pattern)
    print_bad_char_table(bad_char, pattern)

    # Good suffix heuristic preprocessing
    bpos = [0] * (m + 1)  # Initialize border positions
    suffix_shift = [0] * (m + 1)  # Initialize shift values
    good_preprocess_strong_suffix(suffix_shift, bpos, pattern, m)  # Compute strong suffix shifts
    good_preprocess_case2(suffix_shift, bpos, pattern, m)  # Handle remaining suffix cases
    print_good_suffix_shifts(suffix_shift, pattern)

    s = 0  # Initialize shift index (pattern aligned at position s in text)
    found_positions = []  # List to store all match positions

    # Start pattern matching
    while s <= n - m:  # Ensure don’t go out of bounds
        j = m - 1  # Start comparing from end of pattern

       # Compare pattern characters with text from right to left
        while j >= 0 and pattern[j] == text[s + j]:  # While characters match
            j -= 1  # Move left in pattern

        if j < 0:  # Match found (j reached -1)
            print(f"Pattern found at index {s}")
            found_positions.append(s)  # Store position
            s += suffix_shift[0]  # Shift by the entire pattern shift
        else:
            # Calculate bad character shift
            bc_shift = max(1, j - bad_char[ord(text[s + j])])
            
            # Get good suffix shift
            gs_shift = suffix_shift[j + 1]
            
            # Use the larger shift between bad character and good suffix
            shift_amount = max(bc_shift, gs_shift)
            print(f"Mismatch at {s + j} ('{text[s + j]}'), shifting by {shift_amount} (BC: {bc_shift}, GS: {gs_shift})")
            s += shift_amount  # Apply shift

    if not found_positions:
        print("Pattern not found")
    return found_positions

# Main function: handles input and runs the search
def main():
    text = input("Enter the text string: ")
    pattern = input("Enter the pattern string: ")

    print(f"\nText: {text}")
    print(f"Pattern: {pattern}")
    print("=" * 40)

    positions = boyer_moore_search(text, pattern)

    print("=" * 40)
    if positions:
        print(f"Pattern found at positions: {positions}")
    else:
        print("Pattern not found.")

if __name__ == "__main__":
    main()
