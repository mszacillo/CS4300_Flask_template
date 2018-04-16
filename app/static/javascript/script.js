$(window).ready(function(){
	$('button').click(function(){
		var query = {"search":$('#input').val()};
		$.ajax({
			url: 'search',
			data: query,
			type: 'POST',
			success: function(response) {
				console.log(response);
				$('.searchresults').html(response)
			},
			error: function(error){
				console.log(error);
			}
 
		});
	});
});