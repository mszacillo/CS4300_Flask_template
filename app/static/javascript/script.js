$(window).ready(function(){
	function getResults(){
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
				htmlOutput += "<table class='table'><thead><tr><th></th><th width='45%'>Title</th><th>Artist</th><th>Match Score</th><th width='4%'></th></thead><tbody>"
				for(var i = 0; i < 10; i++){
					htmlOutput += "<tr data-lyrics='"+String(2*i+2)+"'><td>Play</td><td>" + j[i]['title'] + "</td>"
					+ "<td>" + j[i]['artist'] + "</td>"
					+ "<td>" + (j[i]['score']).toFixed(2) + "</td>"
					+ "<td class='imgholder'><img class='lyricsbutton' src='/static/images/lyrics.png'></img></td>"
					+ "</tr>"
					+ "<tr class='hidden'><td Colspan='5' class='lyrics'>"+j[i]['lyrics']+"</td></tr>"
				};
				htmlOutput += "</tbody></table>";
				$('.searchresults').html(htmlOutput)

				$('.imgholder').on('click',function(){
					index = Number($(this).closest('tr').attr('data-lyrics'))
					console.log(index)
					myself= $("tr:nth-of-type("+String(index)+")")
					console.log(myself)
					if(myself.hasClass('hidden')){
						myself.removeClass('hidden')
					}
					else{
						myself.addClass('hidden')
					}
				});
			},
			error: function(error){
				console.log(error);
			}
		});
	};
	$('button').click(function(){
		getResults();
		return false;
	});
	$('form').submit(function(){
		getResults();
		return false;
	})
});
