import math
from typing import Dict, List, Set
from collections import defaultdict


def parse_file(file_name:str):
    with open(file_name) as fp:
        data = fp.read()

    lines = data.strip().split('\n')
    lines = map(lambda line: line.strip(), lines)

    # n = prendas
    # m = incompatiblidades
    n, m = None, None
    edges, times = defaultdict(set), {}
    for line in lines:
        if line.startswith('c '):
            # skip comment
            continue

        if line.startswith('p'):
            # problem definition
            _, _, n, m = line.split()
        elif line.startswith('e'):
            # incompatibilidad
            _, id1, id2 = line.split()
            edges[id1].add(id2)
            edges[id2].add(id1)
        elif line.startswith('n'):
            # tiempos de lavado
            _, id, duration = line.split()
            times[id] = int(duration)
        else:
            assert False, f'Unexpected line type "{line}"'

    # safety check
    total_edges = sum(len(e) for e in edges.values())
    assert total_edges / 2 == int(m), f'{total_edges / 2=} != {int(m)=}'
    assert len(times) == int(n), f'{len(times)=} != {int(n)=}'

    return edges, times


def solve_greedy(edges: Dict[str, set], times: Dict[str, int]):
    def can_insert(item: str, set: set):
        for incompatible in edges[item]:
            if incompatible in set:
                return False
        return True

    # ordeno las prendas por su duración (de mayor a menor)
    by_weight = sorted(times, key=lambda k: -times[k])

    # mapa en el que la clave es el tiempo del lavado y los valores son listas
    # de lavados con ese tiempo
    # por ejemplo, {3: [{1, 2}]} significa que hay un lavado con las prendas "1" y "2"
    # que tiene una duración calculada de "3"
    sets: Dict[List[set]] = defaultdict(list)
    for item in by_weight:
        t = times[item]

        target_set_key = None

        # intento asignar la prenda en algún lavado existente, empezando por los de mayor duración
        for set_t in sorted(sets, reverse=True):
            set_list = sets[set_t]
            for i, s in enumerate(set_list):
                if can_insert(item, s):
                    target_set_key = (set_t, i)
                    break
            if target_set_key is not None:
                break

        if target_set_key is None:
            # no se pudo encontrar un lavado compatible, se crea uno nuevo
            sets[t].append({item})
        else:
            set_t, set_id = target_set_key

            # agrego la prenda al lavado
            s = sets[set_t][set_id]
            s.add(item)
            if t > set_t:
                # la prenda tiene un tiempo mayor a todas las otras
                # se actualiza el tiempo de lavado
                del sets[set_t][set_id]
                sets[t].append(s)

    # armo la solución final recolectando todos los lavados
    solution = []
    for set_list in sets.values():
        solution += set_list

    return solution


def write_output(solution: List[set], output_file: str):
    with open(output_file, 'wt') as fp:
        for i, items in enumerate(solution, start=1):
            for item in items:
                fp.write(f'{item} {i}\n')



def print_stats(solution: List[Set[str]], times: Dict[str, int]):
    durations = [max(times[c] for c in s) for s in solution]
    for i, s in enumerate(solution):
        print(f' - Lavado {i+1:2d} ({durations[i]:2d}):', ', '.join(s))
    print('total', sum(durations))


if __name__ == '__main__':
    import sys
    assert len(sys.argv) == 3, '  Usage: ./tp1 INPUT_FILE OUTPUT_FILE'

    edges, times = parse_file(file_name=sys.argv[1])
    solution = solve_greedy(edges=edges, times=times)

    print_stats(solution, times)
    write_output(solution=solution, output_file=sys.argv[2])
