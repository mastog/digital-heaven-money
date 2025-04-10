import { useState, useCallback } from 'react';
import FormComponent from './FormComponents';

const ModalForm = ({
  children,
  fields,
  onSuccess,
  submitText = "Submit",
  cancelText = "Cancel",
  showCancelButton = true, // 新增的控制按钮数量的参数
  ...formProps
}) => {
  const [isOpen, setIsOpen] = useState(false);

  const handleTriggerClick = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsOpen(true);
  }, []);

  const handleSubmitSuccess = useCallback((data) => {
    setIsOpen(false);
    onSuccess?.(data);
  }, [onSuccess]);

  const handleClose = useCallback(() => {
    setIsOpen(false);
  }, []);

  return (
    <div onClick={handleTriggerClick}>
      <style>
        {`
          @keyframes fadeIn {
            0% {
              opacity: 0;
            }
            100% {
              opacity: 1;
            }
          }

          .animate-fadeIn {
            animation: fadeIn 0.3s ease-out forwards;
          }
        `}
      </style>
      {children}

      {isOpen && (
        <div
          className="fixed inset-0 bg-transparent flex items-center justify-center p-4 z-50 backdrop-blur-sm"
          onClick={(e) => e.stopPropagation()}
        >
          <div className="bg-transparent w-full max-w-md form-component-class shadow-lg opacity-0 transition-opacity duration-300 animate-fadeIn">
              <FormComponent
                {...formProps}
                fields={fields}
                submitText={submitText}
                cancelText={cancelText}
                showCancelButton={showCancelButton}
                onSuccess={handleSubmitSuccess}
                onClose={handleClose}
              />
          </div>
        </div>
      )}
    </div>
  );
};

export default ModalForm;
