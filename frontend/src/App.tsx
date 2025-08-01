import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import CandidatesList from './pages/CandidatesList';
import CandidateDetail from './pages/CandidateDetail';
import Metrics from './pages/Metrics';
import Admins from './pages/Admins';
import Notifications from './pages/Notifications';
import './styles/design-system.css';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={
          <Layout>
            <Dashboard />
          </Layout>
        } />
        <Route path="/candidates" element={
          <Layout>
            <CandidatesList />
          </Layout>
        } />
        <Route path="/candidate/:id" element={
          <Layout>
            <CandidateDetail />
          </Layout>
        } />
        <Route path="/metrics" element={
          <Layout>
            <Metrics />
          </Layout>
        } />
        <Route path="/admins" element={
          <Layout>
            <Admins />
          </Layout>
        } />
        <Route path="/notifications" element={
          <Layout>
            <Notifications />
          </Layout>
        } />
      </Routes>
    </Router>
  );
}

export default App; 