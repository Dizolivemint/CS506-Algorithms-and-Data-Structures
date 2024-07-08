import React from 'react';
import styled, { keyframes } from 'styled-components';

// Define the keyframes for the spinner animation
const spin = keyframes`
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
`;

// Create a styled div for the spinner
const Spinner = styled.div`
  border: 4px solid rgba(0, 0, 0, 0.1);
  border-top: 4px solid #007bff;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: ${spin} 1s linear infinite;
`;

// Define the Loading component
const Loader: React.FC = () => {
  return <Spinner />;
};

export default Loader;
