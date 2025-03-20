# API Development Manual (Updated)

## User Management

| Route           | Method | Description                     | Request Body Fields               | Response Body Fields               | Status Code |
|-----------------|--------|---------------------------------|-----------------------------------|------------------------------------|-------------|
| /register       | POST   | Register a new user            | username, password, email, pic_url | message                            | 201         |
| /login          | POST   | User login                     | username, password                | access_token                       | 200         |
| /profile        | GET    | Get current user's profile    | None                              | user object                        | 200         |
| /profile        | PUT    | Update current user's profile | username, email, pic_url        | updated user object                | 200         |

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

## Other Functions

| Route           | Method | Description                     | Request Body Fields               | Response Body Fields               | Status Code |
|-----------------|--------|---------------------------------|-----------------------------------|------------------------------------|-------------|
| /dailyQuestion  | GET    | Get daily question             | None                              | question, answerA, answerB, answerC, answerD, correctAnswer, explanation | 200         |
| /history        | GET    | Get historical events for today | None                              | list of historical events          | 200         |
| /upload_pic     | POST   | Upload a picture               | pic (file)                        | message, pic_name                  | 200         |

## Error Handlers

| Route           | Method | Description                     | Request Body Fields               | Response Body Fields               | Status Code |
|-----------------|--------|---------------------------------|-----------------------------------|------------------------------------|-------------|
| /<any>          | GET    | Handle 404 Not Found errors    | None                              | error message                      | 404         |
| /<any>          | GET    | Handle 500 Internal Server errors | None                              | error message                      | 500         |


## User Management

### Register

- **URL**: `/register`
- **Method**: POST
- **Request Format**:
  ```json
  {
    "username": "string",
    "email": "string",
    "password": "string",
    "pic_url": "string",
    "is_admin": "boolean"
  }
  ```
- **Response Format**:
  ```json
  {
    "message": "Success"
  }
  ```
- **Description**: Registers a new user. The password is hashed before storage.

### Login

- **URL**: `/login`
- **Method**: POST
- **Request Format**:
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```
- **Response Format**:
  ```json
  {
    "access_token": "string"
  }
  ```
- **Description**: Authenticates a user and returns an access token for subsequent requests. [Maintaining User Login State with JWT in the Frontend](docs/JWT.md)

### Profile

- **URL**: `/profile`
- **Method**: GET, PUT
- **Request Format** (PUT):
  ```json
  {
    "email": "string",
    "pic_url": "string",
    "is_admin": "boolean"
  }
  ```
- **Response Format**:
  ```json
  {
    "id": "integer",
    "username": "string",
    "email": "string",
    "pic_url": "string",
    "is_admin": "boolean",
    "created_at": "datetime"
  }
  ```
- **Description**: GET retrieves the current user's profile. PUT updates the profile information.

## Data Management (CRUD)

- **URL**: `/crud/<resource>`
- **Method**: POST, GET, PUT, DELETE
- **Request Format**:
  ```json
  {
    "field1": "value1",
    "field2": "value2",
    "..."
  }
  ```
- **Response Format**:
  ```json
  {
    "id": "integer",
    "field1": "value1",
    "field2": "value2",
    "..."
  }
  ```
- **Description**: Handles CRUD operations for various resources. The `<resource>` parameter specifies the type of data to manage (e.g., "Memorial", "MemorialUser", "InviteKey", etc.). The exact fields depend on the resource type.


## Invite Users to Memorial Hall

- **URL**: `/memorial/<int:id>/invite`
- **Method**: POST
- **Response Format**:
  ```json
  {
    "invite_key": "string"
  }
  ```
- **Description**: Generates an invitation key for inviting users to a specific memorial hall. The key is hashed for security.

## AI Request

- **URL**: `/ai`
- **Method**: POST
- **Request Format**:
  ```json
  {
    "text": "string"
  }
  ```
- **Response Format**:
  ```json
  {
    "response": "string"
  }
  ```
- **Description**: Sends a request to the AI service and returns the response.

### Daily Question

- **URL**: `/dailyQuestion`
- **Method**: GET
- **Response Format**:
  ```json
  {
    "id": "integer",
    "question": "string",
    "answerA": "string",
    "answerB": "string",
    "answerC": "string",
    "answerD": "string",
    "correctAnswer": "string",
    "explanation": "string"
  }
  ```
- **Description**: Returns the daily question based on the current date. The same date will always return the same question.

### Today in hostory

- **URL**: `/history`
- **Method**: GET
- **Response Format**:
  ```json
  [
    {
      "id": "integer",
      "date": "integer",
      "name": "string",
      "year": "integer",
      "description": "string",
      "url": "string"
    }
  ]
  ```
- **Description**: Returns historical events for the current date in MMDD format.

### Upload Picture

- **URL**: `/upload_pic`
- **Method**: POST
- **Request Format**: multipart/form-data with a file field
- **Response Format**:
  ```json
  {
    "message": "Picture uploaded successfully",
    "pic_name": "string"
  }
  ```
- **Description**: Uploads a picture file. Supported file types are determined by the `allowed_file` function. The uploaded file is saved with a timestamp in its name to ensure uniqueness. First upload the image and then assign the returned file name to "pic_url".

## Error Handling

- **404 Not Found**: Returned when a requested resource is not found.
- **500 Internal Server Error**: Indicates an unexpected error occurred on the server.

## Example Usage

### Register a User
```bash
curl -X POST -H "Content-Type: application/json" -d '{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "securepassword",
  "pic_url": "avatar.jpg",
  "is_admin": false
}' http://localhost:5000/register
```

### Login
```bash
curl -X POST -H "Content-Type: application/json" -d '{
  "username": "john_doe",
  "password": "securepassword"
}' http://localhost:5000/login
```

### Get Profile
```bash
curl -H "Authorization: Bearer <access_token>" http://localhost:5000/profile
```

### Update Profile
```bash
curl -X PUT -H "Content-Type: application/json" -H "Authorization: Bearer <access_token>" -d '{
  "email": "new_email@example.com",
  "pic_url": "new_avatar.jpg"
}' http://localhost:5000/profile
```

### Create a Memorial
```bash
curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer <access_token>" -d '{
  "name": "John\'s Memorial",
  "description": "A memorial for John Doe",
  "is_private": true
}' http://localhost:5000/crud/Memorial
```

### Invite Users to Memorial
```bash
curl -X POST -H "Authorization: Bearer <access_token>" http://localhost:5000/memorial/1/invite
```

### AI Interaction
```bash
curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer <access_token>" -d '{
  "text": "What is the meaning of life?"
}' http://localhost:5000/ai
```

### Get Daily Question
```bash
curl http://localhost:5000/dailyQuestion
```

### Get Today in History
```bash
curl http://localhost:5000/history
```

### Upload Picture
```bash
curl -X POST -F "pic=@/path/to/your/file.jpg" http://localhost:5000/upload_pic
```