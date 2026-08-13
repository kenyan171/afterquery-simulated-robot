import json
import math

from experiment import RobotExperiment


def features(q, qd, qdd):
    rows = []

    for i in range(3):
        j = (i + 1) % 3
        sign = 1.0 if qd[i] >= 0 else -1.0

        rows.append([
            qdd[i],
            qdd[i] * math.cos(q[i]),
            math.sin(q[i]),
            qd[i],
            sign,
            math.sin(q[j]) * qdd[i],
            qd[i] * qd[j],
            1.0,
        ])

    return rows


def ridge_regression(X, y, lam=1e-7):
    n = len(X[0])

    A = [[0.0] * n for _ in range(n)]
    b = [0.0] * n

    for row, target in zip(X, y):
        for i in range(n):
            b[i] += row[i] * target

            for j in range(n):
                A[i][j] += row[i] * row[j]

    for i in range(n):
        A[i][i] += lam

    # Gaussian elimination with pivoting.
    for i in range(n):
        pivot = max(
            range(i, n),
            key=lambda k: abs(A[k][i])
        )

        A[i], A[pivot] = A[pivot], A[i]
        b[i], b[pivot] = b[pivot], b[i]

        if abs(A[i][i]) < 1e-12:
            continue

        divisor = A[i][i]

        for j in range(i, n):
            A[i][j] /= divisor

        b[i] /= divisor

        for k in range(n):
            if k == i:
                continue

            factor = A[k][i]

            for j in range(i, n):
                A[k][j] -= factor * A[i][j]

            b[k] -= factor * b[i]

    return b


def make_trajectory(phase, amplitude, frequency):
    trajectory = []

    for k in range(80):
        t = k * 0.05

        q = []
        qd = []
        qdd = []

        for joint in range(3):
            w = frequency * (1.0 + 0.17 * joint)
            phase_j = phase + 0.9 * joint

            q.append(
                amplitude * math.sin(w * t + phase_j)
            )

            qd.append(
                amplitude * w * math.cos(w * t + phase_j)
            )

            qdd.append(
                -amplitude * w * w
                * math.sin(w * t + phase_j)
            )

        trajectory.append({
            "q": q,
            "qd": qd,
            "qdd": qdd,
        })

    return trajectory


def main():
    env = RobotExperiment()

    X = [[] for _ in range(3)]
    Y = [[] for _ in range(3)]

    # Deliberately varied excitation trajectories.
    experiments = [
        (0.00, 0.45, 0.70),
        (0.70, 0.65, 0.90),
        (1.30, 0.85, 1.10),
        (2.00, 0.55, 1.35),
        (2.70, 0.95, 0.62),
        (3.40, 0.70, 1.55),
        (4.10, 0.90, 0.82),
        (4.80, 0.50, 1.75),
        (5.50, 1.00, 1.00),
        (0.35, 0.80, 1.25),
        (1.75, 0.60, 1.60),
        (3.90, 0.92, 0.74),
    ]

    for design in experiments:
        trajectory = make_trajectory(*design)
        measurements = env.measure(trajectory)

        for sample in measurements:
            f = features(
                sample["q"],
                sample["qd"],
                sample["qdd"],
            )

            for joint in range(3):
                X[joint].append(f[joint])
                Y[joint].append(sample["tau"][joint])

    coefficients = []

    for joint in range(3):
        coefficients.append(
            ridge_regression(
                X[joint],
                Y[joint]
            )
        )

    # These are used only to generate the submitted predictions.
    # The reference does not query them from the experiment interface.
    evaluation_designs = [
        (0.23, 0.58, 1.08),
        (1.91, 0.88, 0.91),
        (4.57, 0.72, 1.43),
        (5.11, 0.96, 0.67),
    ]

    predictions = []

    for design in evaluation_designs:
        trajectory = make_trajectory(*design)

        for sample in trajectory:
            f = features(
                sample["q"],
                sample["qd"],
                sample["qdd"],
            )

            torque = []

            for joint in range(3):
                value = sum(
                    a * b
                    for a, b in zip(
                        coefficients[joint],
                        f[joint],
                    )
                )

                torque.append(value)

            predictions.append(torque)

    with open("/app/output.json", "w") as f:
        json.dump(
            {"predictions": predictions},
            f
        )


if __name__ == "__main__":
    main()
