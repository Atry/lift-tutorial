function remove_node(node){node.parentNode.removeChild(node);}
window.onload=function(){
Array.prototype.slice.call(document.querySelectorAll(".formula")).forEach(function(e){katex.render(e.getAttribute("alt"),e,{displayMode:e.tagName==="DIV"})});
remove_node(document.getElementsByTagName("link")[0]);
};
