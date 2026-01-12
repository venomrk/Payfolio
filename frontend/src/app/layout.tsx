import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
    title: "Payfolio - Your Financial Command Center",
    description: "Unified financial operating system for individuals, founders, freelancers, and small businesses. See your complete financial reality in one place.",
    keywords: ["personal finance", "net worth tracker", "financial dashboard", "money management", "investment tracker"],
};

export default function RootLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    return (
        <html lang="en" className="dark">
            <body className="min-h-screen bg-bg-dark text-text-primary antialiased">
                {children}
            </body>
        </html>
    );
}
