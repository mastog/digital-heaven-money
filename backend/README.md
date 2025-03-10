# API Development Manual

## Table of Contents
1. [User Management](#user-management)
2. [Data Management (CRUD)](#data-management-crud)
3. [Invite Users to Memorial Hall](#invite-users-to-memorial-hall)
4. [AI Request](#ai-request)
5. [Error Handlers](#error-handlers)

## User Management

| Route           | Method | Description                     | Request Body Fields               | Response Body Fields               | Status Code |
|-----------------|--------|---------------------------------|-----------------------------------|------------------------------------|-------------|
| /register       | POST   | Register a new user            | username, password, email, photo_url | message                            | 201         |
| /login          | POST   | User login                     | username, password                | access_token                       | 200         |
| /profile        | GET    | Get current user's profile    | None                              | user object                        | 200         |
| /profile        | PUT    | Update current user's profile | username, email, photo_url        | updated user object                | 200         |

## Data Management (CRUD)

| Route           | Method | Description                     | Request Body Fields               | Response Body Fields               | Status Code |
|-----------------|--------|---------------------------------|-----------------------------------|------------------------------------|-------------|
| /crud/<resource>| POST   | Create a new resource          | Depends on resource type          | created resource object            | 200         |
| /crud/<resource>| PUT    | Update an existing resource    | id, fields to update              | updated resource object            | 200         |
| /crud/<resource>| GET    | Get all resources              | filter fields (optional)          | list of resource objects           | 200         |
| /crud/<resource>| DELETE | Delete a resource              | id                                | success message                    | 200         |

## Invite Users to Memorial Hall

| Route           | Method | Description                     | Request Body Fields               | Response Body Fields               | Status Code |
|-----------------|--------|---------------------------------|-----------------------------------|------------------------------------|-------------|
| /memorial/<id>/invite | POST | Invite users to a memorial hall | None                              | invite_key                         | 201         |

## AI Request

| Route           | Method | Description                     | Request Body Fields               | Response Body Fields               | Status Code |
|-----------------|--------|---------------------------------|-----------------------------------|------------------------------------|-------------|
| /ai             | POST   | Send a request to AI service   | text                              | response                           | 201         |

## Error Handlers

| Route           | Method | Description                     | Request Body Fields               | Response Body Fields               | Status Code |
|-----------------|--------|---------------------------------|-----------------------------------|------------------------------------|-------------|
| /<any>          | GET    | Handle 404 Not Found errors    | None                              | error message                      | 404         |
| /<any>          | GET    | Handle 500 Internal Server errors | None                              | error message                      | 500         |