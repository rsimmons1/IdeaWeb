var nodes = new vis.DataSet([])
	var edges = new vis.DataSet([])
	var network
	var container
	var nodeTotal
	var max
	var extensions = []
	var totalNodes = {}
	var min = 10
	
	$("#clicker").click(function(){
		$.ajax({
		  data: {'q':$('#search').val()},
		  url: "/ideaWeb/ajax/",
		}).done(function(result) {
		  generateGraph(result)
		});
	});
	function generateGraph(result){
		info = JSON.parse(result)
		var nodeArray = []
		var edgeArray = []
		extensions = []
		totalNodes = []
		nodeTotal = 1
		nodes = new vis.DataSet(nodeArray);
		edges = new vis.DataSet(edgeArray);
		nodes.add({id: 0, label: info.title,size: 75,group:0})
		totalNodes[info.title.toUpperCase()] = 0
		max = nodes.get(0)['size']
		extensions.push(info.save)
		branch(info,nodes.get(0),5)		
		container = document.getElementById('mynetwork');
		var data = {
		nodes: nodes,
		edges: edges
		};

		//Network Options

		var options = {
			nodes: {
				mass: 3.5,
			    shape: 'dot',
			    font: {
			        size: 32,
			        color: '#ffffff'
			    },
			    borderWidth: 2
			},
			edges: {
			    width: 5,
			    physics: true,
			    scaling:{
			      min: 1,
			      max: 150,
			  },
			  length: 200,
			},
			layout:{randomSeed:2},
		};
		network = new vis.Network(container, data, options);

		//Event Handling

		network.on("dragEnd", function (params) {
	        params.event = "[original event]";
	        nodeData = nodes.get(Number(params['nodes']))
	        if(!isInArray(nodeData['label'].toUpperCase(),extensions)){
			    $.ajax({
				  data: {'q':nodeData['label']},
				  url: "/ideaWeb/ajax/",
				}).done(function(result) {
				  	branch(info = JSON.parse(result),nodeData,5)
				});
			}
	    });
	    network.on("doubleClick",function(params){
	    	if(params['nodes'].length != 0){
		    	newNodeData = nodes.get(Number(params['nodes']))
		    	network.focus(Number(params['nodes']),{animation : true})
		    	$("#showWiki").attr({'src':'about:blank'})
			    $("#loader").css({'opacity': 0})
		    	$("#showWiki").attr({'src':'https://en.wikipedia.org/wiki/'+newNodeData['label']}) 
		    	window.location.replace('#firstPage/2')
		    	
				
	    	}
	    })
	}
	function branch(newNodes, root, size){
		var nodeArray = []
		var edgeArray = []
		var groups = []
		var connectNum = 0
		var node = 0
		var initialSize = 19
		if(!(Number(root['group']) === 0)){
			for (var i = 0; i < size; i++){
				groups.push(root['group'])
			}
		}
		else{
			for (var i = 0; i < size; i++){
				groups.push(nodeTotal+i)
			}
		}
		for (var i = 0; i < size; i++){
			nodeTotal++
			if(!totalNodes.hasOwnProperty(newNodes.edges[i][0].toUpperCase()) ){
				totalNodes[newNodes.edges[i][0].toUpperCase()] = nodeTotal
				nodeArray.push({id: nodeTotal,label:newNodes.edges[i][0], size: 15, group:groups[i]})
				edgeArray.push({from:nodeTotal, to: Number(root['id'])})
			}
			else{
				node = totalNodes[newNodes.edges[i][0].toUpperCase()]
				nodes.update({id: node, size: limit(nodes.get(node)['size'] + 20,max,initialSize)})
				edges.add({from: Number(root['id']), to: node})
			}
		}
		nodes.add(nodeArray)
		edges.add(edgeArray)
		extensions.push(root['label'].toUpperCase())
	}
	function limit(num,max,min){
		if(num > max){
			return max
		}
		else if(num < min){
			return min
		}
		else{
			return num
		}
	}
	function isInArray(value, array) {
	  return array.indexOf(value) > -1;
	}