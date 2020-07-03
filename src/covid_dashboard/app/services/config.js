import Service from '@ember/service';
import { tracked } from '@glimmer/tracking';

export class Plot {
    id = '';
    name = '';

    constructor(id, name) {
        this.id = id;
        this.name = name;
    }
}

export default class ConfigService extends Service {
    @tracked states = [];
    @tracked counties = [];
    @tracked plots = [];

    availablePlots = [
        new Plot('deaths', "Deaths per Day"),
        new Plot('positive', "Cases per Day"),
        new Plot('hospitalizations', "Hospitalizations"),
        new Plot('tests', "Positive Test Rate"),
    ];
}