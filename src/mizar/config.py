"""Process configuration read from environment variables only."""

from typing import Literal

from pydantic import Field, SecretStr, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Validated configuration of the api process.

    Every field is required and comes from the environment variable with the
    same name in upper case; there are no defaults.

    Attributes:
        api_host: Interface the HTTP server binds to inside its container.
        api_port: TCP port of the HTTP server.
        postgres_host: Host name of the PostgreSQL server.
        postgres_port: TCP port of the PostgreSQL server.
        postgres_user: Database role used by the api.
        postgres_password: Password of that role; never logged or returned.
        postgres_db: Database name.
        health_timeout_seconds: Upper bound for one database health check.
        log_level: Minimum level of emitted log records.
    """

    model_config = SettingsConfigDict(frozen=True)

    api_host: str = Field(min_length=1)
    api_port: int = Field(ge=1, le=65535)
    postgres_host: str = Field(min_length=1)
    postgres_port: int = Field(ge=1, le=65535)
    postgres_user: str = Field(min_length=1)
    postgres_password: SecretStr = Field(min_length=1)
    postgres_db: str = Field(min_length=1)
    health_timeout_seconds: float = Field(gt=0, le=60)
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"]


class ConfigurationError(Exception):
    """Raised when required environment variables are missing or invalid.

    Attributes:
        variables: Names of the offending variables, sorted; never their values.
    """

    def __init__(self, variables: list[str]) -> None:
        """Store the offending variable names and build the message."""
        self.variables = variables
        super().__init__(
            f"missing or invalid environment variables: {', '.join(variables)}"
        )


def load_settings() -> Settings:
    """Read and validate the configuration from the environment.

    Returns:
        The validated settings.

    Raises:
        ConfigurationError: If any variable is missing or invalid.
    """
    try:
        # Pyright cannot see that BaseSettings fills required fields from the
        # environment, so it reports missing constructor arguments.
        return Settings()  # pyright: ignore[reportCallIssue]
    except ValidationError as err:
        names = sorted(
            {str(error["loc"][0]).upper() for error in err.errors(include_input=False)}
        )
        # The validation error carries the raw input, which can include the
        # password, so it must not travel as the exception's cause.
        raise ConfigurationError(names) from None
