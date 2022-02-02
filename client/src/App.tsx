import { Route, Routes } from 'react-router';
import Admin from './components/Admin';
import AuthProvider from './components/AuthProvider';
import EndUser from './components/EndUser';
import Login from './components/Login';
import RequireAuth from './components/RequireAuth';

function App() {
  return (
    <AuthProvider>
   <Routes>
     <Route path="/" element={<EndUser />} />
     <Route path="/login" element={<Login />} />
      <Route
            path="/ap"
            element={
              <RequireAuth>
                <Admin />
              </RequireAuth>
            }
          />
   </Routes>
    </AuthProvider>
  );
}

export default App;
