let trace = {
    x: [],
    y: [],
    mode: "lines+markers",
    line: { color: "royalblue", width: 3 },
    marker: { size: 8 },
    name: "dane"
};

let layout = {
    title: "Symulowane dane w czasie rzeczywistym",
    margin: { l: 40, r: 30, b: 40, t: 40 },
    yaxis: { range: [5, 27] }
};

Plotly.newPlot('plotly-div', [trace], layout, {responsive: true});

function updatePlot(data) {
    let x = data.map(p => p.x);
    let y = data.map(p => p.y);
    Plotly.update("plotly-div", {x: [x], y: [y]}, {}, [0]);
}

// Fetch + aktualizacja co 2 sekundy
setInterval(() => {
    fetch("/api/data")
      .then(resp => resp.json())
      .then(updatePlot);
}, 2000);

// pobierz pierwsze dane
fetch("/api/data").then(resp => resp.json()).then(updatePlot);
