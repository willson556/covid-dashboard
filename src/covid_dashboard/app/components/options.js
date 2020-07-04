import Component from '@glimmer/component';
import { action } from '@ember/object';
import { inject as service } from '@ember/service';

export default class OptionsComponent extends Component {
    @service config;

    get isPerCapita() {
        return this.config.perCapita;
    }

    @action
    onPerCapitaChanged() {
        this.config.perCapita = !this.config.perCapita;
    }
}
