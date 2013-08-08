var actionScroll = false;
var scrollCount = 0;

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

var Find = Backbone.Collection.extend({
    initialize: function(models, options) {
        this.id = options.id;
    },
    url: function() {
        return '/myfinds/' + this.id + '/';
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
        job.fetch({
            success: function(job) {
                var JSON = job.toJSON();
                console.log(JSON);
                var template = _.template($('#jobs_template').html(), {jobs: JSON});
                that.$el.html(template);
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
                var findList = new FindList();
            }
        }
    });
    
    loadFinds();
});

function adelete(id){
    alert(id);
}

function getTries(id){
    var jobList = new JobList({id : id, el : '#to'+id});
    var div = $('#to'+id);
    if (div.css('display')=='none') {
        div.show('blind', 250);
    }
}

function loadFinds() {    
    var findList = new FindList();
}
    