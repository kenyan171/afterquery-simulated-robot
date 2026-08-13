import math

N = 3

# Hidden deterministic dynamics parameters.
# These are deliberately NOT exposed through the public API.
PARAMS = {
    "mass": [2.2, 1.5, 1.1],
    "inertia": [0.55, 0.38, 0.25],
    "gravity": [3.8, 2.4, 1.7],
    "viscous": [0.22, 0.16, 0.12],
    "coulomb": [0.10, 0.075, 0.055],
    "coupling": 0.18,
}


def dynamics(q, qd, qdd):
    out = []

    for i in range(N):
        ip = (i + 1) % N

        qi = q[i]
        vi = qd[i]
        ai = qdd[i]

        tau = (
            PARAMS["inertia"][i] * ai
            + PARAMS["mass"][i]
            * (0.22 + 0.08 * (i + 1))
            * ai
            * math.cos(qi)
            + PARAMS["gravity"][i] * math.sin(qi)
            + PARAMS["viscous"][i] * vi
            + PARAMS["coulomb"][i] * (1.0 if vi >= 0 else -1.0)
        )

        tau += PARAMS["coupling"] * (
            math.sin(q[ip]) * ai
            + 0.35 * vi * qd[ip]
        )

        out.append(tau)

    return out
