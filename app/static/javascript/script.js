$(window).ready(function(){
	$('button').click(function(){
		var query = $('#input').val();
		$.ajax({
			url: 'http://0.0.0.0:5000/search',
			data: $('#search').serialize(),
			type: 'POST',
			success: function(response) {
				console.log(response);
			},
			error: function(error){
				console.log(error);
				console.log("My call failed")
			}
 
		});
	});
});