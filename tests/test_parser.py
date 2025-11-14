import asyncio

from care_mcp_server.schema_parser import SchemaParser


async def _load_schema(parser: SchemaParser) -> bool:
    return await parser.load_schema()


def test_load_schema_failure(monkeypatch):
    class DummyResponse:
        def raise_for_status(self):
            raise ValueError("boom")

    class DummyClient:
        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):  # noqa: ANN001, ANN201
            return False

        async def get(self, *args, **kwargs):  # noqa: ANN001, D401
            return DummyResponse()

    monkeypatch.setattr("httpx.AsyncClient", DummyClient)

    parser = SchemaParser("http://invalid")
    assert asyncio.run(_load_schema(parser)) is False


def test_map_openapi_type_default():
    assert SchemaParser.map_openapi_type("unknown") is str
