"""hangman - 终端猜词游戏（吊死鬼）。

纯标准库。6 次猜错机会，用 ASCII 绞架画出 7 个阶段。
"""
import argparse
import random
import sys

_W = (
    "apple banana orange grape lemon melon peach pear plum kiwi mango cherry",
    "tiger lion bear wolf fox eagle shark whale snake frog horse sheep goat",
    "house table chair door window floor roof wall garden park road bridge",
    "water fire earth wind stone wood metal light dark cloud rain snow",
    "book pen paper music song dance game sport ball team win lose",
    "happy brave clever kind smart quick slow big small long short high low",
    "computer phone mouse key ball clock watch lamp radio clock",
    "river mountain sea lake island tree flower grass leaf root",
    "bread rice meat fish egg milk cheese cake cookie candy",
    "train plane ship car bike bus walk run jump swim fly",
)

WORDS = " ".join(_W).split()

MAX_WRONG = 6

# 7 个阶段的绞架（自己画的）：0=空绞架 … 6=完整小人
STAGES = [
    r"""
  +---+
  |   |
      |
      |
      |
      |
=========""",
    r"""
  +---+
  |   |
  O   |
      |
      |
      |
=========""",
    r"""
  +---+
  |   |
  O   |
  |   |
      |
      |
=========""",
    r"""
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========""",
    r"""
  +---+
  |   |
  O   |
 /|\  |
      |
      |
=========""",
    r"""
  +---+
  |   |
  O   |
 /|\  |
 /    |
      |
=========""",
    r"""
  +---+
  |   |
  O   |
 /|\  |
 / \  |
      |
=========""",
]


def render(word, guessed, wrong):
    shown = " ".join(c if c in guessed else "_" for c in word)
    return STAGES[wrong] + f"\n\n  {shown}\n  已用字母：{' '.join(sorted(guessed)) or '（无）'}\n  剩余机会：{MAX_WRONG - wrong}"


def play(word, guesses):
    """用预设猜测序列玩一局（测试/演示用）。返回 (won, wrong_count, log)。"""
    guessed, wrong, log = set(), 0, []
    for g in guesses:
        g = g.lower()
        if len(g) != 1 or not g.isalpha():
            log.append(f"跳过非法输入：{g!r}")
            continue
        if g in guessed:
            log.append(f"重复猜测 {g!r}，不扣机会")
            continue
        guessed.add(g)
        if g in word:
            log.append(f"猜中 {g!r}")
        else:
            wrong += 1
            log.append(f"猜错 {g!r}（{wrong}/{MAX_WRONG}）")
        if all(c in guessed for c in word):
            return True, wrong, log
        if wrong >= MAX_WRONG:
            return False, wrong, log
    return all(c in guessed for c in word), wrong, log


def interactive(word):
    guessed, wrong = set(), 0
    print("===== 猜词游戏 =====")
    print(f"单词有 {len(word)} 个字母，猜错 {MAX_WRONG} 次就输了。输入 q 退出。")
    while True:
        print(render(word, guessed, wrong))
        try:
            g = input("猜一个字母：").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\n游戏结束。")
            return 1
        if g == "q":
            print(f"答案是：{word}")
            return 1
        if len(g) != 1 or not g.isalpha():
            print("请输入单个字母。")
            continue
        if g in guessed:
            print(f"{g!r} 已经猜过了，不扣机会。")
            continue
        guessed.add(g)
        if g not in word:
            wrong += 1
            print(f"错了！（{wrong}/{MAX_WRONG}）")
        if all(c in guessed for c in word):
            print(render(word, guessed, wrong))
            print(f"\n🎉 猜中了！答案是 {word}，共错 {wrong} 次。")
            return 0
        if wrong >= MAX_WRONG:
            print(render(word, guessed, wrong))
            print(f"\n😅 机会用完了。答案是：{word}")
            return 1


def auto_demo(word):
    """演示模式：按字母表顺序自动猜，验证流程可跑通。"""
    order = "etaoinshrdlcumwfgypbvkjxqz"
    guesses = [c for c in order if c not in set()]
    won, wrong, log = play(word, guesses)
    print(f"演示单词：{word}")
    for line in log[:12]:
        print("  " + line)
    print(f"结果：{'胜' if won else '负'}，错 {wrong} 次")
    return 0 if won else 1


def main(argv=None):
    p = argparse.ArgumentParser(prog="hangman", description="终端猜词游戏（吊死鬼）")
    p.add_argument("--word", help="固定单词（测试用）")
    p.add_argument("--auto", action="store_true", help="自动演示模式")
    p.add_argument("--seed", type=int, help="随机种子")
    p.add_argument("--version", action="version", version="hangman 0.1.0")
    a = p.parse_args(argv)
    if a.seed is not None:
        random.seed(a.seed)
    word = (a.word or random.choice(WORDS)).lower()
    if not word.isalpha():
        print("error: 单词只能包含字母", file=sys.stderr)
        return 2
    if a.auto:
        return auto_demo(word)
    return interactive(word)


if __name__ == "__main__":
    sys.exit(main())
