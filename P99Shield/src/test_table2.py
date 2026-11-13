from p99shield import percentile_latency
p95 = percentile_latency(80, 100, 0.95) * 1000
p99 = percentile_latency(80, 100, 0.99) * 1000
print(f"P95={p95:.0f} ms  P99={p99:.0f} ms")   # expected ~150 and ~230 (Table 2)
assert round(p95) == 150 and round(p99) == 230
assert p99 <= 250 and not p99 <= 200
print("Table 2 reproduced.")
