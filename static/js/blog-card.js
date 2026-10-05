// Membuat elemen card blog
function buildCardElement(item) {
    const blog = item.fields;

    const listElement = document.createElement('li');

    // Dummy UUID digunakan untuk digantikan oleh ID asli dari data JSON
    const blogPostUrl = BASE_BLOG_POST_URL.replace('Manifesto', encodeURIComponent(blog.title));

    const completeCardHtml = `
        ${blog.created_at}
        <a href="${blogPostUrl}">${escapeHtml(blog.title)}</a>
    `;

    listElement.innerHTML = completeCardHtml;
    return listElement;
}
