import type { Config } from "tailwindcss";

const config: Config = {
    content: [
        "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
        "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
        "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
    ],
    darkMode: "class",
    theme: {
        extend: {
            colors: {
                // Brand Palette
                "money-green": "#10B981",
                "wealth-purple": "#8B5CF6",
                "alert-red": "#EF4444",
                "neutral-blue": "#3B82F6",
                "gold-accent": "#F59E0B",

                // Dark Mode
                "bg-dark": "#0A0F1C",
                "surface": "#111827",
                "surface-elevated": "#1F2937",
                "border-subtle": "#374151",
                "text-primary": "#F9FAFB",
                "text-secondary": "#9CA3AF",
                "text-tertiary": "#6B7280",

                // Light Mode
                "bg-light": "#F8FAFC",
                "surface-light": "#FFFFFF",
                "border-light": "#E5E7EB",
                "text-dark": "#111827",
            },
            fontFamily: {
                sans: ["Inter", "sans-serif"],
            },
            fontSize: {
                "display": ["48px", { lineHeight: "1.1", fontWeight: "700" }],
                "h1": ["32px", { lineHeight: "1.2", fontWeight: "600" }],
                "h2": ["24px", { lineHeight: "1.3", fontWeight: "600" }],
                "h3": ["20px", { lineHeight: "1.4", fontWeight: "500" }],
                "body": ["16px", { lineHeight: "1.5", fontWeight: "400" }],
                "small": ["14px", { lineHeight: "1.5", fontWeight: "400" }],
                "micro": ["12px", { lineHeight: "1.4", fontWeight: "500" }],
            },
            animation: {
                "fade-in": "fadeIn 0.3s ease-out",
                "slide-up": "slideUp 0.4s ease-out",
                "pulse-soft": "pulseSoft 2s ease-in-out infinite",
            },
            keyframes: {
                fadeIn: {
                    "0%": { opacity: "0" },
                    "100%": { opacity: "1" },
                },
                slideUp: {
                    "0%": { opacity: "0", transform: "translateY(10px)" },
                    "100%": { opacity: "1", transform: "translateY(0)" },
                },
                pulseSoft: {
                    "0%, 100%": { opacity: "1" },
                    "50%": { opacity: "0.7" },
                },
            },
        },
    },
    plugins: [],
};

export default config;
