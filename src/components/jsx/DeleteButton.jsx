
import { apiRequest } from "../../utils/api";

export default function DeleteButton({ id }) {
  async function handleClick() {
    await apiRequest(`/crud/Deceased/delete`, "POST", { "id":id });
    const {showNotification} = await import('../../utils/notifications.js');
    showNotification(["Delete successfully!"]);
    await new Promise(resolve => setTimeout(resolve, 1000));
    window.location.href = "/private-memorial-hall";
  }

  return (
    <button className="btn-primary mb-5" onClick={handleClick}>
      Delete Deceased
    </button>
  );
}
