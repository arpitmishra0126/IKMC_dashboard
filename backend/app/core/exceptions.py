"""Backend-specific exceptions, translated to HTTP responses in app.main."""


class UnknownValidationCheckError(Exception):
    """Raised when /api/validation/{check} is called with a check name that
    has no corresponding indicator function."""

    def __init__(self, check: str, known_checks: list[str]):
        self.check = check
        self.known_checks = known_checks
        super().__init__(
            f"Unknown validation check '{check}'. Known checks: {known_checks}"
        )


class UpstreamDataError(Exception):
    """Raised when the existing services.loader / services.api_service code
    fails to load data (e.g. upstream API unreachable, bad credentials,
    malformed response). The original exception is preserved as __cause__
    for logging, but its message is not echoed verbatim to the client to
    avoid leaking upstream URLs/headers."""

    def __init__(self, detail: str = "Upstream data source is unavailable."):
        self.detail = detail
        super().__init__(detail)
