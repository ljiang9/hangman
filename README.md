# hangman

终端猜词游戏（吊死鬼）。猜错 6 次小人就上绞架了。

## 安装

```bash
cd hangman
python3 -m hangman
```

## 玩法

```
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========

  a p p _ _
  已用字母：a e p z
  剩余机会：4
猜一个字母：
```

- 每次猜一个字母，猜中显示位置，猜错画一笔
- 6 次猜错（头、身、两臂、两腿画完）即失败并公布答案
- 重复猜已经猜过的字母**不扣机会**

## 参数

| 参数 | 说明 |
|---|---|
| `--word APPLE` | 固定单词（测试/演示用） |
| `--auto` | 自动演示模式（按字母频率顺序猜） |
| `--seed N` | 随机种子 |

```bash
python3 -m hangman --word apple   # 固定单词
python3 -m hangman --auto --word banana
```

## 设计取舍

- 7 个绞架阶段为手绘 ASCII，不是经典 hangman 图案
- 内置 115 个常见英文单词；英文 only
- `--auto` 是演示流程用，不是"最优策略"

## 已知局限

- 终端交互游戏，无图形界面、无存档、无排行榜
- 单词表是人工精选快照，冷僻词不在其中

## License

MIT，Copyright (c) 2026 ljiang9。
