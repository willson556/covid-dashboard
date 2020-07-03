import Service from '@ember/service';
import { inject as service } from '@ember/service';

// export class PlotDataResponse {
//     deaths = {};
//     hospitalized = {};
//     positive = {};
//     tests = {};
//     locales = {};
// }

class Plot {
    options = {}
    data = []

    constructor(options, data) {
        this.options = options;
        this.data = data;
    }
}

export default class PlotDataService extends Service {
    @service config;

    startTime = "2020-05-01";
    endTime = "2020-07-01";
    
    async _getData(states, counties) {
        var url = `/api/data?start_time=${this.startTime}&end_time=${this.endTime}`;

        states.forEach(state => {
            url += `&states=${state}`
        });

        counties.forEach(county => {
            url += `&counties=${county}`
        });

        let response = await fetch(url);
        let data = await response.json();
        
        return data;
    }

    _convertSeriesData(data) {
        return {
            name : data[0],
            data: Object.entries(data[1]).map(p => [ parseInt(p[0]), p[1] ])
        };
    }

    _getPlot(title, data) {
        let chartOptions = {
            chart: {
                type: 'line' //?
            },
            title: {
                text: title
            },
            xAxis: {
                type: 'datetime'
            },
            yAxis: {}
        };

        let chartData = Object.entries(data).map(this._convertSeriesData);

        return new Plot(chartOptions, chartData);
    }

    async getPlots(states, counties, plots) {
        let data = await this._getData(states, counties);

        return plots.map(plot => {
            let plotDefinition = this.config.availablePlots.find(p => p.id == plot)
            return this._getPlot(plotDefinition.name, data[plotDefinition.id]);
        });
    }
}