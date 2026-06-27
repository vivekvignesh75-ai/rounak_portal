/** @odoo-module **/

document.addEventListener("DOMContentLoaded", function () {
    const DEPARTMENTS = [
        { name: "Sales & Enquiries", icon: "fa-line-chart", channel: "sales" },
        { name: "Support & Service", icon: "fa-life-ring", channel: "support" },
        { name: "Billing & Accounts", icon: "fa-file-text-o", channel: "billing" },
        { name: "Licensing & Subscriptions", icon: "fa-key", channel: "licensing" },
    ];

    function injectRouter() {
        if (document.querySelector(".rounak-livechat-router")) return;

        const btn = document.createElement("button");
        btn.className = "rounak-livechat-fab";
        btn.innerHTML = '<i class="fa fa-comments"></i>';
        btn.title = "Chat with us";
        btn.addEventListener("click", togglePanel);
        document.body.appendChild(btn);

        const panel = document.createElement("div");
        panel.className = "rounak-livechat-router";
        panel.style.display = "none";
        panel.innerHTML =
            '<div class="rounak-lc-header">' +
            '  <span>How can we help you today?</span>' +
            '  <button class="rounak-lc-close" title="Close">&times;</button>' +
            "</div>" +
            '<div class="rounak-lc-body"></div>';
        document.body.appendChild(panel);

        panel.querySelector(".rounak-lc-close").addEventListener("click", togglePanel);

        const body = panel.querySelector(".rounak-lc-body");
        DEPARTMENTS.forEach(function (dept) {
            const item = document.createElement("a");
            item.href = "#";
            item.className = "rounak-lc-dept";
            item.innerHTML =
                '<i class="fa ' + dept.icon + '"></i> ' + dept.name;
            item.addEventListener("click", function (e) {
                e.preventDefault();
                panel.style.display = "none";
                var lcBtn = document.querySelector(".o_livechat_button");
                if (lcBtn) lcBtn.click();
            });
            body.appendChild(item);
        });

        var offline = document.createElement("div");
        offline.className = "rounak-lc-offline";
        offline.innerHTML =
            '<p class="text-muted" style="font-size:12px;margin:8px 0 0;">' +
            "No operators available? " +
            '<a href="/my/rounak/support">Submit a ticket</a> instead.</p>';
        body.appendChild(offline);
    }

    function togglePanel() {
        var panel = document.querySelector(".rounak-livechat-router");
        if (panel) {
            panel.style.display = panel.style.display === "none" ? "block" : "none";
        }
    }

    if (document.querySelector(".rounak-sidebar")) {
        injectRouter();
    }
});
