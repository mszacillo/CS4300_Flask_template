$(window).ready(function(){
	$('button').click(function(){
		var query = {"search":$('#input').val()};
		$.ajax({
			url: 'search',
			data: query,
			type: 'POST',
			success: function(response) {
				console.log(response);
				console.log("yayyyy")
			},
			error: function(error){
				console.log(error);
				console.log("My call failed")
			}
 
		});
	});
});