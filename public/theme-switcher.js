/* Setcraft marketing site — live theme toggle.
   The page's resting skin is Yacht Rock. The toggle offers five of the app's
   themes; the choice persists in localStorage and is applied to <html>
   synchronously on load to avoid a flash of the default theme.

   This is a self-contained marketing gag, not the app's real theme engine.
   The brand mark (raspberry -> coral -> amber) stays constant across the
   themes, so it is never recoloured here. */
(function () {
    var STORAGE_KEY = 'sc-site-theme';
    var DEFAULT = 'yacht';
    var THEMES = ['yacht', '808', 'synthwave', 'metal', 'typo'];

    function applyTheme(theme) {
        if (THEMES.indexOf(theme) === -1) theme = DEFAULT;
        // Suppress transitions during the swap. A CSS transition on `background`
        // freezes the value when a theme custom-property changes via attribute,
        // so we cloak transitions, flip the attribute, then restore them.
        var root = document.documentElement;
        root.classList.add('sc-theming');
        root.setAttribute('data-site-theme', theme);
        try { localStorage.setItem(STORAGE_KEY, theme); } catch (e) {}
        // Force a reflow so the new values paint before transitions return.
        void root.offsetHeight;
        requestAnimationFrame(function () {
            requestAnimationFrame(function () { root.classList.remove('sc-theming'); });
        });
        // Swap the favicon to the active theme's icon, mirroring the app.
        var fav = document.getElementById('favicon');
        if (fav) fav.setAttribute('href', 'assets/icons/icon-' + theme + '.svg');
        // Reflect selection on any toggle buttons.
        document.querySelectorAll('[data-theme-btn]').forEach(function (b) {
            b.setAttribute('aria-pressed', b.getAttribute('data-theme-btn') === theme ? 'true' : 'false');
        });
    }

    // Apply immediately to avoid FOUC.
    var stored;
    try { stored = localStorage.getItem(STORAGE_KEY); } catch (e) {}
    applyTheme(stored || DEFAULT);

    window.SetcraftTheme = {
        apply: applyTheme,
        current: function () {
            try { return localStorage.getItem(STORAGE_KEY) || DEFAULT; } catch (e) { return DEFAULT; }
        },
        all: THEMES.slice()
    };

    document.addEventListener('DOMContentLoaded', function () {
        applyTheme(window.SetcraftTheme.current());
        document.querySelectorAll('[data-theme-btn]').forEach(function (b) {
            b.addEventListener('click', function () {
                applyTheme(b.getAttribute('data-theme-btn'));
            });
        });
    });
})();
