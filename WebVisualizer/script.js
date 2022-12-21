var serverUrl = 'http://127.0.0.1'

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
        </div>
    `);
  waitingRoads.append(widget)

  // setRoadState('in-road-south-1', 3, 'green');

  // TODO: Fetching State every 5 seconds
  // setInterval(function() {
  //   console.log("Fetching new state");
  //   $.ajax({url: serverUrl+'/state', success: function(result){
  //     console.warn("(not implemented) setting state based on server info");
  //   }});
  // }, 5000);

});