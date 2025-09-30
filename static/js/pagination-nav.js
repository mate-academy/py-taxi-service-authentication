(() => {
    const CONTENT_REGION_SELECTOR = ".content-inner";
    const FETCH_HEADERS = {"X-Requested-With": "XMLHttpRequest"};
    const REQUEST_TIMEOUT_MS = 8000;

    let activeRequestController = null;

    if ("scrollRestoration" in history) {
        history.scrollRestoration = "manual";
    }

    const isSameOriginURL = (href) => {
        try {
            const parsedURL = new URL(href, location.href);
            return parsedURL.origin === location.origin;
        } catch {
            return false;
        }
    };

    const areURLsIdentical = (leftHref, rightHref) => {
        try {
            const left = new URL(leftHref, location.href);
            const right = new URL(rightHref, location.href);
            return left.href === right.href;
        } catch {
            return false;
        }
    };

    const setLinkLoadingState = (linkElement, isLoading) => {
        if (!linkElement) return;
        linkElement.classList.toggle("is-loading", isLoading);
        linkElement.setAttribute("aria-disabled", isLoading ? "true" : "false");
        linkElement.style.pointerEvents = isLoading ? "none" : "";
    };

    const setGlobalBusyState = (enabled) => {
        document.documentElement.classList.toggle("is-busy", enabled);
    };

    const parseContentRegionFromHTML = (htmlText) => {
        const parsedDocument = new DOMParser().parseFromString(
            htmlText,
            "text/html",
        );
        return parsedDocument.querySelector(CONTENT_REGION_SELECTOR);
    };

    const updateDocumentTitleFromHTML = (htmlText) => {
        const match = htmlText.match(/<title[^>]*>([\s\S]*?)<\/title>/i);
        if (match) document.title = match[1].trim();
    };

    const focusPrimaryHeading = (containerElement) => {
        if (!containerElement) return;
        const headingElement =
            containerElement.querySelector("h1, [role='heading']") ||
            containerElement;

        const previousTabIndex = headingElement.getAttribute("tabindex");
        headingElement.setAttribute("tabindex", "-1");
        headingElement.focus({preventScroll: false});
        if (previousTabIndex === null) headingElement.removeAttribute("tabindex");
    };

    const swapContentRegion = (nextContainerElement) => {
        const currentContainer = document.querySelector(CONTENT_REGION_SELECTOR);
        if (!currentContainer || !nextContainerElement) return;

        currentContainer.replaceWith(nextContainerElement);

        window.dispatchEvent(
            new CustomEvent("spa:navigated", {
                detail: {container: nextContainerElement},
            }),
        );

        focusPrimaryHeading(nextContainerElement);
    };

    const performNavigation = async (
        destinationURL,
        triggerLinkElement,
        {pushHistory} = {pushHistory: true},
    ) => {
        const containerElement = document.querySelector(CONTENT_REGION_SELECTOR);

        if (!containerElement || !isSameOriginURL(destinationURL)) {
            location.assign(destinationURL);
            return;
        }

        if (areURLsIdentical(destinationURL, location.href)) {
            return; // no-op: already at the same URL
        }

        if (activeRequestController) activeRequestController.abort();
        const requestController = new AbortController();
        activeRequestController = requestController;

        const timeoutId = setTimeout(() => {
            try {
                requestController.abort("timeout");
            } catch {
            }
        }, REQUEST_TIMEOUT_MS);

        setLinkLoadingState(triggerLinkElement, true);
        setGlobalBusyState(true);
        containerElement.setAttribute("aria-busy", "true");

        try {
            const response = await fetch(destinationURL, {
                headers: FETCH_HEADERS,
                signal: requestController.signal,
                cache: "no-store",
            });

            if (!response.ok) {
                location.assign(destinationURL);
                return;
            }

            const htmlText = await response.text();
            const nextContainerElement = parseContentRegionFromHTML(htmlText);

            if (!nextContainerElement) {
                location.assign(destinationURL);
                return;
            }

            swapContentRegion(nextContainerElement);
            updateDocumentTitleFromHTML(htmlText);

            if (pushHistory) {
                history.pushState({spa: true}, "", destinationURL);
            }
        } catch (error) {
            const aborted =
                (error instanceof DOMException && error.name === "AbortError") ||
                error === "timeout";
            if (!aborted) location.assign(destinationURL);
        } finally {
            clearTimeout(timeoutId);

            if (activeRequestController === requestController) {
                activeRequestController = null;
            }

            const freshContainer = document.querySelector(CONTENT_REGION_SELECTOR);
            if (freshContainer) freshContainer.removeAttribute("aria-busy");

            setGlobalBusyState(false);
            setLinkLoadingState(triggerLinkElement, false);
        }
    };

    document.addEventListener("click", (event) => {
        if (!event.target.closest("nav.pagination-bar")) return;

        const linkElement = event.target.closest(
            "a.page-link[data-role='pager-link']",
        );
        if (!linkElement) return;

        if (
            event.metaKey ||
            event.ctrlKey ||
            event.shiftKey ||
            event.altKey ||
            event.button === 1 ||
            linkElement.getAttribute("aria-disabled") === "true" ||
            linkElement.target === "_blank"
        ) {
            return;
        }

        event.preventDefault();
        void performNavigation(linkElement.href, linkElement, {
            pushHistory: true,
        });
    });

    window.addEventListener("popstate", (event) => {
        if (event.state && event.state.spa) {
            void performNavigation(location.href, null, {pushHistory: false});
        }
    });
})();
