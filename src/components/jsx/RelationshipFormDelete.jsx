import ModalForm from '../ModalForm';
import modalStyles from '../../utils/formConfigs/modal';
export default function RelationshipFormDelete({ options}) {
    const formFieldsTime = [
    { name: 'id', label: 'Delete', type: 'select' , required: true,options:options},
];
  return (
      <ModalForm
            apiUrl="/crud/FamilyTree/delete"
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
            <button className="btn-primary mb-5">
                Delete Relationship
                </button>
        </ModalForm>
  );
}