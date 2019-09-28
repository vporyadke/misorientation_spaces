import re


def parse_quaternion(s):
    q_reg = r"([-+]?\d*\.\d+[\*ijk]*|[-+]?\d+[\*ijk]*)"
    res = re.findall(q_reg, s.replace(' ', ''))
    qs = [0] * 4
    for r in res:
        r = r.replace('*', '')
        if 'i' in r:
            r = r.replace('i', '')
            qs[1] += float(r)
        elif 'j' in r:
            r = r.replace('j', '')
            qs[2] += float(r)
        elif 'k' in r:
            r = r.replace('k', '')
            qs[3] += float(r)
        else:
            qs[0] += float(r)
    return qs


def unparse_quaternion(q):
    return f'{q[0]} + {q[1]} i + {q[2]} j + {q[3]} k'


def parse_group(G_str):
    return [
        parse_quaternion(q)
        for q in G_str.split('\n')
    ]
