from Settings.gamesettings import X, O, EMPTY

# ALPHA BETA PRUNING
MAX_TREE_DEPTH_LEVEL = 2
EXPANSION_RANGE = 2

# EVALUATION SCORE
EMPTY = 0

X_6_PATTERNS = [[EMPTY, X, X, X, X, EMPTY],
                [EMPTY, X, X, X, EMPTY, EMPTY],
                [EMPTY, EMPTY, X, X, X, EMPTY],
                [EMPTY, X, X, EMPTY, X, EMPTY],
                [EMPTY, X, EMPTY, X, X, EMPTY],
                [EMPTY, EMPTY, X, X, EMPTY, EMPTY],
                [EMPTY, EMPTY, X, EMPTY, X, EMPTY],
                [EMPTY, X, EMPTY, X, EMPTY, EMPTY],
                [EMPTY, X, EMPTY, EMPTY, X, EMPTY],
                [EMPTY, EMPTY, X, EMPTY, EMPTY, EMPTY],
                [EMPTY, EMPTY, EMPTY, X, EMPTY, EMPTY]]

X_6_PATTERNS_SCORES = [500_000, 250, 250, 250, 250, 150, 150, 150, 150, 10, 10]

X_5_PATTERNS = [[X, X, X, X, X],
                [X, X, X, X, EMPTY],
                [EMPTY, X, X, X, X],
                [X, X, EMPTY, X, X],
                [X, EMPTY, X, X, X],
                [X, X, X, EMPTY, X],
                [X, EMPTY, X, EMPTY, X],
                [X, X, EMPTY, EMPTY, X],
                [X, EMPTY, EMPTY, X, X],
                [EMPTY, X, X, EMPTY, X],
                [X, EMPTY, X, X, EMPTY],
                [EMPTY, X, X, X, EMPTY],
                [X, X, X, EMPTY, EMPTY],
                [EMPTY, EMPTY, X, X, X]]

X_5_PATTERNS_SCORES = [2_000_000, 50_000, 50_000, 50_000, 50_000, 50_000, 150, 150, 150, 150, 150, 150, 150, 150]

X_END_GAME_PATTERN = [X, X, X, X, X]

O_6_PATTERNS = [[EMPTY, O, O, O, O, EMPTY],
                [EMPTY, O, O, O, EMPTY, EMPTY],
                [EMPTY, EMPTY, O, O, O, EMPTY],
                [EMPTY, O, O, EMPTY, O, EMPTY],
                [EMPTY, O, EMPTY, O, O, EMPTY],
                [EMPTY, EMPTY, O, O, EMPTY, EMPTY],
                [EMPTY, EMPTY, O, EMPTY, O, EMPTY],
                [EMPTY, O, EMPTY, O, EMPTY, EMPTY],
                [EMPTY, O, EMPTY, EMPTY, O, EMPTY],
                [EMPTY, EMPTY, O, EMPTY, EMPTY, EMPTY],
                [EMPTY, EMPTY, EMPTY, O, EMPTY, EMPTY]]

O_6_PATTERNS_SCORES = [500_000, 250, 250, 250, 250, 150, 150, 150, 150, 10, 10]

O_5_PATTERNS = [[O, O, O, O, O],
                [O, O, O, O, EMPTY],
                [EMPTY, O, O, O, O],
                [O, O, EMPTY, O, O],
                [O, EMPTY, O, O, O],
                [O, O, O, EMPTY, O],
                [O, EMPTY, O, EMPTY, O],
                [O, O, EMPTY, EMPTY, O],
                [O, EMPTY, EMPTY, O, O],
                [EMPTY, O, O, EMPTY, O],
                [O, EMPTY, O, O, EMPTY],
                [EMPTY, O, O, O, EMPTY],
                [O, O, O, EMPTY, EMPTY],
                [EMPTY, EMPTY, O, O, O]]

O_5_PATTERNS_SCORES = [2_000_000, 50_000, 50_000, 50_000, 50_000, 50_000, 150, 150, 150, 150, 150, 150, 150, 150]

O_END_GAME_PATTERN = [O, O, O, O, O]