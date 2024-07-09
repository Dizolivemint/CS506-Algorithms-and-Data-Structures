import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
import { createGlobalStyle, ThemeProvider } from 'styled-components';
import Head from './components/head';

const GlobalStyle = createGlobalStyle`
  body {
    font-family: 'Nunito', sans-serif;
    font-size: clamp(1rem, 1.5vw, 2rem);
    
  }

  h1, h2, h3, h4, h5, h6 {
    font-family: 'Maven Pro', sans-serif;
  }

  label, input, button, [] {
    font-family: 'Nunito', sans-serif;
    font-size: clamp(1rem, 1.5vw, 2rem);
  }
`;

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);
root.render(
  <React.StrictMode>
    <Head />
    <ThemeProvider theme={{}}>
      <GlobalStyle />
      <App />
    </ThemeProvider>
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
