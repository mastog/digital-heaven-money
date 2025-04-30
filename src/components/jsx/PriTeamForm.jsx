import ModalForm from '../ModalForm';
import modalStyles from '../../utils/formConfigs/modal';
import { Image } from "astro:assets";
import p0 from "../../assets/team/d0.png";
const pic = p0;
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
                  <picture className="w-[175px] h-[175px] shrink-0"><img src={pic.src} alt={name} /></picture>
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