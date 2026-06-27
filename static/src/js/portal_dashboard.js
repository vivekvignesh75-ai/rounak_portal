/** @odoo-module **/

document.addEventListener("DOMContentLoaded", function () {
    const dashboard = document.querySelector(".rounak-dashboard");
    if (!dashboard) return;

    const kpiTiles = dashboard.querySelectorAll(".rounak-kpi-tile");
    kpiTiles.forEach(function (tile) {
        tile.style.opacity = "0";
        tile.style.transform = "translateY(8px)";
    });

    requestAnimationFrame(function () {
        kpiTiles.forEach(function (tile, i) {
            setTimeout(function () {
                tile.style.transition = "opacity 0.3s ease, transform 0.3s ease";
                tile.style.opacity = "1";
                tile.style.transform = "translateY(0)";
            }, i * 60);
        });
    });
});
