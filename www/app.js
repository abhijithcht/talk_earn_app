// CONFIG
// Set window.TALK_EARN_HOST before loading this script to override (e.g. from Flutter or build tool).
// Falls back to the current browser hostname (works for both local dev and production).





// STATE
function showError(element, message) {
    if (typeof message === 'object') {
        if (Array.isArray(message)) {
            message = message.map(err => err.msg || JSON.stringify(err)).join(', ');
        } else {
            message = JSON.stringify(message);
        }
    }
    element.innerText = message;
    element.style.display = 'block';
    element.classList.remove('error-animate');
    void element.offsetWidth; // trigger reflow to restart animation
    element.classList.add('error-animate');
}
let currentToken = null;
let currentUserId = null;
let currentUserName = null;
let ws = null;
let peerConnection = null;
let localStream = null;
let isMatching = false;
let matchedUserId = null;
let currentMedium = null;
let earningInterval = null;

// WEBRTC CONFIG
const rtcConfig = {
    iceServers: [{ urls: "stun:stun.l.google.com:19302" }]
};

// UI ELEMENTS
const landingView = document.getElementById('landing-view');
const authView = document.getElementById('auth-view');
const dashboardView = document.getElementById('dashboard-view');
const authForm = document.getElementById('auth-form');
const authBtnText = document.querySelector('#auth-btn .btn-text');
const genderGroup = document.getElementById('gender-group');
const authToggle = document.getElementById('auth-toggle');
const authSwitchText = document.getElementById('auth-switch-text');
const authError = document.getElementById('auth-error');
const authTitle = document.getElementById('auth-title');
const authSubtitle = document.getElementById('auth-subtitle');
const loader = document.querySelector('.loader');

// OTP ELEMENTS
const authContainer = document.getElementById('auth-container');
const otpContainer = document.getElementById('otp-container');
const otpForm = document.getElementById('otp-form');
const otpError = document.getElementById('otp-error');
const otpBtnText = document.querySelector('#otp-btn .btn-text');
const otpLoader = document.getElementById('otp-loader');

let pendingEmail = null;
let pendingPassword = null;

const walletBalance = document.getElementById('wallet-balance');
const refreshWalletBtn = document.getElementById('refresh-wallet-btn');
const withdrawBtn = document.getElementById('withdraw-btn');
const walletMsg = document.getElementById('wallet-msg');
const savePrefBtn = document.getElementById('save-pref-btn');
const prefGender = document.getElementById('pref-gender');

const wsStatus = document.getElementById('ws-status');
const findTextBtn = document.getElementById('find-text-btn');
const findAudioBtn = document.getElementById('find-audio-btn');
const findVideoBtn = document.getElementById('find-video-btn');
const matchControls = document.getElementById('match-controls');
const endCallBtn = document.getElementById('end-call-btn');
const localVideo = document.getElementById('local-video');
const remoteVideo = document.getElementById('remote-video');
const radarUI = document.getElementById('radar-ui');
const videoUI = document.getElementById('video-ui');
const textChatUI = document.getElementById('text-chat-ui');
const messagesContainer = document.getElementById('messages-container');
const chatMessageInput = document.getElementById('chat-message-input');
const sendMsgBtn = document.getElementById('send-msg-btn');
const logsDiv = document.getElementById('logs');
const logoutBtn = document.getElementById('logout-btn');

const settingsBtn = document.getElementById('settings-btn');
const settingsModal = document.getElementById('settings-modal');
const closeSettingsBtn = document.getElementById('close-settings-btn');
const studioModal = document.getElementById('avatar-studio-modal');
const openStudioBtn = document.getElementById('avatar-studio-btn');
const closeStudioBtn = document.getElementById('close-studio-btn');
const renderTarget = document.getElementById('studio-avatar-render');
const headerAvatarTarget = document.getElementById('header-avatar-container');

const profileEditForm = document.getElementById('profile-edit-form');
const openStudioFromSettings = document.getElementById('open-studio-from-settings');
const triggerUploadBtn = document.getElementById('trigger-upload-btn');
const profileUploadInput = document.getElementById('profile-upload-input');
const uploadMsg = document.getElementById('upload-msg');
const passwordForm = document.getElementById('password-form');
const deleteAccountForm = document.getElementById('delete-account-form');
const saveAvatarBtn = document.getElementById('save-avatar-btn');

let preOfferAnswerFromUser;
let currentUserAvatar = localStorage.getItem('talk_avatar') || '👤';

// --- AUDIO SYNTHESIS SYSTEM ---
class SoundSystem {
    constructor() {
        this.ctx = null;
    }

    initContext() {
        if (!this.ctx) {
            this.ctx = new (window.AudioContext || window.webkitAudioContext)();
        }
    }

    playClick() {
        this.initContext();
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.connect(gain);
        gain.connect(this.ctx.destination);

        osc.type = 'sine';
        osc.frequency.setValueAtTime(600, this.ctx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(300, this.ctx.currentTime + 0.1);

        gain.gain.setValueAtTime(0.1, this.ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.01, this.ctx.currentTime + 0.1);

        osc.start();
        osc.stop(this.ctx.currentTime + 0.1);
    }

    playMatch() {
        this.initContext();
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.connect(gain);
        gain.connect(this.ctx.destination);

        osc.type = 'triangle';
        osc.frequency.setValueAtTime(440, this.ctx.currentTime);
        osc.frequency.setValueAtTime(659.25, this.ctx.currentTime + 0.1); // E5
        osc.frequency.setValueAtTime(880, this.ctx.currentTime + 0.2); // A5

        gain.gain.setValueAtTime(0.1, this.ctx.currentTime);
        gain.gain.linearRampToValueAtTime(0, this.ctx.currentTime + 0.5);

        osc.start();
        osc.stop(this.ctx.currentTime + 0.5);
    }

    playMessage() {
        this.initContext();
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.connect(gain);
        gain.connect(this.ctx.destination);

        osc.type = 'sine';
        osc.frequency.setValueAtTime(800, this.ctx.currentTime);
        osc.frequency.setValueAtTime(1200, this.ctx.currentTime + 0.05);

        gain.gain.setValueAtTime(0.05, this.ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.01, this.ctx.currentTime + 0.15);

        osc.start();
        osc.stop(this.ctx.currentTime + 0.15);
    }
}
const soundSys = new SoundSystem();

let isLoginMode = true;

// INIT
function init() {
    const savedToken = localStorage.getItem('talk_earn_token');

    // Attach click sound to all buttons
    document.querySelectorAll('.btn').forEach(btn => {
        btn.addEventListener('click', () => {
            if (soundSys.ctx && soundSys.ctx.state === 'suspended') soundSys.ctx.resume();
            soundSys.playClick();
        });
    });

    initAvatarSelector();

    if (savedToken) {
        currentToken = savedToken;
        loadDashboard();
    }
}

function showView(viewId, setLogin = true) {
    landingView.classList.remove('active');
    authView.classList.remove('active');
    dashboardView.classList.remove('active');

    setTimeout(() => {
        document.getElementById(viewId).classList.add('active');
        if (viewId === 'auth-view') {
            isLoginMode = !setLogin; // forces toggle below to correct state
            authToggle.click();
        }
    }, 400);
}

// TOGGLE AUTH MODE
authToggle.addEventListener('click', () => {
    isLoginMode = !isLoginMode;
    if (isLoginMode) {
        authTitle.innerText = "Welcome Back";
        authSubtitle.innerText = "Sign in to access your dashboard.";
        authBtnText.innerText = "Sign In";
        genderGroup.style.display = "none";
        authSwitchText.innerText = "Don't have an account?";
        authToggle.innerText = "Register";
    } else {
        authTitle.innerText = "Create Account";
        authSubtitle.innerText = "Join the global network today.";
        authBtnText.innerText = "Sign Up";
        genderGroup.style.display = "block";
        authSwitchText.innerText = "Already have an account?";
        authToggle.innerText = "Log in";
    }
    authError.style.display = "none";
});

// AUTH SUBMIT
authForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    authError.style.display = "none";
    setLoading(true);

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    try {
        if (!isLoginMode) {
            // Register
            const gender = document.getElementById('gender').value;
            const res = await window.apiService.register(email, password, gender);

            if (!res.ok) {
                const errData = await res.json();
                throw new Error(errData.detail || "Registration failed");
            }

            logToUI("Registration successful! OTP Sent.");
            pendingEmail = email;
            pendingPassword = password;
            authContainer.style.display = "none";
            otpContainer.style.display = "block";
            setLoading(false);
            return; // Exit here, wait for OTP submit
        }

        // Login (run immediately after register, or distinct)
        const resObj = await window.apiService.login(email, password);

        if (!resObj.ok) {
            const errData = await resObj.json();
            let errorMsg = "Invalid credentials";
            if (errData.detail) {
                if (Array.isArray(errData.detail)) {
                    errorMsg = errData.detail.map(e => e.msg).join(". ");
                } else {
                    errorMsg = errData.detail;
                }
            }
            throw new Error(errorMsg);
        }
        const data = await resObj.json();

        currentToken = data.access_token;
        localStorage.setItem('talk_earn_token', currentToken);

        loadDashboard();
    } catch (err) {
        showError(authError, err.message);
    } finally {
        setLoading(false);
    }
});

// OTP SUBMIT
otpForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    otpError.style.display = "none";
    otpBtnText.style.display = "none";
    otpLoader.style.display = "block";

    const otp_code = document.getElementById('otp-code').value;

    try {
        const res = await window.apiService.verifyEmail(pendingEmail, otp_code);

        if (!res.ok) {
            const err = await res.json();
            throw new Error(err.detail || "Verification failed");
        }

        // Auto-login via token
        const resObj = await window.apiService.login(pendingEmail, pendingPassword);

        if (!resObj.ok) throw new Error("Auto-login failed. Please refresh and try logging in.");
        const data = await resObj.json();

        currentToken = data.access_token;
        localStorage.setItem('talk_earn_token', currentToken);

        authContainer.style.display = "block";
        otpContainer.style.display = "none";

        loadDashboard();

    } catch (err) {
        showError(otpError, err.message);
    } finally {
        otpBtnText.style.display = "inline";
        otpLoader.style.display = "none";
    }
});

function setLoading(isLoading) {
    if (isLoading) {
        authBtnText.style.display = "none";
        loader.style.display = "block";
    } else {
        authBtnText.style.display = "inline";
        loader.style.display = "none";
    }
}

// AVATAR SELECTOR
function initAvatarSelector() {
    const options = document.querySelectorAll('.avatar-option');

    // Set initial active state based on localStorage
    options.forEach(opt => {
        if (opt.dataset.avatar === currentUserAvatar) {
            opt.classList.add('selected');
        } else {
            opt.classList.remove('selected');
        }

        opt.addEventListener('click', (e) => {
            if (soundSys.ctx) soundSys.playClick();

            options.forEach(o => o.classList.remove('selected'));
            e.target.classList.add('selected');

            currentUserAvatar = e.target.dataset.avatar;
            localStorage.setItem('talk_avatar', currentUserAvatar);
        });
    });
}

// LOAD DASHBOARD
async function loadDashboard() {
    authView.classList.remove('active');
    landingView.classList.remove('active');
    setTimeout(() => dashboardView.classList.add('active'), 400);

    // Parse JWT roughly to get user ID
    try {
        const payload = JSON.parse(atob(currentToken.split('.')[1]));
        currentUserId = parseInt(payload.sub);
        // We will fetch the actual username below, but for now we default to the ID
        logToUI(`Logged in as User #${currentUserId}`);
    } catch (e) { console.error(e); }

    await refreshWallet();
    connectWebSocket();
    connectGlobalWebSocket();
}

// WALLET & PREFERENCE
refreshWalletBtn.addEventListener('click', refreshWallet);
async function refreshWallet() {
    try {
        const meRes = await window.apiService.getProfile();
        const meData = await meRes.json();
        currentUserId = meData.id;
        currentUserName = meData.full_name || `User ${meData.id}`;

        // Load custom avatar if exists
        try {
            if (meData.profile_picture_url) {
                if (headerAvatarTarget) {
                    headerAvatarTarget.innerHTML = `<img src="${meData.profile_picture_url}" style="width: 100%; height: 100%; object-fit: cover;" />`;
                }
                currentUserAvatar = meData.profile_picture_url;
            } else if (meData.customizations) {
                const parsedState = JSON.parse(meData.customizations);
                currentAvatarState = { ...currentAvatarState, ...parsedState };
                currentUserAvatar = renderAvatarSVG(currentAvatarState);
                if (headerAvatarTarget) headerAvatarTarget.innerHTML = currentUserAvatar;
            } else {
                // If it's a first time user, parse their old emoji if they had one cached, or default
                const cachedEmoji = localStorage.getItem('talk_avatar');
                if (cachedEmoji && headerAvatarTarget) {
                    headerAvatarTarget.innerHTML = `<span style="font-size: 1.2rem;">${cachedEmoji}</span>`;
                    currentUserAvatar = cachedEmoji;
                }
            }
        } catch (e) { console.error("Avatar Parse Error", e); }

        const res = await window.apiService.getWalletBalance();
        if (res.ok) {
            const data = await res.json();
            walletBalance.innerText = data.balance;
        }
    } catch (err) { console.error(err); }
}

withdrawBtn.addEventListener('click', async () => {
    try {
        const res = await window.apiService.withdrawCoins('paypal', 100);

        const data = await res.json();
        walletMsg.style.display = "block";

        if (res.ok) {
            walletMsg.style.color = "var(--accent)";
            walletMsg.innerText = `Success! Remaining: ${data.remaining_balance}`;
            refreshWallet();
        } else {
            walletMsg.style.color = "#f87171";
            walletMsg.innerText = data.detail || "Withdrawal failed (Check Ratings/Balance)";
        }
        setTimeout(() => walletMsg.style.display = "none", 5000);
    } catch (err) { console.log(err); }
});

savePrefBtn.addEventListener('click', async () => {
    try {
        const res = await window.apiService.updateProfile({ gender_preference: prefGender.value });
        if (res.ok) logToUI(`Preference saved: ${prefGender.value}`);
    } catch (err) { console.error(err); }
});

// LOGOUT
logoutBtn.addEventListener('click', () => {
    localStorage.removeItem('talk_earn_token');
    currentToken = null;
    if (ws) ws.close();
    if (globalWs) globalWs.close();
    dashboardView.classList.remove('active');
    setTimeout(() => landingView.classList.add('active'), 400);
});

// --- WEBRTC & SIGNALING ---
let globalWs = null;

function connectGlobalWebSocket() {
    // Generate a temporary display name for the lobby if one doesn't exist yet
    const rawUsername = `User_${currentUserId}`;

    globalWs = new WebSocket(`${window.apiService.WS_BASE}/chat/ws/global/${rawUsername}`);

    const statusEl = document.getElementById('global-ws-status');
    const msgContainer = document.getElementById('global-messages-container');

    globalWs.onopen = () => {
        statusEl.innerText = "Connected";
        statusEl.style.color = "var(--accent)";
    };

    // Modify onmessage slightly to parse our custom nested payload
    globalWs.onmessage = (event) => {
        try {
            const data = JSON.parse(event.data);
            const msgEl = document.createElement('div');
            msgEl.className = 'global-msg';

            const isSelf = data.from_user === rawUsername;
            if (!isSelf) soundSys.playMessage();

            // Unpack our nested payload
            let displayMsg = data.message;
            let displayAvatar = '👤';

            try {
                const nested = JSON.parse(data.message);
                if (nested.text) {
                    displayMsg = nested.text;
                    displayAvatar = nested.avatar || '👤';
                }
            } catch (e) { } // If it wasn't JSON, it's a raw system message

            msgEl.innerHTML = `
                <div class="global-msg-author" style="${isSelf ? 'color: var(--accent);' : ''}">
                    ${displayAvatar} ${isSelf ? 'You' : data.from_user}
                </div>
                <div style="color: white;">${displayMsg}</div>
            `;

            msgContainer.appendChild(msgEl);
            msgContainer.scrollTop = msgContainer.scrollHeight;
        } catch (e) { console.error(e); }
    };

    globalWs.onclose = () => {
        statusEl.innerText = "Disconnected";
        statusEl.style.color = "#f87171";
    };
}

// Global Chat UI Bindings
const globalChatInput = document.getElementById('global-chat-input');
const sendGlobalBtn = document.getElementById('send-global-btn');

function sendGlobalMessage() {
    if (!globalWs || globalWs.readyState !== WebSocket.OPEN) return;
    const text = globalChatInput.value.trim();
    if (!text) return;

    // Send the raw text; The backend intercepts this, wraps it in JSON, but we can prepend the avatar.
    // However, since the backend just blindly broadcasts `data` as a string under the "message" key,
    // we should really send a stringified JSON if we want to pass the avatar. Since the backend
    // expects raw text and does `json.dumps({"from_user": user_name, "message": data})`,
    // we will inject the avatar into the raw text stream.

    // A better approach: We'll prefix the avatar to the message itself, and parse it back out
    // in the `onmessage` block, or just let it render natively.

    // To keep the backend pure, we'll serialize a tiny JSON here that the frontend unrolls.
    const packet = JSON.stringify({ text: text, avatar: currentUserAvatar });
    globalWs.send(packet);

    globalChatInput.value = "";
}

sendGlobalBtn.addEventListener('click', sendGlobalMessage);
globalChatInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendGlobalMessage();
});


function connectWebSocket() {
    ws = new WebSocket(`${window.apiService.WS_BASE}/chat/ws/${currentToken}`);

    ws.onopen = () => {
        wsStatus.innerText = "Connected & Ready";
        wsStatus.style.color = "var(--accent)";
        logToUI("WebSocket Connected");
    };

    ws.onmessage = async (event) => {
        try {
            const data = JSON.parse(event.data);

            // Display "Found User" card if metadata is provided in signaling
            if (data.from_name && (data.type === "offer" || data.type === "answer")) {
                showFoundUser(data.from_name, data.from_avatar);
            }

            // Handling signals
            if (data.type === "offer") {
                logToUI(`Received WebRTC Offer from User #${data.from}`);
                matchedUserId = data.from;
                await handleOffer(data.payload);
            } else if (data.type === "answer") {
                logToUI(`Received WebRTC Answer from User #${data.from}`);
                soundSys.playMatch();
                await handleAnswer(data.payload);
            } else if (data.type === "candidate") {
                logToUI(`Received ICE Candidate`);
                await handleCandidate(data.payload);
            } else if (data.type === "text") {
                receiveTextMessage(data.payload);
            } else if (data.type === 'end_call') {
                logToUI("Remote user ended the call.");
                if (peerConnection) {
                    peerConnection.close();
                    peerConnection = null;
                }
                if (matchedUserId) {
                    // Force rating modal for the receiver too
                    document.getElementById('end-call-btn').style.display = "none";
                    document.getElementById('rating-modal').classList.add('active');
                } else {
                    resetCallUI();
                }
            }
        } catch (err) {
            console.error("Signaling parsing error", err);
        }
    };

    ws.onclose = () => {
        wsStatus.innerText = "Disconnected";
        wsStatus.style.color = "#f87171";
        logToUI("WebSocket Disconnected", true);
    };
}

// MATCHMAKING API
findTextBtn.addEventListener('click', () => startMatchmaking('text'));
findAudioBtn.addEventListener('click', () => startMatchmaking('audio'));
findVideoBtn.addEventListener('click', () => startMatchmaking('video'));

async function startMatchmaking(medium) {
    if (isMatching) return;

    try {
        isMatching = true;
        currentMedium = medium;

        const originalContents = {
            'text': findTextBtn.innerHTML,
            'audio': findAudioBtn.innerHTML,
            'video': findVideoBtn.innerHTML
        };

        findTextBtn.disabled = true;
        findAudioBtn.disabled = true;
        findVideoBtn.disabled = true;

        if (medium === 'text') findTextBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i>';
        if (medium === 'audio') findAudioBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i>';
        if (medium === 'video') findVideoBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i>';

        radarUI.style.display = "flex";
        videoUI.style.display = "none";
        textChatUI.style.display = "none";

        if (medium === 'video' || medium === 'audio') {
            const mediaStarted = await startLocalMedia(medium === 'video');
            if (!mediaStarted) throw new Error("Could not access media devices.");
        }

        logToUI(`Requested /match/random pool entry for ${medium}...`);

        const res = await fetch(`${window.apiService.API_BASE}/match/random`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${currentToken}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ medium: medium })
        });

        const data = await res.json();

        if (data.matched_user_id) {
            matchedUserId = data.matched_user_id;
            logToUI(`🎉 Match Found! User #${matchedUserId}. Initiating session...`);

            // Show visual "Found" beat
            showFoundUser(data.matched_user_name, data.matched_user_customizations);

            if (medium === 'video' || medium === 'audio') {
                await createOffer();
            }
            // Add a small delay for the visual "Found" transition before hiding radar
            setTimeout(() => uiInCall(medium), 1500);
        } else {
            logToUI(`⏳ ${data.message}`);
            // Wait for someone else to match with us and send an offer
        }

    } catch (err) {
        logToUI(err.message, true);
        resetCallUI();
    }
}

endCallBtn.addEventListener('click', () => {
    logToUI("Session Ended manually.");
    if (peerConnection) peerConnection.close();
    if (localStream) localStream.getTracks().forEach(t => t.stop());
    resetCallUI();
});


// WEBRTC PEER LOGIC
async function startLocalMedia(isVideoEnabled) {
    try {
        localStream = await navigator.mediaDevices.getUserMedia({ video: isVideoEnabled, audio: true });

        if (isVideoEnabled) {
            localVideo.srcObject = localStream;
            localVideo.style.display = "block";
            remoteVideo.style.display = "block";
            logToUI("Camera and Mic Activated");
        } else {
            localVideo.style.display = "none";
            remoteVideo.style.display = "none";
            logToUI("Microphone Activated");
        }
        return true;
    } catch (err) {
        logToUI("Failed to get Media. Is it allowed?", true);
        return false;
    }
}

function createPeerConnection() {
    peerConnection = new RTCPeerConnection(rtcConfig);

    // Add local stream
    if (localStream) {
        localStream.getTracks().forEach(track => {
            peerConnection.addTrack(track, localStream);
        });
    }

    // Handle incoming stream
    peerConnection.ontrack = (event) => {
        if (!remoteVideo.srcObject) {
            remoteVideo.srcObject = event.streams[0];
            logToUI("Received Remote Stream");
            uiInCall(currentMedium);
        }
    };

    // Ice candidates
    peerConnection.onicecandidate = (event) => {
        if (event.candidate) {
            sendSignal("candidate", event.candidate);
        }
    };
}

async function createOffer() {
    createPeerConnection();
    const offer = await peerConnection.createOffer();
    await peerConnection.setLocalDescription(offer);
    sendSignal("offer", offer);
}

async function handleOffer(offer) {
    // Determine medium implicitly from what we are accepting. Assume currentMedium is set if we are in pool.
    // If we received an offer and have no medium, default to audio or video?
    // Usually we already clicked the button.
    if ((currentMedium === 'video' || currentMedium === 'audio') && !localStream) {
        await startLocalMedia(currentMedium === 'video');
    }

    createPeerConnection();
    await peerConnection.setRemoteDescription(new RTCSessionDescription(offer));
    const answer = await peerConnection.createAnswer();
    await peerConnection.setLocalDescription(answer);
    sendSignal("answer", answer);
    uiInCall(currentMedium);
}

async function handleAnswer(answer) {
    await peerConnection.setRemoteDescription(new RTCSessionDescription(answer));
    soundSys.playMatch();
}

async function handleCandidate(candidate) {
    if (peerConnection) {
        await peerConnection.addIceCandidate(new RTCIceCandidate(candidate));
    }
}

function sendSignal(type, payload) {
    if (ws && ws.readyState === WebSocket.OPEN && matchedUserId) {
        ws.send(JSON.stringify({
            target_user_id: matchedUserId,
            type: type,
            payload: payload,
            from_name: currentUserName,
            from_avatar: currentAvatarState
        }));
    }
}

// UI HELPERS
function logToUI(msg, isError = false) {
    const p = document.createElement('div');
    p.className = `log-entry ${isError ? 'log-error' : ''}`;
    p.innerText = `[${new Date().toLocaleTimeString()}] ${msg}`;
    logsDiv.prepend(p);
}

document.getElementById('cancel-match-btn').addEventListener('click', async () => {
    if (!isMatching) return;

    try {
        await fetch(`${window.apiService.API_BASE}/match/cancel`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${currentToken}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ medium: currentMedium })
        });
        logToUI("Matchmaking cancelled by user.");
    } catch (err) {
        console.error("Failed to cancel match:", err);
    }

    resetCallUI();
});

const showChatBtn = document.getElementById('show-chat-btn');
const hideChatBtn = document.getElementById('hide-chat-btn');

showChatBtn.addEventListener('click', () => {
    textChatUI.style.display = "flex";
    setTimeout(() => {
        textChatUI.classList.remove('closed');
        showChatBtn.style.transform = "scale(0)";
        setTimeout(() => showChatBtn.style.display = "none", 200);
    }, 10);
});

hideChatBtn.addEventListener('click', () => {
    textChatUI.classList.add('closed');
    setTimeout(() => {
        textChatUI.style.display = "none";
        showChatBtn.style.display = "flex";
        setTimeout(() => showChatBtn.style.transform = "scale(1)", 10);
    }, 300);
});

function uiInCall(medium) {
    radarUI.style.display = "none";
    matchControls.style.display = "none";
    endCallBtn.style.display = "inline-block";

    if (medium === 'video' || medium === 'audio') {
        videoUI.style.display = "grid";
        textChatUI.classList.remove('text-only-mode');
        textChatUI.classList.add('closed');
        textChatUI.style.display = "none"; // start hidden
        showChatBtn.style.display = "flex";
        showChatBtn.style.transform = "scale(1)";
    } else if (medium === 'text') {
        videoUI.style.display = "none";
        textChatUI.classList.add('text-only-mode');
        textChatUI.classList.remove('closed');
        textChatUI.style.display = "flex";
        showChatBtn.style.display = "none";
    }

    startEarningLoop();
}

function showFoundUser(name, customizations) {
    const statusText = document.getElementById('radar-status-text');
    const animation = document.getElementById('radar-animation');
    const card = document.getElementById('found-user-card');
    const nameEl = document.getElementById('found-user-name');
    const avatarEl = document.getElementById('found-user-avatar');

    if (statusText) statusText.innerText = "Found a match!";
    if (animation) animation.style.display = "none";
    if (card) card.style.display = "flex";
    if (nameEl) nameEl.innerText = name || "Someone Special";

    if (avatarEl && customizations) {
        try {
            const parsed = typeof customizations === 'string' ? JSON.parse(customizations) : customizations;
            avatarEl.innerHTML = renderAvatarSVG(parsed, "80px");
        } catch (e) {
            avatarEl.innerHTML = '<span style="font-size: 2rem;">👤</span>';
        }
    }
}

function resetCallUI() {
    isMatching = false;
    matchedUserId = null;
    currentMedium = null;

    stopEarningLoop();

    if (localVideo.srcObject) localVideo.srcObject = null;
    if (remoteVideo.srcObject) remoteVideo.srcObject = null;

    radarUI.style.display = "none";

    // Reset Radar UI internally
    const rStatus = document.getElementById('radar-status-text');
    const rAnim = document.getElementById('radar-animation');
    const rCard = document.getElementById('found-user-card');
    if (rStatus) rStatus.innerText = "Searching for friends...";
    if (rAnim) rAnim.style.display = "flex";
    if (rCard) rCard.style.display = "none";

    videoUI.style.display = "none";
    textChatUI.style.display = "none";
    showChatBtn.style.display = "none";
    textChatUI.classList.add('closed');
    textChatUI.classList.remove('text-only-mode');

    matchControls.style.display = "flex";
    findTextBtn.innerHTML = '<i class="fa-solid fa-comment"></i> Text Chat';
    findAudioBtn.innerHTML = '<i class="fa-solid fa-phone"></i> Voice Call';
    findVideoBtn.innerHTML = '<i class="fa-solid fa-video"></i> Video Call';
    findTextBtn.disabled = false;
    findAudioBtn.disabled = false;
    findVideoBtn.disabled = false;

    endCallBtn.style.display = "none";
    messagesContainer.innerHTML = '<div style="text-align: center; color: var(--text-muted); font-size: 0.85rem;">Session started. Say hi!</div>';
}

// EARNING LOOP
function startEarningLoop() {
    if (earningInterval) clearInterval(earningInterval);
    // Ping the backend every 60 seconds to earn credits for the current medium
    earningInterval = setInterval(async () => {
        try {
            const res = await fetch(`${window.apiService.API_BASE}/wallet/earn`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${currentToken}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ minutes: 1, medium: currentMedium || 'text' })
            });
            const data = await res.json();
            if (data.balance !== undefined) {
                const walletBalance = document.getElementById('wallet-balance');
                walletBalance.innerText = data.balance;
                logToUI(`💰 Earned coins! New balance: ${data.balance}`);
            }
        } catch (err) {
            console.error("Earning ping failed", err);
        }
    }, 60000);
}

function stopEarningLoop() {
    if (earningInterval) {
        clearInterval(earningInterval);
        earningInterval = null;
    }
}

// TEXT CHAT LOGIC
sendMsgBtn.addEventListener('click', sendTextMessage);
chatMessageInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendTextMessage();
});

function sendTextMessage() {
    const msg = chatMessageInput.value.trim();
    if (!msg || !matchedUserId) return;

    div.style.fontSize = '0.95rem';
    div.innerText = msg;
    messagesContainer.appendChild(div);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;

    chatMessageInput.value = '';
}

function receiveTextMessage(msg) {
    const div = document.createElement('div');
    div.style.alignSelf = 'flex-start';
    div.style.background = 'rgba(255,255,255,0.1)';
    div.style.color = 'white';
    div.style.padding = '0.5rem 1rem';
    div.style.borderRadius = '16px';
    div.style.maxWidth = '80%';
    div.style.fontSize = '0.95rem';
    div.innerText = msg;
    messagesContainer.appendChild(div);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
    uiInCall('text'); // Ensure UI swaps if receiving a text message initializes it
}

// CARTOON BACKGROUND ANIMATION
function initAnimatedBackground() {
    const container = document.getElementById('floating-bg-container');
    if (!container) return;

    const emojis = ['💰', '💬', '❤️', '🤝', '✨', '💸'];

    // Spawn initial batch
    for (let i = 0; i < 15; i++) {
        spawnEmoji(container, emojis);
    }

    // Continuously spawn new ones
    setInterval(() => {
        spawnEmoji(container, emojis);
    }, 2000);
}

function spawnEmoji(container, emojis) {
    const el = document.createElement('div');
    el.className = 'floating-emoji';

    // Randomize Emoji
    el.innerText = emojis[Math.floor(Math.random() * emojis.length)];

    // Randomize Position & Scale
    el.style.left = `${Math.random() * 100}vw`;
    el.style.fontSize = `${1.5 + Math.random() * 2.5}rem`;

    // Randomize Animation properties
    const duration = 15 + Math.random() * 20; // 15s to 35s
    el.style.animationDuration = `${duration}s`;
    el.style.animationDelay = `${Math.random() * 5}s`;

    container.appendChild(el);

    // Cleanup to prevent DOM bloat
    setTimeout(() => {
        if (el.parentNode === container) {
            container.removeChild(el);
        }
    }, duration * 1000 + 5000);
}

// LIVE STATS TICKER
function initLiveStatsTicker() {
    const onlineEl = document.getElementById('stat-online');
    const callsEl = document.getElementById('stat-calls');
    const cryptoEl = document.getElementById('stat-crypto');

    if (!onlineEl || !callsEl || !cryptoEl) return;

    setInterval(() => {
        // Randomly increment sometimes to simulate live traffic
        if (Math.random() > 0.4) {
            let online = parseInt(onlineEl.innerText.replace(/,/g, ''));
            online += Math.floor(Math.random() * 3) - 1; // fluctuants up and down slightly
            onlineEl.innerText = online.toLocaleString();

            let calls = parseInt(callsEl.innerText.replace(/,/g, ''));
            calls += Math.floor(Math.random() * 2);
            callsEl.innerText = calls.toLocaleString();

            let crypto = parseInt(cryptoEl.innerText.replace(/,/g, ''));
            crypto += Math.floor(Math.random() * 5);
            cryptoEl.innerText = crypto.toLocaleString();
        }
    }, 3000);
}

// --- ACCOUNT SETTINGS SYSTEM ---
if (settingsBtn) {
    settingsBtn.addEventListener('click', async () => {
        settingsModal.classList.add('active');
        try {
            const res = await window.apiService.getProfile();
            const data = await res.json();

            // Populate Readonly Info
            document.getElementById('setting-email-display').innerText = data.email || "Unknown";
            document.getElementById('setting-age-display').innerText = data.age ? `${data.age} yrs` : "Not verified";

            // Populate Editable Fields
            document.getElementById('setting-name-input').value = data.full_name || "";
            document.getElementById('setting-gender-input').value = data.gender || "male";
            document.getElementById('setting-interests-input').value = data.interests || "";

            const svgTarget = document.getElementById('setting-profile-svg-preview');
            const picTarget = document.getElementById('setting-profile-pic-preview');

            if (data.profile_picture_url) {
                picTarget.src = data.profile_picture_url;
                picTarget.style.display = 'block';
                svgTarget.style.display = 'none';
            } else if (data.customizations) {
                picTarget.style.display = 'none';
                svgTarget.style.display = 'flex';
                const parsed = JSON.parse(data.customizations);
                svgTarget.innerHTML = renderAvatarSVG(parsed);
            }
        } catch (e) { console.error(e); }
    });
}

// PROFILE EDIT FORM
if (profileEditForm) {
    profileEditForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const msgDiv = document.getElementById('profile-edit-msg');
        const updateData = {
            full_name: document.getElementById('setting-name-input').value,
            gender: document.getElementById('setting-gender-input').value,
            interests: document.getElementById('setting-interests-input').value
        };

        try {
            const res = await fetch(`${window.apiService.API_BASE}/profile/`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${currentToken}`
                },
                body: JSON.stringify(updateData)
            });

            if (!res.ok) throw new Error("Failed to update profile");

            msgDiv.style.display = 'block';
            msgDiv.style.color = '#10b981';
            msgDiv.innerText = "Profile updated successfully!";
            setTimeout(() => msgDiv.style.display = 'none', 3000);

            // Update local state if needed
            refreshWallet();
        } catch (err) {
            msgDiv.style.color = '#ef4444';
            showError(msgDiv, err.message);
        }
    });
}

// BRIDGE TO STUDIO
if (openStudioFromSettings) {
    openStudioFromSettings.addEventListener('click', () => {
        settingsModal.classList.remove('active');
        studioModal.style.display = 'flex';
        updateStudioPreview();
    });
}

if (triggerUploadBtn && profileUploadInput) {
    triggerUploadBtn.addEventListener('click', () => profileUploadInput.click());

    profileUploadInput.addEventListener('change', async (e) => {
        const file = e.target.files[0];
        if (!file) return;

        const formData = new FormData();
        formData.append('file', file);

        uploadMsg.style.display = 'block';
        uploadMsg.style.color = 'var(--text-muted)';
        uploadMsg.innerText = 'Uploading...';

        try {
            const res = await window.apiService.uploadProfilePicture(formData);

            if (!res.ok) {
                const err = await res.json();
                throw new Error(err.detail || "Upload failed");
            }
            const data = await res.json();

            uploadMsg.style.color = '#10b981';
            uploadMsg.innerText = 'Success!';

            document.getElementById('setting-profile-pic-preview').src = data.url;
            document.getElementById('setting-profile-pic-preview').style.display = 'block';
            document.getElementById('setting-profile-svg-preview').style.display = 'none';

            const headerAvatar = document.getElementById('header-avatar-container');
            if (headerAvatar) {
                headerAvatar.innerHTML = `<img src="${data.url}" style="width: 100%; height: 100%; object-fit: cover;" />`;
            }
            currentUserAvatar = data.url;

            setTimeout(() => uploadMsg.style.display = 'none', 3000);

        } catch (err) {
            uploadMsg.style.color = '#ef4444';
            uploadMsg.innerText = err.message;
        }
    });
}

if (closeSettingsBtn) {
    closeSettingsBtn.addEventListener('click', () => {
        settingsModal.classList.remove('active');
        document.getElementById('password-msg').style.display = 'none';
        document.getElementById('delete-msg').style.display = 'none';
    });
}

if (passwordForm) {
    passwordForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const currentPassword = document.getElementById('current-password').value;
        const newPassword = document.getElementById('new-password').value;
        const msgDiv = document.getElementById('password-msg');

        try {
            const res = await fetch(`${window.apiService.API_BASE}/profile/password`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${currentToken}`
                },
                body: JSON.stringify({ current_password: currentPassword, new_password: newPassword })
            });

            if (!res.ok) {
                const err = await res.json();
                throw new Error(err.detail || "Update failed");
            }
            msgDiv.style.display = 'block';
            msgDiv.style.color = '#10b981';
            msgDiv.innerText = "Password updated successfully!";
            passwordForm.reset();
        } catch (err) {
            msgDiv.style.display = 'block';
            msgDiv.style.color = '#ef4444';
            msgDiv.innerText = err.message;
        }
    });
}

if (deleteAccountForm) {
    deleteAccountForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const confirmPassword = document.getElementById('delete-password').value;
        const msgDiv = document.getElementById('delete-msg');

        if (!confirm("Are you absolutely sure you want to permanently delete your account?")) return;

        try {
            const res = await fetch(`${window.apiService.API_BASE}/profile/account/delete`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${currentToken}`
                },
                body: JSON.stringify({ current_password: confirmPassword })
            });

            if (!res.ok) {
                const err = await res.json();
                throw new Error(err.detail || "Deletion failed");
            }

            // Success - log out
            settingsModal.classList.remove('active');
            logoutBtn.click();
            alert("Your account has been permanently deleted.");
        } catch (err) {
            msgDiv.style.display = 'block';
            msgDiv.style.color = '#ef4444';
            msgDiv.innerText = err.message;
        }
    });
}


// --- 3D AVATAR STUDIO SYSTEM ---
const avatarAssets = {
    skins: {
        light: { base: '#fed7aa', shadow: '#fdba74', highlight: '#ffedd5', ears: '#fdba74' },
        medium: { base: '#f59e0b', shadow: '#d97706', highlight: '#fcd34d', ears: '#d97706' },
        dark: { base: '#78350f', shadow: '#451a03', highlight: '#92400e', ears: '#451a03' },
        alien: { base: '#10b981', shadow: '#047857', highlight: '#6ee7b7', ears: '#047857' },
        blue: { base: '#3b82f6', shadow: '#1d4ed8', highlight: '#93c5fd', ears: '#1d4ed8' }
    },
    hair: {
        bald: '',
        short: '<path d="M 22 42 C 15 10, 85 10, 78 42 Q 50 35 22 42 Z" fill="url(#hairGrad)" filter="url(#dropShadow)" />',
        fade: '<path d="M 25 40 C 20 0, 80 0, 75 40 Z" fill="url(#hairGrad)" filter="url(#dropShadow)"/><rect x="22" y="40" width="8" height="20" fill="currentColor"/><rect x="70" y="40" width="8" height="20" fill="currentColor"/>',
        long: '<path d="M 20 35 C 10 -5, 90 -5, 80 35 C 98 70, 98 100, 80 105 C 60 90, 40 90, 20 105 C 2 100, 2 70, 20 35 Z" fill="url(#hairGrad)" filter="url(#dropShadow)"/>',
        bun: '<circle cx="50" cy="15" r="12" fill="url(#hairGrad)"/><path d="M 20 40 C 15 10, 85 10, 80 40 Z" fill="url(#hairGrad)" filter="url(#dropShadow)"/>',
        spiky: '<path d="M 15 45 Q 25 0 35 35 Q 45 -10 50 35 Q 55 -10 65 35 Q 75 0 85 45 Z" fill="url(#hairGrad)" filter="url(#dropShadow)"/>'
    },
    hairColors: ['#0f172a', '#451a03', '#b45309', '#fde047', '#dc2626', '#d946ef', '#3b82f6'],
    faces: {
        smile: `
            <!-- Eyes with Pupils -->
            <g class="eyes">
                <circle cx="36" cy="45" r="5" fill="white"/>
                <circle cx="36" cy="45" r="2.5" fill="#1e293b"/>
                <circle cx="37" cy="44" r="0.8" fill="white" opacity="0.8"/>

                <circle cx="64" cy="45" r="5" fill="white"/>
                <circle cx="64" cy="45" r="2.5" fill="#1e293b"/>
                <circle cx="65" cy="44" r="0.8" fill="white" opacity="0.8"/>
            </g>
            <!-- Humanoid Nose -->
            <path d="M 47 55 Q 50 62 53 55" stroke="rgba(0,0,0,0.15)" stroke-width="2.5" fill="none" stroke-linecap="round"/>
            <!-- Expressive Mouth -->
            <path d="M 38 68 Q 50 82 62 68" stroke="#991b1b" stroke-width="4.5" fill="url(#mouthGrad)" stroke-linecap="round"/>
        `,
        cool: `
            <g class="eyes">
                <path d="M 25 42 L 45 42 L 45 50 L 25 50 Z" fill="#0f172a" filter="url(#dropShadow)"/>
                <path d="M 55 42 L 75 42 L 75 50 L 55 50 Z" fill="#0f172a" filter="url(#dropShadow)"/>
                <path d="M 45 45 L 55 45" stroke="#0f172a" stroke-width="3"/>
            </g>
            <path d="M 48 58 Q 50 63 52 58" stroke="rgba(0,0,0,0.2)" stroke-width="2" fill="none"/>
            <path d="M 42 72 Q 50 75 58 72" stroke="#1e293b" stroke-width="3" fill="none" stroke-linecap="round"/>
        `,
        shocked: `
            <g class="eyes">
                <circle cx="36" cy="43" r="6" fill="white"/>
                <circle cx="36" cy="43" r="3" fill="#1e293b"/>
                <circle cx="64" cy="43" r="6" fill="white"/>
                <circle cx="64" cy="43" r="3" fill="#1e293b"/>
            </g>
            <path d="M 48 56 Q 50 62 52 56" stroke="rgba(0,0,0,0.1)" stroke-width="2" fill="none"/>
            <circle cx="50" cy="75" r="6" fill="url(#mouthGrad)" filter="url(#dropShadow)"/>
        `,
        wink: `
            <g class="eyes">
                <path d="M 28 45 Q 36 40 44 45" stroke="#1e293b" stroke-width="3" fill="none" stroke-linecap="round"/>
                <circle cx="64" cy="45" r="5" fill="white"/>
                <circle cx="64" cy="45" r="2.5" fill="#1e293b"/>
            </g>
            <path d="M 47 55 Q 50 62 53 55" stroke="rgba(0,0,0,0.1)" stroke-width="2" fill="none"/>
            <path d="M 38 68 Q 50 82 62 68" stroke="#991b1b" stroke-width="4" fill="url(#mouthGrad)" stroke-linecap round"/>
        `
    },
    bodies: {
        tshirt: '<path d="M 12 100 Q 12 70 30 70 L 70 70 Q 88 70 88 100 Z" fill="url(#bodyGrad)" filter="url(#dropShadow)"/><path d="M 30 70 Q 50 85 70 70" fill="rgba(0,0,0,0.15)"/>',
        hoodie: '<path d="M 10 100 Q 10 65 30 65 L 70 65 Q 90 65 90 100 Z" fill="url(#bodyGrad)" filter="url(#dropShadow)"/><path d="M 25 65 Q 50 90 75 65" stroke="rgba(0,0,0,0.25)" stroke-width="8" fill="none"/><path d="M 47 78 L 47 100 M 53 78 L 53 100" stroke="rgba(255,255,255,0.4)" stroke-width="2.5"/>',
        suit: '<path d="M 12 100 Q 12 70 30 70 L 70 70 Q 88 70 88 100 Z" fill="url(#bodyGrad)" filter="url(#dropShadow)"/><polygon points="30,70 50,100 70,70" fill="#f8fafc"/><polygon points="30,70 50,96 44,70" fill="#0f172a"/><polygon points="70,70 50,96 56,70" fill="#0f172a"/><rect x="48" y="85" width="4" height="15" fill="#ef4444"/>'
    },
    bodyColors: ['#1e293b', '#ef4444', '#3b82f6', '#10b981', '#f59e0b', '#c084fc', '#6366f1']
};

let currentAvatarState = {
    skin: 'light',
    hair: 'short',
    hairColor: '#0f172a',
    face: 'smile',
    body: 'tshirt',
    bodyColor: '#3b82f6'
};

function renderAvatarSVG(state, size = "100%") {
    const skinTones = avatarAssets.skins[state.skin] || avatarAssets.skins['light'];

    const hex2rgb = (hex) => {
        const r = parseInt(hex.slice(1, 3), 16);
        const g = parseInt(hex.slice(3, 5), 16);
        const b = parseInt(hex.slice(5, 7), 16);
        return `${r},${g},${b}`;
    };

    let svg = `<svg width="${size}" height="${size}" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <radialGradient id="skinGrad" cx="35%" cy="35%" r="65%">
                <stop offset="0%" stop-color="${skinTones.highlight}" />
                <stop offset="60%" stop-color="${skinTones.base}" />
                <stop offset="100%" stop-color="${skinTones.shadow}" />
            </radialGradient>

            <linearGradient id="hairGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" stop-color="${state.hairColor}" />
                <stop offset="100%" stop-color="rgba(0,0,0,0.7)" />
            </linearGradient>

            <linearGradient id="bodyGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="${state.bodyColor}" />
                <stop offset="100%" stop-color="rgba(${hex2rgb(state.bodyColor)}, 0.3)" />
            </linearGradient>

            <linearGradient id="mouthGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" stop-color="#450a0a" />
                <stop offset="100%" stop-color="#991b1b" />
            </linearGradient>

            <filter id="dropShadow" x="-20%" y="-20%" width="140%" height="140%">
                <feDropShadow dx="0" dy="4" stdDeviation="4" flood-opacity="0.4"/>
            </filter>

            <filter id="innerShadow">
                <feOffset dx="0" dy="2"/>
                <feGaussianBlur stdDeviation="2" result="offset-blur"/>
                <feComposite operator="out" in="SourceGraphic" in2="offset-blur" result="inverse"/>
                <feFlood flood-color="black" flood-opacity="0.2" result="color"/>
                <feComposite operator="in" in="color" in2="inverse" result="shadow"/>
                <feComposite operator="over" in="shadow" in2="SourceGraphic"/>
            </filter>
        </defs>`;

    // 1. Humanoid Ears
    svg += `<circle cx="23" cy="48" r="7" fill="${skinTones.ears}" />`;
    svg += `<circle cx="77" cy="48" r="7" fill="${skinTones.ears}" />`;

    // 2. Body/Clothing
    let bodyPath = avatarAssets.bodies[state.body] || avatarAssets.bodies['tshirt'];
    svg += `<g>${bodyPath}</g>`;

    // 3. Humanoid Neck
    svg += `<rect x="38" y="62" width="24" height="15" rx="8" fill="${skinTones.shadow}" />`;

    // 4. Detailed Head
    svg += `<circle cx="50" cy="45" r="28" fill="url(#skinGrad)" filter="url(#dropShadow)"/>`;

    // 5. Face/Expression (Detailed)
    let facePath = avatarAssets.faces[state.face] || avatarAssets.faces['smile'];
    svg += `<g filter="url(#innerShadow)">${facePath}</g>`;

    // 6. Hair Asset
    let hairPath = avatarAssets.hair[state.hair] || '';
    svg += `<g style="color: ${state.hairColor};">${hairPath}</g>`;

    svg += `</svg>`;
    return svg;
}

// UI Bindings for Studio
function updateStudioPreview() {
    const svgData = renderAvatarSVG(currentAvatarState);
    if (renderTarget) renderTarget.innerHTML = svgData;
    if (headerAvatarTarget) headerAvatarTarget.innerHTML = svgData;
}

function buildTraitGrid(elementId, optionsObj, type, isColor = false) {
    const container = document.getElementById(elementId);
    if (!container) return;
    container.innerHTML = '';

    const keys = Array.isArray(optionsObj) ? optionsObj : Object.keys(optionsObj);

    keys.forEach(key => {
        const btn = document.createElement('div');
        btn.className = 'trait-btn';

        if (isColor) {
            btn.style.width = '30px';
            btn.style.height = '30px';
            btn.style.borderRadius = '50%';
            btn.style.background = key;
            btn.style.padding = '0';
            if (currentAvatarState[type] === key) btn.classList.add('active');
        } else {
            btn.innerText = key.charAt(0).toUpperCase() + key.slice(1);
            if (currentAvatarState[type] === key) btn.classList.add('active');
        }

        btn.addEventListener('click', () => {
            Array.from(container.children).forEach(c => c.classList.remove('active'));
            btn.classList.add('active');
            currentAvatarState[type] = key;
            updateStudioPreview();
        });

        container.appendChild(btn);
    });
}

function initAvatarStudio() {
    buildTraitGrid('trait-grid-skin', avatarAssets.skins, 'skin');

    // Hair needs two rows (styles and colors)
    const hairContainer = document.getElementById('trait-grid-hair');
    const styleDiv = document.createElement('div'); styleDiv.className = 'trait-grid'; styleDiv.style.marginBottom = '0.5rem';
    hairContainer.appendChild(styleDiv);
    buildTraitGrid(styleDiv, avatarAssets.hair, 'hair');
    buildTraitGrid(hairContainer.id, avatarAssets.hairColors, 'hairColor', true);

    buildTraitGrid('trait-grid-face', avatarAssets.faces, 'face');

    // Body needs two rows
    const bodyContainer = document.getElementById('trait-grid-body');
    const bStyleDiv = document.createElement('div'); bStyleDiv.className = 'trait-grid'; bStyleDiv.style.marginBottom = '0.5rem';
    bodyContainer.appendChild(bStyleDiv);
    buildTraitGrid(bStyleDiv, avatarAssets.bodies, 'body');
    buildTraitGrid(bodyContainer.id, avatarAssets.bodyColors, 'bodyColor', true);

    updateStudioPreview();
}

if (openStudioBtn) {
    openStudioBtn.addEventListener('click', () => {
        studioModal.style.display = 'flex';
        initAvatarStudio();
    });
}

if (closeStudioBtn) {
    closeStudioBtn.addEventListener('click', () => {
        studioModal.style.display = 'none';
        // Need to restore state to whatever is actually saved if they close without saving
    });
}

if (saveAvatarBtn) {
    saveAvatarBtn.addEventListener('click', async () => {
        try {
            const res = await window.apiService.updateProfile({ customizations: JSON.stringify(currentAvatarState) });

            if (!res.ok) throw new Error("Failed to save avatar");

            // Generate full SVG, cache it
            currentUserAvatar = renderAvatarSVG(currentAvatarState);
            localStorage.setItem('talk_avatar_state', JSON.stringify(currentAvatarState));

            studioModal.style.display = 'none';
            logToUI("Avatar successfully customized and synced.");
        } catch (err) {
            const errDiv = document.getElementById('studio-error-msg');
            showError(errDiv, err.message);
        }
    });
}


// BOOT
initAnimatedBackground();
initLiveStatsTicker();
init();
