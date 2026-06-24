import time


class MetricsTracker:

    def __init__(self):

        self.total_runs = 0
        self.successes = 0
        self.validation_failures = 0
        self.repairs = 0
        self.retries = 0

        self.latencies = []
        self.failure_types = {}

    def start_timer(self):
        return time.time()

    def stop_timer(self, start):

        latency = time.time() - start

        self.latencies.append(latency)

    def record_success(self):
        self.successes += 1

    def record_run(self):
        self.total_runs += 1

    def record_validation_failure(self):
        self.validation_failures += 1

    def record_repair(self):
        self.repairs += 1

    def record_retry(self):
        self.retries += 1

    def record_failure_type(self, failure_type):
        self.failure_types[failure_type] = self.failure_types.get(failure_type, 0) + 1

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

        validation_pass_rate = 0
        if self.total_runs:
            validation_pass_rate = (
                (self.total_runs - self.validation_failures)
                / self.total_runs
            ) * 100

        return {
            "total_runs": self.total_runs,
            "success_rate": success_rate,
            "validation_pass_rate": validation_pass_rate,
            "validation_failures": self.validation_failures,
            "repairs": self.repairs,
            "retries": self.retries,
            "avg_latency_seconds": round(avg_latency, 2),
            "failure_types": self.failure_types
        }
