import gymnasium as gym
import numpy as np
import matplotlib.pyplot as plt

env = gym.make("CartPole-v1")
goal_average_steps = 195
max_number_of_steps = 500
num_consecutive_iterations = 100
num_episodes = 5000

last_time_steps = np.zeros(num_consecutive_iterations)
step_list = []
N_BINS = 8
q_table = np.random.uniform(low=-1, high=1, size=(N_BINS ** 4, env.action_space.n))


def bins(clip_min, clip_max, num):
    return np.linspace(clip_min, clip_max, num + 1)[1:-1]


def digitize_state(observation):
    cart_pos, cart_v, pole_angle, pole_v = observation
    digitized = [
        np.digitize(cart_pos, bins=bins(-2.4, 2.4, N_BINS)),
        np.digitize(cart_v, bins=bins(-3.0, 3.0, N_BINS)),
        np.digitize(pole_angle, bins=bins(-0.21, 0.21, N_BINS)),
        np.digitize(pole_v, bins=bins(-2.0, 2.0, N_BINS)),
    ]
    return sum(x * (N_BINS ** i) for i, x in enumerate(digitized))


def select_action(state, epsilon):
    if np.random.random() < epsilon:
        return env.action_space.sample()
    return np.argmax(q_table[state])


def get_action(state, action, observation, reward, epsilon, done):
    next_state = digitize_state(observation)
    alpha = 0.2
    gamma = 0.99
    target = reward if done else reward + gamma * np.max(q_table[next_state])
    q_table[state, action] = (1 - alpha) * q_table[state, action] + alpha * target
    next_action = select_action(next_state, epsilon)
    return next_action, next_state


for episode in range(num_episodes):
    epsilon = max(0.01, 0.5 * (0.99 ** episode))

    observation, info = env.reset()
    state = digitize_state(observation)
    action = select_action(state, epsilon)
    episode_reward = 0

    for t in range(max_number_of_steps):
        observation, reward, terminated, truncated, info = env.step(action)
        done = terminated or truncated
        episode_reward += reward
        if done and t + 1 < max_number_of_steps:
            reward = -200
        action, state = get_action(state, action, observation, reward, epsilon, done)

        if done:
            last_time_steps = np.hstack((last_time_steps[1:], [episode_reward]))
            step_list.append(last_time_steps.mean())
            print(
                "%d Episode finished after %d time steps / mean %.2f"
                % (episode, t + 1, last_time_steps.mean())
            )
            break

    if last_time_steps.mean() >= goal_average_steps and not hasattr(env, "_solved_at"):
        print("Episode %d train agent successfully!" % episode)
        env._solved_at = episode

env.close()

test_env = gym.make("CartPole-v1", max_episode_steps=100000)
observation, info = test_env.reset()
for t in range(100000):
    state = digitize_state(observation)
    action = np.argmax(q_table[state])
    observation, reward, terminated, truncated, info = test_env.step(action)
    if terminated or truncated:
        print(f"[eval] pole fell at step {t + 1}")
        break
else:
    print("[eval] pole survived 100000 steps")
test_env.close()

plt.figure(figsize=(10, 5))
plt.plot(step_list)
plt.axhline(goal_average_steps, color="r", linestyle="--", label=f"goal={goal_average_steps}")
plt.xlabel("Episode")
plt.ylabel(f"Mean reward (last {num_consecutive_iterations})")
plt.title("CartPole Q-learning training progress")
plt.legend()
plt.tight_layout()
plt.savefig("training_curve.png", dpi=120)
print("saved -> training_curve.png")
