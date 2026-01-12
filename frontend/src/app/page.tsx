import Link from "next/link";
import { ArrowRight, TrendingUp, Shield, Zap, BarChart3, Wallet, PieChart, Bell, Sparkles, ChevronRight, Star, Users, Globe } from "lucide-react";

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
                        <div className="relative w-10 h-10 rounded-xl bg-gradient-to-br from-wealth-purple via-blue to-money-green p-0.5 group-hover:glow-purple transition-all duration-300">
                            <div className="w-full h-full rounded-xl bg-bg-dark flex items-center justify-center">
                                <span className="text-white font-bold text-lg gradient-text">P</span>
                            </div>
                        </div>
                        <span className="text-xl font-bold text-text-primary">Payfolio</span>
                    </Link>

                    <div className="hidden md:flex items-center gap-8">
                        <Link href="#features" className="text-text-secondary hover:text-text-primary transition-colors">Features</Link>
                        <Link href="#how-it-works" className="text-text-secondary hover:text-text-primary transition-colors">How it Works</Link>
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

            {/* Hero Section */}
            <section className="relative pt-32 pb-20 overflow-hidden">
                <div className="max-w-7xl mx-auto px-6">
                    <div className="grid lg:grid-cols-2 gap-12 items-center">
                        {/* Left Content */}
                        <div className="stagger-children">
                            {/* Badge */}
                            <div className="inline-flex items-center gap-2 px-4 py-2 glass rounded-full mb-8">
                                <span className="relative flex h-2 w-2">
                                    <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-money-green opacity-75"></span>
                                    <span className="relative inline-flex rounded-full h-2 w-2 bg-money-green"></span>
                                </span>
                                <span className="text-sm text-text-secondary">Your financial brain, unified</span>
                                <Sparkles className="w-4 h-4 text-gold" />
                            </div>

                            {/* Headline */}
                            <h1 className="text-5xl md:text-6xl lg:text-7xl font-extrabold text-text-primary mb-6 leading-[1.1]">
                                See your complete
                                <span className="block gradient-text">
                                    financial reality
                                </span>
                            </h1>

                            {/* Subheadline */}
                            <p className="text-xl text-text-secondary mb-10 max-w-xl leading-relaxed">
                                Payfolio connects all your banks, wallets, investments, and liabilities
                                into one real-time dashboard with <span className="text-wealth-purple font-semibold">AI-powered insights</span>.
                            </p>

                            {/* CTA Buttons */}
                            <div className="flex flex-wrap items-center gap-4 mb-12">
                                <Link href="/signup" className="btn-primary px-8 py-4 rounded-2xl font-bold text-lg group">
                                    <span className="flex items-center gap-3">
                                        Start Free Trial
                                        <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
                                    </span>
                                </Link>
                                <Link href="#demo" className="glass-card px-8 py-4 rounded-2xl font-semibold text-lg flex items-center gap-3 hover:border-wealth-purple/50">
                                    <div className="w-10 h-10 rounded-full bg-wealth-purple/20 flex items-center justify-center">
                                        <div className="w-0 h-0 border-l-8 border-l-wealth-purple border-t-4 border-t-transparent border-b-4 border-b-transparent ml-1"></div>
                                    </div>
                                    Watch Demo
                                </Link>
                            </div>

                            {/* Trust Badges */}
                            <div className="flex items-center gap-6 text-text-tertiary">
                                <div className="flex items-center gap-2">
                                    <Shield className="w-5 h-5 text-money-green" />
                                    <span className="text-sm">Bank-grade security</span>
                                </div>
                                <div className="flex items-center gap-2">
                                    <Users className="w-5 h-5 text-wealth-purple" />
                                    <span className="text-sm">10K+ users</span>
                                </div>
                            </div>
                        </div>

                        {/* Right - Dashboard Preview */}
                        <div className="relative">
                            {/* Glow Effect */}
                            <div className="absolute inset-0 bg-gradient-to-r from-wealth-purple/30 to-money-green/30 blur-3xl rounded-full"></div>

                            {/* Main Card */}
                            <div className="relative glass-card rounded-3xl p-8 shimmer">
                                {/* Net Worth Header */}
                                <div className="mb-8">
                                    <p className="text-text-secondary text-sm mb-2">Total Net Worth</p>
                                    <div className="flex items-end gap-4">
                                        <span className="text-4xl md:text-5xl font-bold gradient-text counter">₹1,23,45,678</span>
                                        <span className="flex items-center gap-1 text-money-green text-lg font-semibold mb-2">
                                            <TrendingUp className="w-5 h-5" />
                                            +12.4%
                                        </span>
                                    </div>
                                </div>

                                {/* Mini Cards */}
                                <div className="grid grid-cols-2 gap-4 mb-6">
                                    {[
                                        { label: "Cash", value: "₹18.5L", color: "from-blue to-blue/50", icon: Wallet },
                                        { label: "Investments", value: "₹89.2L", color: "from-wealth-purple to-wealth-purple/50", icon: TrendingUp },
                                        { label: "Crypto", value: "₹12.0L", color: "from-gold to-gold/50", icon: Globe },
                                        { label: "Liabilities", value: "-₹8.4L", color: "from-alert-red to-alert-red/50", icon: PieChart },
                                    ].map((item, i) => (
                                        <div key={i} className="glass-card rounded-xl p-4 group cursor-pointer">
                                            <div className="flex items-center gap-2 mb-2">
                                                <div className={`w-8 h-8 rounded-lg bg-gradient-to-br ${item.color} flex items-center justify-center`}>
                                                    <item.icon className="w-4 h-4 text-white" />
                                                </div>
                                                <span className="text-text-secondary text-sm">{item.label}</span>
                                            </div>
                                            <span className={`text-xl font-bold ${item.label === "Liabilities" ? "text-alert-red" : "text-text-primary"}`}>
                                                {item.value}
                                            </span>
                                        </div>
                                    ))}
                                </div>

                                {/* AI Insight */}
                                <div className="gradient-border rounded-xl p-4 bg-wealth-purple/5">
                                    <div className="flex items-start gap-3">
                                        <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-wealth-purple to-blue flex items-center justify-center flex-shrink-0 pulse-ring">
                                            <Sparkles className="w-5 h-5 text-white" />
                                        </div>
                                        <div>
                                            <p className="text-sm font-medium text-wealth-purple mb-1">AI Insight</p>
                                            <p className="text-text-secondary text-sm">Your cash runway is 4.2 months based on spending patterns.</p>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            {/* Floating Elements */}
                            <div className="absolute -top-4 -right-4 glass-card rounded-xl p-3 animate-bounce" style={{ animationDuration: '3s' }}>
                                <Bell className="w-6 h-6 text-gold" />
                                <span className="absolute -top-1 -right-1 w-3 h-3 bg-alert-red rounded-full"></span>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            {/* Stats Section */}
            <section className="py-16 relative">
                <div className="max-w-7xl mx-auto px-6">
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-6 stagger-children">
                        {[
                            { value: "₹500Cr+", label: "Assets Tracked", color: "text-money-green" },
                            { value: "25K+", label: "Active Users", color: "text-wealth-purple" },
                            { value: "50+", label: "Integrations", color: "text-blue" },
                            { value: "99.9%", label: "Uptime", color: "text-gold" },
                        ].map((stat, i) => (
                            <div key={i} className="glass-card rounded-2xl p-6 text-center tilt-card">
                                <div className={`text-3xl md:text-4xl font-bold ${stat.color} counter mb-2`}>{stat.value}</div>
                                <div className="text-text-secondary">{stat.label}</div>
                            </div>
                        ))}
                    </div>
                </div>
            </section>

            {/* Features Section */}
            <section id="features" className="py-24 relative">
                <div className="max-w-7xl mx-auto px-6">
                    <div className="text-center mb-16 stagger-children">
                        <span className="inline-block px-4 py-2 glass rounded-full text-sm text-wealth-purple font-medium mb-4">
                            ✨ Powerful Features
                        </span>
                        <h2 className="text-4xl md:text-5xl font-bold text-text-primary mb-6">
                            Everything you need in <span className="gradient-text">one place</span>
                        </h2>
                        <p className="text-xl text-text-secondary max-w-2xl mx-auto">
                            Stop juggling between apps. Payfolio brings your entire financial life together with intelligent insights.
                        </p>
                    </div>

                    <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 stagger-children">
                        {[
                            { icon: BarChart3, title: "Unified Dashboard", desc: "All accounts, investments, and liabilities in one beautiful view", color: "from-blue to-blue/50" },
                            { icon: Sparkles, title: "AI-Powered Insights", desc: "Get smart recommendations and alerts based on your spending", color: "from-wealth-purple to-wealth-purple/50" },
                            { icon: Shield, title: "Bank-Grade Security", desc: "256-bit encryption with read-only access to your accounts", color: "from-money-green to-money-green/50" },
                            { icon: Zap, title: "Real-Time Sync", desc: "Always up-to-date data across all your financial accounts", color: "from-gold to-gold/50" },
                            { icon: PieChart, title: "Smart Categorization", desc: "Auto-categorize transactions with machine learning", color: "from-alert-red to-alert-red/50" },
                            { icon: Bell, title: "Custom Alerts", desc: "Get notified about large transactions and bill reminders", color: "from-blue to-wealth-purple" },
                        ].map((feature, i) => (
                            <div key={i} className="glass-card rounded-2xl p-6 group cursor-pointer">
                                <div className={`w-14 h-14 rounded-2xl bg-gradient-to-br ${feature.color} flex items-center justify-center mb-5 group-hover:scale-110 transition-transform`}>
                                    <feature.icon className="w-7 h-7 text-white" />
                                </div>
                                <h3 className="text-xl font-bold text-text-primary mb-3">{feature.title}</h3>
                                <p className="text-text-secondary leading-relaxed">{feature.desc}</p>
                            </div>
                        ))}
                    </div>
                </div>
            </section>

            {/* How it Works */}
            <section id="how-it-works" className="py-24 relative">
                <div className="max-w-7xl mx-auto px-6">
                    <div className="text-center mb-16">
                        <span className="inline-block px-4 py-2 glass rounded-full text-sm text-money-green font-medium mb-4">
                            🚀 Get Started in Minutes
                        </span>
                        <h2 className="text-4xl md:text-5xl font-bold text-text-primary mb-6">
                            How it <span className="gradient-text">works</span>
                        </h2>
                    </div>

                    <div className="grid md:grid-cols-3 gap-8">
                        {[
                            { step: "01", title: "Connect Accounts", desc: "Securely link your bank accounts, investments, and wallets" },
                            { step: "02", title: "See Your Portfolio", desc: "Get a unified view of your complete financial picture" },
                            { step: "03", title: "Get AI Insights", desc: "Receive personalized recommendations to grow your wealth" },
                        ].map((item, i) => (
                            <div key={i} className="relative">
                                <div className="glass-card rounded-2xl p-8 text-center group">
                                    <div className="text-6xl font-bold gradient-text mb-4 group-hover:scale-110 transition-transform">{item.step}</div>
                                    <h3 className="text-xl font-bold text-text-primary mb-3">{item.title}</h3>
                                    <p className="text-text-secondary">{item.desc}</p>
                                </div>
                                {i < 2 && (
                                    <ChevronRight className="hidden md:block absolute top-1/2 -right-4 w-8 h-8 text-border-subtle" />
                                )}
                            </div>
                        ))}
                    </div>
                </div>
            </section>

            {/* Testimonials */}
            <section className="py-24 relative">
                <div className="max-w-7xl mx-auto px-6">
                    <div className="text-center mb-16">
                        <span className="inline-block px-4 py-2 glass rounded-full text-sm text-gold font-medium mb-4">
                            ⭐ Loved by Users
                        </span>
                        <h2 className="text-4xl md:text-5xl font-bold text-text-primary">
                            What our users <span className="gradient-text">say</span>
                        </h2>
                    </div>

                    <div className="grid md:grid-cols-3 gap-6">
                        {[
                            { name: "Priya Sharma", role: "Startup Founder", text: "Finally, I can see my runway without opening 5 different apps. Payfolio is a game-changer!" },
                            { name: "Rahul Verma", role: "Freelance Developer", text: "Tracking income from multiple clients was a nightmare. Now it's all in one beautiful dashboard." },
                            { name: "Anita Patel", role: "Investment Banker", text: "The AI insights caught a subscription I forgot about. Saved me ₹12K/year!" },
                        ].map((testimonial, i) => (
                            <div key={i} className="glass-card rounded-2xl p-6">
                                <div className="flex gap-1 mb-4">
                                    {[...Array(5)].map((_, j) => (
                                        <Star key={j} className="w-5 h-5 text-gold fill-gold" />
                                    ))}
                                </div>
                                <p className="text-text-secondary mb-6 leading-relaxed">"{testimonial.text}"</p>
                                <div className="flex items-center gap-3">
                                    <div className="w-10 h-10 rounded-full bg-gradient-to-br from-wealth-purple to-blue flex items-center justify-center">
                                        <span className="text-white font-bold">{testimonial.name[0]}</span>
                                    </div>
                                    <div>
                                        <div className="font-semibold text-text-primary">{testimonial.name}</div>
                                        <div className="text-sm text-text-secondary">{testimonial.role}</div>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </section>

            {/* CTA Section */}
            <section className="py-24 relative">
                <div className="max-w-4xl mx-auto px-6 text-center">
                    <div className="glass-card rounded-3xl p-12 relative overflow-hidden">
                        {/* Background Glow */}
                        <div className="absolute inset-0 bg-gradient-to-br from-wealth-purple/20 via-transparent to-money-green/20"></div>

                        <div className="relative z-10">
                            <h2 className="text-4xl md:text-5xl font-bold text-text-primary mb-6">
                                Ready to see your true <span className="gradient-text">financial picture</span>?
                            </h2>
                            <p className="text-xl text-text-secondary mb-10 max-w-2xl mx-auto">
                                Join thousands of smart users who trust Payfolio to manage their finances.
                            </p>
                            <Link href="/signup" className="btn-primary inline-flex items-center gap-3 px-10 py-5 rounded-2xl font-bold text-xl">
                                <span className="flex items-center gap-3">
                                    Start Free — No Credit Card
                                    <ArrowRight className="w-6 h-6" />
                                </span>
                            </Link>
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
                                <span className="text-white font-bold">P</span>
                            </div>
                            <span className="text-lg font-bold">Payfolio</span>
                        </div>

                        <div className="flex items-center gap-8 text-text-secondary">
                            <Link href="#" className="hover:text-text-primary transition-colors">Privacy</Link>
                            <Link href="#" className="hover:text-text-primary transition-colors">Terms</Link>
                            <Link href="#" className="hover:text-text-primary transition-colors">Contact</Link>
                        </div>

                        <div className="text-text-tertiary text-sm">
                            © 2026 RKO Labs. All rights reserved.
                        </div>
                    </div>
                </div>
            </footer>
        </main>
    );
}
