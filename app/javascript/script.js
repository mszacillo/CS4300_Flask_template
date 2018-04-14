$(function(){
	$('button').click(function(){
		var query = $('#input').val();
		$.ajax({
			url: '../python/searchQuery',
			data: $('#search').serialize(),
			type: 'POST',
			success: function(response) {
				console.log(response);
			},
			error: function(error){
				console.log(error);
			}
 
		});
	});
});
