ALPHABET_SIZE = 256  # Total number of ASCII characters

# Build the Bad Character Table (last occurrence of each character in the pattern)
def build_bad_char_table(pattern):
    bad_char = [-1] * ALPHABET_SIZE  # Initialize all to -1
    for i in range(len(pattern)):
        char = pattern[i]
        bad_char[ord(char)] = i  # Record the last position of each character in the pattern
    return bad_char

def print_bad_char_table(bad_char, pattern):
    m = len(pattern)
    unique_chars = sorted(set(pattern))  # Display each unique character in the pattern
    
    print("Bad Character Table:")
    for c in unique_chars:
        # Calculate shift using max(1, m - last_pos - 1)
        last_pos = bad_char[ord(c)]
        print(f"'{c}': Last Position at {last_pos}")
    print(f"*: Last position at -1")  # For wildcard (any other character not in pattern)
    print("-" * 40)


# Preprocessing for strong good suffix rule
def good_preprocess_strong_suffix(shift, bpos, pat, m):
    i = m
    j = m + 1
    bpos[i] = j

    while i > 0:
        while j <= m and pat[i - 1] != pat[j - 1]:
            if shift[j] == 0:
                shift[j] = j - i
            j = bpos[j]
        i -= 1
        j -= 1
        bpos[i] = j

# Preprocessing for case 2
def good_preprocess_case2(shift, bpos, pat, m):
    j = bpos[0]
    for i in range(m + 1):
        if shift[i] == 0:
            shift[i] = j
        if i == j:
            j = bpos[j]

def print_good_suffix_shifts(shift, pattern):
    m = len(pattern)
    print("Good Suffix Shifts:")
    for i in range(m + 1):
        if i == 0:
            print(f"Entire pattern match: shift {shift[i]}")
        else:
            print(f"After mismatch at {i-1}: shift {shift[i]}")
    print("-" * 40)

def boyer_moore_search(text, pattern):
    n = len(text)
    m = len(pattern)

    # Bad character heuristic preprocessing
    bad_char = build_bad_char_table(pattern)
    print_bad_char_table(bad_char, pattern)

    # Good suffix heuristic preprocessing
    bpos = [0] * (m + 1)
    suffix_shift = [0] * (m + 1)
    good_preprocess_strong_suffix(suffix_shift, bpos, pattern, m)
    good_preprocess_case2(suffix_shift, bpos, pattern, m)
    print_good_suffix_shifts(suffix_shift, pattern)

    s = 0  # Current shift of the pattern with respect to text
    found_positions = []

    while s <= n - m:
        j = m - 1  # Index in pattern

        # Keep reducing index j while characters match
        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1

        if j < 0:  # Pattern found
            print(f"Pattern found at index {s}")
            found_positions.append(s)
            s += suffix_shift[0]  # Shift by the entire pattern shift
        else:
            # Calculate bad character shift
            bc_shift = max(1, j - bad_char[ord(text[s + j])])
            
            # Get good suffix shift
            gs_shift = suffix_shift[j + 1]
            
            # Apply the maximum shift
            shift_amount = max(bc_shift, gs_shift)
            print(f"Mismatch at {s + j} ('{text[s + j]}'), shifting by {shift_amount} (BC: {bc_shift}, GS: {gs_shift})")
            s += shift_amount

    if not found_positions:
        print("Pattern not found")
    return found_positions

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
