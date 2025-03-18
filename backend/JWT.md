# Maintaining User Login State with JWT in the Frontend

To maintain a user's login state even after the browser is closed and reopened, you can store the JWT token in the browser's `localStorage`. `localStorage` provides a persistent storage mechanism that persists data across browser sessions until explicitly cleared by the user.

## 1. Storing the Token After Successful Login

After a successful login, store the JWT token returned by the backend in `localStorage`.

```javascript
// Example login request code
fetch('/login', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        username: 'test',
        password: 'test'
    })
})
.then(response => response.json())
.then(data => {
    if (data.access_token) {
        // Store the token in localStorage
        localStorage.setItem('accessToken', data.access_token);
        console.log('Login successful, token stored');
    }
});
```

## 2. Restoring Login State on Page Load

When the page loads, retrieve the token from `localStorage` and use it to restore the user's login state.

```javascript
// Execute on page load
document.addEventListener('DOMContentLoaded', function() {
    const accessToken = localStorage.getItem('accessToken');
    if (accessToken) {
        // If a token exists, include it in the request header
        fetch('/protected', {
            method: 'GET',
            headers: {
                'Authorization': 'Bearer ' + accessToken
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log('Login state restored successfully', data);
        });
    } else {
        console.log('No token found, user is not logged in');
    }
});
```

## 3. Including the Token in Each Request

For each request to protected routes, retrieve the token from `localStorage` and include it in the request header.

```javascript
function makeProtectedRequest() {
    const accessToken = localStorage.getItem('accessToken');
    if (accessToken) {
        fetch('/protected', {
            method: 'GET',
            headers: {
                'Authorization': 'Bearer ' + accessToken
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log('Protected data', data);
        });
    } else {
        console.log('User not logged in, cannot access protected data');
    }
}
```

## 4. Handling Token Expiration

If the token expires, the backend will return a 401 unauthorized response. The frontend can then prompt the user to log in again or use a refresh token to obtain a new access token.

```javascript
function makeProtectedRequest() {
    const accessToken = localStorage.getItem('accessToken');
    if (accessToken) {
        fetch('/protected', {
            method: 'GET',
            headers: {
                'Authorization': 'Bearer ' + accessToken
            }
        })
        .then(response => {
            if (response.status === 401) {
                // Token expired, handle expiration
                console.log('Token expired, need to log in again or refresh token');
                // Implement token refresh logic here
                return refreshToken();
            }
            return response.json();
        })
        .then(data => {
            if (data) {
                console.log('Protected data', data);
            }
        });
    } else {
        console.log('User not logged in, cannot access protected data');
    }
}

// Example token refresh function
function refreshToken() {
    const refreshToken = localStorage.getItem('refreshToken');
    if (refreshToken) {
        return fetch('/refresh', {
            method: 'POST',
            headers: {
                'Authorization': 'Bearer ' + refreshToken
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.access_token) {
                // Update the access token in localStorage
                localStorage.setItem('accessToken', data.access_token);
                console.log('Token refreshed successfully');
                return data.access_token;
            } else {
                console.log('Token refresh failed, need to log in again');
                return null;
            }
        });
    } else {
        console.log('No refresh token available, need to log in again');
        return null;
    }
}
```

## 5. Logging Out

When the user logs out, remove the tokens from `localStorage`.

```javascript
function logout() {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    console.log('User logged out');
}
```