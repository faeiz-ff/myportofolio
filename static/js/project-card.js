// Membuat elemen card project
function buildCardElement(item) {
    const project = item;
    const projectId = item.pk || item.id;

    const listElement = document.createElement('li');

    // Tombol Hapus (hanya untuk Superuser)
    const deleteHtml = IS_SUPERUSER
        ? `<button type="button" 
                   data-action="delete" 
                   data-id="${projectId}" 
                   class="button button-danger">Hapus</button>`
        : '';

    const isStarredClass = project.is_starred ? " is-starred" : "";
    const starText = project.is_starred ? "Unstar" : "Star";
    const starTitle = project.star_count > 0
        ? `Dibintangi oleh ${escapeHtml(project.starred_by_names)}`
        : "Jadilah yang pertama memberi star";

    const git_link = project.git_link
        ? `<a class="link-button" href="${escapeHtml(project.git_link)}">GitHub</a>`
        : '';
    const other_link = project.other_link
        ? `<a class="link-button" href="${escapeHtml(project.other_link)}">Website</a>`
        : '';

    // Komponen card bersih tanpa wrapper form
    const completeCardHtml = `
        <article>
            <h2>${escapeHtml(project.title)}</h2>
            <p>${escapeHtml(project.time_range_str)}</p>
            <nav class="actions">
                ${git_link}
                ${other_link}
                <button type="button" 
                        data-action="star" 
                        data-id="${projectId}" 
                        class="button button-star${escapeHtml(isStarredClass)}"
                        title="${escapeHtml(starTitle)}">
                    <span aria-hidden="true">★</span>
                    ${escapeHtml(starText)}
                    <span class="star-count">${escapeHtml(project.star_count)}</span>
                </button>
                ${deleteHtml}
            </nav>
            <p>${escapeHtml(project.description)}</p>
        </article>
    `;

    listElement.innerHTML = completeCardHtml;
    return listElement;
}
