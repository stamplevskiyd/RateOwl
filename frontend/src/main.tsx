// frontend/src/main.tsx
import React from 'react';
import ReactDOM from 'react-dom/client';
import {BrowserRouter} from 'react-router-dom';

import App from './App';
import {ErrorProvider} from '@/context/ErrorContext';

import '@/index.css'; // Tailwind + глобальные стили

ReactDOM.createRoot(document.getElementById('root')!).render(
    <React.StrictMode>
        {/* Глобальный провайдер карточек ошибок */}
        <ErrorProvider>
            {/* SPA-роутинг */}
            <BrowserRouter>
                <App/>
            </BrowserRouter>
        </ErrorProvider>
    </React.StrictMode>,
);