import sys

def match_pattern(input_line, pattern):
    if pattern == "\\d":
        for char in input_line:
            if char.isdigit():
                return True
        return False
    elif len(pattern) == 1:
        return pattern in input_line
    else:
        raise RuntimeError("Unhandled pattern: " + pattern)

def main():
    pattern = sys.argv[2]
    input_line = sys.stdin.read()

    if sys.argv[1] != "-E":
        print("Expected first argument to be '-E'")
        exit(1)

    if match_pattern(input_line, pattern):
        exit(0)
    else:
        exit(1)

if __name__ == "__main__":
    main()
