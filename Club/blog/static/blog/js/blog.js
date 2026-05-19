document.addEventListener('DOMContentLoaded', ()=>{
  // dark mode toggle: store in localStorage
  const root = document.documentElement;
  const theme = localStorage.getItem('ice_theme') || 'light';
  root.setAttribute('data-theme', theme);
  // simple toast helper
  window.showToast = function(message){
    const t = document.createElement('div');
    t.className = 'toast align-items-center text-bg-dark border-0 position-fixed';
    t.style.right='1rem';t.style.bottom='1rem';
    t.innerHTML = `<div class="d-flex"><div class="toast-body">${message}</div><button class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button></div>`;
    document.body.appendChild(t);
    const bs = new bootstrap.Toast(t, {});
    bs.show();
    setTimeout(()=>{bs.hide(); t.remove()}, 4000);
  }
});
