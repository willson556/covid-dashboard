import Component from '@glimmer/component';
import { action } from '@ember/object';
import { inject as service } from '@ember/service';

export default class LocaleTreeComponent extends Component {
    @service config;

    @action
    clear() {
        this.config.states.clear();
        this.config.counties.clear();
    }
}