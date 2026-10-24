document.addEventListener("click", function (event) {
    if (!(event.target instanceof Element)) {
        return;
    }

    const logoutLink = event.target.closest("a[href]");

    if (!logoutLink) {
        return;
    }

    const logoutUrl = new URL(logoutLink.href, window.location.href);
    const route = logoutUrl.pathname.replace(/\/+$/, "").split("/").pop();

    if (route !== "logout") {
        return;
    }

    event.preventDefault();

    if (document.querySelector(".logout-confirm-backdrop")) {
        return;
    }

    const previousFocus = document.activeElement;
    const previousOverflow = document.body.style.overflow;
    const backdrop = document.createElement("div");
    const dialog = document.createElement("section");
    const heading = document.createElement("h2");
    const message = document.createElement("p");
    const actions = document.createElement("div");
    const cancelButton = document.createElement("button");
    const confirmButton = document.createElement("button");

    backdrop.className = "logout-confirm-backdrop";
    dialog.className = "logout-confirm-dialog";
    dialog.setAttribute("role", "dialog");
    dialog.setAttribute("aria-modal", "true");
    dialog.setAttribute("aria-labelledby", "logout-confirm-title");
    heading.id = "logout-confirm-title";
    heading.textContent = "Confirm logout";
    message.textContent = "Are you sure you want to log out?";
    actions.className = "logout-confirm-actions";
    cancelButton.type = "button";
    cancelButton.className = "logout-confirm-cancel";
    cancelButton.textContent = "Cancel";
    confirmButton.type = "button";
    confirmButton.className = "logout-confirm-submit";
    confirmButton.textContent = "Log out";

    actions.append(cancelButton, confirmButton);
    dialog.append(heading, message, actions);
    backdrop.append(dialog);
    document.body.append(backdrop);
    document.body.style.overflow = "hidden";
    cancelButton.focus();

    function closeDialog() {
        backdrop.remove();
        document.body.style.overflow = previousOverflow;

        if (previousFocus instanceof HTMLElement && previousFocus.isConnected) {
            previousFocus.focus();
        }
    }

    cancelButton.addEventListener("click", closeDialog);
    backdrop.addEventListener("click", function (clickEvent) {
        if (clickEvent.target === backdrop) {
            closeDialog();
        }
    });

    dialog.addEventListener("keydown", function (keyEvent) {
        if (keyEvent.key === "Escape") {
            keyEvent.preventDefault();
            closeDialog();
            return;
        }

        if (keyEvent.key === "Tab") {
            keyEvent.preventDefault();

            if (keyEvent.shiftKey) {
                confirmButton.focus();
            } else {
                cancelButton.focus();
            }
        }
    });

    confirmButton.addEventListener("click", function () {
        window.location.assign(logoutUrl.href);
    });
});
