// api.js - Centralized API Service for Talk & Earn Web Client

class ApiService {
    constructor() {
        this.LOCAL_IP = window.TALK_EARN_HOST || window.location.hostname || "127.0.0.1";
        this.isMobile = /Android|iPhone|iPad/i.test(navigator.userAgent) || window.location.hostname !== "127.0.0.1";
        this.API_BASE = this.isMobile ? `http://${this.LOCAL_IP}:8000` : "http://127.0.0.1:8000";
        this.WS_BASE = this.isMobile ? `ws://${this.LOCAL_IP}:8000` : "ws://127.0.0.1:8000";
    }

    getToken() {
        return window.currentToken || localStorage.getItem('talk_earn_token');
    }

    getHeaders(isAuth = true, isFormData = false) {
        const headers = {};
        if (!isFormData) {
            headers['Content-Type'] = 'application/json';
        }
        if (isAuth) {
            const token = this.getToken();
            if (token) headers['Authorization'] = `Bearer ${token}`;
        }
        return headers;
    }

    // --- AUTHENTICATION ---

    async register(email, password, gender) {
        return fetch(`${this.API_BASE}/auth/register`, {
            method: 'POST',
            headers: this.getHeaders(false),
            body: JSON.stringify({ email, password, gender })
        });
    }

    async login(username, password) {
        return fetch(`${this.API_BASE}/auth/token`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: `username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`
        });
    }

    async verifyEmail(email, otp_code) {
        return fetch(`${this.API_BASE}/auth/verify-email`, {
            method: 'POST',
            headers: this.getHeaders(false),
            body: JSON.stringify({ email, otp_code })
        });
    }

    // --- PROFILE ---

    async getProfile() {
        return fetch(`${this.API_BASE}/profile/me`, {
            headers: this.getHeaders()
        });
    }

    async updateProfile(data) {
        return fetch(`${this.API_BASE}/profile/`, {
            method: 'PUT',
            headers: this.getHeaders(),
            body: JSON.stringify(data)
        });
    }

    async uploadProfilePicture(formData) {
        return fetch(`${this.API_BASE}/profile/picture/upload`, {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${this.getToken()}` }, // No Content-Type header so browser boundary is added
            body: formData
        });
    }

    async changePassword(current_password, new_password) {
        return fetch(`${this.API_BASE}/profile/password`, {
            method: 'PUT',
            headers: this.getHeaders(),
            body: JSON.stringify({ current_password, new_password })
        });
    }

    async deleteAccount(current_password) {
        return fetch(`${this.API_BASE}/profile/account/delete`, {
            method: 'POST',
            headers: this.getHeaders(),
            body: JSON.stringify({ current_password })
        });
    }

    // --- WALLET ---

    async getWalletBalance() {
        return fetch(`${this.API_BASE}/wallet/balance`, {
            headers: this.getHeaders()
        });
    }

    async earnCoins(medium, minutes) {
        return fetch(`${this.API_BASE}/wallet/earn`, {
            method: 'POST',
            headers: this.getHeaders(),
            body: JSON.stringify({ medium, minutes })
        });
    }

    async withdrawCoins(payout_provider, amount) {
        return fetch(`${this.API_BASE}/wallet/withdraw`, {
            method: 'POST',
            headers: this.getHeaders(),
            body: JSON.stringify({ payout_provider, amount })
        });
    }

    // --- MATCHMAKING ---

    async requestRandomMatch(medium) {
        return fetch(`${this.API_BASE}/match/random`, {
            method: 'POST',
            headers: this.getHeaders(),
            body: JSON.stringify({ medium })
        });
    }

    async cancelMatch() {
        return fetch(`${this.API_BASE}/match/cancel`, {
            method: 'POST',
            headers: this.getHeaders()
        });
    }
}

// Global Singleton
window.apiService = new ApiService();
