import Component from '@glimmer/component';
import { action } from '@ember/object';
import { inject as service } from '@ember/service';

export default class PlotPickerEntryComponent extends Component {
    @service config;

    get isChecked() {
        return this.config.plots.indexOf(this.args.plot.id) >= 0;
    }

    @action
    onChecked() {
        let plot = this.args.plot;
        if (!this.isChecked) { // isChecked isn't updated yet.
            this.config.plots.addObject(plot.id);
        } else {
            this.config.plots.removeObject(plot.id);
        }
    }
}
