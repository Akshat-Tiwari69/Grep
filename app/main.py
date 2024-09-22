#!/usr/bin/env python3
import sys

def match_pattern(input_line, pattern):
    if pattern.startswith('^') and pattern.endswith('$'):
        return match_at_position(input_line, pattern[1:-1], 0, True)
    elif pattern.startswith('^'):
        return match_at_position(input_line, pattern[1:], 0, False)
    elif pattern.endswith('$'):
        return match_at_position(input_line, pattern[:-1], len(input_line) - len(pattern) + 1, True)
    else:
        for start in range(len(input_line)):
            if match_at_position(input_line, pattern, start, False):
                return True
    return False

def match_at_position(input_line, pattern, start, must_end):
    input_idx = start
    pattern_idx = 0

    while pattern_idx < len(pattern):
        if input_idx >= len(input_line):
            # Check if the rest of the pattern is optional
            while pattern_idx < len(pattern) - 1 and pattern[pattern_idx + 1] == '?':
                pattern_idx += 2
            return pattern_idx == len(pattern)

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
        elif pattern[pattern_idx] == '+':
            if pattern_idx == 0:
                return False
            prev_char = pattern[pattern_idx - 1]
            while input_idx < len(input_line) and (prev_char == input_line[input_idx] or
                                                  (prev_char == '\\' and
                                                   (prev_char == 'd' and input_line[input_idx].isdigit() or
                                                    prev_char == 'w' and (input_line[input_idx].isalnum() or input_line[input_idx] == '_')))):
                input_idx += 1
        elif pattern[pattern_idx] == '?':
            # Handle the ? quantifier
            if pattern_idx == 0:
                return False
            # The previous character is optional, so we can skip it
            pattern_idx += 1
            continue
        else:
            if pattern[pattern_idx] != input_line[input_idx]:
                if pattern_idx + 1 < len(pattern) and pattern[pattern_idx + 1] == '?':
                    # Skip this optional character in the pattern
                    pattern_idx += 2
                    continue
                return False
            input_idx += 1
        pattern_idx += 1

    return not must_end or input_idx == len(input_line)

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