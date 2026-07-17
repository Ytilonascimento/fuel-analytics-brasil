const botao = document.getElementById("buscar");

botao.addEventListener("click", buscarCidade);

const botaoComparar = document.getElementById("comparar");

botaoComparar.addEventListener("click", compararCidades);

async function buscarCidade() {

    const cidade = document.getElementById("cidade").value;

    if (cidade === "") {

        alert("Digite uma cidade.");

        return;
    }

    try {

        const resposta = await fetch(
            `http://127.0.0.1:8000/combustivel?cidade=${cidade}`
        );

        const dados = await resposta.json();

        mostrarResultado(dados);

    } catch (erro) {

        alert("Erro ao conectar com a API.");

        console.log(erro);

    }

}

function mostrarResultado(dados) {

    const resultado = document.getElementById("resultado");

    let cards = "";

for (const combustivel in dados.precos) {

    let icone = "⛽";
    let classe = "padrao";

    if (combustivel.includes("ETANOL")) {
        icone = "🌱";
        classe = "etanol";
    }

    else if (combustivel.includes("GASOLINA")) {
        icone = "🟡";
        classe = "gasolina";
    }

    else if (combustivel.includes("DIESEL")) {
        icone = "⚫";
        classe = "diesel";
    }

    else if (combustivel.includes("GNV")) {
        icone = "🔵";
        classe = "gnv";
    }

    cards += `
        <div class="card-combustivel ${classe}">

            <h3>${icone} ${combustivel}</h3>

            <p>
                R$ ${dados.precos[combustivel].toFixed(2)}
            </p>

        </div>
    `;
}

    resultado.innerHTML = `

    <div class="dashboard">

    <div class="kpi">

        <span>📍</span>

        <h4>Cidade</h4>

        <h2>${dados.cidade}</h2>

    </div>

    <div class="kpi">

        <span>🏆</span>

        <h4>Melhor opção</h4>

        <h2>${dados.melhor_opcao}</h2>

    </div>

    <div class="kpi">

        <span>💲</span>

        <h4>Menor preço</h4>

        <h2>R$ ${dados.estatisticas.menor_preco}</h2>

    </div>

    <div class="kpi">

        <span>⛽</span>

        <h4>Produtos</h4>

        <h2>${Object.keys(dados.precos).length}</h2>

    </div>

</div>

        <h2>${dados.cidade}</h2>

        <div class="cards">
            ${cards}
        </div>

        <div class="info">

            <p><strong>Melhor opção:</strong>
            ${dados.melhor_opcao}</p>

            <p><strong>Mais barato:</strong>
            ${dados.estatisticas.combustivel_mais_barato}
            (R$ ${dados.estatisticas.menor_preco})</p>

            <p><strong>Mais caro:</strong>
            ${dados.estatisticas.combustivel_mais_caro}
            (R$ ${dados.estatisticas.maior_preco})</p>

        </div>

        <hr>

<h3>📈 Gráfico dos Combustíveis</h3>

<canvas id="graficoCombustiveis"></canvas>
`;

criarGrafico(dados);
}

let grafico = null;

let graficoComparacao = null;

function criarGrafico(dados) {

    const canvas = document.getElementById("graficoCombustiveis");

    if (!canvas) {
        return;
    }

    if (grafico) {
        grafico.destroy();
    }

    const labels = Object.keys(dados.precos);

const valores = Object.values(dados.precos);

const cores = labels.map(combustivel => {

    if (combustivel.includes("ETANOL"))
        return "#22c55e";

    if (combustivel.includes("GASOLINA"))
        return "#f59e0b";

    if (combustivel.includes("DIESEL"))
        return "#374151";

    if (combustivel.includes("GNV"))
        return "#2563eb";

    return "#6b7280";

});

grafico = new Chart(canvas, {

    type: "bar",

    data: {

        labels: labels,

        datasets: [{

            label: "Preço Médio (R$)",

            data: valores,

            backgroundColor: cores,

            borderColor: "#ffffff",

            borderWidth: 1,

            borderRadius: 8,

            barThickness: 45,

            maxBarThickness: 50


        }]

    },

options: {

    responsive: true,

    maintainAspectRatio: false,

    animation: {

        duration: 1500

    },

    plugins: {

        legend: {

            display: true,

            position: "top"

        },

        tooltip: {

            callbacks: {

                label: function(context) {

                    return "R$ " + context.raw.toFixed(2);

                }

            }

        }

    },

scales: {

    y: {

        min: 4,

        max: 8,

        ticks: {

            stepSize: 0.5

        }

    }

}

        }

    });

}

async function compararCidades() {

    const cidade1 = document.getElementById("cidade1").value;
    const cidade2 = document.getElementById("cidade2").value;

    if (cidade1 === "" || cidade2 === "") {

        alert("Digite as duas cidades.");
        return;

    }

    try {

        const resposta = await fetch(
            `http://127.0.0.1:8000/comparar?cidade1=${cidade1}&cidade2=${cidade2}`
        );

        const dados = await resposta.json();

        mostrarComparacao(dados);

    } catch (erro) {

        alert("Erro ao comparar cidades.");

        console.log(erro);

    }

}

function mostrarComparacao(dados) {

    const resultado = document.getElementById("resultado");

    let html = `

        <h2>📊 Comparação</h2>

        <h3>${dados.cidade1} × ${dados.cidade2}</h3>

        <table class="tabela-comparacao">

            <tr>
                <th>Combustível</th>
                <th>${dados.cidade1}</th>
                <th>${dados.cidade2}</th>
                <th>Melhor preço</th>
            </tr>

    `;

dados.comparacao.forEach(item => {

    html += `

        <tr>

            <td>

${item.combustivel.includes("ETANOL") ? "🌱" :
item.combustivel.includes("GASOLINA") ? "🟡" :
item.combustivel.includes("DIESEL") ? "⚫" :
item.combustivel.includes("GNV") ? "🔵" :
"⛽"}

${item.combustivel}

</td>

            <td class="${
                item.mais_barata === dados.cidade1
                    ? "melhor-preco"
                    : ""
            }">
                R$ ${item.cidade1.toFixed(2)}
            </td>

            <td class="${
                item.mais_barata === dados.cidade2
                    ? "melhor-preco"
                    : ""
            }">
                R$ ${item.cidade2.toFixed(2)}
            </td>

            <td>

                <span class="badge">

                    🏆 ${item.mais_barata}

                </span>

            </td>

        </tr>

    `;

});

html += `
</table>

<hr>

<h3>📊 Comparação Visual</h3>

<div class="grafico-container">
    <canvas id="graficoComparacao"></canvas>
</div>
`;

resultado.innerHTML = html;

criarGraficoComparacao(dados);

}

function criarGraficoComparacao(dados){

    const canvas = document.getElementById("graficoComparacao");

    if(!canvas){
        return;
    }

    if(graficoComparacao){
        graficoComparacao.destroy();
    }

    const labels = dados.comparacao.map(item => item.combustivel);

    const cidade1 = dados.comparacao.map(item => item.cidade1);

    const cidade2 = dados.comparacao.map(item => item.cidade2);

    graficoComparacao = new Chart(canvas,{

        type:"bar",

        data:{

            labels:labels,

            datasets:[

                {

                    label:dados.cidade1,

                    data:cidade1

                },

                {

                    label:dados.cidade2,

                    data:cidade2

                }

            ]

        },

        options:{

            responsive:true,

            maintainAspectRatio:false

        }

    });

}