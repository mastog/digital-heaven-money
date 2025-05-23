import FormComponent from '../FormComponents.jsx';
import login from '../../utils/formConfigs/login';

export default function RegistrationForm() {
  return (
          <FormComponent
          client:load
          apiUrl="/register"
          method="POST"
          fields={[
            { name: 'username', label: 'Username*', type: 'text', placeholder: 'Username', required: true },
            { name: 'email', label: 'Email*', type: 'email', placeholder: 'Email', required: true },
            { name: 'password', label: 'Password*', type: 'password', placeholder: 'Password', required: true },
            { name: 'confirm_password', label: 'Confirm Password*', type: 'password', placeholder: 'Confirm Password', required: true }
          ]}
          submitText="Join"
          classConfig={login}
          onSuccess={async () => {
              const {showNotification} = await import('../../utils/notifications.js');
              showNotification(['Registration successful!']);
              await new Promise(resolve => setTimeout(resolve, 1000));
              window.location.reload();
          }}
        />
  );
}