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
    url: '/myfinds/'
});

var FindList = Backbone.View.extend({
    el: '#data',
    initialize: function(){
         this.render();
    },
    render: function () {
        var that = this;
        var find = new Find();
        find.fetch({
            success: function(find) {
                var JSON = find.toJSON();
                console.log(JSON);
                var template = _.template($('#finds_template').html(), {finds: JSON});
                that.$el.html(template);
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
    