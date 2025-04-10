import FormComponent from '../FormComponents.jsx';
import login from '../../utils/formConfigs/login';

export default function LoginForm() {
  return (
      <FormComponent
          client:load
          apiUrl="/login"
          method="POST"
          fields={[
            { name: 'username', label: 'Username*', type: 'text', placeholder: 'Username', required: true },
            { name: 'password', label: 'Password*', type: 'password', placeholder: 'Password', required: true }
          ]}
          submitText="Login"
          classConfig={login}
          onSuccess={(data) => {
            if (data.access_token && data.refresh_token) {
              localStorage.setItem('accessToken', data.access_token);
              localStorage.setItem('refreshToken', data.refresh_token);
              alert('Login successful!');
              window.location.href = '/';
            }
          }}
        />
  );
}
