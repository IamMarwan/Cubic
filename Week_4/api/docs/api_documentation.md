# Week 4 – Secured API Documentation

## Overview
This API provides a secured endpoint for submitting user queries.  
Week 4 focuses on transitioning the API from a prototype to a production-ready service by adding authentication, request validation, rate limiting, structured logging, and standardized responses.

## Base URL
http://127.0.0.1:8000

## Authentication
All requests must include an API key to access the endpoint.

### Required Header
X-API-Key: <internal-api-key>

### Authentication Behavior
Requests without an API key are rejected.  
Requests with an invalid API key are rejected.

### Authentication Errors
401 – Missing API key  
403 – Invalid API key

## Rate Limiting
Requests are rate-limited per API key to prevent abuse.  
Limit: 60 requests per minute per API key  
Exceeded limit returns: 429 Too Many Requests

## Endpoint
### POST /query
This endpoint accepts a user query and returns a processed response.

### Request Headers
X-API-Key: <internal-api-key>  
Content-Type: application/json

### Request Body
{
  "query": "string"
}

### Validation Rules
query is required  
query must be a string  
Minimum length: 1 character  
Maximum length: 500 characters  
Invalid requests are rejected automatically with a validation error

## Success Response
Returned when the request is valid, authenticated, and within rate limits.

{
  "status": "success",
  "data": {
    "answer": "Received query: example"
  },
  "error": null
}

## Error Response Format
All custom error responses follow this structure.

{
  "status": "error",
  "data": null,
  "error": {
    "code": "ERROR_CODE",
    "message": "Description of the error"
  }
}

## Common Error Scenarios
400 – Request validation failed  
401 – Missing API key  
403 – Invalid API key  
429 – Rate limit exceeded  
500 – Unexpected server error

## Security Notes
API keys are stored in environment variables.  
Secrets are never hardcoded in the source code.  
Sensitive data such as API keys or full request payloads is never logged.  
.env files are excluded from version control using .gitignore.

## Demo
Interactive API documentation and testing are available via Swagger UI at  
http://127.0.0.1:8000/docs