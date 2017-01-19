$("#back").click(function(){
		window.location.replace('#firstPage/1')
})

$("#search").keyup(function(event){
	    if(event.keyCode == 13){
	        $("#clicker").click();
	        $('#search').blur();
	    }
});

$(document).ready(function(){
	$.fn.fullpage.setAllowScrolling(false);
});
