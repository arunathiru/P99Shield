"""Reference implementation of Algorithm 1 (P99Shield) and Eq. (4).

Simplified, dependency-free illustration of the published algorithm. It is NOT
the Kubernetes Scheduler Framework plugin used in the experiments.
"""
import math
from dataclasses import dataclass, field

def percentile_latency(lam, mu, p=0.99):
    """M/M/1 sojourn-time percentile: -ln(1-p)/(mu-lam); seconds. Requires lam < mu."""
    if lam >= mu:
        return math.inf
    return -math.log(1.0 - p) / (mu - lam)

@dataclass
class Node:
    name: str
    cpu_max: float
    mem_max: float
    lam: float            # arrival rate incl. incoming workload (post-placement)
    mu: float             # service rate
    cpu_used: float = 0.0
    mem_used: float = 0.0
    workloads: list = field(default_factory=list)   # profile vectors of co-located workloads

@dataclass
class Workload:
    cpu: float
    mem: float
    sla_s: float          # latency bound, seconds
    profile: tuple = (0, 0, 0, 0)   # CPU, memory, I/O, network share

def sim(a, b):
    """Cosine similarity of resource-usage profiles (example choice of sim)."""
    na = math.sqrt(sum(x * x for x in a)); nb = math.sqrt(sum(x * x for x in b))
    return 0.0 if na == 0 or nb == 0 else sum(x * y for x, y in zip(a, b)) / (na * nb)

def interference(w, node):
    """Eq. (5): sum of pairwise similarity to co-located workloads."""
    return sum(sim(w.profile, k) for k in node.workloads)

def schedule(w, nodes, theta, exclude=None):
    """Phases 1-3 (lines 1-10): return best node or None."""
    best, min_p99 = None, math.inf
    for n in nodes:
        if exclude is not None and n is exclude:
            continue
        if n.cpu_used + w.cpu > n.cpu_max or n.mem_used + w.mem > n.mem_max:
            continue                                  # Eq. (2)
        if n.lam >= n.mu:
            continue                                  # saturated
        p99 = percentile_latency(n.lam, n.mu)         # Eq. (4)
        if p99 > w.sla_s:
            continue                                  # Eq. (3)
        if interference(w, n) > theta:
            continue                                  # Eq. (5), Phase 2
        if p99 < min_p99:
            best, min_p99 = n, p99                    # Phase 3
    return best

def monitor_step(observed_p99_s, w, violations, v_max):
    """Phase 4 (lines 13-14): update violation counter; True => attempt migration."""
    violations = violations + 1 if observed_p99_s > w.sla_s else 0
    return violations, violations >= v_max
