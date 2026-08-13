# Active Robot Dynamics Identification

You are given access to a hidden simulated 3-joint robotic arm through `/app/experiment.py`.

Your goal is to identify enough of its dynamics from noisy experiments to accurately predict joint torques on trajectories that are sealed from you.

The robot follows a deterministic rigid-body-inspired model containing inertial, gravity, viscous-friction, and Coulomb-friction effects. The true parameters are hidden.

## Experiment budget

You may perform at most 12 experiments.

The verifier enforces this limit.

Each experiment is a trajectory containing samples of joint position `q`, velocity `qd`, and acceleration `qdd`.

The measurement interface returns noisy torque observations.

You must choose the experiments yourself.

Good excitation should cover different joint combinations, amplitudes, frequencies, and configurations.

Random low-amplitude experiments are intentionally inefficient.

## Public interface

Use:

```python
from experiment import RobotExperiment

env = RobotExperiment()

spec = env.get_spec()
measurement = env.measure(trajectory)
remaining = env.remaining_budget()
env.finalize()
EOF 

### 3. Create the environment Dockerfile

```bash
cat > environment/Dockerfile <<'EOF'
FROM python:3.13-slim-bookworm

WORKDIR /app

COPY robot.py /app/robot.py
COPY experiment.py /app/experiment.py

RUN mkdir -p /app

CMD ["python", "-c", "print('robot environment ready')"]
