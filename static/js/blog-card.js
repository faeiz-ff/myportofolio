// Membuat elemen card blog
function buildCardElement(blog) {
    const listElement = document.createElement('li');

    // "Manifesto" adalah placeholder judul di BASE_BLOG_POST_URL
    const blogPostUrl = BASE_BLOG_POST_URL.replace('Manifesto', encodeURIComponent(blog.title));

    listElement.innerHTML = `
        ${escapeHtml(blog.created_at_str)}
        <a href="${blogPostUrl}">${escapeHtml(blog.title)}</a>
    `;
    return listElement;
}
