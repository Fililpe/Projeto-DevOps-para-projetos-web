function configuraModalAddProduto() {
  const modalAddProduto = document.getElementById("modalAddProduto");
  const form = document.getElementById("formProduto");
  const campos = form.querySelectorAll("input");
  const nome = document.getElementById("pNome");
  const descricao = document.getElementById("pDescricao");
  const preco = document.getElementById("pPreco");
  const quantidade = document.getElementById("pQtd");

  function validaCampo(input) {
    if (input === nome) {
      if (input.value.length > 0 && input.value.trim() === "") {
        input.setCustomValidity("O nome não pode conter apenas espaços.");
      } else {
        input.setCustomValidity("");
      }
    }

    const wrapper = input.closest(".campo-wrapper");
    const feedback = wrapper.querySelector(".invalid-feedback");
    feedback.textContent = input.validationMessage;
  }

  campos.forEach((campo) => {
    campo.addEventListener("input", () => validaCampo(campo));
  });

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    campos.forEach((campo) => validaCampo(campo));
    form.classList.add("was-validated");

    if (!form.checkValidity()) {
      return;
    }

    const submitBtn = form.querySelector('[type="submit"]');
    submitBtn.disabled = true;

    try {
      const resposta = await fetch("/api/produtos", {
        method: "POST",
        credentials: "include",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          nome: nome.value.trim(),
          descricao: descricao.value.trim(),
          preco: preco.value,
          quantidade: quantidade.value,
        }),
      });

      if (!resposta.ok) {
        mostraToast(
          "Não foi possível adicionar o produto. Tente novamente.",
          "danger",
        );
        return;
      }

      bootstrap.Modal.getInstance(modalAddProduto).hide();
      mostraToast("Produto adicionado.");
      await recarregaTabelaProdutos();
    } catch (error) {
      console.error(error);
      mostraToast(
        "Falha de conexão. Verifique sua internet e tente novamente.",
        "danger",
      );
    } finally {
      submitBtn.disabled = false;
    }
  });

  modalAddProduto.addEventListener("hidden.bs.modal", () => {
    form.reset();
    form.classList.remove("was-validated");
    form.querySelectorAll("input, select, textarea").forEach((campo) => {
      campo.classList.remove("is-invalid", "is-valid");
    });
    form.querySelectorAll(".invalid-feedback").forEach((div) => {
      div.textContent = "";
    });
  });
}

function configuraModalEditProduto() {
  const modalEditProduto = document.getElementById("modalEditProduto");
  const form = document.getElementById("formEditProduto");
  const produtoId = document.getElementById("eId");
  const produtoNome = document.getElementById("eNome");
  const produtoDesc = document.getElementById("eDescricao");
  const produtoPreco = document.getElementById("ePreco");
  const produtoQtd = document.getElementById("eQtd");

  // :not([type="hidden"]) evita pegar o #eId, que não tem .campo-wrapper
  const campos = form.querySelectorAll('input:not([type="hidden"])');

  function validaCampo(input) {
    if (input.id === "eNome") {
      if (input.value.trim() === "") {
        input.setCustomValidity("O nome não pode conter apenas espaços.");
      } else {
        input.setCustomValidity("");
      }
    }
    const wrapper = input.closest(".campo-wrapper");
    const feedback = wrapper.querySelector(".invalid-feedback");
    feedback.textContent = input.validationMessage;
  }

  campos.forEach((campo) => {
    campo.addEventListener("input", () => validaCampo(campo));
  });

  modalEditProduto.addEventListener("show.bs.modal", (event) => {
    const { id, nome, descricao, preco, quantidade } =
      event.relatedTarget.dataset;
    produtoId.value = id;
    produtoNome.value = nome;
    produtoDesc.value = descricao;
    produtoPreco.value = preco;
    produtoQtd.value = quantidade;
  });

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    campos.forEach((campo) => validaCampo(campo));
    form.classList.add("was-validated");

    if (!form.checkValidity()) {
      return;
    }

    const submitBtn = form.querySelector('[type="submit"]');
    submitBtn.disabled = true;

    try {
      const resposta = await fetch(`/api/produtos/${produtoId}`, {
        method: "PUT",
        credentials: "include",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          nome: produtoNome.value.trim(),
          descricao: produtoDesc.value.trim(),
          preco: produtoPreco.value,
          quantidade: produtoQtd.value,
        }),
      });

      if (!resposta.ok) {
        mostraToast(
          "Não foi possível editar o produto. Tente novamente.",
          "danger",
        );
        return;
      }

      bootstrap.Modal.getInstance(modalEditProduto).hide();
      mostraToast("Produto atualizado.");
      await recarregaTabelaProdutos();
    } catch (error) {
      console.error(error);
      mostraToast(
        "Falha de conexão. Verifique sua internet e tente novamente.",
        "danger",
      );
    } finally {
      submitBtn.disabled = false;
    }
  });

  modalEditProduto.addEventListener("hidden.bs.modal", () => {
    form.reset();
    form.querySelectorAll("input, select, textarea").forEach((campo) => {
      campo.classList.remove("is-invalid", "is-valid");
    });
    form.querySelectorAll(".invalid-feedback").forEach((divErro) => {
      divErro.textContent = "";
    });
    form.classList.remove("was-validated");
  });
}

function configuraModalRmProduto() {
  const modalRmProduto = document.getElementById("modalRmProduto");
  const btnRemocao = document.getElementById("btnConfirmarRemocao");
  let produtoId = null;

  modalRmProduto.addEventListener("show.bs.modal", (event) => {
    const { id, nome } = event.relatedTarget.dataset;
    produtoId = id;
    document.getElementById("nomeProdutoRemocao").textContent = nome;
  });

  btnRemocao.addEventListener("click", async () => {
    const modal = bootstrap.Modal.getInstance(modalRmProduto);

    try {
      btnRemocao.disabled = true;

      const resposta = await fetch(`/api/produtos/${produtoId}`, {
        method: "DELETE",
        credentials: "include",
        headers: { "Content-Type": "application/json" },
      });

      if (!resposta.ok) {
        mostraToast(
          "Não foi possível excluir o produto. Tente novamente.",
          "danger",
        );
        modal.hide();
        return;
      }

      modal.hide();
      mostraToast("Produto removido.", "secondary");
      await recarregaTabelaProdutos();
    } catch (error) {
      console.error(error);
      mostraToast(
        "Falha de conexão. Verifique sua internet e tente novamente.",
        "danger",
      );
    } finally {
      btnRemocao.disabled = false;
    }
  });
}

function configuraModalLogout() {
  const modalLogoff = document.getElementById("modalLogout");
  const modal = bootstrap.Modal.getInstance(modalLogoff);

  document
    .getElementById("btnConfirmarLogout")
    .addEventListener("click", async () => {
      try {
        const response = await fetch("/api/auth/logout", {
          method: "POST",
          credentials: "include",
          headers: { "Content-Type": "application/json" },
        });

        if (!response.ok) {
          console.error(`Falha ao sair [${response.status}]`);
          modal.hide();
          mostraToast("Não foi possível sair. Tente novamente.", "danger");
          return;
        }

        localStorage.removeItem("usuario");
        window.location.href = "index.html";
      } catch (error) {
        console.error(error);
        modal.hide();
        mostraToast(
          "Falha de conexão. Verifique sua internet e tente novamente.",
          "danger",
        );
      }
    });
}

configuraModalAddProduto();
configuraModalEditProduto();
configuraModalRmProduto();
configuraModalLogout();
