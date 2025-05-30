import { useRef, useState, useEffect } from 'react';
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
  useEffect(() => {
    const observer = new MutationObserver(() => {
      alert("Don't do that please.")
      window.location.reload();
    });

    const hiddenInputs = formRef.current?.querySelectorAll('input[type="hidden"]') || [];

    hiddenInputs.forEach(input => {
      observer.observe(input, {
        attributes: true,
        attributeFilter: ['value']
      });
    });

    return () => observer.disconnect();
  }, []);

  const handleFileChange = async (e) => {
    const file = e.target.files[0];
    if (file) {
      const allowedExtensions = ['png', 'jpg', 'jpeg'];
      const fileExtension = file.name.split('.').pop().toLowerCase();

      if (!allowedExtensions.includes(fileExtension)) {
        const {showNotification} = await import('../utils/notifications.js');
        showNotification(['Invalid file type. Only PNG, JPG, and JPEG files are allowed.']);
        e.target.value = ""; // 清除文件选择
        setImagePreview(null);
        return;
      }

      if (file.size > 1 * 1024 * 1024) { // 2MB
        const {showNotification} = await import('../utils/notifications.js');
        showNotification(['Image size is too large, please no more than 1mb.']);
        e.target.value = ""; // 清除文件选择
        setImagePreview(null);
        return;
      }
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

    const fileInput = formRef.current.querySelector('input[type="file"]');
    if (fileInput && !fileInput.files[0]) {
      formData.delete('pic'); // 如果没有文件，移除 pic 字段
    }

    for (const field of fields) {
    const fieldType = field.type || 'text';
    if (['file', 'select'].includes(fieldType)) {
      continue; // 跳过文件和选择框
    }

    const value = formData.get(field.name);
    const trimmedValue = (value || '').trim();

    // 必填字段检查
    if (field.required && trimmedValue === '') {
      const { showNotification } = await import('../utils/notifications.js');
      showNotification([`${field.label} cannot be empty or only contain Spaces.`]);
      return;
    }

    // 非必填字段但输入了内容，检查是否全空格
    if (!field.required && value !== '' && trimmedValue === '') {
      const { showNotification } = await import('../utils/notifications.js');
      showNotification([`${field.label} cannot only contain Spaces.`]);
      return;
    }

    if ((field.type || 'text') === 'text') {
      const value = formData.get(field.name) || '';
      if (value.length > 50) {
        const { showNotification } = await import('../utils/notifications.js');
        showNotification([`${field.label} cannot exceed 50 characters.`]);
        return;
      }
    }
  }

    const password = formData.get('password');
    const confirmPassword = formData.get('confirm_password');
    if (password && confirmPassword && password !== confirmPassword) {
      const {showNotification} = await import('../utils/notifications.js');
              showNotification(['Passwords do not match!']);
      return;
    }

    // Get birth_date and death_date values
    const birthDate = formData.get('birth_date');
    const deathDate = formData.get('death_date');
    const photoDate = formData.get('photo_date');

    const today = new Date();
    today.setHours(23, 59, 59, 999);

    if (birthDate && new Date(birthDate) > today) {
      const { showNotification } = await import('../utils/notifications.js');
      showNotification(['Birth date cannot be in the future. What do you think you\'re doing?!']);
      return;
    }

    if (deathDate && new Date(deathDate) > today) {
      const { showNotification } = await import('../utils/notifications.js');
      showNotification(['Death date cannot be in the future. What do you think you\'re doing?!']);
      return;
    }

    if (photoDate && new Date(photoDate) > today) {
      const { showNotification } = await import('../utils/notifications.js');
      showNotification(['Timeline date cannot be in the future. What do you think you\'re doing?!']);
      return;
    }


    // Check if birth_date is later than death_date
    if (birthDate && deathDate && new Date(birthDate) > new Date(deathDate)) {
      const {showNotification} = await import('../utils/notifications.js');
              showNotification(['Birth date must be before death date!']);
      return;
    }

    const keysToDelete = [];
    for (let [key, value] of formData.entries()) {
      if (!value) {
        keysToDelete.push(key);
      }
    }

    for (let key of keysToDelete) {
      formData.delete(key);
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
  const handleLengthCheck = async (e, field) => {
      const value = e.target.value;
      if (field.type === 'text' && value.length >= 50) {
        const { showNotification } = await import('../utils/notifications.js');
        showNotification([`${field.label} has reached the 50 character limit.`]);
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
                className={`${classConfig.input || ""} appearance-none pr-10 hover:border-darkgray hover:ring-1 hover:ring-darkgray transition-all duration-150`} // 留出空间给图标
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
              className={`${classConfig.input || ""} resize-none overflow-hidden hover:border-darkgray hover:ring-1 hover:ring-darkgray transition-all duration-150`}
              rows={1}
              onInput={(e) => {
                e.target.style.height = 'auto';
                e.target.style.height = `${e.target.scrollHeight}px`;
              }}
              ref={(el) => {
                if (el) {
                  el.style.height = 'auto';
                  el.style.height = `${el.scrollHeight}px`;
                }
              }}
            />
          ): (
            <input
              type={field.type || 'text'}
              id={field.name}
              name={field.name}
              placeholder={field.placeholder}
              required={field.required}
              defaultValue={field.value}
              className={`${classConfig.input || ""} hover:border-darkgray hover:ring-1 hover:ring-darkgray transition-all duration-150`}
              {...(field.type === 'text' ? { maxLength: 50 } : {})}
              onInput={(e) => handleLengthCheck(e, field)}
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
