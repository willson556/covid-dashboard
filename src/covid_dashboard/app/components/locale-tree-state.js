import Component from '@glimmer/component';
import { tracked } from '@glimmer/tracking';
import { action } from '@ember/object';
import { inject as service } from '@ember/service';

export default class LocaleTreeStateComponent extends Component {
    @service config;
    @tracked showCounties = false;

    get isChecked() {
        return this.config.states.indexOf(this.args.state.id) >= 0;
    }

    @action
    expandState() {
        console.log('expand state');
        this.showCounties = !this.showCounties;
    }

    @action
    onChecked() {
        let state = this.args.state;
        if (!this.isChecked) { // isChecked isn't updated yet.
            this.config.states.addObject(state.id);
        } else {
            this.config.states.removeObject(state.id);
        }
    }
}
