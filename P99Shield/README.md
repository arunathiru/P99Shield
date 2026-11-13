# P99Shield: data and reference implementation

Supplementary material for *Reducing Tail Latency in Multi-Tenant Kubernetes through
Interference-Aware Container Scheduling* (Aruna, Thiruvengadam, Padmapriya).

## Contents
| Path | Description |
|---|---|
| `data/p99_latency_by_load.csv` | Default vs P99Shield P99 latency and P95/P99 reductions (Fig. 2, Fig. 5, Table 3) |
| `data/sla_compliance_by_tenancy.csv` | SLA compliance for 1, 2, 4 and 8 concurrent workloads (Fig. 3) |
| `data/cpu_utilization_per_node_high_load.csv` | Per-node CPU utilisation at high load (Fig. 6) |
| `data/p99_estimation_example.csv` | M/M/1 worked example (Table 2) |
| `src/p99shield.py` | Reference implementation of Eq. (4) and Algorithm 1 |
| `src/test_table2.py` | Reproduces the Table 2 numbers |
| `raw/` | Raw logs, manifests and scheduler plugin source (see `raw/README.md`) |

## Testbed (from the paper)
Kubernetes v1.28; 1 master + 4 workers (quad-core, 8-16 GB RAM, SSD, Gigabit Ethernet);
traffic from Apache JMeter and Locust; results averaged over 10 runs per scenario.

## Reproduce
```
cd src && python test_table2.py
```

## Licence
Code: MIT. Data: CC BY 4.0 (see `LICENSE`).
