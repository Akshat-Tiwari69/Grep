#!/usr/bin/env python3
import sys

def match_pattern(input_line, pattern):
    for start in range(len(input_line)):
        if match_at_position(input_line[start:], pattern):
            return True
    return False

def match_at_position(input_line, pattern):
    input_idx = 0
    pattern_idx = 0

    while pattern_idx < len(pattern):
        if input_idx >= len(input_line):
            return False

        if pattern[pattern_idx] == '\\':
            pattern_idx += 1
            if pattern_idx >= len(pattern):
                return False
            if pattern[pattern_idx] == 'd':
                if not input_line[input_idx].isdigit():
                    return False
                input_idx += 1
            elif pattern[pattern_idx] == 'w':
                if not (input_line[input_idx].isalnum() or input_line[input_idx] == '_'):
                    return False
                input_idx += 1
        elif pattern[pattern_idx] == '[':
            end_idx = pattern.find(']', pattern_idx)
            if end_idx == -1:
                raise RuntimeError("Unmatched [")
            char_class = pattern[pattern_idx+1:end_idx]
            if char_class.startswith('^'):
                if input_line[input_idx] in char_class[1:]:
                    return False
            else:
                if input_line[input_idx] not in char_class:
                    return False
            input_idx += 1
            pattern_idx = end_idx
        else:
            if pattern[pattern_idx] != input_line[input_idx]:
                return False
            input_idx += 1
        pattern_idx += 1

    return True

def main():
    if len(sys.argv) != 3 or sys.argv[1] != "-E":
        print("Usage: ./your_program.sh -E <pattern>")
        sys.exit(1)

    pattern = sys.argv[2]
    input_line = sys.stdin.read().strip()

    if match_pattern(input_line, pattern):
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()