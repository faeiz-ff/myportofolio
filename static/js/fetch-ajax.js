const loadingState = document.getElementById('loading');
const errorState = document.getElementById('error');
const emptyState = document.getElementById('empty');
const instanceListContainer = document.getElementById('instance-list');
const searchForm = document.getElementById('search-form');
const searchInput = document.getElementById('search-input');
const modelForm = document.getElementById('model-form');

function displayPageSection({ showLoading = false, showError = false, showEmpty = false, showInstances = false }) {
    if (loadingState) loadingState.classList.toggle('hide', !showLoading);
    if (errorState) errorState.classList.toggle('hide', !showError);
    if (emptyState) emptyState.classList.toggle('hide', !showEmpty);
    if (instanceListContainer) instanceListContainer.classList.toggle('hide', !showInstances);
}

function escapeHtml(value) {
    return String(value ?? '')
        .replaceAll('&', '&amp;')
        .replaceAll('<', '&lt;')
        .replaceAll('>', '&gt;')
        .replaceAll('"', '&quot;')
        .replaceAll("'", '&#39;');
}

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

function buildEndpoint(pattern, id) {
    return pattern.replace('00000000-0000-0000-0000-000000000000', id);
}

function apiErrorMessage(data, status) {
    if (data && data.errors) {
        return Object.values(data.errors)
            .flat()
            .map(err => (typeof err === 'object' && err.message ? err.message : err))
            .join(' ');
    }
    if (data && typeof data === 'object') {
        const messages = Object.values(data).flat().filter(v => typeof v === 'string');
        if (messages.length > 0) return messages.join(' ');
    }
    return data?.message || `Terjadi kesalahan (HTTP ${status}).`;
}

async function writeInstance(url, method = 'POST', body = null) {
    const headers = {
        'Accept': 'application/json',
        'X-CSRFToken': getCookie('csrftoken'),
    };

    const isFormData = body instanceof FormData;
    if (!isFormData && body !== null) {
        headers['Content-Type'] = 'application/json';
    }

    const response = await fetch(url, {
        method,
        headers,
        body: isFormData ? body : (body !== null ? JSON.stringify(body) : undefined),
    });

    if (response.status === 204) return null;
    const data = await response.json().catch(() => ({}));

    if (!response.ok) {
        throw new Error(apiErrorMessage(data, response.status));
    }
    return data;
}

async function fetchInstances(searchQuery = '') {
    if (instancesAbortController) instancesAbortController.abort();
    instancesAbortController = new AbortController();

    try {
        displayPageSection({ showLoading: true });

        const url = new URL(BASE_ENDPOINT, window.location.origin);
        if (searchQuery) {
            url.searchParams.set('title', searchQuery);
        }

        const response = await fetch(url, {
            headers: { 'Accept': 'application/json' },
            signal: instancesAbortController.signal,
        });

        if (!response.ok) throw new Error(`HTTP error ${response.status}`);

        const instanceData = await response.json();

        if (!Array.isArray(instanceData) || instanceData.length === 0) {
            displayPageSection({ showEmpty: true });
        } else {
            instanceListContainer.replaceChildren(...instanceData.map(buildCardElement));
            displayPageSection({ showInstances: true });
        }
    } catch (error) {
        if (error.name === 'AbortError') return;
        console.error(`Error loading ${MODEL_NAME}:`, error);
        displayPageSection({ showError: true });
    }
}

function searchInstances() {
    fetchInstances(searchInput ? searchInput.value.trim() : '');
}

if (searchInput) {
    searchInput.addEventListener('input', function() {
        clearTimeout(searchDebounceTimer);
        searchDebounceTimer = setTimeout(searchInstances, SEARCH_DEBOUNCE_DELAY);
    });
}

if (searchForm) {
    searchForm.addEventListener('submit', function(event) {
        event.preventDefault();
        clearTimeout(searchDebounceTimer);
        searchInstances();
    });
}

function closeModal() {
    const modal = document.getElementById('add-instance-modal');
    if (modal && typeof modal.hidePopover === 'function') {
        modal.hidePopover();
    }
}

async function addInstance(event) {
    event.preventDefault();

    const submitButton = modelForm.querySelector('button[type="submit"]');
    if (submitButton) submitButton.disabled = true;

    try {
        await writeInstance(CREATE_PROJECT_ENDPOINT, 'POST', new FormData(modelForm));
        modelForm.reset();
        closeModal();
        showToast('Berhasil', `${MODEL_NAME} baru berhasil ditambahkan!`, 'success');
        fetchInstances(searchInput ? searchInput.value.trim() : '');
    } catch (error) {
        console.error(`Error adding ${MODEL_NAME}:`, error);
        showToast(`Gagal menambahkan ${MODEL_NAME}`, error.message, 'error');
    } finally {
        if (submitButton) submitButton.disabled = false;
    }
}

if (modelForm) {
    modelForm.addEventListener('submit', addInstance);
}

if (instanceListContainer) {
    instanceListContainer.addEventListener('click', async function(event) {
        const button = event.target.closest('button[data-action]');
        if (!button || button.disabled) return;

        const action = button.dataset.action;
        const instanceId = button.dataset.id;
        if (!instanceId) return;

        if (action === 'delete' && !window.confirm(`Hapus ${MODEL_NAME} ini?`)) return;

        button.disabled = true;
        try {
            const pattern = action === 'star' ? BASE_STAR_URL : BASE_DELETE_URL;
            const targetUrl = buildEndpoint(pattern, instanceId);
            await writeInstance(targetUrl, action === 'star' ? 'POST' : 'DELETE');
            showToast('Berhasil', action === 'star' ? 'Status bintang diperbarui.' : `${MODEL_NAME} berhasil dihapus.`, 'success');
            fetchInstances(searchInput ? searchInput.value.trim() : '');
        } catch (error) {
            console.error(`Error processing ${action} action:`, error);
            showToast('Gagal', error.message, 'error');
        } finally {
            button.disabled = false;
        }
    });
}

fetchInstances(searchInput ? searchInput.value.trim() : '');
