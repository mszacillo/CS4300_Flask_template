token = ""

widgethtml1 = '<iframe src="https://open.spotify.com/embed?uri='
widgethtml2 = '" width="300" height="80" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>'

function searchsong(artist,track,idx){
  //console
  base_url = "https://api.spotify.com/v1/search"
  artistdata = JSON.stringify({"track":track,"artist":artist})
  $.ajax({
    type:'POST',
    url:'getsong',
    contentType: "application/json; charset=utf-8",
    dataType: "json",
    data:artistdata,
    success: function(response){
      var myjson = JSON.parse(response)
      try{
        var uri = myjson['tracks']['items'][0]['uri']
        var returnitem = widgethtml1+uri+widgethtml2
      }
      catch(err){
        var returnitem = "Unable to find song"
      }
      $('.embedded').eq(idx).find('.loader').remove()
      $('.embedded').eq(idx).html(returnitem)
    },
    error: function(error){
      $('.embedded').eq(idx).find('.loader').remove()
      $('.embedded').eq(idx).html("Log into Spotify for song previews")
    }
  })
}

function getcode(){
    $.ajax({
      url: 'getcode',
      contentType:'application/json',
      type: 'POST',
      success: function(response) {
        return response
      },
      error: function(error){
        console.log(error);
      }
    });
}

function refreshtoken(token){
    $.ajax({
      url: 'getcode',
      contentType:'application/json',
      type: 'POST',
      success: function(response) {
        console.log(JSON.parse(response))
        return JSON.parse(response)
      },
      error: function(error){
        console.log(error);
      }
    });
}