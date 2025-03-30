/**
 * Example code for creating a registration form using the FormComponent:
 *
* @param {string} apiUrl - The API request URL for the registration form
 * @param {string} method - The HTTP request method for the registration form
 * @param {Array} fields - An array defining form fields, where each field object includes:
 * @param {string} fields[].name - The field name, corresponding to the backend API field name
 * @param {string} fields[].label - The field label displayed in the form
 * @param {string} fields[].type - The field type, such as "text", "email", "password", etc.
 * @param {boolean} fields[].required - Whether the field is required
 * @param {Function} onSuccess - Optional callback function to handle successful form submission data
 * @param {boolean} isFileUpload - Determines whether the form handles file uploads (default: false)
 * @param {boolean} requiresAuth - Indicates whether authentication is required for submission (default: false)
 * @param {string} submitText - The text displayed on the submit button (default: "Submit")
 * @param {Object} classConfig - An object containing class names for styling form elements
 * @param {string} classConfig.form - The CSS class for the form element
 * @param {string} classConfig.label - The CSS class for the label elements
 * @param {string} classConfig.input - The CSS class for the input elements
 * @param {string} classConfig.button - The CSS class for the submit button
 *
 * Example usage:
 * import login from '../../utils/formConfigs/login';
 * <FormComponent
 *   apiUrl="/register"
 *   method="POST"
 *   fields={[
 *     { name: 'username', label: 'Username', type: 'text', required: true },
 *     { name: 'email', label: 'Email', type: 'email', required: true },
 *     { name: 'password', label: 'Password', type: 'password', required: true },
 *     { name: 'confirm_password', label: 'Confirm Password', type: 'password', required: true },
 *   ]}
 *   classConfig: login,
 *   onSuccess={(data) => console.log('Registration successful:', data)}
 *   client:load
 * />
 *
 * Notes:
 * - The fields array defines multiple fields including username, email, password, confirm password, profile picture URL, and admin status
 * - password and confirm_password fields use "password" type to hide user input
 * - confirm_password field is used for front-end password confirmation
 * - pic_url field is optional (required: false)
 * - onSuccess callback is invoked after successful form submission, receiving the API response data as a parameter
 */

import { useRef } from 'react';
import { apiRequest } from '../utils/api';

const FormComponent = ({
  apiUrl,
  method,
  fields,
  isFileUpload = false,
  requiresAuth = false,
  submitText = "Submit",
  classConfig = {}, // classConfig is accepted here as props
  onSuccess
}) => {
  const formRef = useRef(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData(formRef.current);


    const password = formData.get('password');
    const confirmPassword = formData.get('confirm_password');
    if (password && confirmPassword && password !== confirmPassword) {
      alert('Passwords do not match!');
      return;
    }

    try {
      // Ready request data
      const requestData = isFileUpload ? formData : Object.fromEntries(formData);

      // Request functions using the generic API
      const responseData = await apiRequest(
        apiUrl,
        method,
        requestData,
        isFileUpload,
        requiresAuth
      );

      console.log('Registration successful:', responseData);

      if (onSuccess) {
        onSuccess(responseData);
      }

      formRef.current.reset();
    } catch (error) {
      alert(`Error! ${error.message}`);
    }
  };

  return (
    <form ref={formRef} onSubmit={handleSubmit} className={classConfig.form || ""}>
      {fields.map((field) => (
        <div key={field.name} className="mb-4">
          <label htmlFor={field.name} className={classConfig.label || ""}>{field.label}</label>
          {field.type === 'file' ? (
            <input
              type={field.type}
              id={field.name}
              name={field.name}
              required={field.required}
              className={classConfig.input || ""}
            />
          ) : (
            <input
              type={field.type || 'text'}
              id={field.name}
              name={field.name}
              placeholder={field.placeholder}
              required={field.required}
              className={classConfig.input || ""}
            />
          )}
        </div>
      ))}
      <button type="submit" className={classConfig.button || ""}>
        {submitText}
      </button>
    </form>
  );
};

export default FormComponent;