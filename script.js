async function carregarDados() {
    const resp = await fetch('dados.json');
    const canais = await resp.json();
    renderizarCanais(canais);
}

function renderizarCanais(canais) {
    const conteudo = document.getElementById('conteudo');
    conteudo.innerHTML = '';

    canais.forEach(canal => {
        const bloco = document.createElement('div');
        bloco.className = 'canal-bloco';

        const header = document.createElement('h2');
        header.textContent = canal.nome;

        const lista = document.createElement('div');
        lista.className = 'videos-lista';

        canal.videos.forEach(video => {
            const item = document.createElement('div');
            item.className = 'video-item';
            item.innerHTML = `
                <img src="${video.thumbnail}" alt="${video.titulo}">
                <div class="video-info">
                    <h3>${video.titulo}</h3>
                    <p>${video.data}</p>
                </div>
            `;

            item.addEventListener('click', () => {
                mostrarVideo(video.embed_url);
            });

            lista.appendChild(item);
        });

        bloco.appendChild(header);
        bloco.appendChild(lista);
        conteudo.appendChild(bloco);
    });

    setupAcordeao();
}

function mostrarVideo(embedUrl) {
    const container = document.getElementById('player-container');
    const iframe = document.getElementById('video-player');
    iframe.src = embedUrl;
    container.classList.remove('hidden');
}

document.getElementById('fechar-player').addEventListener('click', () => {
    const container = document.getElementById('player-container');
    const iframe = document.getElementById('video-player');
    iframe.src = '';
    container.classList.add('hidden');
});

function setupAcordeao() {
    const canalHeaders = document.querySelectorAll('.canal-bloco h2');

    canalHeaders.forEach(header => {
        header.addEventListener('click', function() {
            const bloco = this.closest('.canal-bloco');
            document.querySelectorAll('.canal-bloco').forEach(item => {
                if (item !== bloco) item.classList.remove('aberto');
            });
            bloco.classList.toggle('aberto');
        });
    });
}

carregarDados();

// Modo Noturno
const botaoModo = document.getElementById('modo-btn');
const corpo = document.body;

// Carregar preferência anterior
if (localStorage.getItem('modo') === 'escuro') {
    corpo.classList.add('modo-escuro');
    botaoModo.textContent = '☀️';
}

// Alternar entre claro/escuro
botaoModo.addEventListener('click', () => {
    corpo.classList.toggle('modo-escuro');
    const modoAtual = corpo.classList.contains('modo-escuro') ? 'escuro' : 'claro';
    botaoModo.textContent = modoAtual === 'escuro' ? '☀️' : '🌙';
    localStorage.setItem('modo', modoAtual);
});
