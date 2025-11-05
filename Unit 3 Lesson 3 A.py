PASS_MARK = 50

def pass_fail(score, mark):
    """Return 'Pass' if score >= mark, else 'Fail'."""
    if score >= mark:
        return "Pass"
    else:
        return "Fail"

def s_min(values):
    """Find smallest number in list."""
    if len(values) == 0:
        return 0
    m = values[0]
    for v in values:
        if v < m:
            m = v
    return m

def s_max(values):
    """Find largest number in list."""
    if len(values) == 0:
        return 0
    m = values[0]
    for v in values:
        if v > m:
            m = v
    return m

def s_average(values):
    """Find average, return 0.0 if the list is empty."""
    if len(values) == 0:
        return 0.0
    total = 0
    for v in values:
        total += v
    return total / len(values)

def analyze(scores, mark=PASS_MARK):
    print("Scores Analyzer")

    if len(scores) == 0:
        print("No scores")
        print("Average:", 0.0)
        return

    passes = 0
    fails = 0

    for score in scores:
        result = pass_fail(score, mark)
        print(result + ":", score)
        if result == "Pass":
            passes += 1
        else:
            fails += 1

    print("Min:", s_min(scores))
    print("Max:", s_max(scores))
    print("Average:", s_average(scores))

def main():
    scores = [72, 48, 91, 60, 60, 37]
    analyze(scores)

main()