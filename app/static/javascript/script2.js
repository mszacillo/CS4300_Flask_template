$(window).ready(function(){
	$('#mainform').submit(function(){
		var query = {"search":$('#input').val()};
		$.ajax({
			url: 'search',
			data: query,
			type: 'POST',
			success: function(response) {
				j = JSON.parse(response).data;
				console.log(j);
				console.log(j[0]);
				var htmlOutput = '';
				for(var i = 0; i < 10; i++){
					htmlOutput += "<p> Artist: " + JSON.stringify(j[i]['artist'])
					+ "<br> Title: " + JSON.stringify(j[i]['title'])
					+ "<br> Match Score: " + JSON.stringify(j[i]['score'])
					+ "<br><br>";
				};
				htmlOutput += "</p>";
				$('.searchresults').html(htmlOutput)
			},
			error: function(error){
				console.log(error);
			}
		});
	});
});
