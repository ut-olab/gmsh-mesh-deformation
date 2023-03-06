import numpy as np
import scipy
import trimesh
import polyscope as ps
import os.path
from pathlib import Path


def double_area(geom):
    i = geom.faces[:, 0]  # [num_faces]
    j = geom.faces[:, 1]  # [num_faces]
    k = geom.faces[:, 2]  # [num_faces]
    V = geom.vertices
    x_kj = V[k] - V[j]  # [num_faces, 3]
    x_ik = V[i] - V[k]  # [num_faces, 3]

    # norm of cross products of two edges = twise area of the triangle
    n = np.cross(x_kj, x_ik)
    dbl_a = np.linalg.norm(n, axis=1).reshape(-1, 1)
    return dbl_a


def calc_gradient(geom):
    # geom: trimesh.Trimesh
    num_verts = geom.vertices.shape[0]
    num_faces = geom.faces.shape[0]

    # vertex indices
    i = geom.faces[:, 0]  # [num_faces]
    j = geom.faces[:, 1]  # [num_faces]
    k = geom.faces[:, 2]  # [num_faces]

    V = geom.vertices  # [num_verts, 3]

    x_kj = V[k] - V[j]  # [num_faces, 3]
    x_ik = V[i] - V[k]  # [num_faces, 3]
    x_ji = V[j] - V[i]  # [num_faces, 3]

    # norm of cross products of two edges = twise area of the triangle
    n = np.cross(x_kj, x_ik)
    dbl_a = double_area(geom)

    u = n / dbl_a  # uniformed normal of the triangle
    eperp_ji = np.cross(u, x_ji) / dbl_a
    eperp_ik = np.cross(u, x_ik) / dbl_a

    Fs = np.tile(np.arange(num_faces, dtype=np.int64), (1, 4))
    mi = np.concatenate([num_faces * 0 + Fs,
                         num_faces * 1 + Fs,
                         num_faces * 2 + Fs]).reshape(-1, 1)
    mj = np.tile(np.array([geom.faces[:, 1],
                           geom.faces[:, 0],
                           geom.faces[:, 2],
                           geom.faces[:, 0]]), (3, 1)).reshape(-1, 1)
    mv = np.concatenate([eperp_ik[:, 0], -eperp_ik[:, 0], eperp_ji[:, 0], -eperp_ji[:, 0],
                         eperp_ik[:, 1], -eperp_ik[:, 1], eperp_ji[:, 1], -eperp_ji[:, 1],
                         eperp_ik[:, 2], -eperp_ik[:, 2], eperp_ji[:, 2], -eperp_ji[:, 2]])
    mv = mv.reshape(-1, 1)

    # Gradient
    G = scipy.sparse.csr_matrix((mv.reshape(-1),
                                 (mi.reshape(-1), mj.reshape(-1))),
                                shape=(num_faces * 3, num_verts))
    return G


def calc_alt_mass_mat(geom):
    d = double_area(geom).reshape(-1)
    T = scipy.sparse.diags((np.hstack([d, d, d]) * 0.5))
    return T


def laplace_beltrami(geom):
    G = calc_gradient(geom)
    T = calc_alt_mass_mat(geom)
    print(-G.T * T * G)
    return - G.T * T * G


def massmatrix(geom):
    V = geom.vertices
    F = geom.faces
    nv = V.shape[0]
    nf = F.shape[0]
    d_areas = double_area(geom)

    # follow barycentric
    mi = np.zeros((nf * 3))
    mi[0 * nf: 1 * nf] = F[:, 0].reshape(-1)
    mi[1 * nf: 2 * nf] = F[:, 1].reshape(-1)
    mi[2 * nf: 3 * nf] = F[:, 2].reshape(-1)

    # Note: d_areas are doubled
    mv = (np.concatenate((d_areas, d_areas, d_areas)) / 6).reshape(-1)
    return scipy.sparse.csr_matrix((mv, (mi, mi)), shape=(nv, nv))


def mesh_smoothing(geom):
    laplace = laplace_beltrami(geom)
    mass = massmatrix(geom)
    v0 = geom.vertices
    s = mass - 0.01 * laplace
    return scipy.sparse.linalg.spsolve(s, mass @ v0)


if __name__ == "__main__":
    # ROOT_PATH = Path(".").resolve()
    currentDir = os.getcwd()
    print(currentDir)
    # print(os.path.abspath(os.path.join(currentDir, os.pardir)))
    parDir = os.path.abspath(os.path.join(currentDir, os.pardir))
    print(parDir)
    # print(os.path.abspath(os.path.join(parDir, "assets", "stanford-bunny.off")))
    assetsDir = os.path.abspath(os.path.join(parDir, "assets"))
    print(assetsDir)
    objectFile = os.path.abspath(os.path.join(assetsDir, "stanford-bunny.off"))
    print(objectFile)

    geom = trimesh.load(objectFile, process=False)
    mesh_smoothing(geom)

    # ps.init()
    # ps.register_surface_mesh("origin", geom.vertices, geom.faces)
    # ps.register_surface_mesh("smoothed", mesh_smoothing(geom), geom.faces)
    # ps.show()
