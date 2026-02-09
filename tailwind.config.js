/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            fontFamily: {
                sans: ['"Plus Jakarta Sans"', 'sans-serif'],
            },
            colors: {
                z5: {
                    dark: '#0B0F19',
                    card: '#131B2C',
                    purple: '#8B5CF6',
                    pink: '#EC4899',
                    text: '#E2E8F0',
                    muted: '#94A3B8',
                }
            },
            backgroundImage: {
                'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
                'gradient-primary': 'linear-gradient(to right, #8B5CF6, #EC4899)',
            },
            animation: {
                'float': 'float 8s ease-in-out infinite',
                'float-slow': 'float 12s ease-in-out infinite',
                'breathe': 'breathe 3s ease-in-out infinite',
                'pulse-glow': 'pulseGlow 2s ease-in-out infinite',
            },
            keyframes: {
                float: {
                    '0%, 100%': { transform: 'translateY(0px)' },
                    '50%': { transform: 'translateY(-15px)' },
                },
                breathe: {
                    '0%, 100%': { filter: 'drop-shadow(0 0 20px rgba(139, 92, 246, 0.5))' },
                    '50%': { filter: 'drop-shadow(0 0 35px rgba(236, 72, 153, 0.7))' },
                },
                pulseGlow: {
                    '0%, 100%': { boxShadow: '0 0 20px rgba(139, 92, 246, 0.4)' },
                    '50%': { boxShadow: '0 0 40px rgba(236, 72, 153, 0.6)' },
                },
            },
            boxShadow: {
                'glow': '0 0 30px rgba(139, 92, 246, 0.3)',
                'glow-pink': '0 0 30px rgba(236, 72, 153, 0.3)',
                'card': '0 20px 40px -10px rgba(139, 92, 246, 0.15)',
            },
        },
    },
    plugins: [],
}
