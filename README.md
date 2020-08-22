# SnakeAI

贪吃蛇 AI

## 参数

| parameter | description |
| --- | --- |
| shape | window size of game, `(4,4)` for default |
| human | play game manually or not, `false` for default |
| render | show the game board or not, `false` for default, ignored when field `human` is `true` |
| training | training the agent or not, `false` for default |

## 人工智能

***人工*** 智能

```sh
python main.py --human --shape=(4,4)
```

## 人工智障

需要保证 `main.py` 的运行目录下有 `model.h5` 文件

```
python main.py
```

### 训练

```sh
python main.py --training=true
```

## 目前存在的问题

| observation | reward |
| --- | --- |
| 死亡 | `-1` |
| 连续左转或右转四次 | `-1` |
| 超过一定步数没有吃到苹果 | `-1` |
| 吃到苹果 | `1` |

训练出来的人工智障只会一直向右或向左（蛇初始长度为 2），暂时不知道是为什么 QAQ
