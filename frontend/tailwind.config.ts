import type {Config} from 'tailwindcss';
import colors from 'tailwindcss/colors';

const config: Config = {
    content: ['./index.html', './src/**/*.{ts,tsx,js,jsx}'],
    theme: {
        extend: {
            colors: {
                /* spruce — ёлочно-зелёный */
                spruce: {
                    50: '#ecf8f4',
                    100: '#cfece0',
                    200: '#a4d9c3',
                    300: '#77c5a4',
                    400: '#4aae85',
                    500: '#25966a',
                    600: '#147e56',
                    700: '#0f6642',
                    800: '#0c4d32',
                    900: '#073321',
                },
                /* базовые нейтральные серые */
                canvas: colors.zinc[900], // фон приложения
                surface: colors.zinc[800], // карточки / панели
            },
        },
    },
    plugins: [],
};

export default config;