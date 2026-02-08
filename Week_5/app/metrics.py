class Metrics:
    def __init__(self):
        self.request_count = 0
        self.error_count = 0
        self.total_latency = 0.0
        self.total_tokens_in = 0
        self.total_tokens_out = 0

    def log_request(self, latency, tokens_in=0, tokens_out=0, error=False):
        self.request_count += 1
        self.total_latency += latency
        self.total_tokens_in += tokens_in
        self.total_tokens_out += tokens_out

        if error:
            self.error_count += 1

    def report(self):
        avg_latency = (
            self.total_latency / self.request_count
            if self.request_count > 0 else 0
        )

        return {
            "requests": self.request_count,
            "errors": self.error_count,
            "avg_latency": round(avg_latency, 4),
            "tokens_in": self.total_tokens_in,
            "tokens_out": self.total_tokens_out,
        }

metrics = Metrics()