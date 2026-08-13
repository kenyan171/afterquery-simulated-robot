import json
import random

from robot import dynamics


class RobotExperiment:

    def __init__(self, seed=271828):
        self._budget = 12
        self._rng = random.Random(seed)

    def get_spec(self):
        return {
            "joints": 3,
            "max_experiments": 12,
            "max_samples_per_experiment": 80,
            "sample_dt": 0.05,
            "noise": {
                "torque_std": 0.035,
                "acceleration_std": 0.01,
            },
            "output": "/app/output.json",
        }

    def remaining_budget(self):
        return self._budget

    def _validate(self, trajectory):
        if not isinstance(trajectory, list):
            raise ValueError("trajectory must be a list")

        if not trajectory:
            raise ValueError("trajectory cannot be empty")

        if len(trajectory) > 80:
            raise ValueError("trajectory exceeds maximum length")

        for sample in trajectory:
            if not isinstance(sample, dict):
                raise ValueError("invalid trajectory sample")

            if len(sample["q"]) != 3:
                raise ValueError("q must contain 3 values")

            if len(sample["qd"]) != 3:
                raise ValueError("qd must contain 3 values")

            if len(sample["qdd"]) != 3:
                raise ValueError("qdd must contain 3 values")

    def measure(self, trajectory):
        self._validate(trajectory)

        if self._budget <= 0:
            raise RuntimeError("experiment budget exhausted")

        self._budget -= 1

        observations = []

        for sample in trajectory:
            q = [float(x) for x in sample["q"]]
            qd = [float(x) for x in sample["qd"]]
            qdd = [float(x) for x in sample["qdd"]]

            clean_tau = dynamics(q, qd, qdd)

            noisy_tau = [
                value + self._rng.gauss(0.0, 0.035)
                for value in clean_tau
            ]

            observations.append({
                "q": q,
                "qd": qd,
                "qdd": qdd,
                "tau": noisy_tau,
            })

        return observations

    def save_model(self, path):
        with open(path, "w") as f:
            json.dump({"saved": True}, f)

    def predict(self, trajectory):
        raise RuntimeError(
            "prediction is evaluated only on sealed trajectories"
        )

    def finalize(self):
        return True
