/**
 * Enhanced API request function with session validation
 * @param {string} endpoint - API endpoint
 * @param {string} method - HTTP method
 * @param {object} data - Request payload
 * @returns {Promise} - Promise resolving to API response
 */
export const apiRequest = async (
  endpoint,
  method,
  data,
) => {
  const isServer = typeof window === "undefined";

  const baseUrl = isServer
    ? import.meta.env.API_BASE_URL // 服务端使用
    : import.meta.env.PUBLIC_API_BASE_URL; // 客户端使用

  const url = baseUrl + endpoint;

  const headers = {};

  let body = method !== "GET" ? data : undefined;

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
      throw new Error(responseData?.error || `HTTP error! status: ${response.status}`);
    }

    return await processResponse(response);
  } catch (error) {
    console.error('API request failed:', error);
    try {
      alert('API request failed: ' + error);
    } catch (error) {}
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