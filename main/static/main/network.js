function toggleNode(nodeID) {
    var nodeList = cy.elements(`node[id="${nodeID}"]`);
    for (var i = 0; i < nodeList.length; i++) {
        if (nodeList[i].style("visibility") === "visible") {
            nodeList[i].style("visibility", "hidden");
            document.getElementById(`${nodeID}_option`).style.backgroundColor = "#5f788a";
        } else {
            nodeList[i].style("visibility", "visible");
            document.getElementById(`${nodeID}_option`).style.backgroundColor = "#ffffff";
        }
    }
}

function toggleStrain(stra) {
    var edgeList = cy.elements(`edge[strain="${stra}"]`);
    for (var i = 0; i < edgeList.length; i++) {
        if (edgeList[i].style("visibility") === "visible") {
            edgeList[i].style("visibility", "hidden");
            document.getElementById(stra).style.backgroundColor = "#5f788a";
        } else {
            edgeList[i].style("visibility", "visible");
            document.getElementById(stra).style.backgroundColor = "#ffffff";
        }
    }
}

function changeBar(evt, display) {
    var i, tabcontent, tablinks;

    tabcontent = document.getElementsByClassName("tabcontent");
    for (i=0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    tablinks = document.getElementsByClassName("tablink");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }

    document.getElementById(display).style.display = "block";
    evt.currentTarget.className += " active";
}

var cy = cytoscape({
	container: document.getElementById("cy"),
	elements: [
		{% for n in nodes %}
			{data: {id: "{{n.id}}", color: "{{n.color}}"}},
		{% endfor %}

		{% for i in interactions %}
			{data: {id: "{{i.id}}", source: "{{i.source}}", target: "{{i.target}}", color: "{{i.color}}", strain: "{{i.strain}}"}},
		{% endfor %}
	],

	style: [
			{
				selector: "node",
				style:
					{
						"background-color": "data(color)", 
						"label": "data(id)",
					}
			},

			{
				selector: "edge",
				style:
				{
					"width": 1,
					"line-color": "data(color)",
					"curve-style": "haystack",
					"haystack-radius": 0.5,
					"line-opacity": .6,
				}

			},
			{
				selector: ":selected",
				style:
				{
					"background-color": "black",
				}
			}
		],

        minZoom: 1e-10,
        maxZoom: 1e10,
		wheelSensitivity: 0.7,

});


var layout = cy.layout({name: "cola", animate: false, fit: true});

layout.run();

//cy minimap
/*
var defaults = {
};

var nav = cy.navigator(defaults);
*/

cy.cxtmenu({
	selector: 'node[color="blue"]',
	commands: [
		{
			content: 'NCBI',
			select: function(ele) {
				window.open("https://www.ncbi.nlm.nih.gov/search/all/?term=" + ele.id(), "_blank");
			}
		},
		{
			content: 'GTEx',
			select: function(ele) {
				window.open("https://gtexportal.org/home/gene/" + ele.id(), "_blank");
			}
		},
		{
			content: 'HPA',
			select: function(ele) {
				window.open("https://www.proteinatlas.org/search/" + ele.id(), "_blank");
			}
		}
	]
});

cy.cxtmenu({
    selector: 'node[color="red"]',
    commands: [
        {
            content: 'UniProt',
            select: function(ele) {
                window.open(`https://www.uniprot.org/uniprot/?query=${ele.id()}+AND+organism%3A%22Severe+acute+respiratory+syndrome+coronavirus+2+%282019-nCoV%29+%5B2697049%5D%22&sort=score`, "_blank");
            }
        },
        {
            content: 'NCBI',
            select: function(ele) {
                window.open(`https://www.ncbi.nlm.nih.gov/protein/?term=${ele.id()}+AND+%22Severe+acute+respiratory+syndrome+coronavirus+2%22%5BOrganism%5D`, "_blank");
            }
        },
    ]
});

