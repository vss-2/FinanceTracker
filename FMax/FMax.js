// ==UserScript==
// @name         Futemax Player Expandido
// @namespace    http://tampermonkey.net/
// @version      1.0
// @description  Expansão no player do Futemax
// @author       github.com/vss-2
// @match        https://futemax.gratis/assistir-*
// @icon         https://www.google.com/s2/favicons?domain=futemax.gratis
// @grant        none
// ==/UserScript==

(function() {
    'use strict';
    console.log('olá futemax');
    document.getElementById('content').style.minWidth = '100%';
    document.getElementsByClassName('image-post')[0].style.minWidth = '100%';
    document.getElementsByClassName('box post')[0].style.minWidth = '100%';
    document.getElementsByClassName('replace_html')[0].style.minWidth = String(document.documentElement.clientWidth)+'px';
    document.getElementsByClassName('replace_html')[0].children[0].style.height = String(Math.floor(document.documentElement.clientHeight * 0.95))+'px';

    const observer = new MutationObserver(
        function(mut){
            console.log('desgrama');
            setTimeout(
                function(){
                    document.body.style.minHeight = '100%';
                    document.getElementsByClassName('replace_html')[0].style.minWidth = String(document.documentElement.clientWidth)+'px';;
                    document.getElementsByClassName('replace_html')[0].children[0].style.height = String(Math.floor(document.documentElement.clientHeight * 0.95))+'px';;
                }
                , 2000);
        }
    );
    
    observer.observe(
        document.getElementsByClassName('replace_html')[0],
        { characterData: true, attributes: true, childList: true, subtree: true }
);

})();
