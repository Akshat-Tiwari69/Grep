import sys
import re

def match_pattern(input_line, pattern):
    if pattern == "\\d":
        return any(char.isdigit() for char in input_line)
    elif pattern == "\\w":
        return any(char.isalnum() or char == "_" for char in input_line)
    elif pattern.startswith("[^") and pattern.endswith("]"):
        characters = pattern[2:-1]
        return any(char not in characters for char in input_line)
    elif pattern.startswith("[") and pattern.endswith("]"):
        characters = pattern[1:-1]
        return any(char in characters for char in input_line)
    else:
        regex_pattern = pattern.replace("\\d", "\\d").replace("\\w", "\\w")
        return bool(re.search(regex_pattern, input_line))

def main():
    pattern = sys.argv[2]
    input_line = sys.stdin.read().strip()

    if sys.argv[1] != "-E":
        print("Expected first argument to be '-E'")
        exit(1)

    if match_pattern(input_line, pattern):
        exit(0)
    else:
        exit(1)

if __name__ == "__main__":
    main()
