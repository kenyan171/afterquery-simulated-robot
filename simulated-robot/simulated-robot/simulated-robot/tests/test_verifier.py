import json
import math
from pathlib import Path

from ground_truth import dynamics
from ground_truth import make_trajectory
from ground_truth import SEALED_TRAJECTORIES


OUTPUT = Path("/app/output.json")

THRESHOLD = 0.055


def test_prediction_accuracy():

    assert OUTPUT.exists(), "output.json was not created"

    data = json.loads(OUTPUT.read_text())

    assert isinstance(data, dict)
    assert "predictions" in data

    predictions = data["predictions"]

    truth = []

    for design in SEALED_TRAJECTORIES:

        trajectory = make_trajectory(*design)

        for sample in trajectory:

            truth.append(
                dynamics(
                    sample["q"],
                    sample["qd"],
                    sample["qdd"],
                )
            )

    assert len(predictions) == len(truth)

    squared_error = 0.0
    squared_truth = 0.0

    for predicted, actual in zip(predictions, truth):

        assert isinstance(predicted, list)
        assert len(predicted) == 3

        for p, t in zip(predicted, actual):

            p = float(p)

            assert math.isfinite(p)

            squared_error += (p - t) ** 2
            squared_truth += t ** 2

    normalized_rmse = math.sqrt(
        squared_error / squared_truth
    )

    print(
        f"Normalized RMSE: {normalized_rmse:.6f}"
    )

    assert normalized_rmse <= THRESHOLD
