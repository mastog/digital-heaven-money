import FormComponent from '../FormComponents.jsx';
import join from '../../utils/formConfigs/join';

export default function JoinForm() {
  return (
      <FormComponent
          client:load
          apiUrl="/join"
          method="POST"
          fields={[
            { name: 'Key', type: 'text', placeholder: 'Redemption Code', required: true }
          ]}
          submitText="Redeem Code"
          classConfig={join}
          onSuccess={async (data) => {
              const {showNotification} = await import('../../utils/notifications.js');
              showNotification([data.message]);
          }}
        />
  );
}