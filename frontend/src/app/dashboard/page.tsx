"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import {
    LayoutDashboard,
    Wallet,
    ArrowRightLeft,
    Lightbulb,
    Settings,
    LogOut,
    Plus,
    RefreshCw,
    TrendingUp,
    TrendingDown,
    ChevronRight,
    Sparkles,
    Building,
    LineChart,
    CreditCard,
    Coins
} from "lucide-react";

// Mock data for demo
const mockPortfolio = {
    net_worth: 12345678,
    net_worth_change: 234567,
    net_worth_change_percent: 1.9,
    breakdown: {
        banks: 1850000,
        investments: 8920000,
        crypto: 1200000,
        wallets: 375678,
    }
};

const mockAccounts = [
    { id: "1", name: "HDFC Savings", institution: "HDFC Bank", type: "bank", balance: 234567, icon: Building },
    { id: "2", name: "Zerodha", institution: "Zerodha Broking", type: "investment", balance: 4580000, icon: LineChart },
    { id: "3", name: "ICICI Credit Card", institution: "ICICI Bank", type: "credit_card", balance: -42000, icon: CreditCard },
    { id: "4", name: "CoinDCX", institution: "CoinDCX", type: "crypto", balance: 1200000, icon: Coins },
];

const mockInsight = {
    title: "Cash runway is 4.2 months",
    description: "Based on your current burn rate of ₹1.2L/month",
    severity: "warning",
};

export default function DashboardPage() {
    const router = useRouter();
    const [user, setUser] = useState<any>(null);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        // Check auth
        const storedUser = localStorage.getItem("user");
        if (!storedUser) {
            router.push("/login");
            return;
        }
        setUser(JSON.parse(storedUser));
        setIsLoading(false);
    }, [router]);

    const handleLogout = () => {
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        localStorage.removeItem("user");
        router.push("/");
    };

    const formatCurrency = (amount: number) => {
        const absAmount = Math.abs(amount);
        if (absAmount >= 10000000) {
            return `₹${(amount / 10000000).toFixed(2)}Cr`;
        } else if (absAmount >= 100000) {
            return `₹${(amount / 100000).toFixed(2)}L`;
        } else {
            return new Intl.NumberFormat("en-IN", {
                style: "currency",
                currency: "INR",
                maximumFractionDigits: 0,
            }).format(amount);
        }
    };

    if (isLoading) {
        return (
            <div className="min-h-screen flex items-center justify-center">
                <div className="w-8 h-8 border-2 border-wealth-purple border-t-transparent rounded-full animate-spin" />
            </div>
        );
    }

    return (
        <div className="min-h-screen flex">
            {/* Sidebar */}
            <aside className="w-64 bg-surface border-r border-border-subtle flex flex-col">
                {/* Logo */}
                <div className="p-6 border-b border-border-subtle">
                    <Link href="/dashboard" className="flex items-center gap-3">
                        <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-wealth-purple to-money-green flex items-center justify-center">
                            <span className="text-white font-bold text-lg">P</span>
                        </div>
                        <span className="text-lg font-bold text-text-primary">Payfolio</span>
                    </Link>
                </div>

                {/* Nav */}
                <nav className="flex-1 p-4 space-y-1">
                    {[
                        { icon: LayoutDashboard, label: "Dashboard", href: "/dashboard", active: true },
                        { icon: Wallet, label: "Accounts", href: "/dashboard/accounts" },
                        { icon: ArrowRightLeft, label: "Transactions", href: "/dashboard/transactions" },
                        { icon: Lightbulb, label: "Insights", href: "/dashboard/insights" },
                        { icon: Settings, label: "Settings", href: "/dashboard/settings" },
                    ].map((item) => (
                        <Link
                            key={item.label}
                            href={item.href}
                            className={`flex items-center gap-3 px-4 py-3 rounded-xl transition-colors ${item.active
                                    ? "bg-wealth-purple/10 text-wealth-purple"
                                    : "text-text-secondary hover:bg-surface-elevated hover:text-text-primary"
                                }`}
                        >
                            <item.icon className="w-5 h-5" />
                            <span className="font-medium">{item.label}</span>
                        </Link>
                    ))}
                </nav>

                {/* User */}
                <div className="p-4 border-t border-border-subtle">
                    <div className="flex items-center gap-3 mb-4">
                        <div className="w-10 h-10 rounded-full bg-wealth-purple/20 flex items-center justify-center">
                            <span className="text-wealth-purple font-semibold">
                                {user?.full_name?.[0] || "U"}
                            </span>
                        </div>
                        <div className="flex-1 min-w-0">
                            <div className="text-small font-medium text-text-primary truncate">
                                {user?.full_name || "User"}
                            </div>
                            <div className="text-micro text-text-tertiary truncate">{user?.email}</div>
                        </div>
                    </div>
                    <button
                        onClick={handleLogout}
                        className="flex items-center gap-2 w-full px-4 py-2 text-text-secondary hover:text-alert-red hover:bg-alert-red/10 rounded-lg transition-colors"
                    >
                        <LogOut className="w-4 h-4" />
                        <span className="text-small">Sign out</span>
                    </button>
                </div>
            </aside>

            {/* Main Content */}
            <main className="flex-1 overflow-auto">
                <div className="max-w-6xl mx-auto p-8">
                    {/* Header */}
                    <div className="mb-8">
                        <h1 className="text-h1 text-text-primary mb-1">
                            Good {new Date().getHours() < 12 ? "morning" : new Date().getHours() < 18 ? "afternoon" : "evening"}, {user?.full_name?.split(" ")[0] || "there"}
                        </h1>
                        <p className="text-text-secondary">Here's your financial overview</p>
                    </div>

                    {/* Net Worth Card */}
                    <div className="bg-gradient-to-br from-surface via-surface to-wealth-purple/5 border border-border-subtle rounded-2xl p-8 mb-8">
                        <div className="text-text-secondary mb-2">Your Net Worth</div>
                        <div className="flex items-end gap-4 mb-4">
                            <div className="text-display text-text-primary number-animate">
                                {formatCurrency(mockPortfolio.net_worth)}
                            </div>
                            <div className={`flex items-center gap-1 text-lg ${mockPortfolio.net_worth_change >= 0 ? "text-money-green" : "text-alert-red"}`}>
                                {mockPortfolio.net_worth_change >= 0 ? <TrendingUp className="w-5 h-5" /> : <TrendingDown className="w-5 h-5" />}
                                <span>{formatCurrency(mockPortfolio.net_worth_change)}</span>
                                <span className="text-text-secondary">({mockPortfolio.net_worth_change_percent}%)</span>
                            </div>
                        </div>

                        {/* Breakdown */}
                        <div className="grid grid-cols-4 gap-4 mt-6">
                            {[
                                { label: "Cash", value: mockPortfolio.breakdown.banks, color: "bg-neutral-blue" },
                                { label: "Investments", value: mockPortfolio.breakdown.investments, color: "bg-wealth-purple" },
                                { label: "Crypto", value: mockPortfolio.breakdown.crypto, color: "bg-gold-accent" },
                                { label: "Wallets", value: mockPortfolio.breakdown.wallets, color: "bg-money-green" },
                            ].map((item) => (
                                <div key={item.label} className="p-4 bg-bg-dark/50 rounded-xl">
                                    <div className="flex items-center gap-2 mb-2">
                                        <div className={`w-2 h-2 rounded-full ${item.color}`} />
                                        <span className="text-small text-text-secondary">{item.label}</span>
                                    </div>
                                    <div className="text-lg font-semibold text-text-primary">
                                        {formatCurrency(item.value)}
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>

                    {/* Two Column Layout */}
                    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                        {/* Accounts */}
                        <div className="lg:col-span-2 bg-surface border border-border-subtle rounded-2xl p-6">
                            <div className="flex items-center justify-between mb-6">
                                <h2 className="text-h3 text-text-primary">Accounts</h2>
                                <div className="flex items-center gap-2">
                                    <button className="p-2 hover:bg-surface-elevated rounded-lg transition-colors">
                                        <RefreshCw className="w-4 h-4 text-text-secondary" />
                                    </button>
                                    <button className="flex items-center gap-2 px-4 py-2 bg-wealth-purple hover:bg-wealth-purple/90 rounded-lg text-small font-medium transition-colors">
                                        <Plus className="w-4 h-4" />
                                        Add Account
                                    </button>
                                </div>
                            </div>

                            <div className="space-y-3">
                                {mockAccounts.map((account) => (
                                    <div
                                        key={account.id}
                                        className="flex items-center justify-between p-4 bg-bg-dark/50 hover:bg-bg-dark rounded-xl cursor-pointer transition-colors group"
                                    >
                                        <div className="flex items-center gap-4">
                                            <div className="w-12 h-12 bg-surface-elevated rounded-xl flex items-center justify-center">
                                                <account.icon className="w-6 h-6 text-text-secondary" />
                                            </div>
                                            <div>
                                                <div className="font-medium text-text-primary">{account.name}</div>
                                                <div className="text-small text-text-tertiary">{account.institution}</div>
                                            </div>
                                        </div>
                                        <div className="flex items-center gap-4">
                                            <div className={`text-lg font-semibold ${account.balance < 0 ? "text-alert-red" : "text-text-primary"}`}>
                                                {formatCurrency(account.balance)}
                                            </div>
                                            <ChevronRight className="w-5 h-5 text-text-tertiary group-hover:text-text-secondary transition-colors" />
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>

                        {/* AI Insight */}
                        <div className="bg-surface border border-border-subtle rounded-2xl p-6">
                            <div className="flex items-center gap-2 mb-4">
                                <Sparkles className="w-5 h-5 text-wealth-purple" />
                                <h2 className="text-h3 text-text-primary">AI Insight</h2>
                            </div>

                            <div className="gradient-border bg-wealth-purple/5 rounded-xl p-5">
                                <div className={`text-micro font-medium mb-2 ${mockInsight.severity === "warning" ? "text-gold-accent" : "text-money-green"
                                    }`}>
                                    {mockInsight.severity === "warning" ? "⚠️ Warning" : "✨ Insight"}
                                </div>
                                <div className="text-text-primary font-medium mb-2">
                                    {mockInsight.title}
                                </div>
                                <div className="text-small text-text-secondary">
                                    {mockInsight.description}
                                </div>
                                <button className="mt-4 text-small text-wealth-purple hover:underline">
                                    View Details →
                                </button>
                            </div>

                            <button className="w-full mt-4 py-3 border border-border-subtle hover:bg-surface-elevated rounded-xl text-small text-text-secondary hover:text-text-primary transition-colors">
                                View All Insights
                            </button>
                        </div>
                    </div>
                </div>
            </main>
        </div>
    );
}
