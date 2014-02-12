<html>
	<head>
	<title>Better Cinepolis Viewer</title>
	<link rel="stylesheet" href="static/cinepolis.css" type="text/css">
	<link rel="stylesheet" href="static/bootstrap/css/bootstrap.min.css" type="text/css">
	</head>

	<body>
		<div id="filters" class="filters">
			<div id="theatre_filter" class="filter">
			  <h5> Filter by Theatres </h5>
			  % for t in theatres:
					<label class="checkbox-inline theatre_check" > <input type="checkbox" id="{{theatres[t]}}"> {{t}}</label>
			  % end
			</div>

			<div id="movie_filter" class="filter">
			  <h5> Filter by Movies </h5>
			  % for item in movies:
					<label class="checkbox-inline movie_check" > <input type="checkbox" id="{{movies[item]}}"> {{item}}</label>
			  % end
			</div>
			<div id="tags_filter" class="filter">
			  <h5> Filter by Tags </h5>
			  % for item in tags:
			   <input type="checkbox" id="{{item}}">  <label class="tag tag-{{item}}" for="{{item}}"> {{item}}</label>
			  % end
			</div>
		</div>
		<div id="movies">

		% for title in data:
			<div class="movie panel panel-primary {{' '.join(data[title]['tags'] + [theatres[t] for t in data[title]['theatres']] + [data[title]['title_hash']])}}">
				<div class="panel-heading">
					<div class = "">
						<h4 class="title">{{data[title]["title"]}} 	</h4>				
	
						
					</div>
				</div>
				<div class="img-holder">
					<div class="overlay-tag-holder">
						% for tag in data[title]["tags"]:
							<span class="overlay-tag tag tag-{{tag}}"> {{tag}} </span>
						% end	
					</div>
					% if "image" in data[title]:
						<img src="{{data[title]["image"]}}">
					% end
					<div id="showings_{{data[title]["hash"]}}" class="showings collapse">
					%for theatre in data[title]["theatres"]:
						<div class="theatre"> 
							<h4> {{theatre}} </h4>
						% for time in data[title]["theatres"][theatre]["times"]:
							<span class="time"> <a href = '{{time["link"]}}'> {{time["time"]}}  </a></span>
						% end
						</div>
					% end
					</div>
				</div>

				<div class="panel-footer" data-toggle="collapse" data-target="#showings_{{data[title]["hash"]}}">
					<h3 class="panel-title">view showtimes</h3>
				</div>
			</div>
		% end

		</div>

		<script src="http://code.jquery.com/jquery.js"></script>
		<script src="static/isotope.pkgd.min.js"></script>
		<script src="static/bootstrap/js/bootstrap.min.js"></script>
		<script>
			$( document ).ready(function() {
				var $container = $('#movies');
				// init
				$container.isotope({
				  // options
				  itemSelector: '.movie',
				  layoutMode: 'masonry',
				  getSortData: {
					title:'.title'
				  }
				});
				$container.isotope({ sortBy : 'title' });

				$('#filters :checkbox').change(function(){
					
					var theatres = $('#theatre_filter :checked') ;
					var movies = $('#movie_filter :checked') ;
					var tags = $('#tags_filter :checked') ;
					var t = ""
					var m = [];
					var s = "";

					for (i= 0; i < tags.length; i++){
						t += "." + tags[i].id
					}
					if (movies.length > 0){
						for (i= 0; i < movies.length; i++){
							m.push("."+movies[i].id+t)
						}
						if (theatres.length > 0){
							for (i= 0; i < theatres.length; i++){
								for(j=0; j < m.length; j++){
									s += "." + theatres[i].id + m[j] + ", ";
								}
							}
						}else{
							for(j=0; j < m.length; j++){
								s += m[j] + ", ";
							}		
						}
						
					}
					else{
						if (theatres.length > 0){
							for (i= 0; i < theatres.length; i++){
								s += "." + theatres[i].id + t + ", ";
							}

						}else{
							s = t + "  ";
						}
					}
					s = s.substring(0, s.length - 2);
					console.log(s)

				  	$container.isotope({ filter: s });
				  	return false;
				});



			});

		</script>
	</body>
</html>