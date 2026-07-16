from prometheus_client import Counter, Histogram

crawl_requests_total = Counter(
    "freshlense_crawl_requests_total",
    "Total crawl requests"
)

crawl_success_total = Counter(
    "freshlense_crawl_success_total",
    "Successful crawl requests"
)

crawl_failure_total = Counter(
    "freshlense_crawl_failure_total",
    "Failed crawl requests"
)

crawl_duration_seconds = Histogram(
    "freshlense_crawl_duration_seconds",
    "Crawler execution time"
)