import Link from "next/link";
import {
    ArrowRight, TrendingUp, Shield, Zap, BarChart3, Wallet, PieChart, Bell, Sparkles,
    ChevronRight, Star, CreditCard, Building2, Smartphone, LineChart, Receipt,
    Banknote, ArrowUpRight, ArrowDownRight, RefreshCw, Plus, Eye, EyeOff,
    IndianRupee, Landmark, Store, Bitcoin, FileText, AlertCircle
} from "lucide-react";

export default function HomePage() {
    return (
        <main className="min-h-screen relative">
            {/* Aurora Background */}
            <div className="aurora-bg" />

            {/* Floating Particles */}
            <div className="particles">
                {[...Array(9)].map((_, i) => (
                    <div key={i} className="particle" />
                ))}
            </div>

            {/* Navigation */}
            <nav className="fixed top-0 left-0 right-0 z-50 glass">
                <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
                    <Link href="/" className="flex items-center gap-3 group">
                        <div className="relative w-10 h-10 rounded-xl bg-gradient-to-br from-wealth-purple via-blue to-money-green p-0.5">
                            <div className="w-full h-full rounded-xl bg-bg-dark flex items-center justify-center">
                                <IndianRupee className="w-5 h-5 text-money-green" />
                            </div>
                        </div>
                        <span className="text-xl font-bold text-text-primary">Payfolio</span>
                    </Link>

                    <div className="hidden md:flex items-center gap-8">
                        <Link href="#features" className="text-text-secondary hover:text-text-primary transition-colors">Features</Link>
                        <Link href="#connections" className="text-text-secondary hover:text-text-primary transition-colors">Connections</Link>
                        <Link href="#pricing" className="text-text-secondary hover:text-text-primary transition-colors">Pricing</Link>
                    </div>

                    <div className="flex items-center gap-4">
                        <Link href="/login" className="text-text-secondary hover:text-text-primary transition-colors font-medium">
                            Sign In
                        </Link>
                        <Link href="/signup" className="btn-primary px-5 py-2.5 rounded-xl font-semibold">
                            <span className="flex items-center gap-2">
                                Get Started <ArrowRight className="w-4 h-4" />
                            </span>
                        </Link>
                    </div>
                </div>
            </nav>

            {/* Hero Section - PhonePe Style */}
            <section className="relative pt-28 pb-16 overflow-hidden">
                <div className="max-w-7xl mx-auto px-6">
                    <div className="grid lg:grid-cols-2 gap-12 items-center">

                        {/* Left Content */}
                        <div className="stagger-children">
                            <div className="inline-flex items-center gap-2 px-4 py-2 glass rounded-full mb-6">
                                <span className="text-sm">🇮🇳</span>
                                <span className="text-sm text-text-secondary">India's First Financial Super-App</span>
                            </div>

                            <h1 className="text-4xl md:text-5xl lg:text-6xl font-extrabold text-text-primary mb-6 leading-[1.1]">
                                All your money.
                                <span className="block gradient-text">One dashboard.</span>
                            </h1>

                            <p className="text-lg text-text-secondary mb-8 max-w-xl">
                                Connect <span className="text-money-green font-semibold">GPay, PhonePe, Paytm</span> •
                                Track <span className="text-wealth-purple font-semibold">Zerodha, Groww, Crypto</span> •
                                Monitor <span className="text-blue font-semibold">SBI, HDFC, ICICI</span> —
                                all in real-time.
                            </p>

                            {/* App Icons Row */}
                            <div className="flex items-center gap-3 mb-8 flex-wrap">
                                {[
                                    { name: "GPay", bg: "bg-blue", icon: "G" },
                                    { name: "PhonePe", bg: "bg-wealth-purple", icon: "P" },
                                    { name: "Paytm", bg: "bg-blue", icon: "₹" },
                                    { name: "Zerodha", bg: "bg-orange-500", icon: "Z" },
                                    { name: "Groww", bg: "bg-money-green", icon: "G" },
                                    { name: "HDFC", bg: "bg-blue", icon: "H" },
                                    { name: "SBI", bg: "bg-blue", icon: "S" },
                                    { name: "+15", bg: "bg-surface-elevated", icon: "..." },
                                ].map((app, i) => (
                                    <div
                                        key={i}
                                        className={`w-10 h-10 ${app.bg} rounded-xl flex items-center justify-center text-white font-bold text-sm shadow-lg`}
                                        title={app.name}
                                    >
                                        {app.icon}
                                    </div>
                                ))}
                            </div>

                            <div className="flex flex-wrap items-center gap-4 mb-8">
                                <Link href="/signup" className="btn-primary px-8 py-4 rounded-2xl font-bold text-lg group">
                                    <span className="flex items-center gap-3">
                                        Connect Your Accounts
                                        <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
                                    </span>
                                </Link>
                            </div>

                            <div className="flex items-center gap-6 text-text-tertiary text-sm">
                                <div className="flex items-center gap-2">
                                    <Shield className="w-4 h-4 text-money-green" />
                                    <span>Read-only access</span>
                                </div>
                                <div className="flex items-center gap-2">
                                    <Eye className="w-4 h-4 text-wealth-purple" />
                                    <span>No transaction access</span>
                                </div>
                            </div>
                        </div>

                        {/* Right - Phone Mockup Style Dashboard */}
                        <div className="relative flex justify-center">
                            <div className="absolute inset-0 bg-gradient-to-r from-wealth-purple/20 to-money-green/20 blur-3xl rounded-full"></div>

                            {/* Phone Frame */}
                            <div className="relative w-[320px] h-[640px] bg-bg-dark rounded-[40px] p-3 border-4 border-surface-elevated shadow-2xl">
                                <div className="w-full h-full bg-surface rounded-[32px] overflow-hidden">
                                    {/* Status Bar */}
                                    <div className="flex items-center justify-between px-6 py-3 bg-bg-dark">
                                        <span className="text-xs text-text-secondary">9:41</span>
                                        <div className="w-20 h-5 bg-black rounded-full"></div>
                                        <div className="flex items-center gap-1">
                                            <div className="w-4 h-2 bg-money-green rounded-sm"></div>
                                        </div>
                                    </div>

                                    {/* App Content */}
                                    <div className="p-4 space-y-4">
                                        {/* Net Worth Card */}
                                        <div className="glass-card rounded-2xl p-4">
                                            <div className="flex items-center justify-between mb-2">
                                                <span className="text-xs text-text-secondary">Total Net Worth</span>
                                                <Eye className="w-4 h-4 text-text-tertiary" />
                                            </div>
                                            <div className="flex items-end gap-2">
                                                <span className="text-2xl font-bold gradient-text">₹12,34,567</span>
                                                <span className="text-money-green text-xs flex items-center mb-1">
                                                    <ArrowUpRight className="w-3 h-3" /> 2.4%
                                                </span>
                                            </div>
                                        </div>

                                        {/* Quick Stats */}
                                        <div className="grid grid-cols-2 gap-3">
                                            <div className="glass-card rounded-xl p-3">
                                                <Landmark className="w-4 h-4 text-blue mb-1" />
                                                <div className="text-xs text-text-secondary">Banks</div>
                                                <div className="text-sm font-semibold">₹4.2L</div>
                                            </div>
                                            <div className="glass-card rounded-xl p-3">
                                                <Smartphone className="w-4 h-4 text-wealth-purple mb-1" />
                                                <div className="text-xs text-text-secondary">Wallets</div>
                                                <div className="text-sm font-semibold">₹12,450</div>
                                            </div>
                                            <div className="glass-card rounded-xl p-3">
                                                <LineChart className="w-4 h-4 text-money-green mb-1" />
                                                <div className="text-xs text-text-secondary">Stocks</div>
                                                <div className="text-sm font-semibold">₹6.8L</div>
                                            </div>
                                            <div className="glass-card rounded-xl p-3">
                                                <Bitcoin className="w-4 h-4 text-gold mb-1" />
                                                <div className="text-xs text-text-secondary">Crypto</div>
                                                <div className="text-sm font-semibold">₹1.2L</div>
                                            </div>
                                        </div>

                                        {/* Recent Transactions */}
                                        <div className="glass-card rounded-2xl p-4">
                                            <div className="flex items-center justify-between mb-3">
                                                <span className="text-xs font-medium">Recent Activity</span>
                                                <ChevronRight className="w-4 h-4 text-text-tertiary" />
                                            </div>
                                            <div className="space-y-3">
                                                {[
                                                    { name: "Swiggy", amount: "-₹249", icon: Store, color: "text-alert-red" },
                                                    { name: "Salary Credit", amount: "+₹85,000", icon: Banknote, color: "text-money-green" },
                                                    { name: "Netflix", amount: "-₹649", icon: Receipt, color: "text-alert-red" },
                                                ].map((txn, i) => (
                                                    <div key={i} className="flex items-center justify-between">
                                                        <div className="flex items-center gap-2">
                                                            <div className="w-8 h-8 bg-surface-elevated rounded-lg flex items-center justify-center">
                                                                <txn.icon className="w-4 h-4 text-text-secondary" />
                                                            </div>
                                                            <span className="text-xs">{txn.name}</span>
                                                        </div>
                                                        <span className={`text-xs font-semibold ${txn.color}`}>{txn.amount}</span>
                                                    </div>
                                                ))}
                                            </div>
                                        </div>

                                        {/* AI Alert */}
                                        <div className="gradient-border rounded-xl p-3 bg-wealth-purple/5">
                                            <div className="flex items-center gap-2">
                                                <Sparkles className="w-4 h-4 text-wealth-purple" />
                                                <span className="text-xs">AI: Your runway is 4.2 months</span>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            {/* Floating Notification */}
                            <div className="absolute -top-2 -right-2 glass-card rounded-xl p-3 shadow-xl animate-bounce" style={{ animationDuration: '3s' }}>
                                <div className="flex items-center gap-2">
                                    <AlertCircle className="w-5 h-5 text-gold" />
                                    <span className="text-xs">EMI due in 3 days</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            {/* What We Connect Section */}
            <section id="connections" className="py-20 relative">
                <div className="max-w-7xl mx-auto px-6">
                    <div className="text-center mb-12">
                        <span className="inline-block px-4 py-2 glass rounded-full text-sm text-money-green font-medium mb-4">
                            🔗 Connect Everything
                        </span>
                        <h2 className="text-3xl md:text-4xl font-bold text-text-primary mb-4">
                            One app. <span className="gradient-text">Every account.</span>
                        </h2>
                        <p className="text-text-secondary max-w-2xl mx-auto">
                            Payfolio connects to all your financial accounts — banks, UPI, investments, and more.
                        </p>
                    </div>

                    <div className="grid md:grid-cols-3 lg:grid-cols-4 gap-4 stagger-children">
                        {[
                            { category: "UPI Wallets", items: ["Google Pay", "PhonePe", "Paytm", "Amazon Pay"], icon: Smartphone, color: "from-wealth-purple to-blue" },
                            { category: "Bank Accounts", items: ["SBI", "HDFC", "ICICI", "Axis", "Kotak"], icon: Landmark, color: "from-blue to-blue/50" },
                            { category: "Investments", items: ["Zerodha", "Groww", "Upstox", "Angel One"], icon: LineChart, color: "from-money-green to-money-green/50" },
                            { category: "Crypto", items: ["CoinDCX", "WazirX", "Binance"], icon: Bitcoin, color: "from-gold to-gold/50" },
                            { category: "Credit Cards", items: ["Any Visa/MC card", "AMEX", "Rupay"], icon: CreditCard, color: "from-alert-red to-alert-red/50" },
                            { category: "Business", items: ["Razorpay", "Stripe", "PayU"], icon: Store, color: "from-blue to-wealth-purple" },
                            { category: "Loans & EMIs", items: ["Home Loan", "Car Loan", "BNPL"], icon: Receipt, color: "from-alert-red to-gold" },
                            { category: "Subscriptions", items: ["Netflix", "Spotify", "AWS", "SaaS"], icon: RefreshCw, color: "from-wealth-purple to-money-green" },
                        ].map((cat, i) => (
                            <div key={i} className="glass-card rounded-2xl p-5 group">
                                <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${cat.color} flex items-center justify-center mb-4 group-hover:scale-110 transition-transform`}>
                                    <cat.icon className="w-6 h-6 text-white" />
                                </div>
                                <h3 className="font-semibold text-text-primary mb-2">{cat.category}</h3>
                                <div className="space-y-1">
                                    {cat.items.slice(0, 3).map((item, j) => (
                                        <div key={j} className="text-xs text-text-secondary">{item}</div>
                                    ))}
                                    {cat.items.length > 3 && (
                                        <div className="text-xs text-wealth-purple">+{cat.items.length - 3} more</div>
                                    )}
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </section>

            {/* What You See Section */}
            <section className="py-20 bg-surface/50 relative">
                <div className="max-w-7xl mx-auto px-6">
                    <div className="text-center mb-12">
                        <span className="inline-block px-4 py-2 glass rounded-full text-sm text-wealth-purple font-medium mb-4">
                            📊 Real-Time Insights
                        </span>
                        <h2 className="text-3xl md:text-4xl font-bold text-text-primary mb-4">
                            See what your money is <span className="gradient-text">actually doing</span>
                        </h2>
                    </div>

                    <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
                        {[
                            { title: "Net Worth", desc: "Your complete financial picture in one number", icon: IndianRupee, value: "₹12,34,567" },
                            { title: "Cash Runway", desc: "How long your money will last at current burn", icon: Zap, value: "4.2 months" },
                            { title: "Monthly Burn", desc: "Track spending across all accounts", icon: ArrowDownRight, value: "₹1,24,500" },
                            { title: "Income Sources", desc: "Salary + freelance + investments", icon: ArrowUpRight, value: "5 sources" },
                            { title: "EMI & Loans", desc: "All liabilities in one view", icon: Receipt, value: "₹42,000/mo" },
                            { title: "Investment P&L", desc: "Stocks, crypto, mutual funds", icon: TrendingUp, value: "+12.4%" },
                        ].map((item, i) => (
                            <div key={i} className="glass-card rounded-2xl p-6 group">
                                <div className="flex items-start justify-between mb-4">
                                    <div className="w-12 h-12 rounded-xl bg-wealth-purple/10 flex items-center justify-center group-hover:scale-110 transition-transform">
                                        <item.icon className="w-6 h-6 text-wealth-purple" />
                                    </div>
                                    <span className="text-lg font-bold text-money-green">{item.value}</span>
                                </div>
                                <h3 className="font-semibold text-text-primary mb-1">{item.title}</h3>
                                <p className="text-sm text-text-secondary">{item.desc}</p>
                            </div>
                        ))}
                    </div>
                </div>
            </section>

            {/* Who Is This For */}
            <section className="py-20 relative">
                <div className="max-w-7xl mx-auto px-6">
                    <div className="text-center mb-12">
                        <h2 className="text-3xl md:text-4xl font-bold text-text-primary mb-4">
                            Built for people who <span className="gradient-text">care about money</span>
                        </h2>
                    </div>

                    <div className="grid md:grid-cols-4 gap-6">
                        {[
                            { title: "Startup Founders", desc: "Track runway, cash flow, salary vs equity", emoji: "🚀" },
                            { title: "Freelancers", desc: "Multiple income sources + tax tracking", emoji: "💻" },
                            { title: "Traders & Investors", desc: "Stocks, crypto, MFs in one portfolio", emoji: "📈" },
                            { title: "Working Professionals", desc: "Salary, EMIs, investments, expenses", emoji: "💼" },
                        ].map((persona, i) => (
                            <div key={i} className="glass-card rounded-2xl p-6 text-center group">
                                <div className="text-4xl mb-4">{persona.emoji}</div>
                                <h3 className="font-semibold text-text-primary mb-2">{persona.title}</h3>
                                <p className="text-sm text-text-secondary">{persona.desc}</p>
                            </div>
                        ))}
                    </div>
                </div>
            </section>

            {/* CTA Section */}
            <section className="py-20 relative">
                <div className="max-w-4xl mx-auto px-6 text-center">
                    <div className="glass-card rounded-3xl p-12 relative overflow-hidden">
                        <div className="absolute inset-0 bg-gradient-to-br from-wealth-purple/20 via-transparent to-money-green/20"></div>

                        <div className="relative z-10">
                            <h2 className="text-3xl md:text-4xl font-bold text-text-primary mb-4">
                                Stop checking <span className="gradient-text">5 different apps</span>
                            </h2>
                            <p className="text-lg text-text-secondary mb-8 max-w-xl mx-auto">
                                Connect all your accounts in 2 minutes. See your complete financial reality.
                            </p>
                            <Link href="/signup" className="btn-primary inline-flex items-center gap-3 px-10 py-5 rounded-2xl font-bold text-lg">
                                <span className="flex items-center gap-3">
                                    Get Started Free
                                    <ArrowRight className="w-5 h-5" />
                                </span>
                            </Link>
                            <p className="text-xs text-text-tertiary mt-4">No credit card required • Read-only access only</p>
                        </div>
                    </div>
                </div>
            </section>

            {/* Footer */}
            <footer className="py-12 glass border-t border-border-subtle/50">
                <div className="max-w-7xl mx-auto px-6">
                    <div className="flex flex-col md:flex-row items-center justify-between gap-6">
                        <div className="flex items-center gap-3">
                            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-wealth-purple to-money-green flex items-center justify-center">
                                <IndianRupee className="w-5 h-5 text-white" />
                            </div>
                            <span className="text-lg font-bold">Payfolio</span>
                        </div>

                        <div className="text-text-tertiary text-sm">
                            © 2026 RKO Labs. Your financial brain, unified.
                        </div>
                    </div>
                </div>
            </footer>
        </main>
    );
}
