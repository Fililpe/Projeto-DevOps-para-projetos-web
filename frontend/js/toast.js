function mostraToast(mensagem, tipo = "success") {
  const container = document.getElementById("toastContainer");

  const toastEl = document.createElement("div");
  toastEl.className = `toast align-items-center text-bg-${tipo} border-0`;
  toastEl.setAttribute("role", tipo === "danger" ? "alert" : "status");
  toastEl.setAttribute("aria-live", tipo === "danger" ? "assertive" : "polite");
  toastEl.setAttribute("aria-atomic", "true");

  toastEl.innerHTML = `
    <div class="d-flex">
      <div class="toast-body"></div>
      <button
        type="button"
        class="btn-close btn-close-white me-2 m-auto"
        data-bs-dismiss="toast"
        aria-label="Fechar"
      ></button>
    </div>
  `;
  // textContent evita que o texto seja interpretado como HTML
  toastEl.querySelector(".toast-body").textContent = mensagem;

  container.appendChild(toastEl);

  const toast = new bootstrap.Toast(toastEl, { delay: 3000 });
  toastEl.addEventListener("hidden.bs.toast", () => toastEl.remove());
  toast.show();
}
