"""Local certificate and projected-function checks on deterministic instances."""
import itertools
import json
import benchmark as b

def sat(cnf, assignment):
    return all(any(assignment[abs(lit)] == (lit > 0) for lit in clause) for clause in cnf)

def check():
    assignments = 0
    for seed in range(40):
        f = b.randomcnf(seed, 5, 8)
        for pivot in (1, 2):
            g = b.exact(f, pivot)
            others = [v for v in range(1, 6) if v != pivot]
            for bits in itertools.product((False, True), repeat=4):
                assignment = dict(zip(others, bits))
                assert sat(g, assignment) == any(sat(f, {**assignment, pivot: val}) for val in (False, True))
                assignments += 1
    random_comparisons = 0
    favorable = 0
    incremental = 0
    indexed = 0
    for seed in range(1000):
        f = b.randomcnf(50000 + seed, 9, 20)
        exact = b.lookahead(f, 1, 2)
        one = b.incremental(f, 1, 2)
        two = b.batch(f, 1, 2)
        assert not one or exact
        assert not two or exact
        random_comparisons += 1
        favorable += int(exact)
        incremental += int(one)
        indexed += int(two)
    assert (assignments, random_comparisons, favorable, incremental, indexed) == (1280, 1000, 406, 10, 10)
    return dict(status="PASS", assignment_checks=assignments, directed_random_comparisons=random_comparisons, favorable=favorable, incremental_certificates=incremental, indexed_certificates=indexed)

if __name__ == "__main__":
    print(json.dumps(check(), indent=2))
