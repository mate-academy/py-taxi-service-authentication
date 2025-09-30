document.addEventListener("DOMContentLoaded", () => {
    const tables = document.querySelectorAll(".cars-table");

    const getHref = (row) =>
        row.querySelector(".row-link")?.getAttribute("href") || row.dataset.href;

    const isInteractive = (element) =>
        element.closest("a, button, input, textarea, select, [role='button']");

    const handleClick = (event) => {
        const row = event.target.closest("tr[data-href]");
        if (!row || isInteractive(event.target)) return;

        const href = getHref(row);
        if (!href) return;

        if (event.metaKey || event.ctrlKey) {
            window.open(href, "_blank", "noopener, noreferrer");
        } else {
            window.location.assign(href);
        }
    };

    const handleAuxClick = (event) => {
        if (event.button !== 1) return;

        const row = event.target.closest("tr[data-href]");
        if (!row || isInteractive(event.target)) return;

        const href = getHref(row);
        if (!href) return;

        window.open(href, "_blank", "noopener, noreferrer");
    };

    tables.forEach((table) => {
        const tbody = table.querySelector("tbody");
        if (!tbody) return;

        tbody.addEventListener("click", handleClick);
        tbody.addEventListener("auxclick", handleAuxClick);
    });
});
