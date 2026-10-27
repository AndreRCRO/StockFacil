const sidebar = document.getElementById('sidebar');
const menuToggle = document.querySelector('[data-menu-toggle]');
const overlay = document.querySelector('[data-menu-overlay]');
const mobileMenuQuery = window.matchMedia('(max-width: 800px)');
if (sidebar) sidebar.inert = mobileMenuQuery.matches;
function setMenu(open) {
    if (sidebar) sidebar.inert = mobileMenuQuery.matches && !open;
    sidebar?.classList.toggle('is-open', open);
    if (overlay) overlay.hidden = !open;
    menuToggle?.setAttribute('aria-expanded', String(open));
    if (open) sidebar?.querySelector('[data-menu-close]')?.focus();
    else menuToggle?.focus();
}
menuToggle?.addEventListener('click', () => setMenu(!sidebar.classList.contains('is-open')));
document.querySelector('[data-menu-close]')?.addEventListener('click', () => setMenu(false));
overlay?.addEventListener('click', () => setMenu(false));
document.addEventListener('keydown', event => {
    if (!sidebar?.classList.contains('is-open')) return;
    if (event.key === 'Escape') setMenu(false);
    if (event.key === 'Tab') {
        const items = [...sidebar.querySelectorAll('a,button')];
        const first = items[0], last = items.at(-1);
        if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last.focus(); }
        else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); }
    }
});
mobileMenuQuery.addEventListener('change', () => setMenu(false));
document.querySelectorAll('form[data-confirm]').forEach(form => form.addEventListener('submit', event => {
    if (!window.confirm(form.dataset.confirm)) event.preventDefault();
}));
document.querySelectorAll('[data-submit-form]').forEach(form => form.addEventListener('submit', () => {
    const button = form.querySelector('button[type="submit"]');
    if (button) { button.disabled = true; button.setAttribute('aria-busy', 'true'); button.textContent = button.dataset.loadingText || 'Guardando…'; }
}));
// Browsers may restore a previously submitted form from the back-forward cache.
window.addEventListener('pageshow', event => { if (event.persisted) window.location.reload(); });
const movementForm = document.querySelector('[data-movement-form]');
if (movementForm) {
    const select = movementForm.querySelector('[data-product-select]');
    const quantity = movementForm.querySelector('[data-quantity]');
    const preview = document.querySelector('[data-preview]');
    function updatePreview() {
        const option = select.selectedOptions[0];
        preview.hidden = !select.value;
        if (!select.value) return;
        const current = Number(option.dataset.stock);
        const minimum = Number(option.dataset.minimum);
        const amount = Number(quantity.value);
        const type = movementForm.querySelector('input[name="type"]:checked')?.value;
        const valid = Number.isInteger(amount) && amount > 0;
        const next = current + (type === 'entrada' ? amount : -amount);
        document.querySelector('[data-current-stock]').textContent = current;
        document.querySelector('[data-next-stock]').textContent = valid ? next : '—';
        preview.classList.toggle('invalid', valid && next < 0);
        document.querySelector('[data-preview-note]').textContent = !valid ? 'Ingresa la cantidad para calcular el resultado.' : next < 0 ? 'La salida supera el stock disponible. Reduce la cantidad.' : next <= minimum ? 'El producto quedará con una alerta de stock.' : 'El producto tendrá stock disponible.';
    }
    movementForm.addEventListener('input', updatePreview);
    movementForm.addEventListener('change', updatePreview);
    updatePreview();
}
