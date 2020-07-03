import Component from '@glimmer/component';
import { action } from '@ember/object';
import { inject as service } from '@ember/service';


export default class LocaleTreeCountyComponent extends Component {
    @service config;

    get isChecked() {
        return this.config.counties.indexOf(this.args.county.id) >= 0;
    }

    @action
    onChecked() {
        let county = this.args.county;
        if (!this.isChecked) { // isChecked isn't updated yet.
            this.config.counties.addObject(county.id);
        } else {
            this.config.counties.removeObject(county.id);
        }
    }
}
