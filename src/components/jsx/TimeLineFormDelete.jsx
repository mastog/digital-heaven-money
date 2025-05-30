import ModalForm from '../ModalForm';
import modalStyles from '../../utils/formConfigs/modal';
export default function TimeLineFormDelete({ options}) {
    const formFieldsTime = [
    { name: 'id', label: 'Delete', type: 'select' , required: true,options:options},
];
  return (
      <ModalForm
            apiUrl="/crud/DeceasedPhoto/delete"
            method="POST"
            fields={formFieldsTime}
            submitText="Confirm"
            cancelText="Cancel"
            classConfig={modalStyles}
            onSuccess={() => {
                window.location.reload();
            }}
            client:load
            >
            <button className="right-button-t">
                Delete Timeline
                </button>
        </ModalForm>
  );
}