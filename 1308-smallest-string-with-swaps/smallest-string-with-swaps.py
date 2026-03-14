class Solution:
    def smallestStringWithSwaps(self, s: str, pairs: List[List[int]]) -> str:    
        root_list = list(range(len(s)))

        for p_1, p_2 in pairs:
            union(p_1, p_2, root_list)

        groups = get_groups(root_list)
        groups = [sorted(list(g)) for g in groups.values()]
        
        s_list = list(s)

        for g in groups:
            g_exp = [s_list[i] for i in g]
            g_exp.sort()
            for i, s_i in enumerate(g):
                s_list[s_i] = g_exp[i]

        return ''.join(s_list)

def find(i, root_list):
    if root_list[i] == i:
        return i

    else:
        root_list[i] = find(root_list[i], root_list)
        return root_list[i]

def union(i, j, root_list):
    root_i = find(i, root_list)
    root_j = find(j, root_list)

    root_list[root_j] = root_i

def get_groups(root_list):
    groups = {}

    for i in range(len(root_list)):
        i_root = find(i, root_list)
        if i_root in groups.keys():
            groups[i_root].append(i)
        else:
            groups[i_root] = [i]

    return groups