# SnakeAI

贪吃蛇 AI

## 参数

| parameter | description |
| --- | --- |
| shape | window size of game, `(9,9)` for default |
| human | play game manually or not, `false` for default |
| render | show the game board or not `false` for default, ignored when field `human` is `true` |
| training | training the agent or not, `false` for default |

## 人工智能

***人工*** 智能

```sh
python main.py --human --shape=(8,8)
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
