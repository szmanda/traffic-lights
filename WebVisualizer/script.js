var serverUrl;

// id of the road, number of people waiting, light color
var setRoadState = function (id, waiting, color) {
  const road = $('#'+id)
  road.find('.light').attr('class', 'light '+color);
  road.find('.counter').text(waiting);
}

$( document ).ready(function() {
  // enable tooltips
  const roads = $('.road, .sidewalk')
  for (let i = 0; i < roads.length; i++) {
    roads[i].setAttribute('data-bs-toggle', "tooltip");
    roads[i].setAttribute('title', roads[i].id);
  }
  var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
  var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl)
  })

  // add widgets displaying number of people waiting and light color
  const waitingRoads = $('.wait')
  const widget = $(`
        <div class="widget">
            <div class="light red"></div>
            <div class="counter">0</div>
            <div class="input-group">
              <input class="btn btn-secondary btn-add" type="button" value="+">
              <input class="btn btn-secondary btn-rem" type="button" value="-">
            </div>
        </div>
    `);
  waitingRoads.append(widget);


  // Setting up the button listeners
  $('.btn-add').click((e) => {
    const road = $(e.target).closest('.road, .sidewalk')[0].id;
    sendCommand('add', road, 1, -10)
  })
  $('.btn-rem').click((e) => {
    const road = $(e.target).closest('.road, .sidewalk')[0].id;
    sendCommand('remove', road, 1, -10)
  })



  // setRoadState('in_road_s_0', 3, 'green');
  
  // TODO: Move the following to a static class Remote

  // TODO: Fetching State every 5 seconds
  /*
  Expecting json:
  {
    "in_road_n_0": {
      "light" : "red|yellow|green"
      "waiting-count" : 0
    },
    ...
  }
  */
  setInterval(function() {
    serverUrl = 'http://' + $('#server-url').val() + ':' + $('#server-port').val();
    console.log(serverUrl);
    $.ajax({url: serverUrl+'/state', success: function(result){
      console.warn("(not implemented) setting state based on server info");
    }})
      .fail(function(e) { console.log("Error connecting to ", serverUrl) });
  }, 5000);


  // TODO: Send an update
  /*
  Changing the number of waiting cars/people in a certain lane
  - add 'n'
  - remove 'n'
  - set to 'n'
  Sending json:
  {
    "in_road_n_0": {
      "count" : 2
      "time-offset": -10
    }
  }
  */
  var sendCommand = function(_command, _road, _count, _timeOffset = 0) {
    var data = {};
    data[_road] = {
      "count" : _count,
      "time-offset" : _timeOffset
    }
    $.ajax({
      url: serverUrl+'/'+_command,
      type: 'POST',
      data: JSON.stringify(data),
      contentType: 'application/json; charset=utf-8',
      success: function(result){
        console.warn("(not implemented) sending a json");
      }
    }).fail(() => {
      console.log("Error while sending:", JSON.stringify(data));
    })
  }
});