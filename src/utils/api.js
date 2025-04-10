// Global state for token refresh management
let isRefreshing = false; // Flag to prevent concurrent refresh attempts
let refreshSubscribers = []; // Queue for requests waiting for token refresh

// Add callback to refresh subscribers queue
const addRefreshSubscriber = (callback) => {
  refreshSubscribers.push(callback);
};

// Execute all queued requests with new token
const onRefreshed = (newToken) => {
  refreshSubscribers.map(callback => callback(newToken));
  refreshSubscribers = []; // Clear the queue
};

/**
 * Enhanced API request function with automatic token refresh
 * @param {string} endpoint - API endpoint
 * @param {string} method - HTTP method
 * @param {object} data - Request payload
 * @param {boolean} requiresAuth - Flag for authenticated requests
 * @returns {Promise} - Promise resolving to API response
 *
 */
export const apiRequest = async (
  endpoint,
  method,
  data,
  requiresAuth = false
) => {
  const url = '/api' + endpoint; //http://127.0.0.1:5000 at local
  const headers = {};

  // Add authorization header if required
  if (requiresAuth) {
    const token = localStorage.getItem('accessToken');
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }
  }

  let body;
  if (method!="GET"){
    body = data;
  }
  try {
    let response = await fetch(url, {
      method,
      headers,
      body
    });

    // Handle token expiration (401 Unauthorized)
    if (response.status === 401 && requiresAuth) {
      if (!isRefreshing) {
        // First encounter of 401 - initiate token refresh
        isRefreshing = true;

        try {
          const newToken = await refreshToken();
          if (newToken) {
            // Update stored token and retry original request
            localStorage.setItem('accessToken', newToken);
            headers['Authorization'] = `Bearer ${newToken}`;
            response = await fetch(url, { method, headers, body, credentials: 'include' });
          } else {
            // Refresh failed - clear tokens and throw error
            localStorage.removeItem('accessToken');
            localStorage.removeItem('refreshToken');
            alert("Login expired, need to log in again")
            return Response.redirect("/login", 302);
          }
        } finally {
          isRefreshing = false;
          onRefreshed(); // Process queued requests
        }
      } else {
        // Token refresh already in progress - queue this request
        return new Promise((resolve) => {
          addRefreshSubscriber((newToken) => {
            headers['Authorization'] = `Bearer ${newToken}`;
            resolve(fetch(url, { method, headers, body, credentials: 'include' }));
          });
        }).then(res => processResponse(res));
      }
    }

    return await processResponse(response);
  } catch (error) {
    console.error('API request failed:', error);
    try {
      alert('API request failed: ' + error)
    }catch(error){

    }
  }
};

/**
 * Process API response and handle errors
 * @param {Response} response - Fetch API response object
 * @returns {Promise} - Promise resolving to parsed response data
 */
const processResponse = async (response) => {
  // Handle 204 No Content responses
  const responseData = response.status === 204 ? null : await response.json();

  if (!response.ok) {
    // Extract error message from response or use default
    throw new Error(responseData?.error || `HTTP error! status: ${response.status}`);
  }

  return responseData;
};

/**
 * Refresh access token using refresh token
 * @returns {Promise<string|null>} - Promise resolving to new access token or null
 */
const refreshToken = async () => {
  const refreshToken = localStorage.getItem('refreshToken');
  if (!refreshToken) {
    console.log('No refresh token available');
    return null;
  }

  try {
    const response = await fetch('http://127.0.0.1:5000/refresh', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${refreshToken}`,
        'Content-Type': 'application/json'
      }
    });

    const data = await response.json();

    if (!response.ok) {
      return null
    }

    return data.access_token;
  } catch (error) {
    console.error('Refresh token failed:', error);
    localStorage.removeItem('refreshToken'); // Clear invalid refresh token
    throw error;
  }
};