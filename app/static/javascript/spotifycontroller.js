token = ""

widgethtml1 = '<iframe src="https://open.spotify.com/embed?uri='
widgethtml2 = '" width="300" height="380" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>'

function searchsong(artist,track,idx){
  //console
  base_url = "https://api.spotify.com/v1/search"
  artistdata = JSON.stringify({"track":track,"artist":artist})
  console.log(artistdata)
  $.ajax({
    type:'POST',
    url:'getsong',
    contentType: "application/json; charset=utf-8",
    dataType: "json",
    data:artistdata,
    async:false,
    success: function(response){
      var myjson = JSON.parse(response)
      var uri = myjson['tracks']['items'][0]['uri']
      returnitem = widgethtml1+uri+widgethtml2
    },
    error: function(error){
      console.log(error)
      returnitem = "error"
    }
  })
  return returnitem
}

function getcode(){
    $.ajax({
      url: 'getcode',
      contentType:'application/json',
      type: 'POST',
      success: function(response) {
        console.log(response)
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