const API_BASE = "/api/v1";

interface RequestOptions {
    method?: string;
    body?: any;
    headers?: Record<string, string>;
}

class ApiClient {
    private getToken(): string | null {
        if (typeof window === "undefined") return null;
        return localStorage.getItem("access_token");
    }

    async request<T>(endpoint: string, options: RequestOptions = {}): Promise<T> {
        const token = this.getToken();

        const headers: Record<string, string> = {
            "Content-Type": "application/json",
            ...options.headers,
        };

        if (token) {
            headers["Authorization"] = `Bearer ${token}`;
        }

        const res = await fetch(`${API_BASE}${endpoint}`, {
            method: options.method || "GET",
            headers,
            body: options.body ? JSON.stringify(options.body) : undefined,
        });

        if (!res.ok) {
            const error = await res.json().catch(() => ({ detail: "Request failed" }));
            throw new Error(error.detail || `HTTP ${res.status}`);
        }

        return res.json();
    }

    // Auth
    async login(email: string, password: string) {
        return this.request("/auth/login", {
            method: "POST",
            body: { email, password },
        });
    }

    async register(email: string, password: string, full_name?: string) {
        return this.request("/auth/register", {
            method: "POST",
            body: { email, password, full_name },
        });
    }

    // Portfolio
    async getPortfolio() {
        return this.request("/users/me/portfolio");
    }

    // Accounts
    async getAccounts() {
        return this.request("/accounts");
    }

    async createAccount(data: any) {
        return this.request("/accounts", { method: "POST", body: data });
    }

    async updateAccount(id: string, data: any) {
        return this.request(`/accounts/${id}`, { method: "PATCH", body: data });
    }

    async deleteAccount(id: string) {
        return this.request(`/accounts/${id}`, { method: "DELETE" });
    }

    // Transactions
    async getTransactions(params?: Record<string, string>) {
        const query = params ? `?${new URLSearchParams(params)}` : "";
        return this.request(`/transactions${query}`);
    }

    async getTransactionStats(from: string, to: string) {
        return this.request(`/transactions/stats/summary?date_from=${from}&date_to=${to}`);
    }

    // Assets
    async getAssets() {
        return this.request("/assets");
    }

    async createAsset(data: any) {
        return this.request("/assets", { method: "POST", body: data });
    }

    // Liabilities
    async getLiabilities() {
        return this.request("/liabilities");
    }

    async createLiability(data: any) {
        return this.request("/liabilities", { method: "POST", body: data });
    }

    // Insights
    async getInsights() {
        return this.request("/insights");
    }

    async generateInsights() {
        return this.request("/insights/generate", { method: "POST" });
    }

    // Billing
    async getSubscription() {
        return this.request("/billing/subscription");
    }

    async createCheckout(plan: string, billing_cycle: string = "monthly") {
        return this.request("/billing/checkout", {
            method: "POST",
            body: { plan, billing_cycle, provider: "stripe" },
        });
    }
}

export const api = new ApiClient();
