// notifications.js
import { apiRequest } from './api'; // 请确保路径正确

let prevItems = [];
let intervalId = null;

// 动态添加样式
const style = document.createElement('style');
style.textContent = `
  @keyframes slideIn {
    from { transform: translate(-50%, -100%); opacity: 0; }
    to { transform: translate(-50%, 0); opacity: 1; }
  }
  @keyframes slideOut {
    from { transform: translate(-50%, 0); opacity: 1; }
    to { transform: translate(-50%, -100%); opacity: 0; }
  }
  @keyframes progress {
    from { width: 0; }
    to { width: 100%; }
  }
  .astro-notification {
    position: fixed;
    top: 1rem;
    left: 50%;
    transform: translate(-50%, -100%);
    background: #f3f3f3;
    padding: 1rem;
    border-radius: 0.5rem;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    z-index: 9999;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    animation: slideIn 0.3s forwards;
  }
  .astro-notification.hide {
    animation: slideOut 0.3s forwards;
  }
  .progress-bar {
    height: 4px;
    background: #e5e7eb;
    border-radius: 2px;
    overflow: hidden;
  }
  .progress-inner {
    width: 0;
    height: 100%;
    background: #000000;
    animation: progress 1s linear forwards;
  }
`;
document.head.appendChild(style);

async function fetchItems(id) {
  try {
    return await apiRequest(`/deceasedOfferings/${id}`, 'GET');
  } catch (error) {
    console.error('Error:', error);
    return null;
  }
}

function detectChanges(currentItems) {
  const changes = [];
  const prevMap = new Map(prevItems.map(item => [item.name, item]));
  for (const currentItem of currentItems) {
    const prevItem = prevMap.get(currentItem.name);
    if (!prevItem || currentItem.count > prevItem.count) {
      if((currentItem.count - (prevItem?.count || 0))===1){
        changes.push(`A ${currentItem.name} has been offered`);
      }else{
        changes.push(`${currentItem.count - (prevItem?.count || 0)} ${currentItem.name} have been offered`);
      }
      for (let i = 0; i < currentItem.count - (prevItem?.count || 0); i++) {
        window.dropCircle(currentItem.image);
      }
    }
  }

  return changes;
}

export function showNotification(messages) {
  const notification = document.createElement('div');
  notification.className = 'astro-notification';

  const content = document.createElement('div');
  content.className = 'text-sm text-gray-800 space-y-1';
  messages.forEach(msg => {
    const p = document.createElement('p');
    p.textContent = msg;
    content.appendChild(p);
  });

  const progressBar = document.createElement('div');
  progressBar.className = 'progress-bar';
  const progressInner = document.createElement('div');
  progressInner.className = 'progress-inner';
  progressBar.appendChild(progressInner);

  notification.appendChild(content);
  notification.appendChild(progressBar);
  document.body.appendChild(notification);

  setTimeout(() => {
    notification.classList.add('hide');
    setTimeout(() => notification.remove(), 300);
  }, 1500);
}

async function checkUpdates(id) {
  const currentItems = await fetchItems(id);
  if (!currentItems) return;

  if (prevItems.length === 0) {
    prevItems = currentItems;
    return;
  }
  const changes = detectChanges(currentItems);
  if (changes.length > 0) {
    showNotification(changes);
  }

  prevItems = currentItems;
}

export async function initPolling(id) {
  try {
    const initialItems = await fetchItems(id);
    if (!initialItems) {
      console.log('The initial request failed and the polling was terminated');
      return;
    }

    prevItems = initialItems;
    intervalId = setInterval(() => checkUpdates(id), 1500);

    window.addEventListener('beforeunload', () => {
      clearInterval(intervalId);
    });
  } catch (error) {
    console.error('Polling initialization failed:', error);
  }
}
