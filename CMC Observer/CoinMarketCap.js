var valores = [{'value': '0', 'datetime': '0'}];

// Código de notificações vindo de:
// https://developer.mozilla.org/pt-BR/docs/Web/API/Notification
var notification = null;
var alteracao = 0;
function notifyMe() {
    // Verifica se o browser suporta notificações
    if (!("Notification" in window)) {
        alert("Este browser não suporta notificações de Desktop");
    }

    else if (Notification.permission !== "denied") {
        Notification.requestPermission(function (permission) {
            if (permission === "granted") {
                notification = new Notification("Permissões ativadas!");
            }
        });
    }
}

function metricas() {
    // var metricas = JSON.stringify(valores);
    var metricas = valores;
    metricas.shift();
    metricas = metricas.map(function(f){ return f.value.slice(1,) })
    var menor = Math.min(... metricas)
    var maior = Math.max(... metricas)
    var m = 0
    var media = function(){ for(c of metricas){ m = Number(m) + Number(c); } return m; }
    media = media();
    console.log(`Maior valor: ${maior}\nMenor valor: ${menor}\nValor médio: ${media/metricas.length}`)
}

document.addEventListener("DOMNodeInserted", function(e){
    // console.log(e);
    if(e.path[4].childNodes[1].childNodes[0].innerHTML.startsWith('$'))  {    
        if(e.path[4].childNodes[1].childNodes[0].innerHTML != valores[valores.length - 1].value){
            valores.push({'value': e.path[4].childNodes[1].childNodes[0].innerHTML, 'datetime': new Date().toISOString()});
            if(valores.length > 2){
                alteracao = valores[valores.length - 1].slice(1,) / valores[1].slice(1,);
                if(alteracao < 1.01){
                    notification = new Notification(`A moeda caiu {alteracao - 1}%`);
                } else {
                    notification = new Notification(`A moeda subiu {alteracao - 1}%`)                
                }
            }
        }
    }
}, false);
