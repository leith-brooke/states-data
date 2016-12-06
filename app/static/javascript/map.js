$(document).ready(function() {
	var mapcolors = getMapColors('default');

	$('#over-md').click(function(event){
		$('#map').usmap('trigger', 'MD', 'mouseover', event);
	});
	  
	$('#out-md').click(function(event){
		$('#map').usmap('trigger', 'MD', 'mouseout', event);
	});

	$('#color-criteria-selector').on('change', function(){
		if($( '#year' ).val() == null){
			alert("Please select a year...")
		}
		getMapColors($( '#color-criteria-selector' ).val());

	});

	$('#year').on('change', function(){
		getMapColors($( '#color-criteria-selector' ).val());
	});

	$('#form-button').click(function(e){
		e.preventDefault();
		var year = $( '#year' ).val();
		if (year == null){
			alert('please select year');
		}
		$.ajax({
			url: ('/query/' + year),
			type: 'POST',
			data: $('#post-form').serialize(),
			success: function(response){
				console.log(response);

				var stateColors = Object.keys(response);
				var stateStyles = new Object();
				
				stateColors.forEach(function(state){
					stateStyles[state] = new Object;
					stateStyles[state]['fill'] = response[state];
				});
				console.log(stateStyles);
				$("#map-key").empty();
				generateMap(stateStyles);

			}
		});
	});

	function prepareAccordions(){
		var acc = document.getElementsByClassName("accordion");
		var accordionIndex;

		for (accordionIndex = 0; accordionIndex < acc.length; accordionIndex++) {
			acc[accordionIndex].onclick = function(){
				this.classList.toggle("active");
				this.nextElementSibling.classList.toggle("show");
			}
		}
	}

	function addStateData(year,stateData){
		var accordionContainer = '<div class="accordion-container">',
			incomeAccordion = '', 
			educationAccordion = '',
			electionAccordion = '', 
			hateGroupsAccordion = '';

		if(stateData.state != null){
			accordionContainer = accordionContainer + '<h3>' + year + ' Data for ' + stateData.state + '</h3><p>(click data category to expand)</p>';
		}
		
		if(stateData.income != null){
			incomeAccordion = '<button class="accordion">Income Data</button><div class="panel"><p>Average household income adjusted to 2015 dollars: $' + stateData.income + '</p></div>';
		}
		if(stateData.education != null){
			var educationYear = stateData.education['year'];
			educationAccordion = '<button class="accordion">Education Data</button><div class="panel"><h5>Percentage of Adults that have attained this education level or higher</h5>';
			var educationLevels = '';

			var educationData = Object.keys(stateData.education);
			educationData.forEach(function(level){
				if (level != 'year'){
					educationLevels = educationLevels + '<p>' + level + ':\t' + stateData.education[level] + '</p>';
				}
			});
			educationAccordion = educationAccordion + educationLevels + '</div>';
		}

		if(stateData.hate_groups != null){
			hateGroupsAccordion = '<button class="accordion">Hate Groups that existed in this state</button><div class="panel"><table><thead><tr><td>Hate group type</td><td>Number of chapters in this state</td></tr></thead><tbody>';
			var hateGroups = Object.keys(stateData.hate_groups);
			var tbody = '';
			hateGroups.forEach(function(group){
				tbody = tbody + '<tr><td>' + group + '</td><td>' + stateData.hate_groups[group] + '</td></tr>';
			});
			hateGroupsAccordion = hateGroupsAccordion + tbody + "</tbody></table></div>";
		}
		
		if(stateData.election_responses != null){
			electionAccordion = '<button class="accordion">Election Results</button><div class="panel"><table><thead><tr><td> </td></tr></thead><tbody>';
			var parties = Object.keys(stateData.election_responses);
			var electionBody = '';
			parties.forEach(function(party){
				electionBody = electionBody + "<tr><td><h5>" + party + " Party</h5></td></tr>";
				var voteTypes = Object.keys(stateData.election_responses[party]);
				voteTypes.forEach(function(voteType){
					electionBody = electionBody + "<tr><td>" + voteType + " Votes:</td><td>" + stateData.election_responses[party][voteType] + "</td></tr>";
				});

			});
			electionAccordion = electionAccordion + electionBody + "</tbody></table></div>";

		}


		accordionContainer = accordionContainer + incomeAccordion + educationAccordion + hateGroupsAccordion + electionAccordion + "</div>";
		return accordionContainer;
	}

	function setAverageData(criteria,avg){
		$("#map-key").remove();
		var aboveColor,belowColor, aboveP, belowP, avgStatement, avgData;
		
		
		if ('election'.localeCompare(criteria) != 0 && 'default'.localeCompare(criteria) != 0){
			switch(criteria){
				case 'bachelors':
					aboveColor = '#008000';
					belowColor = '#DC143C';
					break;
				case 'hs':
					aboveColor = '#008000';
					belowColor = '#DC143C';
					break;
				case 'hate':
					aboveColor = '#E6E6FA';
					belowColor = '#B22222';
					break;
				case 'income':
					aboveColor = '#000';
					belowColor = '#E91D0E';
					break;
				case 'default':
					aboveColor = '';
					belowColor = '';
					break;
			}
			aboveP = '<p class="color-key"<p>Greater than national average: ' + '<div style="width: 100px;height: 20px;background:' + aboveColor + '"></div></p></p>';
			belowP = '<p class="color-key"<p>Less than national average: ' + '<div style="width: 100px;height: 20px;background:' + belowColor + '"></div></p></p>';
			avgStatement = '<div id="map-key"><p>National average: ' + avg + '</p>';
			avgData = avgStatement + aboveP + belowP + '</div>';
			$("#map-section").after(avgData);
			return;
		}
		
		var demP, demColor = '#290EE9';
		var repP, repColor = '#E91D0E';

		demP = '<p class="color-key"<p>Democratic Party: ' + '<div style="width: 100px;height: 20px;background:' + demColor + '"></div></p></p>';
		repP = '<p class="color-key"<p>Republican Party: ' + '<div style="width: 100px;height: 20px;background:' + repColor + '"></div></p></p>';
		$("#map-section").after('<div id="map-key">' + demP + repP + '</div>');
	}

	function getMapColors(criteria){
		if(criteria == 'default'){
			criteria = 'election';
		}

		var year = $( '#year' ).val();
			if (year == null){
				year = 2016;
		}

		$.ajax({url:('/colors/' + criteria + '/' + year), success: function(response){

				var stateColors = Object.keys(response);
				var stateStyles = new Object();
				
				setAverageData(criteria, response['avg']);
				stateColors.forEach(function(state){
					stateStyles[state] = new Object;
					stateStyles[state]['fill'] = response[state];
				});
				console.log(stateStyles);
				generateMap(stateStyles);
		},
		statusCode:{
			500: function(){
//do the thing here where i say no data
			}
		}});
	}

	function generateMap(mapcolors){
		$('#map').remove();
		console.log(mapcolors);
		var mapString = '<div id="map" style="width: 590px; height: 400px"></div>';
		$( '.map-section' ).append(mapString);
		$('#map').usmap({

			'stateSpecificStyles': mapcolors,

			'click' : function(event, data) {
			$('#alert')
				.stop()
				.animate({backgroundColor: '#ddd'}, 1000);

				var stateName = data.name;
				var year = $( '#year' ).val();
				if(year == null){
					alert("Please select a year...")
				}
				$.ajax({url:("/year/" + year + "/state/" + stateName), success: function(response){

					$(".accordion-container").remove();
					$("#map-key").after(addStateData(year, response));
					prepareAccordions();
					console.log(response);
				}});
			}
		});
	}
});
