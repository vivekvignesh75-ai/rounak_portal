/** @odoo-module **/

document.addEventListener("DOMContentLoaded", function () {
    const sidebar = document.querySelector(".rounak-sidebar");
    if (!sidebar) return;

    const links = sidebar.querySelectorAll(".rounak-sidebar-nav a");
    const current = window.location.pathname;

    links.forEach(function (link) {
        const href = link.getAttribute("href");
        if (href && current.startsWith(href)) {
            link.closest("li").classList.add("active");
        } else {
            link.closest("li").classList.remove("active");
        }
    });
});
