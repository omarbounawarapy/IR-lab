"""Paired significance testing between two runs' per-topic scores.

The paired t-test is the field's most common choice (Section 0.3: ~65%
of SIGIR/TOIS papers that test significance use it), so it's the one
implemented here. No third-party statistics library is added for this --
the regularized incomplete beta function needed for the t-distribution's
p-value is a small, self-contained, well-known numerical routine.
"""
import math


def _betacf(a: float, b: float, x: float) -> float:
    """Continued-fraction expansion for the incomplete beta function
    (Numerical Recipes' betacf)."""
    MAXIT = 200
    EPS = 3e-14
    FPMIN = 1e-300

    qab = a + b
    qap = a + 1.0
    qam = a - 1.0
    c = 1.0
    d = 1.0 - qab * x / qap
    if abs(d) < FPMIN:
        d = FPMIN
    d = 1.0 / d
    h = d

    for m in range(1, MAXIT + 1):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        if abs(d) < FPMIN:
            d = FPMIN
        c = 1.0 + aa / c
        if abs(c) < FPMIN:
            c = FPMIN
        d = 1.0 / d
        h *= d * c

        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        if abs(d) < FPMIN:
            d = FPMIN
        c = 1.0 + aa / c
        if abs(c) < FPMIN:
            c = FPMIN
        d = 1.0 / d
        delta = d * c
        h *= delta

        if abs(delta - 1.0) < EPS:
            break

    return h


def _regularized_incomplete_beta(a: float, b: float, x: float) -> float:
    if x <= 0.0:
        return 0.0
    if x >= 1.0:
        return 1.0

    ln_beta = math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)
    front = math.exp(ln_beta + a * math.log(x) + b * math.log(1.0 - x))

    if x < (a + 1.0) / (a + b + 2.0):
        return front * _betacf(a, b, x) / a
    return 1.0 - front * _betacf(b, a, 1.0 - x) / b


def two_sided_p_value(t_stat: float, df: int) -> float:
    """Two-tailed p-value of Student's t-distribution with `df` degrees
    of freedom, for a given t statistic."""
    if math.isinf(t_stat):
        return 0.0
    x = df / (df + t_stat * t_stat)
    return _regularized_incomplete_beta(df / 2.0, 0.5, x)


def paired_t_test(scores_a: list, scores_b: list) -> dict:
    """Paired, two-tailed t-test between two runs' per-topic scores
    (e.g. per-query AP). Requires the same topics in the same order."""
    if len(scores_a) != len(scores_b):
        raise ValueError("paired t-test requires equal-length paired samples")
    n = len(scores_a)
    if n < 2:
        raise ValueError("paired t-test requires at least 2 paired topics")

    diffs = [a - b for a, b in zip(scores_a, scores_b)]
    mean_diff = sum(diffs) / n
    variance = sum((d - mean_diff) ** 2 for d in diffs) / (n - 1)
    df = n - 1

    if variance == 0.0:
        t_stat = 0.0 if mean_diff == 0.0 else math.inf
    else:
        std_err = math.sqrt(variance / n)
        t_stat = mean_diff / std_err

    return {
        "n_topics": n,
        "mean_diff": mean_diff,
        "t_statistic": t_stat,
        "degrees_of_freedom": df,
        "p_value": two_sided_p_value(abs(t_stat), df),
    }
