$(document).ready(function(){
	resizeDiv();
});

window.onresize = function(event) {
	resizeDiv();
	console.log($("a.navbar-brand").css('margin-right'));
}

function resizeDiv() {
	$("a.navbar-brand").css("margin-right", parseInt($(window).width())*0.4 + "px");
}

$(document).ready(function() {
  
});

