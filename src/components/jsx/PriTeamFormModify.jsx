import ModalForm from '../ModalForm';
import modalStyles from '../../utils/formConfigs/modal';
export default function PriTeamFormModify({deceased}) {
    const formFields = [
    { name: 'pic', label: 'Picture', type: 'file'},
    { name: 'name', label: 'Name', type: 'text',value:deceased.name },
    { name: 'birth_date', label: 'Birth Date', type: 'date',value:deceased.birth_date },
    { name: 'death_date', label: 'Death Date', type: 'date',value:deceased.death_date },
    { name: 'biography', label: 'Description', type: 'textarea',value:deceased.biography },
    { name: 'id', type: 'hidden', value: deceased.id }
];
  return (
      <ModalForm
            apiUrl="/crud/Deceased/update"
            method="POST"
            fields={formFields}
            submitText="Submit"
            cancelText="Cancel"
            classConfig={modalStyles}
            onSuccess={() => {
                window.location.reload();
            }}
            client:load
            >
          <button className="btn-primary flex items-center mb-5">
              <img src="/images/edit-2.svg" alt="Icon" className="btn-icon"/>
              <span className="btn-text">Modify Deceased</span>
          </button>
        </ModalForm>
  );
}