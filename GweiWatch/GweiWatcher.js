// Monitora valores
const valorMaximo = 100;
let valores    = [];
let timestamps = [];
const observer = new MutationObserver(
    function(mut){
        valores.push(mut[0].addedNodes[0].textContent.split(' ')[0]);
        timestamps.push(new Date());
        if(valores[valores.length-1] < valorMaximo){ 
            new Notification('Entrar no mercado');
        } 
    }
);

function exportarValores(){
	let output = [];
	for(let v = 0; v < valores.length; v++){
		output.push({
			[v]: new Object({
				"price": valores[v], 
				"timestamp": timestamps[v] 
			})
		});
	}
	console.log(JSON.stringify(output));
}

// Download arquivo
function salvar(){
	var valoresBlob = new Blob([exportarValores()], {type: 'application/json'});
	var aTag  = document.createElement('a');
	aTag.href = URL.createObjectURL(valoresBlob);
	aTag.download  = "valores.json";
	aTag.hidden    = true;
	document.body.appendChild(aTag);
	aTag.innerHTML = "Salvar";
	aTag.click();
}

// Observer feito para monitorar http://polygonscan.com
observer.observe(
    document.getElementById('fastgas'), 
    { characterData: true, attributes: true, childList: true } 
);
