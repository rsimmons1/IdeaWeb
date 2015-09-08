$("#back").click(function(){
		$( "#displayBlock" ).animate({'left':'100%'}, "slow", function() {$("#loader").css({'opacity': 1})});
})