/**
 * Enhanced API request function with separated data and astro context
 * @param {string} endpoint - API endpoint
 * @param {string} method - HTTP method
 * @param {object|null} data - Request body (for POST, PUT, etc)
 * @param {AstroGlobal|null} astro - Astro context for server-side cookie injection
 * @returns {Promise<any>} - API response
 */
export const apiRequest = async (
  endpoint,
  method,
  data = null,
  astro = null
) => {
  const isServer = typeof window === "undefined";

  const baseUrl = isServer
    ? import.meta.env.API_BASE_URL // 服务端使用
    : import.meta.env.PUBLIC_API_BASE_URL; // 客户端使用

  const url = baseUrl + endpoint;

  const headers = {};

  let body;

  if (method !== "GET" && data) {
    if (data instanceof FormData) {
      body = data;
    } else if (typeof data === 'object') {
      body = new URLSearchParams(data).toString();
      headers["Content-Type"] = "application/x-www-form-urlencoded";
    } else {
      body = data;
    }
  }

  if (isServer && astro) {
    const cookie = astro.request.headers.get('cookie');
    if (cookie) {
      headers["Cookie"] = cookie;
    }
  }
  try {
    const response = await fetch(url, {
      method,
      headers: {
        ...headers,
      },
      body,
      credentials: 'include'
    });

    if (!response.ok) {
      const responseData = await response.json();

      if (!isServer) {
        if (response.status === 401) {
          alert('Require login');
          window.location.href = '/login';
        } else if (response.status === 404) {
          alert(responseData?.error || 'Resource not found');
          window.location.href = '/404';
        } else if (response.status === 400) {
          alert(responseData?.error || 'Something wrong happened');
        }
      }
      throw new Error(responseData?.error || `HTTP error! status: ${response.status}`);
    }

    return await processResponse(response);
  } catch (error) {
    console.error('API request failed:', error);
    if(!isServer){
      throw(error)
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
  return responseData;
};