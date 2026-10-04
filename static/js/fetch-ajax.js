// Elemen DOM
const loadingState = document.getElementById('loading');
const errorState = document.getElementById('error');
const emptyState = document.getElementById('empty');
const instanceListContainer = document.getElementById('instance-list');
const searchForm = document.getElementById('search-form');
const searchInput = document.getElementById('search-input');

// Menyembunyikan/Menampilkan section halaman
function displayPageSection({ showLoading = false, showError = false, showEmpty = false, showInstances = false }) {
    loadingState.classList.toggle('hide', !showLoading);
    errorState.classList.toggle('hide', !showError);
    emptyState.classList.toggle('hide', !showEmpty);
    instanceListContainer.classList.toggle('hide', !showInstances);
}

// Mengubah karakter khusus HTML menjadi entity agar ditampilkan sebagai teks
function escapeHtml(value) {
    return String(value ?? '')
        .replaceAll('&', '&amp;')
        .replaceAll('<', '&lt;')
        .replaceAll('>', '&gt;')
        .replaceAll('"', '&quot;')
        .replaceAll("'", '&#39;');
}

// Fetch data 
async function fetchInstances(searchQuery = "") {
    if (instancesAbortController) instancesAbortController.abort();
    instancesAbortController = new AbortController();

    try {
        displayPageSection({ showLoading: true });
        
        const url = searchQuery ? `${BASE_ENDPOINT}?title=${encodeURIComponent(searchQuery)}` : BASE_ENDPOINT;
        
        const response = await fetch(url, {
            headers: { 'Accept': 'application/json' },
            signal: instancesAbortController.signal,
        });

        if (!response.ok) throw new Error('Failed to fetch data');

        const instanceData = await response.json();

        if (instanceData.length === 0) {
            displayPageSection({ showEmpty: true });
        } else {
            instanceListContainer.innerHTML = '';
            instanceData.forEach(item => {
                instanceListContainer.appendChild(buildCardElement(item));
            });
            displayPageSection({ showInstances: true });
        }
    } catch (error) {
        if (error.name === 'AbortError') return;
        console.error(`Error loading ${MODEL_NAME}:`, error);
        displayPageSection({ showError: true });
    }
}

function searchInstances() {
    fetchInstances(searchInput.value.trim());
}

searchInput.addEventListener("input", function() { 
    clearTimeout(searchDebounceTimer);

    searchDebounceTimer = setTimeout(function() {
        searchInstances();
    }, SEARCH_DEBOUNCE_DELAY);
});

searchForm.addEventListener("submit", function(event) {
    event.preventDefault();
    clearTimeout(searchDebounceTimer);
    searchInstances();
});

function closeModal() {
    document.getElementById("add-instance-modal").hidePopover();
}

const modelForm = document.getElementById('model-form');

// Membaca nilai cookie, digunakan untuk mengambil token CSRF
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Mengirim data form ke server
async function addInstance(event) {
    event.preventDefault();

    const submitButton = modelForm.querySelector('button[type="submit"]');
    submitButton.disabled = true;

    try {
        const response = await fetch(CREATE_PROJECT_ENDPOINT, {
            method: 'POST',
            headers: { 'X-CSRFToken': getCookie('csrftoken') },
            body: new FormData(modelForm),
        });
        const result = await response.json().catch(() => ({}));

        if (response.ok) {
            modelForm.reset();
            closeModal();
            showToast('Berhasil', MODEL_NAME + ' baru berhasil ditambahkan!', 'success');
            fetchInstances(searchInput.value.trim());
        } else {
            const errorMessages = result.errors
                ? Object.values(result.errors).flat().map(error => error.message)
                : [result.message || `Terjadi kesalahan (status ${response.status}).`];
            showToast('Gagal menambahkan ' + MODEL_NAME, errorMessages.join(' '), 'error');
        }
    } catch (error) {
        console.error(`Error adding ${MODEL_NAME}: `, error);
        showToast('Gagal menambahkan ' + MODEL_NAME, 'Tidak dapat terhubung ke server. Silakan coba lagi.', 'error');
    } finally {
        submitButton.disabled = false;
    }
}

if (modelForm) {
    modelForm.addEventListener('submit', addInstance);
}

// Start application
fetchInstances(searchInput.value.trim());
