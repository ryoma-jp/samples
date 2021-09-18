#! -*- coding: utf-8 -*-

"""
  [q_learning]
    python3 dqn.py --help
"""

#---------------------------------
# モジュールのインポート
#---------------------------------
import os
import sys
import time
import argparse
import gym

import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
from collections import deque

#---------------------------------
# メモ
#---------------------------------
"""
■動的にグラフを更新するサンプル
	https://blog.amedama.jp/entry/2018/07/13/001155
"""

#---------------------------------
# 定数定義
#---------------------------------
OBSERVATION_SIZE = 4
ACTION_SIZE = 2
EPISODE_REWARD_TH = 195
REWARD_PENALTY = -1
MEMORY_SIZE = 1000

BATCH_SIZE = 32
TRAIN_DONE_TH = 10

MODEL_FILE = 'dqn_model.h5'

#---------------------------------
# 関数
#---------------------------------

"""
  関数名: ArgParser
  説明：引数を解析して値を取得する
"""
def ArgParser():
	parser = argparse.ArgumentParser(description='DQN')
	
	# --- 引数を追加 ---
	parser.add_argument('--train_on', dest='train_on', action='store_true', help='学習時指定', required=False)
	parser.add_argument('--model_file', dest='model_file', type=str, default=MODEL_FILE, help='モデルファイル', required=False)
	parser.add_argument('--max_episodes', dest='max_episodes', type=int, default=2000, help='エピソード数', required=False)
	parser.add_argument('--episode_length', dest='episode_length', type=int, default=200, help='エピソードあたりのイタレーション数', required=False)
	parser.add_argument('--output_dir', dest='output_dir', type=str, help='DQNサンプルの出力ディレクトリ', default='output-dqn', required=False)
	
	args = parser.parse_args()
	
	return args
	
#---------------------------------
# クラス
#---------------------------------
class Memory:
	# --- コンストラクタ ---
	def __init__(self, max_size=1000):
		self.buffer = deque(maxlen=max_size)
#		self.buffer = []
	
	# --- リストの最後段にデータを追加 ---
	def append(self, data):
		self.buffer.append(data)
	
	# --- バッファ長を返す ---
	def len(self):
		return len(self.buffer)
	
	# --- 指定サイズのデータを返す ---
	def get_data(self, size):
		idx = np.random.choice(np.arange(self.len()), size=size, replace=False)
		return [self.buffer[i] for i in idx]

class DQN:
	# --- コンストラクタ ---
	def __init__(self, state_size, action_size, learning_rate=0.001, hidden_size=16, fix_seed=True):
		if (fix_seed):
			print('random seed = 1234')
			random.seed(1234)
			np.random.seed(seed=1234)
		
		# --- ネットワーク構造定義 ---
		self.model = Sequential()
		self.model.add(Dense(hidden_size, activation='relu', input_dim=state_size))
		self.model.add(Dense(hidden_size, activation='relu'))
		self.model.add(Dense(action_size, activation='linear'))
		self.optimizer = Adam(lr=learning_rate)
		self.model.compile(loss='mse', optimizer=self.optimizer)
		
		return
		
	# --- 次のアクションを取得(ε-greedy法) ---
	def get_action(self, state, episode):
		if (episode < 0):
			# --- 推論時 ---
			next_action = np.argmax(self.model.predict(state)[0])
		else:
			# --- 学習時 ---
			epsilon = 0.5 * (1 / (episode + 1))
			if epsilon <= np.random.uniform(0, 1):
				next_action = np.argmax(self.model.predict(state)[0])
			else:
				next_action = np.random.choice([0, 1])
		
		return next_action
	
	# --- 重み更新 ---
	def fit(self, memory, batch_size, target_qn, gamma=0.99):
		time_start = time.time()
		x = np.zeros((batch_size, OBSERVATION_SIZE))
		y = np.zeros((batch_size, ACTION_SIZE))
		minibatch = memory.get_data(batch_size)
		
		# --- このfor分に時間がかかる(2秒くらい)ので短縮したい ---
		for i, (_state, _action, _reward, _next_state) in enumerate(minibatch):
			x[i:i+1] = _state
			target = _reward
			
			if not(_next_state == np.zeros(_state.shape)).all(axis=1):
				next_action = np.argmax(self.model.predict(_next_state)[0])
				target = _reward + gamma * target_qn.model.predict(_next_state)[0][next_action]
		
			y[i] = self.model.predict(_state)
			y[i][_action] = target
		
		self.model.fit(x, y, epochs=1, verbose=0)
		
		return
		
#---------------------------------
# メイン処理
#---------------------------------
def main():
	# --- 引数処理 ---
	args = ArgParser()
	max_episodes = args.max_episodes
	episode_length = args.episode_length
	output_dir = args.output_dir
	os.makedirs(output_dir, exist_ok=True)
	
	if (args.train_on):
		# --- Q学習オブジェクト作成 ---
		main_qn = DQN(OBSERVATION_SIZE, ACTION_SIZE)
		target_qn = DQN(OBSERVATION_SIZE, ACTION_SIZE)
		env = gym.make('CartPole-v0')
		
		# --- エピソードデータ蓄積用バッファ(Fixed target Q-Network, Experience replay用) ---
		#   https://www.renom.jp/ja/notebooks/tutorial/reinforcement_learning/DQN-theory/notebook.html
		memory = Memory(max_size=MEMORY_SIZE)
		
		print('[Spec] https://github.com/openai/gym/blob/master/gym/envs/classic_control/cartpole.py')
		print(' * Observation:')
		print('     Type: Box(4)')
		print('     Num     Observation               Min             Max')
		print('     0       Cart Position             -4.8            4.8')
		print('     1       Cart Velocity             -Inf            Inf')
		print('     2       Pole Angle                -24 deg         24 deg')
		print('     3       Pole Velocity At Tip      -Inf            Inf')
		print(' * Actions:')
		print('     Type: Discrete(2)')
		print('     Num  Action')
		print('     0    Push cart to the left')
		print('     1    Push cart to the right')
		print(' * Episode Termination:')
		print('     Pole Angle is more than 12 degrees.')
		print('     Cart Position is more than 2.4 (center of the cart reaches the edge of the display).')
		print('     Episode length is greater than 200.')
		print(' * Solved Requirements:')
		print('     Considered solved when the average reward is greater than or equal to 195.0 over 100 consecutive trials.')
		
		log_header = ['episode', 'iter', 'episode_reward']
		log_data = None
		
		goal_count = 0
		
		for episode in range(max_episodes):
			observation = env.reset()
#			observation_digitized = DigitizeState(observation)
			episode_reward = 0
			
			action = random.choice([0, 1])
			observation, reward, done, info = env.step(action)
			observation = observation.reshape([1, -1])
			
			target_qn.model.set_weights(main_qn.model.get_weights())
			
			for t in range(episode_length):
				time_start = time.time()
				env.render()
				
				action = main_qn.get_action(observation, episode)
				next_observation, reward, done, info = env.step(action)
				next_observation = next_observation.reshape([1, -1])
				
				if (done):
					next_observation = np.zeros(observation.shape)
					if (t < EPISODE_REWARD_TH):
						# 失敗
						reward = REWARD_PENALTY
				else:
					reward = 0
				
				episode_reward += 1
				
				# --- メモリ更新 ---
				memory.append((observation, action, reward, next_observation))
				
				# --- 観測値更新 ---
				observation = next_observation
				
				# --- 重み更新 ---
				if (memory.len() > BATCH_SIZE):
					main_qn.fit(memory, BATCH_SIZE, target_qn)
					target_qn.model.set_weights(main_qn.model.get_weights())
				
				if (done):
					if (log_data is None):
						log_data = np.array([episode, t, episode_reward])
					else:
						log_data = np.vstack((log_data, [episode, t, episode_reward]))
					
					if (episode_reward >= EPISODE_REWARD_TH):
						goal_count += 1
					else:
						goal_count = 0
					
					print('Episode {} Done: t={}, episode_reward={}, goal_count={}'.format(episode, t, episode_reward, goal_count))
					
					break
					
			if (goal_count >= TRAIN_DONE_TH):
				break
			
		env.close()
		
		pd.DataFrame(log_data).to_csv(os.path.join(output_dir, 'dqn_log.csv'), header=log_header, index=False)
		
		fig = plt.figure(0)
		plt.plot(log_data[:, 0], log_data[:, 2])
		plt.savefig(os.path.join(output_dir, 'dqn_log_graph.png'))
		plt.show()
		plt.close(fig)
		
		np.save(os.path.join(output_dir, 'dqn_weights.npy'), main_qn.model.get_weights())
		main_qn.model.save(os.path.join(output_dir, args.model_file))
	else:
		# --- モデル読み込み ---
		main_qn = DQN(OBSERVATION_SIZE, ACTION_SIZE)
		main_qn.model = tf.keras.models.load_model(args.model_file)
		
		# --- CartPole環境構築 ---
		env = gym.make('CartPole-v0')
		env.reset()
		
		action = random.choice([0, 1])
		observation, reward, done, info = env.step(action)
		observation = observation.reshape([1, -1])
		
		for t in range(episode_length):
			env.render()
			
			action = main_qn.get_action(observation, -1)
			observation, reward, done, info = env.step(action)
			observation = observation.reshape([1, -1])
			
			print('#{:03} observation={}, reward={}, done={}'.format(t, observation, reward, done))
			
			if (done):
				break
			
		
if __name__ == '__main__':
	main()
