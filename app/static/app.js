// Firebase config
firebase.initializeApp({
    apiKey: "AIzaSyAptsW8AG_womu5SFHZ4pBZlDPLx0R8zQc",
    authDomain: "agentcore-467421.firebaseapp.com",
    projectId: "agentcore-467421",
    appId: "1:261903456205:web:8e89277914c7da25b91684",
});

const authProvider = new firebase.auth.GoogleAuthProvider();
let currentUser = null;
let idToken = null;

// DOM elements
const signinBtn = document.getElementById("signin-btn");
const signinBtnMain = document.getElementById("signin-btn-main");
const signoutBtn = document.getElementById("signout-btn");
const userInfo = document.getElementById("user-info");
const userAvatar = document.getElementById("user-avatar");
const userName = document.getElementById("user-name");
const loginPrompt = document.getElementById("login-prompt");
const mainApp = document.getElementById("main-app");

const uploadZone = document.getElementById("upload-zone");
const fileInput = document.getElementById("file-input");
const uploadContent = document.getElementById("upload-content");
const uploadPreview = document.getElementById("upload-preview");
const previewImage = document.getElementById("preview-image");
const clearBtn = document.getElementById("clear-btn");
const analyzeBtn = document.getElementById("analyze-btn");
const btnText = analyzeBtn.querySelector(".btn-text");
const btnLoader = document.getElementById("btn-loader");
const resultsPanel = document.getElementById("results-panel");
const resultImage = document.getElementById("result-image");
const breedCards = document.getElementById("breed-cards");
const noDogs = document.getElementById("no-dogs");
const historyList = document.getElementById("history-list");
const historyEmpty = document.getElementById("history-empty");

let selectedFile = null;

// Auth state listener
firebase.auth().onAuthStateChanged(async (user) => {
    if (user) {
        currentUser = user;
        idToken = await user.getIdToken();
        showAuthenticatedUI(user);
        loadHistory();
    } else {
        currentUser = null;
        idToken = null;
        showUnauthenticatedUI();
    }
});

// Refresh token periodically (tokens expire after 1 hour)
setInterval(async () => {
    if (currentUser) {
        idToken = await currentUser.getIdToken(true);
    }
}, 50 * 60 * 1000);

function showAuthenticatedUI(user) {
    signinBtn.classList.add("hidden");
    userInfo.classList.remove("hidden");
    userAvatar.src = user.photoURL || "";
    userName.textContent = user.displayName || user.email;
    loginPrompt.classList.add("hidden");
    mainApp.classList.remove("hidden");
}

function showUnauthenticatedUI() {
    signinBtn.classList.remove("hidden");
    userInfo.classList.add("hidden");
    loginPrompt.classList.remove("hidden");
    mainApp.classList.add("hidden");
}

function signIn() {
    firebase.auth().signInWithPopup(authProvider).catch((err) => {
        if (err.code !== "auth/popup-closed-by-user") {
            alert("Sign-in failed: " + err.message);
        }
    });
}

signinBtn.addEventListener("click", signIn);
signinBtnMain.addEventListener("click", signIn);
signoutBtn.addEventListener("click", () => firebase.auth().signOut());

// Helper: make authenticated fetch
function authFetch(url, options = {}) {
    return fetch(url, {
        ...options,
        headers: {
            ...options.headers,
            Authorization: `Bearer ${idToken}`,
        },
    });
}

// Upload zone interactions
uploadZone.addEventListener("click", () => {
    if (!selectedFile) fileInput.click();
});

uploadZone.addEventListener("dragover", (e) => {
    e.preventDefault();
    uploadZone.classList.add("dragover");
});

uploadZone.addEventListener("dragleave", () => {
    uploadZone.classList.remove("dragover");
});

uploadZone.addEventListener("drop", (e) => {
    e.preventDefault();
    uploadZone.classList.remove("dragover");
    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith("image/")) {
        setFile(file);
    }
});

fileInput.addEventListener("change", () => {
    if (fileInput.files[0]) setFile(fileInput.files[0]);
});

clearBtn.addEventListener("click", (e) => {
    e.stopPropagation();
    clearFile();
});

analyzeBtn.addEventListener("click", uploadAndAnalyze);

function setFile(file) {
    selectedFile = file;
    const reader = new FileReader();
    reader.onload = (e) => {
        previewImage.src = e.target.result;
        uploadContent.classList.add("hidden");
        uploadPreview.classList.remove("hidden");
        analyzeBtn.disabled = false;
    };
    reader.readAsDataURL(file);
}

function clearFile() {
    selectedFile = null;
    fileInput.value = "";
    previewImage.src = "";
    uploadContent.classList.remove("hidden");
    uploadPreview.classList.add("hidden");
    analyzeBtn.disabled = true;
}

async function uploadAndAnalyze() {
    if (!selectedFile || !idToken) return;

    analyzeBtn.disabled = true;
    btnText.textContent = "Analyzing...";
    btnLoader.classList.remove("hidden");

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
        const res = await authFetch("/api/upload", { method: "POST", body: formData });
        if (!res.ok) {
            const err = await res.json();
            throw new Error(err.detail || "Upload failed");
        }
        const data = await res.json();
        showResults(data);
        loadHistory();
    } catch (err) {
        alert(err.message);
    } finally {
        btnText.textContent = "Identify Breed";
        btnLoader.classList.add("hidden");
        analyzeBtn.disabled = false;
    }
}

function showResults(data) {
    resultsPanel.classList.remove("hidden");
    resultImage.src = data.image_url;

    breedCards.innerHTML = "";
    noDogs.classList.add("hidden");

    if (data.results.no_dogs_detected || data.results.detected_dogs.length === 0) {
        noDogs.classList.remove("hidden");
        return;
    }

    data.results.detected_dogs.forEach((dog) => {
        const card = document.createElement("div");
        card.className = "breed-card";
        card.innerHTML = `
            <div class="breed-header">
                <span class="breed-name">${escapeHtml(dog.breed)}</span>
                <span class="confidence-tag ${dog.confidence}">${dog.confidence}</span>
            </div>
            <p class="breed-desc">${escapeHtml(dog.description)}</p>
            ${dog.breed_info ? `<p class="breed-info">${escapeHtml(dog.breed_info)}</p>` : ""}
        `;
        breedCards.appendChild(card);
    });

    resultsPanel.scrollIntoView({ behavior: "smooth", block: "nearest" });
}

async function loadHistory() {
    if (!idToken) return;
    try {
        const res = await authFetch("/api/history?limit=20");
        if (!res.ok) return;
        const data = await res.json();

        if (data.items.length === 0) {
            historyEmpty.classList.remove("hidden");
            return;
        }

        historyEmpty.classList.add("hidden");
        historyList.innerHTML = "";

        data.items.forEach((item) => {
            const breeds = item.results.detected_dogs;
            const breedText = breeds.length > 0
                ? breeds.map((d) => d.breed).join(", ")
                : "No dogs detected";

            const time = new Date(item.timestamp).toLocaleString();

            const el = document.createElement("div");
            el.className = "history-item";
            el.innerHTML = `
                <img class="history-thumb" src="${escapeAttr(item.image_url)}" alt="Query image">
                <div class="history-info">
                    <div class="history-breed">${escapeHtml(breedText)}</div>
                    <div class="history-time">${escapeHtml(time)}</div>
                </div>
                <button class="history-delete" title="Delete">&times;</button>
            `;
            el.addEventListener("click", (e) => {
                if (e.target.closest(".history-delete")) return;
                document.querySelectorAll(".history-item.active").forEach((i) => i.classList.remove("active"));
                el.classList.add("active");
                showResults(item);
            });
            el.querySelector(".history-delete").addEventListener("click", async (e) => {
                e.stopPropagation();
                try {
                    const res = await authFetch(`/api/history/${item.query_id}`, { method: "DELETE" });
                    if (res.ok) {
                        el.remove();
                        if (historyList.children.length === 0) {
                            historyEmpty.classList.remove("hidden");
                        }
                    }
                } catch { /* ignore */ }
            });
            historyList.appendChild(el);
        });
    } catch {
        // silently fail on history load
    }
}

function escapeHtml(str) {
    const div = document.createElement("div");
    div.textContent = str;
    return div.innerHTML;
}

function escapeAttr(str) {
    return str.replace(/&/g, "&amp;").replace(/"/g, "&quot;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}
