import json

HIGH_SCORE_PATH = "highscore.json"


def load_high_score():
    try:
        with open(HIGH_SCORE_PATH) as file:
            return int(json.load(file).get("high_score", 0))
    except (FileNotFoundError, ValueError, json.JSONDecodeError, TypeError):
        return 0


def save_high_score(score):
    with open(HIGH_SCORE_PATH, "w") as file:
        json.dump({"high_score": int(score)}, file)


def record_score(score):
    best = load_high_score()
    if score > best:
        save_high_score(score)
        return score
    return best
