import FormComponent from '../FormComponents.jsx';
import login from '../../utils/formConfigs/login';

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
          classConfig={login}
          onSuccess={async (data) => {
              const {showNotification} = await import('../../utils/notifications.js');
              showNotification([data.message]);
          }}
        />
  );
}