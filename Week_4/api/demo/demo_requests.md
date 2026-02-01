# Week 4 – API Demo Requests

## Overview
This demo shows the behavior of the secured API when accessed with valid and invalid credentials.  
It demonstrates authentication enforcement, request validation, and rate limiting as required in Week 4.

## Base URL
http://127.0.0.1:8000

## Endpoint
POST /query

Request body used in all examples:
{
  "query": "Hello world"
}

## Case 1 – Authorized Request (Valid API Key)
Description  
A request is sent with a valid API key.

Header  
X-API-Key: cubic-week4-key

Expected Result  
Status Code: 200  
The request is processed successfully and a response is returned.

Response Example  
{
  "status": "success",
  "data": {
    "answer": "Received query: Hello world"
  },
  "error": null
}

## Case 2 – Unauthorized Request (Missing API Key)
Description  
A request is sent without an API key.

Expected Result  
Status Code: 401  
The request is rejected because the API key is missing.

Response Example  
{
  "detail": "Missing API key"
}

## Case 3 – Unauthorized Request (Invalid API Key)
Description  
A request is sent with an incorrect API key.

Header  
X-API-Key: wrong-key

Expected Result  
Status Code: 403  
The request is rejected because the API key is invalid.

Response Example  
{
  "detail": "Invalid API key"
}

## Case 4 – Rate Limiting
Description  
Multiple requests are sent rapidly using the same valid API key.

Expected Result  
After exceeding the allowed number of requests:
Status Code: 429  
The API blocks further requests temporarily.

Response Example  
{
  "detail": "Rate limit exceeded. Try again later."
}

## Demo Summary
This demo confirms that:
- Only authorized users can access the API
- Invalid or missing API keys are rejected
- Rate limiting is enforced per API key
- The API behaves predictably under valid and invalid conditions