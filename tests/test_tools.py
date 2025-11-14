from care_mcp_server.tool_generator import ToolGenerator
from care_mcp_server.schema_parser import SchemaParser
from care_mcp_server.auth import AuthHandler
from care_mcp_server.whitelist import WhitelistManager
from care_mcp_server.enhancements import EnhancementManager


class DummyParser(SchemaParser):
    def __init__(self):  # noqa: D107
        self.schema = {
            "paths": {
                "/foo": {
                    "get": {
                        "operationId": "foo_get",
                        "parameters": [],
                    }
                }
            }
        }

    def get_paths(self):  # noqa: D401
        return self.schema["paths"]

    def extract_parameters(self, operation):  # noqa: D401
        return {}


class DummyWhitelist(WhitelistManager):
    def __init__(self):  # noqa: D107
        self.whitelist = {"foo_get": True}


def test_generate_tools_registers_tools():
    parser = DummyParser()
    auth = AuthHandler(base_url="https://example.com")
    whitelist = DummyWhitelist()
    enhancements = EnhancementManager(enhancements={})

    generator = ToolGenerator(
        schema_parser=parser,
        auth_handler=auth,
        base_url="https://example.com",
        whitelist=whitelist,
        enhancements=enhancements,
    )

    count = generator.generate_tools()
    assert count == 1
