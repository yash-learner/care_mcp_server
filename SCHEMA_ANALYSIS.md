# Care API Schema Analysis Summary

## Overview

The Care MCP Server has been successfully updated to work with the **actual Care Healthcare API schema** from https://careapi.ohc.network/api/schema/.

## Schema Details

- **OpenAPI Version**: 3.0.3
- **API Title**: Care API
- **API Version**: 1.0.0
- **Total API Paths**: 325
- **Total Operations**: 539

## Whitelisted Operations

The server now includes **26 whitelisted operations** that all exist in the real Care API schema:

### Facility Operations (7 operations)
- `api_v1_facility_create` - POST /api/v1/facility/
- `api_v1_facility_list` - GET /api/v1/facility/
- `api_v1_facility_retrieve` - GET /api/v1/facility/{external_id}/
- `api_v1_facility_update` - PUT /api/v1/facility/{external_id}/
- `api_v1_facility_partial_update` - PATCH /api/v1/facility/{external_id}/
- `api_v1_facility_users_list` - GET /api/v1/facility/{facility_external_id}/users/
- `api_v1_facility_users_retrieve` - GET /api/v1/facility/{facility_external_id}/users/{external_id}/

### Organization Operations (5 operations)
- `api_v1_organization_create` - POST /api/v1/organization/
- `api_v1_organization_list` - GET /api/v1/organization/
- `api_v1_organization_retrieve` - GET /api/v1/organization/{external_id}/
- `api_v1_organization_update` - PUT /api/v1/organization/{external_id}/
- `api_v1_organization_partial_update` - PATCH /api/v1/organization/{external_id}/

### Location Operations (5 operations)
- `api_v1_facility_location_create` - POST /api/v1/facility/{facility_external_id}/location/
- `api_v1_facility_location_list` - GET /api/v1/facility/{facility_external_id}/location/
- `api_v1_facility_location_retrieve` - GET /api/v1/facility/{facility_external_id}/location/{external_id}/
- `api_v1_facility_location_update` - PUT /api/v1/facility/{facility_external_id}/location/{external_id}/
- `api_v1_facility_location_partial_update` - PATCH /api/v1/facility/{facility_external_id}/location/{external_id}/

### User Operations (3 operations)
- `api_v1_users_list` - GET /api/v1/users/
- `api_v1_users_retrieve` - GET /api/v1/users/{username}/
- `api_v1_users_getcurrentuser_retrieve` - GET /api/v1/users/getcurrentuser/

### Patient Operations (2 operations)
- `api_v1_patient_list` - GET /api/v1/patient/
- `api_v1_patient_retrieve` - GET /api/v1/patient/{external_id}/

### Encounter Operations (2 operations)
- `api_v1_encounter_list` - GET /api/v1/encounter/
- `api_v1_encounter_retrieve` - GET /api/v1/encounter/{external_id}/

### Resource Operations (2 operations)
- `api_v1_resource_list` - GET /api/v1/resource/
- `api_v1_resource_retrieve` - GET /api/v1/resource/{external_id}/

## Key Changes Made

1. **Updated Whitelist** (`src/care_mcp_server/whitelist.py`):
   - Changed from simplified IDs (e.g., `facility_create`) to actual API operation IDs (e.g., `api_v1_facility_create`)
   - Removed non-existent operations (bed management, geography endpoints that don't exist in current API)
   - Added actual operations: patient, encounter, and resource read operations
   - Total: 26 verified operations

2. **Updated Enhancements** (`src/care_mcp_server/enhancements.py`):
   - Updated all enhancement keys to match actual operation IDs
   - Added enhancements for patient, encounter, and resource operations
   - Removed enhancements for non-existent operations (bed, state, district, ward)
   - All enhanced operations exist in the real schema

3. **Updated Tests**:
   - Updated all test assertions to use actual operation IDs
   - Added new test file `test_real_schema.py` with 5 tests to validate against the actual schema
   - All 39 tests pass successfully

4. **Added Schema File**:
   - The real Care API schema (`care_api_swagger_schema.json`) is now part of the repository
   - Size: 58,526 lines
   - Used for validation and testing

5. **Added Analysis Tool**:
   - Created `scripts/analyze_schema.py` to analyze the schema structure
   - Shows top entity types and validates whitelisted operations
   - Confirms all 26 whitelisted operations exist in the schema

## Top Entity Types in Care API

1. **facility** - 241 operations (facility management, devices, appointments, etc.)
2. **patient** - 103 operations (patient records, medications, observations, etc.)
3. **questionnaire** - 23 operations (forms and questionnaires)
4. **valueset** - 19 operations (medical code sets and terminologies)
5. **organization** - 15 operations (healthcare organizations)
6. **supply** - 14 operations (medical supplies and inventory)
7. **encounter** - 13 operations (patient visits and admissions)
8. **users** - 13 operations (user management)
9. **resource** - 11 operations (clinical resources)
10. **files** - 8 operations (file attachments)

## Validation Results

✅ **All Tests Passing**: 39/39 tests pass
✅ **All Whitelisted Operations Valid**: 26/26 operations exist in schema
✅ **All Enhanced Operations Valid**: All enhancements match real operations
✅ **Code Quality**: Black formatted, Ruff linted (0 issues)
✅ **Production Ready**: Ready to deploy with actual Care API

## Notes

- The Care API does **not** have dedicated bed management endpoints in the current schema
- The Care API does **not** have geography endpoints (state, district, ward, localBody) as standalone resources
- Locations are facility-scoped (managed within each facility)
- The API is much richer than originally anticipated with 539 operations across 325 paths
- Focus is on FHIR-compliant resources: Patient, Encounter, Organization, Location, etc.

## Usage

The server can now be run and will automatically fetch and parse the real Care API schema:

```bash
# Set credentials
export CARE_USERNAME=your_username
export CARE_PASSWORD=your_password

# Run the server
care-mcp-server
```

The server will:
1. Authenticate with Care API
2. Fetch the OpenAPI schema from https://careapi.ohc.network/api/schema/
3. Parse 539 operations
4. Filter to 26 whitelisted operations
5. Generate MCP tools with AI-friendly enhancements
6. Start serving on stdio for Claude Desktop integration
