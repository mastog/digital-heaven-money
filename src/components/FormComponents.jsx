/**
 * Example code for creating a registration form using the FormComponent:
 *
 * @param {string} apiUrl - Set the API request URL for a registration form
 * @param {string} method - Set the HTTP request method for a registration form
 * @param {Array} fields - Array defining form fields, each field object includes:
 * @param {string} fields[].name - Field name, matching the backend API field name
 * @param {string} fields[].label - Field label displayed in the form
 * @param {string} fields[].type - Field type, such as "text", "email", "password", etc.
 * @param {boolean} fields[].required - Whether the field is required
 * @param {Function} onSuccess - Optional callback to handle successful form submission data
 *
 * Example usage:
 * <FormComponent
 *   apiUrl="/register"
 *   method="POST"
 *   fields={[
 *     { name: 'username', label: 'Username', type: 'text', required: true },
 *     { name: 'email', label: 'Email', type: 'email', required: true },
 *     { name: 'password', label: 'Password', type: 'password', required: true },
 *     { name: 'confirm_password', label: 'Confirm Password', type: 'password', required: true },
 *   ]}
 *   onSuccess={(data) => console.log('Registration successful:', data)}
 * />
 *
 * Notes:
 * - The fields array defines multiple fields including username, email, password, confirm password, profile picture URL, and admin status
 * - password and confirm_password fields use "password" type to hide user input
 * - confirm_password field is used for front-end password confirmation
 * - pic_url field is optional (required: false)
 * - is_admin field uses "checkbox" type for boolean input
 * - onSuccess callback is invoked after successful form submission, receiving the API response data as a parameter
 */

import { useRef } from 'react';

const FormComponent = ({
  apiUrl,
  method,
  fields,
  isFileUpload = false,
  submitText = "Submit",
  onSuccess // Add the onSuccess callback function
}) => {
  const formRef = useRef(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData(formRef.current);

    // Verify that the two passwords are the same (if there is a confirm_password field)
    const password = formData.get('password');
    const confirmPassword = formData.get('confirm_password');

    if (password && confirmPassword && password !== confirmPassword) {
      alert('Passwords do not match!');
      return;
    }

    let config = {
      method: method,
      headers: {
        'Content-Type': isFileUpload ? 'multipart/form-data' : 'application/json',
      },
      body: isFileUpload ? formData : JSON.stringify(Object.fromEntries(formData)),
    };

    try {
      const response = await fetch('http://127.0.0.1:5000'+apiUrl, config);
      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || `HTTP error! status: ${response.status}`);
      }

      console.log('Response:', data);
      alert('Success!');

      // Call the onSuccess callback, passing the data to the parent component
      if (onSuccess) {
        onSuccess(data);
      }

      formRef.current.reset();
    } catch (error) {
      console.error('Error:', error);
      alert(`Error! ${error.message}`);
    }
  };

  return (
    <form ref={formRef} onSubmit={handleSubmit} className="bg-gray sm:p-6 h-full w-full lg:max-w-lg">
      {fields.map((field) => (
        <div key={field.name} className="mb-4">
          <label htmlFor={field.name} className="block text-black mb-2">{field.label}</label>
          {field.type === 'file' ? (
            <input
              type={field.type}
              id={field.name}
              name={field.name}
              required={field.required}
              className="w-full px-[30px] py-[18px] border border-black rounded-[14px] text-black outline-none"
            />
          ) : (
            <input
              type={field.type || 'text'}
              id={field.name}
              name={field.name}
              placeholder={field.placeholder}
              required={field.required}
              className="w-full px-[30px] py-[18px] border border-black rounded-[14px] text-black outline-none"
            />
          )}
        </div>
      ))}
      <button type="submit" className="btn-primary w-full">
        {submitText}
      </button>
    </form>
  );
};

export default FormComponent;