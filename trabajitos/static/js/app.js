var actionScroll = false;
var scrollCount = 0;
var action = 'f';

var all=true;


var Alert = Backbone.Collection.extend({
    url: '/myalerts/'
});

var AlertList = Backbone.View.extend({
    el: '#alerts',
    initialize: function(){
        this.render();
    },
    render: function () {
        var that = this;
        var alert = new Alert();
        alert.fetch({
            success: function(search) {
                var JSON = search.toJSON();
                console.log(JSON);
                var template = _.template($('#alerts_template').html(), {alerts: JSON});
                that.$el.html(template);
            }
        })
    }
});

var Search = Backbone.Collection.extend({
    url: '/mysearchs/'
});

var SearchList = Backbone.View.extend({
    el: '#searchs',
    initialize: function(){
        this.render();
    },
    render: function () {
        var that = this;
        var search = new Search();
        search.fetch({
            success: function(search) {
                var JSON = search.toJSON();
                console.log(JSON);
                var template = _.template($('#searchs_template').html(), {searchs: JSON});
                that.$el.html(template);
            }
        })
    }
});

var JAlert = Backbone.Collection.extend({
    initialize: function(models, options) {
        this.id = options.id;
    },
    url: function() {
        return '/myjobalert/' + this.id + '/';
    }
});

var JAlertList = Backbone.View.extend({
    el: '#data',
    initialize: function(){
        actionScroll = true;
        if (scrollCount>=0) {
            $("#loader").css("display","inline");
            this.render();
        }
    },
    render: function () {
        var that = this;
        var jalert = new JAlert([], { id: scrollCount });
        jalert.fetch({
            success: function(jalert) {
                var JSON = jalert.toJSON();
                if($.isEmptyObject(JSON)){
                    scrollCount = -1;
                    $("#loader").css("display","none");
                    return;
                }
                var template = _.template($('#jalerts_template').html(), {jalerts: JSON});
                that.$el.append(template);
                actionScroll = false;
                scrollCount = scrollCount+1;
                $("#loader").css("display","none");
            }
        })
    }
});

var Find = Backbone.Collection.extend({
    initialize: function(models, options) {
        this.id = options.id;
    },
    url: function() {
        if (all==true) {
            return '/myfinds/' + this.id + '/';
        }else{
             return '/mygoodfinds/' + this.id + '/';
        }
        
    }
});

var FindList = Backbone.View.extend({
    el: '#data',
    initialize: function(){
        actionScroll = true;
        if (scrollCount>=0) {
            $("#loader").css("display","inline");
            this.render();
        }
    },
    render: function () {
        var that = this;
        var find = new Find([], { id: scrollCount });
        find.fetch({
            success: function(find) {
                var JSON = find.toJSON();
                if($.isEmptyObject(JSON)){
                    scrollCount = -1;
                    $("#loader").css("display","none");
                    return;
                }
                var template = _.template($('#finds_template').html(), {finds: JSON});
                that.$el.append(template);
                actionScroll = false;
                scrollCount = scrollCount+1;
                $("#loader").css("display","none");
            }
        })
    }
});

var Job = Backbone.Collection.extend({
  initialize: function(models, options) {
    this.id = options.id;
  },
  url: function() {
    return '/myjobs/' + this.id + '/';
  }
});

var JobList = Backbone.View.extend({
    el: '',
    initialize: function(attrs){
        this.options = attrs;
        this.el = attrs.el;
        this.render();
    },
    render: function () {
        var that = this;
        var job = new Job([], { id: this.options.id });
        var toggle = this.options.toggle
        job.fetch({
            success: function(job) {
                var JSON = job.toJSON();
                console.log(JSON);
                var template = _.template($('#jobs_template').html(), {jobs: JSON});
                that.$el.html(template);
                if(toggle && toggle==true){
                	that.$el.toggle(150*that.$el.find('li').size());
                }
            }
        })
    }
});

$(document).ready(function() {
    $("#find").click(function(){
        if ($("#afind").css('display')!='none') {
            $("#afind").hide('blind', 250);
            $("#searchs").html("");
        }else{
            $("#afind").show('blind', 250);
        
            var searchList = new SearchList();
        }
    });
    $("#alert").click(function(){
        if ($("#aalert").css('display')!='none') {
            $("#aalert").hide('blind', 250);
        }else{
            $("#aalert").show('blind', 250);

            var alertList = new AlertList();
        }
    });
    $("#account").click(function(){
        if ($("#aaccount").css('display')!='none') {
            $("#aaccount").hide('blind', 250);
        }else{
            $("#aaccount").show('blind', 250);
        }
    });
    
    $(window).scroll(function() {
        if  ($(window).scrollTop()+200 >= ($(document).height() - ($(window).height()))){
            if (actionScroll == false) {
                if(action=='f'){
                    var findList = new FindList();
                }else{
                    var jAlertList = new JAlertList();
                }
            }
        }
    });
    
    $("#all").click(function() {
        if (all==true) {
            all=false;
            $("#all").html(allMsg);
            scrollCount = 0;
            $("#data").html("");
        }else{
            all=true;
            $("#all").html(goodMsg);
            scrollCount = 0;
            $("#data").html("");
        }
        loadFinds();
        action = 'f';
    });
    

    $("#jobalerts").click(function() {
    	$("#data").html("");
        scrollCount = 0;
        action = 'a';
    	loadJAlerts();
    });
    
    loadFinds();
});

function adelete(id){
    $.ajax({
	url: "/deletefind/"+id+"/",
	dataType: "json",
	success: function(data){
	    if(data.state==false){
		alert(comerror);
	    }else{
		$("#search"+id).remove();
	    }
	},
	error: function(e, xhr){
	    alert(comerror);
	}
    });
}

function alertdelete(id){
    $.ajax({
	url: "/deletealert/"+id+"/",
	dataType: "json",
	success: function(data){
	    if(data.state==false){
		alert(comerror);
	    }else{
		$("#alert"+id).remove();
	    }
	},
	error: function(e, xhr){
	    alert(comerror);
	}
    });
}

function getTries(id){
	var div = $('#to'+id);
    if (div.css('display')=='none') {
        var jobList = new JobList({id : id, el : '#to'+id, toggle: true});
    }else{
    	div.toggle(150*div.find('li').size());
    }
    /*var div = $('#to'+id);
    div.toggle(150*div.find('li').size());
    if (div.css('display')=='none') {
        div.show('blind', 550*div.find('li').size());
    }else{
    	div.hide('blind', 150*div.find('li').size(), function(){div.css('display','none');div.html("");});
    }*/
}

function loadFinds() {    
    var findList = new FindList();
}


function loadJAlerts() {    
    var jAlertList = new JAlertList();
}
    