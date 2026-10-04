// Membuat elemen card project
function buildCardElement(item) {
    const project = item.fields;
    const projectId = item.pk;

    const listElement = document.createElement('li');

    // Dummy UUID digunakan untuk digantikan oleh ID asli dari data JSON
    const deleteUrl = BASE_DELETE_URL.replace('00000000-0000-0000-0000-000000000000', projectId);
    const starUrl = BASE_STAR_URL.replace('00000000-0000-0000-0000-000000000000', projectId);

    const deleteHtml = IS_SUPERUSER 
        ? `<form method="post" action="${deleteUrl}">
            ${csrf_token}
            <button type="submit" class="button button-danger" onclick="return confirm('Yakin ingin menghapus project ini?');">Hapus</button>
        </form>`
        : '';

    const isStarredClass = project.is_starred ? " is-starred" : "";
    const starText = project.is_starred ? "Unstar" : "Star";

    const starTitle = project.star_count > 0 
        ? `Dibintangi oleh ${escapeHtml(project.starred_by_names)}` 
        : "Jadilah yang pertama memberi star";

    // Komponen card
    const completeCardHtml = `
        <h2>${escapeHtml(project.title)}</h2>
        <div class="actions">
            <form method="post" action="${escapeHtml(starUrl)}" class="star-form">
                ${csrf_token}
                <button type="submit" 
                        class="button button-star${escapeHtml(isStarredClass)}"
                        title="${escapeHtml(starTitle)}">
                    <span aria-hidden="true">★</span>
                    ${escapeHtml(starText)}
                    <span class="star-count">${escapeHtml(project.star_count)}</span>
                </button>
            </form>
            ${deleteHtml}
        </div>
        <p class="experience-description">${escapeHtml(project.description)}</p>
    `;

    listElement.innerHTML = completeCardHtml;
    return listElement;
}
