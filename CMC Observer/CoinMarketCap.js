var valores = [];
document.addEventListener("DOMNodeInserted", function(e){
    if(e.path[4].childNodes[1].childNodes[0].innerHTML.startsWith('$'))  {    
//        valores.push(e.target);
        valores.push(e.path[4].childNodes[1].childNodes[0].innerHTML);
    }
//    console.log(e);
}, false);
