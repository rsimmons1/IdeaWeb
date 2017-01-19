	var nodes = new vis.DataSet([])
	var edges = new vis.DataSet([])
	var network
	var container
	var nodeTotal
	var max
	var extensions = []
	var totalNodes = {}
	var min = 10
	var branchSize = 5
	var largeText = 80
	var selectedNode = 0
	$("#clicker").click(function(){
		$.ajax({
		  data: {'q':$('#search').val()},
		  url: "/ajax/",
		}).done(function(result) {
		  generateGraph(result)
		});
	});
	$("#branch").click(function(){
		var nodeGroup = nodes.get(selectedNode)['group']
		var expNode = [selectedNode]
		var items = network.getConnectedNodes(selectedNode.toString())
		items = items.concat(expNode)
		items.forEach(function(n){
			(function(){
				var TnodeData = nodes.get(n);
				if(!isInArray(TnodeData['label'].toUpperCase(),extensions)){
				    $.ajax({
					  data: {'q':TnodeData['label']},
					  url: "/ajax/",
					  success: (function(result) {
								var info = JSON.parse(result)
							  	branch(info,TnodeData,branchSize) })
					})
				}
			})()
			
		})
	})
	function biggestNodes(){
		var nodeMax = 0
		var biggestNode = []
		var nodeIndex = 0
		var nodeId = 0
		for (var i=1; i < branchSize+1; i++){
			nodeId = 0
			nodeMax = 80
			nodeIndex = 0
			var groupNodes = nodes.get({
				filter: function (item) {
					return item.group == i;
				}
			});
			for(var j = 0; j <groupNodes.length; j++){
				if(groupNodes[j]['size'] > nodeMax){
					nodeIndex = j
					nodeId = groupNodes[j]['id']
					nodes.update({id: groupNodes[j]['id'],font:{size:largeText},scaling:{label:{min:40,max:200}}})
				}
				else{
					nodes.update({id: groupNodes[j]['id'],font:{size:32}})
				}
			}
			biggestNode.push(groupNodes[nodeIndex])
			
		}
		
	}
	function generateGraph(result){
		info = JSON.parse(result)
		var nodeArray = []
		var edgeArray = []
		extensions = []
		totalNodes = []
		nodeTotal = 1
		nodes = new vis.DataSet(nodeArray);
		edges = new vis.DataSet(edgeArray);
		nodes.add({id: 0, label: info.title,size: 75,group:0,font:{size:largeText}})
		totalNodes[info.title.toUpperCase()] = 0
		max = 600
		extensions.push(info.save)
		branch(info,nodes.get(0),branchSize)		
		container = document.getElementById('mynetwork');
		var data = {
		nodes: nodes,
		edges: edges
		};

		//Network Options

		var options = {
			physics: {
				barnesHut: {
					avoidOverlap: 0.1,
				}
			},
			nodes: {
				mass: 3.5,
			    shape: 'dot',
			    font: {
			        size: 32,
			        color: '#ffffff'
			    },
			    borderWidth: 2,
			    scaling:{
			    	label:{drawThreshold: 10,}
			    }
			},
			edges: {
				arrows: {
			      to:     {enabled: false, scaleFactor:1},
			      middle: {enabled: false, scaleFactor:1},
			      from:   {enabled: true, scaleFactor:0.5}
			    },
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
				  url: "/ajax/",
				}).done(function(result) {
				  	branch(info = JSON.parse(result),nodeData,branchSize)
				});
			}
	    });
	    network.on("select",function(params){
	    	selectedNode = Number(params['nodes'])
	    })
	    network.on("doubleClick",function(params){
	    	
	    	if(params['nodes'].length != 0){
		    	newNodeData = nodes.get(Number(params['nodes']))
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
			if(!totalNodes.hasOwnProperty(newNodes.edges[i][0].toUpperCase()) ){
				nodeTotal++
				totalNodes[newNodes.edges[i][0].toUpperCase()] = nodeTotal
				nodeArray.push({id: nodeTotal,label:newNodes.edges[i][0], size: 35, group:groups[i]})
				edgeArray.push({from:nodeTotal, to: Number(root['id'])})
			}
			else{
				node = totalNodes[newNodes.edges[i][0].toUpperCase()]
				if (nodes.get(node)['size'] + 20 > 80){
					nodes.update({id: node, font:{size:largeText},size: limit(nodes.get(node)['size'] + 20,max,initialSize)})
				}
				else{
					nodes.update({id: node, size: limit(nodes.get(node)['size'] + 20,max,initialSize)})
					edges.add({from: node, to: Number(root['id'])})
				}
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
