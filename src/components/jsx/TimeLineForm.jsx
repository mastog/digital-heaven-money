import ModalForm from '../ModalForm';
import modalStyles from '../../utils/formConfigs/modal';
export default function TimeLineForm({ id}) {
    const formFieldsTime = [
    { name: 'pic', label: 'Picture', type: 'file' , required: true},
    { name: 'title', label: 'Title', type: 'text', required: true },
    { name: 'photo_date', label: 'Time', type: 'month' , required: true},
    { name: 'description', label: 'Description', type: 'textarea', required: true },
    { name: 'deceased_id', type: 'hidden', value: id }
];
  return (
      <ModalForm
            apiUrl="/crud/DeceasedPhoto/create"
            method="POST"
            fields={formFieldsTime}
            submitText="Add"
            cancelText="Cancel"
            classConfig={modalStyles}
            onSuccess={() => {
                window.location.reload();
            }}
            client:load
            >
            <button className="btn-primary items-center mb-5">
                Add Timeline
                </button>
        </ModalForm>
  );
}