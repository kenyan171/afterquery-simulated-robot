import math

PARAMS = {
    "mass": [2.2, 1.5, 1.1],
    "inertia": [0.55, 0.38, 0.25],
    "gravity": [3.8, 2.4, 1.7],
    "viscous": [0.22, 0.16, 0.12],
    "coulomb": [0.10, 0.075, 0.055],
    "coupling": 0.18,
}


def dynamics(q, qd, qdd):
    result = []

    for i in range(3):
        j = (i + 1) % 3

        tau = (
            PARAMS["inertia"][i] * qdd[i]
            + PARAMS["mass"][i]
            * (0.22 + 0.08 * (i + 1))
            * qdd[i]
            * math.cos(q[i])
            + PARAMS["gravity"][i] * math.sin(q[i])
            + PARAMS["viscous"][i] * qd[i]
            + PARAMS["coulomb"][i]
            * (1.0 if qd[i] >= 0 else -1.0)
        )

        tau += PARAMS["coupling"] * (
            math.sin(q[j]) * qdd[i]
            + 0.35 * qd[i] * qd[j]
        )

        result.append(tau)

    return result


def make_trajectory(phase, amplitude, frequency):
    result = []

    for k in range(80):
        t = k * 0.05

        q = []
        qd = []
        qdd = []

        for joint in range(3):
            w = frequency * (1.0 + 0.17 * joint)
            p = phase + 0.9 * joint

            q.append(
                amplitude * math.sin(w * t + p)
            )

            qd.append(
                amplitude * w * math.cos(w * t + p)
            )

            qdd.append(
                -amplitude
                * w
                * w
                * math.sin(w * t + p)
            )

        result.append({
            "q": q,
            "qd": qd,
            "qdd": qdd,
        })

    return result


SEALED_TRAJECTORIES = [
    (0.23, 0.58, 1.08),
    (1.91, 0.88, 0.91),
    (4.57, 0.72, 1.43),
    (5.11, 0.96, 0.67),
]
