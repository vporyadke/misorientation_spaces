import numpy as np
from scipy.linalg import svd

from parse_quaternion import unparse_quaternion


def diff_mx(q_a, q_c):
    sa, xa, ya, za = q_a
    sc, xc, yc, zc = q_c
    
    return np.array([
        [sa - sc, xc - xa, yc - ya, zc - za],
        [xa - xc, sa - sc, -za - zc, ya + yc],
        [ya - yc, za + zc, sa - sc, -xa - xc],
        [za - zc, -ya - yc, xa + xc, sa - sc],
    ])


def stereographic_proj(x):
    if np.allclose(x, [1, 0, 0, 0]):
        return [0, 0, 0]
    a, b, c, d = x
    return 4 / ((a - 1)**2 + b**2 + c**2 + d**2) * np.array([b, c, d])

def _make_plot(q1, q2, c=0):
    mx = diff_mx(q1, q2)
    
    rank = np.linalg.matrix_rank(mx)
    if rank == 1 or rank == 3:
        raise Exception('rank = ' + str(rank))
    if rank != 2:
        return None
        
    _, sigma, v = svd(mx)
    v_1 = np.linalg.inv(v)
    res = []

    idxs = np.where(np.isclose(sigma, np.zeros(4)))[0]
    x = np.zeros(4)
    
    for alpha in np.arange(0.01, 2 * np.pi - 0.01, 0.1):
        x[idxs] = np.array([np.cos(alpha), np.sin(alpha)])
        new_x = stereographic_proj(v_1 @ x)

        if np.all(np.abs(new_x) < 10):
            res.append(new_x.tolist())
    res.append(res[0])
    return res


def make_plot(G1, G2):
    res = []
    for i, q_1 in enumerate(G1):
        for j, q_2 in enumerate(G2):
            p = _make_plot(q_1, q_2)
            if p is not None:
                cur_plot = np.array(_make_plot(q_1, q_2, (i * len(G2) + j) / (len(G1) * len(G2))))
                res.append({
                    'xs': cur_plot[:, 0].tolist(),
                    'ys': cur_plot[:, 1].tolist(),
                    'zs': cur_plot[:, 2].tolist(),
                    'name': unparse_quaternion(q_1) + '; ' + unparse_quaternion(q_2)
                })
    return res
