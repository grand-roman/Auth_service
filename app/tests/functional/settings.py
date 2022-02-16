from dataclasses import dataclass

from pydantic import BaseSettings, Field


@dataclass
class HTTPResponse:
    body: dict
    headers: dict
    status: int


class TestSettings(BaseSettings):
    es_host: str = Field('elasticsearch:9200', env='ELASTIC_HOST')
    redis_host: str = Field('redis', env='REDIS_HOST')
    redis_port: str = Field(6379, env='REDIS_PORT')
    service_url: str = Field('http://auth:9000', env='SERVICE_URL')


test_settings = TestSettings()
redis_host = test_settings.redis_host
redis_port = test_settings.redis_port
service_url = test_settings.service_url
