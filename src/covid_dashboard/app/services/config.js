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
    @tracked startDate = "2020-03-01";
    @tracked endDate = new Date().toISOString().substring(0,10);
    @tracked perCapita = true;

    availablePlots = [
        new Plot('deaths', "Deaths per Day"),
        new Plot('positive', "Cases per Day"),
        new Plot('hospitalized', "Hospitalizations"),
    ];
}