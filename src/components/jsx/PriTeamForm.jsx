import ModalForm from '../ModalForm';
import modalStyles from '../../utils/formConfigs/modal';
const name = "";
const role = "";
const description = "Add a private cemetery.";
const link = "#";
export default function PriTeamForm() {
    const formFields = [
    { name: 'pic', label: 'Picture', type: 'file', required: true },
    { name: 'name', label: 'Name', type: 'text', required: true },
    { name: 'birth_date', label: 'Birth Date', type: 'date' , required: true},
    { name: 'death_date', label: 'Death Date', type: 'date' , required: true},
    { name: 'biography', label: 'Description', type: 'textarea', required: true }
];
  return (
      <ModalForm
            apiUrl="/createMemorial"
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
          <div className="p-[60px]">
              <div className="flex flex-col sm:flex-row relative">
                  <picture className="w-[175px] h-[175px] rounded-lg shrink-0"><img src="/team/d0.png" alt={name} className="w-full h-full rounded-lg object-cover transform will-change-transform transition-transform duration-300 hover:scale-105"/></picture>
                  <div className="flex flex-col justify-end sm:ml-5">
                      <h3 className="text-lg font-medium">{name}</h3>
                      <p className="text-sm font-normal">{role}</p>
                  </div>
              </div>
              <div className="w-full h-[1px] bg-black my-7"></div>
              <div>{description}</div>
          </div>
        </ModalForm>
  );
}