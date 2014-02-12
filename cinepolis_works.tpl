<div id="filters">
	<ul id="theatres">
	  % for item in theatres:
	    <li>{{item}}</li>
	  % end
	</ul>

	<ul id="movies">
	  % for item in movies:
	    <li>{{item}}</li>
	  % end
	</ul>
</div>
<div id="actual movies">
% for item in data:
	<div class = "movie">
		<h3 class="theatre"> {{item["theatre"]}} </h3>
		<h2 class="title"> {{item["title"]}} </h2>
		% if item["title"] in images:
			<img src="{{images[item["title"]]}}">
		% end
		<span class="time"> <a href = "#suckit"> {{item["time"]}}  </a></span>
		% for tag in item["tags"]:
			<span class="tag {{tag}}"> {{tag}} </tag>
		% end
	</div>
% end

% for im in images:
	{{im}} <br>
% end
</div>