if (new URLSearchParams(window.location.search).get("cadastro") === "ok") {
  mostraToast("Conta criada. Faça login para continuar.");
}

const form = document.getElementById("formLogin");
const erroLogin = document.getElementById("erroLogin");
const campos = form.querySelectorAll("input");
const email = document.getElementById("lEmail");
const senha = document.getElementById("lSenha");

function validaCampo(input) {
  if (input == email) {
    if (input.validity.patternMismatch) {
      input.setCustomValidity("Digite um e-mail válido, como nome@dominio.com");
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
    erroLogin.classList.add("d-none");
  });
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  campos.forEach((campo) => validaCampo(campo));
  form.classList.add("was-validated");

  if (!form.checkValidity()) {
    return;
  }

  const submitBtn = form.querySelector('button[type="submit"]');
  const textoOriginal = submitBtn.textContent;
  submitBtn.disabled = true;
  submitBtn.textContent = "Entrando...";

  try {
    const resposta = await fetch("/api/auth/login", {
      method: "POST",
      credentials: "include",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        email: email.value.trim(""),
        senha: senha.value,
      }),
    });

    if (resposta.status === 401) {
      erroLogin.classList.remove("d-none");
      return;
    }

    if (!resposta.ok) {
      mostraToast(
        "Serviço temporariamente indisponível. Tente novamente em alguns minutos.",
        "danger",
      );
      return;
    }

    const dados = await resposta.json();
    localStorage.setItem("usuario", JSON.stringify(dados.usuario));
    window.location.href = "dashboard.html";
  } catch (erro) {
    mostraToast("Não foi possível conectar ao servidor.", "danger");
  } finally {
    submitBtn.disabled = false;
    submitBtn.textContent = textoOriginal;
  }
});
