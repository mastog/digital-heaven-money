import { useRef, useState } from 'react';
import { apiRequest } from '../utils/api';

const FormComponent = ({
  apiUrl,
  method,
  fields,
  requiresAuth = false,
  submitText = "Submit",
  cancelText = "Cancel",
  classConfig = {},
  onSuccess,
  onClose,
  showCancelButton = false
}) => {
  const formRef = useRef(null);
  const [imagePreview, setImagePreview] = useState(null); // State for image preview

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setImagePreview(reader.result); // Set the image preview to the file's data URL
      };
      reader.readAsDataURL(file); // Read the file as a data URL
    } else {
      setImagePreview(null); // Clear preview if no file is selected
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData(formRef.current);

    const password = formData.get('password');
    const confirmPassword = formData.get('confirm_password');
    if (password && confirmPassword && password !== confirmPassword) {
      alert('Passwords do not match!');
      return;
    }

    // Get birth_date and death_date values
    const birthDate = formData.get('birth_date');
    const deathDate = formData.get('death_date');

    // Check if birth_date is later than death_date
    if (birthDate && deathDate && new Date(birthDate) > new Date(deathDate)) {
      alert('Birth date must be before death date!');
      return;
    }

    // Check file type
    const fileInput = formRef.current.querySelector('input[type="file"]');
    if (fileInput && fileInput.files.length > 0) {
      const file = fileInput.files[0];
      const allowedExtensions = ['png', 'jpg', 'jpeg'];
      const fileExtension = file.name.split('.').pop().toLowerCase();
      if (!allowedExtensions.includes(fileExtension)) {
        alert('Invalid file type. Only PNG, JPG, and JPEG files are allowed.');
        return;
      }
    }

    try {
      // Ready request data
      const requestData = formData;
      // Request functions using the generic API
      const responseData = await apiRequest(
        apiUrl,
        method,
        requestData,
      );

      console.log('Successful:', responseData);
      if (typeof onSuccess === 'function') {
        console.log('Calling onSuccess');
        onSuccess(responseData);
      }

      formRef.current.reset();
      setImagePreview(null); // Clear the image preview after submission
    } catch (error) {
    }
  };

  return (
    <form ref={formRef} onSubmit={handleSubmit} className={classConfig.form || ""}>
      {fields.map((field) => (
        <div key={field.name} className="mb-4">
          <div className={classConfig.label || ""}>
            {field.label}
          </div>
          {field.type === 'file' ? (
            <div className="file-upload-container flex items-center gap-4">
              {/* Image preview */}
              {imagePreview && (
                <div className="image-preview overflow-hidden w-32 h-32">
                  <img
                    src={imagePreview}
                    alt="Preview"
                    className="w-full h-full object-cover scale-90 rounded-lg"
                  />
                </div>
              )}
              {/* Custom file input button */}
              <div className="relative inline-block">
                <div className="file-input-label bg-green text-white py-2 px-4 rounded-lg transition-all duration-200 cursor-pointer">
                  Choose File
                  <input
                    type="file"
                    id={field.name}
                    name="pic"
                    required={field.required}
                    className="absolute inset-0 opacity-0 cursor-pointer"
                    onChange={handleFileChange}
                  />
                </div>
              </div>
            </div>

          ) : field.type === 'select' ? (
            <div className="relative">
              <select
                id={field.name}
                name={field.name}
                required={field.required}
                className={`${classConfig.input || ""} appearance-none pr-10`} // 留出空间给图标
                defaultValue=""
              >
                <option value="" disabled hidden>
                  {field.label}
                </option>
                {field.options?.map((option) => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </select>

              {/* 自定义下拉箭头 */}
              <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-3 text-gray-500">
                <svg
                  className="h-4 w-4"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                  aria-hidden="true"
                >
                  <path
                    fillRule="evenodd"
                    d="M5.23 7.21a.75.75 0 011.06.02L10 10.939l3.71-3.71a.75.75 0 111.06 1.06l-4.24 4.24a.75.75 0 01-1.06 0L5.25 8.27a.75.75 0 01-.02-1.06z"
                    clipRule="evenodd"
                  />
                </svg>
              </div>
            </div>

          ) : field.type === 'textarea' ? (
            <textarea
              id={field.name}
              name={field.name}
              placeholder={field.placeholder}
              required={field.required}
              defaultValue={field.value}
              className={`${classConfig.input || ""} resize-none overflow-hidden`}
              rows={1}
              onInput={(e) => {
                e.target.style.height = 'auto';
                e.target.style.height = `${e.target.scrollHeight}px`;
              }}
            />
          ): (
            <input
              type={field.type || 'text'}
              id={field.name}
              name={field.name}
              placeholder={field.placeholder}
              required={field.required}
              value={field.value}
              className={classConfig.input || ""}
            />
          )}
        </div>
      ))}

      <div className="flex justify-between gap-6 mt-10">
        {showCancelButton && (
          <button
            type="button"
            onClick={onClose}
            className={`${classConfig.button || ""} flex-grow`}
            style={{ flex: '1 1 0%' }}
          >
            {cancelText}
          </button>
        )}
        <button
          type="submit"
          className={`${classConfig.button || ""} btn-primary flex-grow`}
          style={{ flex: '3 1 0%' }}
        >
          {submitText}
        </button>
      </div>
    </form>
  );
};

export default FormComponent;
