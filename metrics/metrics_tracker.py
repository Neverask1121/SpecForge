import time


class MetricsTracker:

    def __init__(self):

        self.total_runs = 0
        self.successes = 0
        self.validation_failures = 0
        self.repairs = 0

        self.latencies = []

    def start_timer(self):
        return time.time()

    def stop_timer(self, start):

        latency = time.time() - start

        self.latencies.append(latency)

    def record_success(self):
        self.total_runs += 1
        self.successes += 1

    def record_validation_failure(self):
        self.validation_failures += 1

    def record_repair(self):
        self.repairs += 1

    def summary(self):

        avg_latency = 0

        if self.latencies:
            avg_latency = (
                sum(self.latencies)
                / len(self.latencies)
            )

        success_rate = 0

        if self.total_runs:
            success_rate = (
                self.successes
                / self.total_runs
            ) * 100

        return {
            "total_runs": self.total_runs,
            "success_rate": success_rate,
            "validation_failures": self.validation_failures,
            "repairs": self.repairs,
            "avg_latency_seconds": round(avg_latency, 2)
        }