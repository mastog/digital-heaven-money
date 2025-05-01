import { useState, useCallback } from 'react';
import { apiRequest } from '../utils/api';

const ModalKey = ({
  children,
  id,
  triggerText = 'Open',
  copyButtonText = 'Copy',
  closeButtonText = 'Close',
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const [fetchedText, setFetchedText] = useState('');
  const [loading, setLoading] = useState(false);

  const handleTriggerClick = useCallback(async (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsOpen(true);
    setLoading(true);
    try {
      const res = await apiRequest(`/invite/${id}`, 'GET');
      const text = await res['invite_key'];
      setFetchedText(text);
    } catch (err) {
      setFetchedText('Failed to get invite key.');
    } finally {
      setLoading(false);
    }
  }, [`/invite/${id}`]);

  const handleClose = useCallback(() => {
    setIsOpen(false);
  }, []);

  const handleCopy = useCallback(() => {
    navigator.clipboard.writeText(fetchedText)
      .then(async () => {
        const {showNotification} = await import('../utils/notifications.js');
        showNotification(['Copied!']);
      })
      .catch(async () => {
        const {showNotification} = await import('../utils/notifications.js');
        showNotification(['Copy failed.']);
      });
  }, [fetchedText]);

  return (
    <div onClick={handleTriggerClick}>
      <style>
        {`
          @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
          }
          .animate-fadeIn {
            animation: fadeIn 0.3s ease-out forwards;
          }
        `}
      </style>

      {children || <button>{triggerText}</button>}

      {isOpen && (
        <div
          className="fixed inset-0 bg-transparent flex items-center justify-center p-4 z-50 backdrop-blur-sm overflow-auto"
          onClick={(e) => e.stopPropagation()}
        >
          <div className="bg-white w-full max-w-md shadow-lg opacity-0 transition-opacity duration-300 animate-fadeIn rounded-2xl overflow-hidden">
            <div className="p-6 max-h-[90vh] overflow-y-auto space-y-4">
              {loading ? (
                <p>Loading...</p>
              ) : (
                <>
                  <pre className="whitespace-pre-wrap break-words border p-2 rounded-lg bg-gray">{fetchedText}</pre>
                  <button
                    onClick={handleCopy}
                    className="px-4 py-2 bg-dark text-white rounded hover:bg-gray"
                  >
                    {copyButtonText}
                  </button>
                </>
              )}
              <button
                onClick={handleClose}
                className="mt-4 px-4 py-2 bg-gray-300 text-black rounded hover:bg-gray-400"
              >
                {closeButtonText}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ModalKey;
