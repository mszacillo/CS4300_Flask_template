function getIndicesOf(searchStr, str, caseSensitive) {
    var searchStrLen = searchStr.length;
    if (searchStrLen == 0) {
        return [];
    }
    var startIndex = 0, index, indices = [];
    if (!caseSensitive) {
        str = str.toLowerCase();
        searchStr = searchStr.toLowerCase();
    }
    while ((index = str.indexOf(searchStr, startIndex)) > -1) {
        indices.push(index);
        startIndex = index + searchStrLen;
    }
    return indices;
}

function getLyricshtml(query,lyricstring){
	var indices = getIndicesOf(lyricstring,query,false);
	if(indices.length > 0){
		console.log("hello")
	}
	return lyricstring
}

$(window).ready(function(){
	function getResults(){
		var query = JSON.stringify({"search":$('#input').val(),"sentiment":$('#selecter').val()});
		$.ajax({
			url: 'search',
			data: query,
			contentType:'application/json',
			type: 'POST',
			success: function(response) {
				j = JSON.parse(response).data;
				var htmlOutput = '';
				htmlOutput += "<table class='table'><thead><tr><th></th><th width='45%'>Title</th><th>Artist</th><th>Match Score</th><th width='4%'></th></thead><tbody>"
				highestindex = Math.min(20,j.length)
				for(var i = 0; i < highestindex; i++){
					console.log(searchsong)
					var embedded = searchsong(j[i]['artist'],j[i]['title'])
					var lyrics = getLyricshtml(String(query),String(j[i]['lyrics']))
					htmlOutput += "<tr data-lyrics='"+String(2*i+2)+"'><td>"+embedded+"</td><td>" + j[i]['title'] + "</td>"
					+ "<td>" + j[i]['artist'] + "</td>"
					+ "<td>" + (j[i]['score']).toFixed(2) + "</td>"
					+ "<td class='imgholder'><img class='lyricsbutton' src='/static/images/lyrics.png'></img></td>"
					+ "</tr>"
					+ "<tr class='hidden'><td Colspan='5' class='lyrics'><div class='lyricsdiv'>"+lyrics+"</div></td></tr>"
				};
				htmlOutput += "</tbody></table>";
				$('.searchresults').html(htmlOutput)

				$('.imgholder').on('click',function(){
					index = Number($(this).closest('tr').attr('data-lyrics'))
					myself= $("tr:nth-of-type("+String(index)+")")
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
	$('.categorysearchlink').click(function(){
		$('.mood-groups').toggleClass('hidden')
		$('.form-group').toggleClass('hidden')
	});
	$('.mood').click(function(){
		$(this).toggleClass('mood-selected')
	})
});
