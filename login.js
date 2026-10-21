const formulario = document.getElementById("loginForm");
const mensagem = document.getElementById("loginMensagem");

formulario.addEventListener("submit", async (event)=>{
    event.preventDefault();

    mensagem.textContent="Entrando no sistema....";
    mensagem.className="mensagem";

    const dados ={
        email: document.getElementById("email").value,
        senha: document.getElementById("senha").value
    }

    try{
        const resposta = await fetch("/api/login",{
            method:"POST",
            headers:{"Content-Type":"application/json"},
            body:JSON.stringify(dados)
        });

        const resultado = await resposta.json();

        if(!resposta.ok){
            throw new Error(resultado.erro || "Erro no login");
        }

        window.location.href="/sistema";

    }catch(erro){
        mensagem.textContent = "ERRO: " + erro.message;
        mensagem.className ="mensagem erro";
    }

});