def compute_first(productions):
    first = {nonterminal: set() for nonterminal in productions}

    def first_of(symbol):
        if symbol in first:
            return first[symbol]
        else:
            return {symbol}

    changed = True
    while changed:
        changed = False
        for nonterminal, rules in productions.items():
            for rule in rules:
                initial_length = len(first[nonterminal])
                if rule == 'e':
                    first[nonterminal].add('e')
                else:
                    for symbol in rule:
                        first[nonterminal].update(first_of(symbol) - {'e'})
                        if 'e' not in first_of(symbol):
                            break
                    else:
                        first[nonterminal].add('e')
                if initial_length != len(first[nonterminal]):
                    changed = True
    return first


def compute_follow(productions, first):
    follow = {nonterminal: set() for nonterminal in productions}
    follow['S'].add('$') 

    def first_of_string(string):
        result = set()
        for symbol in string:
            if symbol in first:
                result.update(first[symbol] - {'e'})
            else:
                result.add(symbol)
                break
            if 'e' not in first[symbol]:
                break
        else:
            result.add('e')
        return result

    changed = True
    while changed:
        changed = False
        for nonterminal, rules in productions.items():
            for rule in rules:
                trailer = follow[nonterminal]
                for symbol in reversed(rule):
                    if symbol in follow:
                        initial_length = len(follow[symbol])
                        follow[symbol].update(trailer)
                        if 'e' in first[symbol]:
                            trailer.update(first[symbol] - {'e'})
                        else:
                            trailer = first[symbol]
                        if initial_length != len(follow[symbol]):
                            changed = True
                    else:
                        trailer = first_of_string(symbol)  
    return follow


def parse_input(input_lines):
    index = 0
    num_cases = int(input_lines[index])
    index += 1
    cases = []

    for _ in range(num_cases):
        num_nonterminals = int(input_lines[index])
        index += 1
        productions = {}

        for _ in range(num_nonterminals):
            line = input_lines[index].strip()
            index += 1
            parts = line.split()
            nonterminal = parts[0]
            rules = parts[1:]
            productions[nonterminal] = rules

        cases.append(productions)

    return cases


def main():
    input_lines = [
        "3",
        "2",
        "S AS A",
        "A a",
        "3",
        "S AB",
        "A aA a",
        "B bBc bc",
        "2",
        "S A",
        "A A b"
    ]

    cases = parse_input(input_lines)

    for productions in cases:
        first = compute_first(productions)
        follow = compute_follow(productions, first)

        for nonterminal in sorted(productions.keys()):
            print(f"First({nonterminal}) = {{{', '.join(sorted(first[nonterminal]))}}}")

        for nonterminal in sorted(productions.keys()):
            print(f"Follow({nonterminal}) = {{{', '.join(sorted(follow[nonterminal]))}}}")
        print()  
        


if __name__ == "__main__":
    main()
