$.fn.fullpage.setAllowScrolling(false);

$("#back").click(function(){
		window.location.replace('#firstPage/1')
})

$("#search").focus(function(){
		$("#searchBar").css({'opacity': '1','transition': 'opacity 0.5s linear'});
	});
$("#search").focusout(function(){
	$("#searchBar").css({'opacity': '0.1','transition': 'opacity 0.5s linear'});
});
$("#search").keyup(function(event){
	    if(event.keyCode == 13){
	        $("#clicker").click();
	        $('#search').blur();
	    }
});
