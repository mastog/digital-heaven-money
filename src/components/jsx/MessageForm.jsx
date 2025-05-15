import ModalForm from '../ModalForm';
import modalStyles from '../../utils/formConfigs/modal';
export default function MessageForm({ id}) {
    const formFields = [
    { name: 'message', label: 'Message', type: 'textarea', required: true },
    { name: 'deceased_id', type: 'hidden', value: id }
];
  return (
      <ModalForm
            apiUrl="/createMessage"
            method="POST"
            fields={formFields}
            submitText="Add"
            cancelText="Cancel"
            classConfig={modalStyles}
            onSuccess={() => {
                window.location.reload();
            }}
            client:load
            >
          <button className="btn-primary flex items-center mb-10">
              <img src="/images/message.svg" alt="Icon" className="btn-icon"/>
              <span className="btn-text">Add Message</span>
          </button>
        </ModalForm>
  );
}