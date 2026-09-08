import gymnasium as gym
import numpy as np
import matplotlib.pyplot as plt


eta = 0.2
sigma = 0.05
max_episodes = 5000
max_number_of_steps = 200
n_states = 4
num_batch = 10
num_consecutive_iterations = 100


def calculate(X, w):
    return np.dot(X, w)


def take_action(X, w):
    return 1 if calculate(X, w) > 0.0 else 0


def do_episode(w, env):
    observation, _ = env.reset()
    num_steps = 0
    done = False
    while not done and num_steps <= max_number_of_steps:
        action = take_action(observation, w)
        observation, _, terminated, truncated, _ = env.step(action)
        done = terminated or truncated
        num_steps += 1
    step_val = -1 if num_steps >= max_number_of_steps else num_steps - max_number_of_steps
    return step_val, num_steps


env = gym.make("CartPole-v1")
w = np.random.randn(n_states)
reward_list = np.zeros(num_batch)
last_time_steps = np.zeros(num_consecutive_iterations)
mean_list = []

for episode in range(max_episodes // num_batch):
    N = np.random.normal(scale=sigma, size=(num_batch, w.shape[0]))
    for i in range(num_batch):
        w_try = w + N[i]
        reward, steps = do_episode(w_try, env)
        if i == num_batch - 1:
            print(
                "%d Episode finished after %d steps / mean %.2f"
                % (episode * num_batch, steps, last_time_steps.mean())
            )
        last_time_steps = np.hstack((last_time_steps[1:], [steps]))
        reward_list[i] = reward
    mean_list.append(last_time_steps.mean())
    if last_time_steps.mean() >= 195:
        print("Solved at batch %d" % episode)
        break
    std = np.std(reward_list)
    if std == 0:
        std = 1
    A = (reward_list - np.mean(reward_list)) / std
    w_delta = eta / (num_batch * sigma) * np.dot(N.T, A)
    w += w_delta

env.close()

plt.figure(figsize=(10, 5))
plt.plot(mean_list)
plt.axhline(195, color="r", linestyle="--", label="goal=195")
plt.xlabel("Batch")
plt.ylabel(f"Mean steps (last {num_consecutive_iterations})")
plt.title("CartPole Evolution Strategies")
plt.legend()
plt.tight_layout()
plt.savefig("es_curve.png", dpi=120)
print("saved -> es_curve.png")
