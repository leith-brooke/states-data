$(document).ready(function() {

	  $('#map').usmap({

	    'click' : function(event, data) {
	      $('#alert')
	        .stop()
	        .animate({backgroundColor: '#ddd'}, 1000);
	    }
	  });
	  
	  
	  $('#over-md').click(function(event){
	    $('#map').usmap('trigger', 'MD', 'mouseover', event);
	  });
	  
	  $('#out-md').click(function(event){
	    $('#map').usmap('trigger', 'MD', 'mouseout', event);
	  });
	});