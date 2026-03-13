class Solution:
    def smallestStringWithSwaps(self, s: str, pairs: List[List[int]]) -> str:
        graph = build_graph(pairs)
        groups = build_groups(graph, len(s))

        s_list = list(s)

        for g in groups:
            g_exp = [s_list[i] for i in g]
            g_exp.sort()
            for i, s_i in enumerate(g):
                s_list[s_i] = g_exp[i]

        return ''.join(s_list)

def build_graph(pairs):
    incidence = {}

    for p in pairs:
        if p[0] in incidence.keys():
            incidence[p[0]].add(p[1])
        else:
            incidence[p[0]] = {p[1]}

        if p[1] in incidence.keys():
            incidence[p[1]].add(p[0])
        else:
            incidence[p[1]] = {p[0]}

    return incidence

def build_groups(incidence, s_len):
    visited = set()
    groups = []

    for idx in range(s_len):
        if idx not in visited:
            current_group = {idx}
            queue = [idx]
            visited.add(idx)

            while len(queue) > 0:
                edges = incidence.get(queue.pop(0), [])

                for e in edges:
                    if e not in visited:
                        current_group.add(e)
                        visited.add(e)
                        queue.append(e)
                    else:
                        continue

            current_group = list(current_group)
            current_group.sort()

            groups.append(current_group)

    return groups


            


        