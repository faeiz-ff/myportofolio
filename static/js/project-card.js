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


    const git_link = `<a class="link-button" href="${project.git_link}">GitHub</a>`;
    const other_link = project.other_link
        ? `<a class="link-button" href="${project.other_link}">Website</a>`
        : '';

    // Komponen card
    const completeCardHtml = `
        <article>
            <h2>${escapeHtml(project.title)}</h2>
            <p>${project.time_range_str}</p>
            <nav class="actions">
                ${git_link}
                ${other_link}
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
            </nav>
            <p>${escapeHtml(project.description)}</p>
        </article>
    `;

    listElement.innerHTML = completeCardHtml;
    return listElement;
}
