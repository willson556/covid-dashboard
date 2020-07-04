import Component from '@glimmer/component';
import { tracked } from '@glimmer/tracking';
import { action } from '@ember/object';
import { inject as service } from '@ember/service';

export default class ChartManagerComponent extends Component {
    @service config;
    @service('plot-data') plotData;
    
    get plots() {
        return this.plotData.getPlots(
            this.config.states,
            this.config.counties,
            this.config.plots,
            this.config.startDate,
            this.config.endDate,
            this.config.perCapita);
    }
}
