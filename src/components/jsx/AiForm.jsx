import ModalForm from '../ModalForm';
import modalStyles from '../../utils/formConfigs/modal';
import Typed from '../Typed.jsx';
import { useEffect } from 'react';

export default function AiForm({ name, description,pic_url }) {
  const formFields = [
    { name: 'text', label: 'Have a talk with your hero', type: 'text' },
    { name: 'description', type: 'hidden', value: description },
    { name: 'name', type: 'hidden', value: name }
  ];

  const updateTypedStrings = (newStrings) => {
    const event = new CustomEvent('update-typed-strings', {
      detail: newStrings
    });
    window.dispatchEvent(event);
  };

  useEffect(() => {
  }, []);

  return (
    <div>
      <ModalForm
        apiUrl="/ai"
        method="POST"
        fields={formFields}
        submitText="Submit"
        cancelText="Cancel"
        classConfig={modalStyles}
        onSuccess={(data) => {
          updateTypedStrings([data.response]);
        }}
      >
        <section className="w-full flex flex-col gap-8 mb-16 sm:mb-24 transition">
          <div
            className="hero hero__bg w-full max-w-[700px] mx-auto aspect-[16/9] hover:scale-110"
            style={{
              '--bg-url': `url(${pic_url})`
            }}
          >
            <div className="hero__content h-full max-w-[700px] mx-auto flex flex-col justify-center items-center text-center">
              <Typed strings={["Have a talk with your hero"]}/>
            </div>
          </div>
        </section>
      </ModalForm>

      <style jsx="true">{`
        .hero__bg {
          position: relative;
        }
        .hero__bg::before {
          z-index: -1;
          content: '';
          width: 100%;
          height: 100%;
          position: absolute;
          background-image: var(--bg-url);
          background-size: cover;
          background-position: center;
          background-repeat: no-repeat;
          opacity: 0.5;
          border-radius: 45px;
          filter: grayscale(100%);
        }
      `}</style>
    </div>
  );
}
