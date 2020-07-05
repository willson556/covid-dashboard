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

    async _getData(states, counties, startDate, endDate) {
        var url = `/api/data?start_time=${startDate}&end_time=${endDate}`;

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

    _convertSeriesData(data, divisor) {
        return {
            name: data[0],
            data: Object.entries(data[1]).map(p => [parseInt(p[0]), p[1] / divisor]),
            marker: {
                enabled: false
            }
        };
    }

    _getPlot(title, data, perCapita, locales) {
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

        var counter = 0;
        let chartData = Object.entries(data).map(d => this._convertSeriesData(d, perCapita ? locales[counter++].population : 1));

        return new Plot(chartOptions, chartData);
    }

    async getPlots(states, counties, plots, startDate, endDate, perCapita) {
        let data = await this._getData(states, counties, startDate, endDate);

        return plots.map(plot => {
            let plotDefinition = this.config.availablePlots.find(p => p.id == plot)
            return this._getPlot(plotDefinition.name, data[plotDefinition.id], perCapita, data.locales);
        });
    }
}