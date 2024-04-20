import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import Home from './pages/Home';
import { AuthContextProvider } from './contexts/AuthContext/AuthContext';

// For material ui
import '@fontsource/roboto/300.css';
import '@fontsource/roboto/400.css';
import '@fontsource/roboto/500.css';
import '@fontsource/roboto/700.css';
import Login from './pages/Login';
import NotFound from './pages/NotFound';
import Signup from './pages/Signup';
import Users from './pages/User';
import { ProtectedRoutes } from './utils';
import Navbar from './components/Navbar';

const router = createBrowserRouter([
  {
    path: '/',
    element: <Navbar />,
    children: [
      { path: '/', element: <Home /> },
      { path: '/login', element: <Login /> },
      { path: '/signup', element: <Signup /> },
    ],
  },
  {
    path: '/',
    element: <ProtectedRoutes />,
    children: [{ path: '/users', element: <Users /> }],
  },
  { path: '*', element: <NotFound /> },
]);

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement,
);
root.render(
  <React.StrictMode>
    <AuthContextProvider>
      <RouterProvider router={router} />
    </AuthContextProvider>
  </React.StrictMode>,
);
