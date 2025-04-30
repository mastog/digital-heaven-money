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
                alert('Success');
                window.location.reload();
            }}
            client:load
            >
            <button className="btn-primary items-center mb-10">
                Add Message
                </button>
        </ModalForm>
  );
}