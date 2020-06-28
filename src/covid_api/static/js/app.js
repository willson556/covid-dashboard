$(function () {
    var DataModel = Backbone.Model.extend({});

    var DataCollection = Backbone.Collection.extend({
        model: DataModel,
    });

    var DataView = Backbone.View.extend({
        el: '#chart-container',
        initialize: function (options) {
            this.data = options.data;
        },
        render: function () {
            this.$el.highcharts({
                title: {
                    text: 'Monthly Average Temperature',
                    x: -20 //center
                },
                subtitle: {
                    text: 'Source: WorldClimate.com',
                    x: -20
                },
                xAxis: {
                    categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
                },
                yAxis: {
                    title: {
                        text: 'Temperature (°C)'
                    },
                    plotLines: [{
                        value: 0,
                        width: 1,
                        color: '#808080'
                    }]
                },
                tooltip: {
                    valueSuffix: '°C'
                },
                legend: {
                    layout: 'vertical',
                    align: 'right',
                    verticalAlign: 'middle',
                    borderWidth: 0
                },
                series: this.data.toJSON()
            });
        }
    });

    var items = new DataCollection([{
        name: 'Tokyo',
        data: [7.0, 6.9, 9.5, 14.5, 18.2, 21.5, 25.2, 26.5, 23.3, 18.3, 13.9, 9.6]
    }, {
        name: 'New York',
        data: [-0.2, 0.8, 5.7, 11.3, 17.0, 22.0, 24.8, 24.1, 20.1, 14.1, 8.6, 2.5]
    }, {
        name: 'Berlin',
        data: [-0.9, 0.6, 3.5, 8.4, 13.5, 17.0, 18.6, 17.9, 14.3, 9.0, 3.9, 1.0]
    }, {
        name: 'London',
        data: [3.9, 4.2, 5.7, 8.5, 11.9, 15.2, 17.0, 16.6, 14.2, 10.3, 6.6, 4.8]
    }]);

    var State = Backbone.Model.extend({
        defaults: {
            "selected": false,
        }
    });

    var States = Backbone.Collection.extend({
        model: State,
        url: "/api/states",
        parse: function(response) {
            return _.map(response, function(state_abbrev){
                return {"Name": state_abbrev};
            })
        }
    });

    var StateView = Backbone.View.extend({
        events: {
            "click" : "click",
        },
        initialize:  function() {
            this.model.on('change', this.render, this);
        },
        render: function(){
            var template = _.template($("#stateTemplate").html());
            var html = template(this.model.toJSON());
            this.$el.html(html);
            
            return this;
        },
        click: function(e) {
            this.model.set("selected", !(this.model.get('selected')));
        }
    })

    var StatesView = Backbone.View.extend({
        el: '#states-container',
        render: function () {
            var self = this;
            this.$el.empty();

            this.model.each(function(state) {
                var stateView = new StateView({model: state});
                self.$el.append(stateView.render().$el);
            });

            return this;
        }
    });

    var view = new DataView({ data: items });
    view.render();

    var states = new States();
    states.fetch({
        success: function() {
            var statesView = new StatesView({model: states});
            statesView.render();
        }
    });

});