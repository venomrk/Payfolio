import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
    return twMerge(clsx(inputs));
}

export function formatCurrency(amount: number, short: boolean = false): string {
    const absAmount = Math.abs(amount);

    if (short) {
        if (absAmount >= 10000000) {
            return `₹${(amount / 10000000).toFixed(2)}Cr`;
        } else if (absAmount >= 100000) {
            return `₹${(amount / 100000).toFixed(2)}L`;
        } else if (absAmount >= 1000) {
            return `₹${(amount / 1000).toFixed(1)}K`;
        }
    }

    return new Intl.NumberFormat("en-IN", {
        style: "currency",
        currency: "INR",
        maximumFractionDigits: 0,
    }).format(amount);
}

export function formatDate(date: string | Date): string {
    return new Intl.DateTimeFormat("en-IN", {
        day: "numeric",
        month: "short",
        year: "numeric",
    }).format(new Date(date));
}

export function formatRelativeTime(date: string | Date): string {
    const now = new Date();
    const target = new Date(date);
    const diffMs = now.getTime() - target.getTime();
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);

    if (diffMins < 1) return "Just now";
    if (diffMins < 60) return `${diffMins}m ago`;
    if (diffHours < 24) return `${diffHours}h ago`;
    if (diffDays < 7) return `${diffDays}d ago`;

    return formatDate(date);
}

export function getGreeting(): string {
    const hour = new Date().getHours();
    if (hour < 12) return "Good morning";
    if (hour < 18) return "Good afternoon";
    return "Good evening";
}

export function getInitials(name: string): string {
    return name
        .split(" ")
        .map((n) => n[0])
        .join("")
        .toUpperCase()
        .slice(0, 2);
}
