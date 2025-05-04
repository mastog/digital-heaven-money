import ModalForm from '../ModalForm';
import modalStyles from '../../utils/formConfigs/modal';
export default function RelationshipForm({ id,options}) {
    const formFieldsTime = [
        { name: 'relation_type', label: 'Relation', type: 'text', required: true },
        { name: 'deceased2_id', label: 'Deceased', type: 'select' , required: true,options:options},
        { name: 'deceased1_id', type: 'hidden', value: id }
];
  return (
      <ModalForm
            apiUrl="/crud/FamilyTree/create"
            method="POST"
            fields={formFieldsTime}
            submitText="Create"
            cancelText="Cancel"
            classConfig={modalStyles}
            onSuccess={() => {
                window.location.reload();
            }}
            client:load
            >
            <button className="btn-primary">
                    Create Relationship
                </button>
        </ModalForm>
  );
}