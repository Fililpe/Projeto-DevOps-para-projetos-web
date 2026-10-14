const form = document.getElementById("formCadastro");
const campos = form.querySelectorAll("input");
const nome = document.getElementById("cNome");
const email = document.getElementById("cEmail");
const senha = document.getElementById("cSenha");
const confirma = document.getElementById("cConfirmaSenha");
const erroCadastro = document.getElementById("erroCadastro");

function validaCampo(input) {
  if (input === nome) {
    if (input.value.length > 0 && input.value.trim() === "") {
      input.setCustomValidity("O nome não pode conter apenas espaços.");
    } else {
      input.setCustomValidity("");
    }
  }

  if (input == senha) {
    if (input.validity.patternMismatch) {
      input.setCustomValidity(
        "A senha deve ter pelo menos 8 caracteres, uma letra maiúcula, uma letra minúscula e um número.",
      );
    } else {
      input.setCustomValidity("");
    }
  }

  if (input == email) {
    if (input.validity.patternMismatch) {
      input.setCustomValidity("Digite um e-mail válido, como nome@dominio.com");
    } else {
      input.setCustomValidity("");
    }
  }

  if (input === confirma) {
    if (input.value !== senha.value) {
      input.setCustomValidity("As senhas não coincidem.");
    } else {
      input.setCustomValidity("");
    }
  }

  const wrapper = input.closest(".campo-wrapper");
  const feedback = wrapper.querySelector(".invalid-feedback");
  feedback.textContent = input.validationMessage;
}

campos.forEach((campo) => {
  campo.addEventListener("input", () => {
    validaCampo(campo);
    erroCadastro.classList.add("d-none");
  });
});

senha.addEventListener("input", () => {
  if (confirma.value !== "") {
    validaCampo(confirma);
  }
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  campos.forEach((campo) => validaCampo(campo));
  form.classList.add("was-validated");

  if (!form.checkValidity()) {
    return;
  }

  const btn = form.querySelector('button[type="submit"]');
  btn.disabled = true;

  try {
    const resposta = await fetch("/api/auth/register", {
      method: "POST",
      credentials: "include",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        nome: nome.value.trim(),
        email: email.value,
        senha: senha.value,
      }),
    });

    if (resposta.status === 409) {
      erroCadastro.textContent = "Este e-mail já está cadastrado.";
      erroCadastro.classList.remove("d-none");
      return;
    }

    if (resposta.status === 422) {
      erroCadastro.textContent = "Dados inválidos.";
      erroCadastro.classList.remove("d-none");
      return;
    }

    if (!resposta.ok) {
      erroCadastro.textContent = "Não foi possível criar a conta.";
      erroCadastro.classList.remove("d-none");
      return;
    }

    window.location.href = "index.html?cadastro=ok";
  } catch (erro) {
    mostraToast("Não foi possível conectar ao servidor.", "danger");
  } finally {
    btn.disabled = false;
  }
});
